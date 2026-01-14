Title:  
Attack Surface Management (ASM)

Problem Statement:  
Organizations face challenges in managing complex and ever-changing IT infrastructures while ensuring vulnerabilities in the system are identified quickly. The lack of visibility and control leaves their infrastructure exposed, which increases the risk of cyberattacks, threatening overall security and operational stability.

What I've Done:
- Setting up a VM with vulnerable services.
- Set up a Docker to run my script:
  - Created a Python script to establish an SSH connection to the vulnerable VM.
  - Developed a bash script to get the running process and their packages. It is then stored into a JSON format, which is what the host VM receives in response.
  - The result is further fine-tuned to ensure the service version is standardized and follows the expected format of input for the next part.
  - The output is stored in the database using SQL—which would be displayed on the website—so that the users can check for abnormal services.

If you try to run the script, do note that:
1. both VMs need to be on the same network.
2. The private SSH key that was included (for the teacher to run our code) would need to be replaced with your own.
