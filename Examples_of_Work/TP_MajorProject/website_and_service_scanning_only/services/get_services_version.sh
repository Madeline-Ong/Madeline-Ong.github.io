#!/bin/bash

declare -A services_list

# Gets all running services that are tied to a port, options:
# t - tcp 
# u - udp
# l - listening
# p - process details
# n - != resolve hostnames or serv names -> shows IP addr and port num as is 
ss_res=$(sudo ss -tulpn)

# Loop through each line of the output - which is 1 process
while IFS= read -r line; do
    # Exclude header lines & IPv6
    #    Didn't specify to ONLY have IPv4 since local addr like *:port would be excluded as well 
    #    If necessary to include IPv6, then either remove the IF or put a True boolean
    if [[ "$line" != *"[::]"* ]]; then
        # Count num of columns by using awk to count fields
        column_count=$(echo "$line" | awk '{print NF}')
        
        # Check have 7 cols
        #    Eg lines: 
        #    Netid      State       Recv-Q      Send-Q                              Local Address:Port              Peer Address:Port      Process
        #    tcp        LISTEN      0           32                                              *:21                           *:*          users:(("vsftpd",pid=888,fd=3)) 
        #    tcp        LISTEN      0           4096                                      0.0.0.0:111                    0.0.0.0:*          users:(("rpcbind",pid=915,fd=4),("systemd",pid=1,fd=46)) 
        #    Which as you can see, has 7 cols
        if [[ "$column_count" -eq 7 ]]; then
            
            # Getting port num 
            #    Using eg above, you can see that port num is technically in col5 (Local Address:Port)
            #    temp is used as a placehold since local addr isn't used 
            #    variable 'temp' can be overwritten to save memory
            temp=$(echo "$line" | awk '{print $5}')
            
            # Extract port num from the local addr (stored as temp)
            #    '0.0.0.0:111' -> '111'
            port=$(echo "$temp" | cut -d':' -f2)


            # Getting the proc name
            #    Using eg above, you can see that process details are in col7 (Process)
            proc_name=$(echo "$line" | awk '{print $7}')
            
            # Get the 1st proc (considered main serv), if there is more than 1 
            #    Eg: 
            #    'users:(("rpcbind",pid=915,fd=4),("systemd",pid=1,fd=46))' -> 'users:(("rpcbind",pid=915,fd=4'
            proc_name=$(echo "$proc_name" | cut -d')' -f1)
            
            # Get just the proc details
            #    Eg
            #    'users:(("rpcbind",pid=915,fd=4' -> '"rpcbind",pid=915,fd=4'
            proc_name="${proc_name:8}"
            
            # Use IFS to split by commas
            #   '"rpcbind",pid=915,fd=4' -> '"rpcbind"'  'pid=915'  'fd=4' 
            #   temp is a placehold since fd not necessary 
            IFS=',' read -r proc_name pid temp <<< "$proc_name"

            # Remove quotes from proc_name
            #    '"rpcbind"' -> 'rpcbind'
            proc_name="${proc_name//\"/}"

            # Extract the PID using parameter expansion
            #    'pid=915' -> '915'
            pid="${pid#pid=}"
            
            # Note: Concatenated keys are used for a nested "dictionary" (eg: "process_name|rpcbind|ports")

            # Check if the key exists in the associative array
            if [[ -v services_list["pid|$pid|ports"] ]]; then

                # Check if $port exists in the list of ports for a given PID
                # Using regex to match the port at the start (^), between commas (,), or at the end ($)
                if [[ ! "${services_list["pid|$pid|ports"]}" =~ (^|,)$port(,|$) ]]; then

                    # If the port is not in the list, append it
                    services_list["pid|$pid|ports"]+=", ${port}"
                fi

                # If port != unique & same name, no need to check for vers & pkg_name - alr stored 
                continue

            # If port not in array, add it in
            else
                services_list["pid|$pid|ports"]="$port"
            fi
            
            services_list["pid|$pid|process_name"]+="${proc_name}"

            # Get the serv exe/binary location
            #   f -  follow symlinks in given path & return absolute path of final target 
            exe_binary_res=$(sudo readlink -f /proc/$pid/exe)
            
            # Search for any instance of the binary in dpkg (to get pkg name)
            #    and capture the result, suppressing stderr 
            #    Eg error: "dpkg-query: no path found matching pattern ..."
            pkg_name_res=$(dpkg -S "$exe_binary_res" 2>/dev/null)

            # If there isnt anyth returned == not a pkg that's in linux by default
            # i.e. might be custom serv, eg pulled from github 
            if [[ -z "$pkg_name_res" ]]; then
                # echo "dpkg cannot find pkg for {exe_binary_res}"
                # TODO : handling custom serv
                continue  
            fi
            
            # Extract pkg name 
            #    Eg of result:       rpcbind: /usr/sbin/rpcbind
            #    Format of result:  pkg_name: exe_location
            pkg_name=$(echo "$pkg_name_res" | cut -d':' -f1)
            
            # Get serv vers
            pkg_vers=$(dpkg-query --show --showformat='${Version}' $pkg_name)
            
            services_list["pid|$pid|package_name"]="$pkg_name"
            services_list["pid|$pid|version"]="$pkg_vers"
            
            # From systemctl & checking using pid, can get the serv info, which has serv name
            #    grep gets only the part stating the location of the serv binary 
            #        Eg: Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled; preset: disabled)
            #    sed is used to only get the serv part of the name, w/o the extension 
            #        Eg: ssh 
            serv_name=$(systemctl status $(ps -o unit= -p $pid) | grep -o '/usr/lib/systemd/system/.*\.service' | sed 's/.*\/\(.*\)\.service/\1/')

            # Check if the serv name contains a newline (\n)
            #    May have more than 1 process / serv that is run using the same binary
            if [[ "$serv_name" =~ $'\n' ]]; then

                # If newline exists, take 1st line as serv name
                serv_name=$(echo "$serv_name" | head -n 1)
            fi

            services_list["pid|$pid|service_name"]="$serv_name"
        fi
    fi 
done <<< "$ss_res"


# Declare the JSON string 
json="{"

# Declare another associative array - used to organize data from services_list
declare -A process_dict

# Iterate through each key-value pair in services_list 
for key in "${!services_list[@]}"; do
    # Split the key into components (e.g., "pid|915|ports" -> ["pid", "915", "ports"])
    IFS='|' read -ra key_parts <<< "$key"
    
    # Extract the pid (the second part of the key)
    pid="${key_parts[1]}"
    
    # The field to store (e.g., "ports", "package_name", etc.)
    field="${key_parts[2]}"

    # Cleaning: Removing any newline characters using tr
    cleaned_value=$(echo "${services_list[$key]}" | tr -d '\n')

    # Initialize the pid key if it does not exist
    if [[ -z "${process_dict[$pid]}" ]]; then
        process_dict["$pid"]=""
    fi

    # Store the data by append each field, will be in a nested structure 
    #   += so that will no override the other fields since they are stored line by line
    process_dict["$pid"]+="\"$field\": \"$cleaned_value\", "
done

# Loop over the process_dict to construct the final JSON
for pid in "${!process_dict[@]}"; do
    json+="\"$pid\": {"

    fields="${process_dict[$pid]}"

    # Remove trailing comma from the last field
    fields=${fields%, }

    json+="$fields"
    json+="}, "
done

# Remove trailing comma from the last process entry and close the JSON
json=${json%, }
json+="}"

# Print the final JSON string - which is get by services.py
echo "$json"
