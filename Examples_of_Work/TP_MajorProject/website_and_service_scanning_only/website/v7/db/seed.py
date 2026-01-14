import sqlite3

# Connect to SQLite database
db_name = 'AsmDB.db'
conn = sqlite3.connect(db_name)
conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
cursor = conn.cursor()

# SQL schema to create tables
schema = '''
-- Create "User" table
CREATE TABLE IF NOT EXISTS "User" (
    "User_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Timestamp" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "Name" TEXT NOT NULL,
    "Password" TEXT NOT NULL,
    "Company" TEXT,
    "Role" TEXT,
    "Working" TEXT NOT NULL
);

-- Create "Maria_Assets" table
CREATE TABLE IF NOT EXISTS "Maria_Assets" (
    "Assets_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "User_ID" INTEGER NOT NULL,
    "Valid_IP_Range" TEXT,
    "Active_Assets" TEXT,
    CONSTRAINT "FK_User" FOREIGN KEY("User_ID") REFERENCES "User"("User_ID") ON DELETE CASCADE
);

-- Create "Madeline_Services" table
CREATE TABLE IF NOT EXISTS "Madeline_Services" (
    "Services_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Assets_ID" INTEGER,
    "User_ID" INTEGER NOT NULL,
    "IP_Address" TEXT,
    "Services" TEXT,
    "Version" TEXT,
    "Ports" TEXT,
    "Package_Name" TEXT,
    "Process_Name" TEXT,
    CONSTRAINT "FK_User" FOREIGN KEY("User_ID") REFERENCES "User"("User_ID") ON DELETE CASCADE,
    CONSTRAINT "FK_Assets" FOREIGN KEY("Assets_ID") REFERENCES "Maria_Assets"("Assets_ID") ON DELETE CASCADE
);

-- Create "Madeline_Credentials" table
CREATE TABLE IF NOT EXISTS "Madeline_Credentials" (
    "Credential_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "User_ID" INTEGER NOT NULL,
    "IP_Address" TEXT NOT NULL,
    "Credential" TEXT,
    CONSTRAINT "FK_User" FOREIGN KEY("User_ID") REFERENCES "User"("User_ID") ON DELETE CASCADE
);

-- Create "Yee_Xiang_CVE" table
CREATE TABLE IF NOT EXISTS "Yee_Xiang_CVE" (
    "CVE_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Services_ID" INTEGER,
    "Assets_ID" INTEGER,
    "User_ID" INTEGER NOT NULL,
    "Cve_Number" TEXT,
    "CVSS_Score" REAL,
    "Severity" TEXT,
    "Reference_Link" TEXT,
    "Publish_Date" TEXT,  -- New column for Publish_Date
    CONSTRAINT "FK_User" FOREIGN KEY("User_ID") REFERENCES "User"("User_ID") ON DELETE CASCADE,
    CONSTRAINT "FK_Services" FOREIGN KEY("Services_ID") REFERENCES "Madeline_Services"("Services_ID") ON DELETE CASCADE
);

-- Create "API_Status" table
CREATE TABLE IF NOT EXISTS "API_Status" (
    "Status_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Discovery" TEXT,
    "Services" TEXT,
    "CVE" TEXT,
    "Assets_ID" INTEGER,
    CONSTRAINT "FK_Assets" FOREIGN KEY("Assets_ID") REFERENCES "Maria_Assets"("Assets_ID") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Logs" (
    "Logs_ID" INTEGER PRIMARY KEY AUTOINCREMENT, 
    "User_ID" INTEGER NOT NULL,                          
    "Timestamp" DATETIME DEFAULT CURRENT_TIMESTAMP, 
    "Action_Type" TEXT,                 
    "Description" TEXT,                          
    CONSTRAINT "FK_User" FOREIGN KEY("User_ID") REFERENCES "User"("User_ID") ON DELETE SET NULL
);

'''

# Execute schema creation
cursor.executescript(schema)

# Seed data for "User" table
sample_user_data = [
    ("Alice", "scrypt:32768:8:1$miYNWo4YQE3FMwS3$8cf1bc29873f570d0a543bdd7e76a38c464b148f01df5a17935a94c5464cf1a21343fdc9d38da41349fb8f99e2f804f46902f066b604f2286e131422dafb6827", "TechCorp", "Boss", "Yes"),
    ("Bob", "scrypt:32768:8:1$miYNWo4YQE3FMwS3$8cf1bc29873f570d0a543bdd7e76a38c464b148f01df5a17935a94c5464cf1a21343fdc9d38da41349fb8f99e2f804f46902f066b604f2286e131422dafb6827", "Overall", "Admin", "Yes"),

    ("Charlie", "scrypt:32768:8:1$miYNWo4YQE3FMwS3$8cf1bc29873f570d0a543bdd7e76a38c464b148f01df5a17935a94c5464cf1a21343fdc9d38da41349fb8f99e2f804f46902f066b604f2286e131422dafb6827", "CloudBase", "Boss", "Yes"),
    ("David", "scrypt:32768:8:1$miYNWo4YQE3FMwS3$8cf1bc29873f570d0a543bdd7e76a38c464b148f01df5a17935a94c5464cf1a21343fdc9d38da41349fb8f99e2f804f46902f066b604f2286e131422dafb6827", "TechCorp", "Worker", "Yes"),
    ("Eve", "scrypt:32768:8:1$miYNWo4YQE3FMwS3$8cf1bc29873f570d0a543bdd7e76a38c464b148f01df5a17935a94c5464cf1a21343fdc9d38da41349fb8f99e2f804f46902f066b604f2286e131422dafb6827", "CloudBase", "Worker", "Yes"),
    ("Willy", "scrypt:32768:8:1$miYNWo4YQE3FMwS3$8cf1bc29873f570d0a543bdd7e76a38c464b148f01df5a17935a94c5464cf1a21343fdc9d38da41349fb8f99e2f804f46902f066b604f2286e131422dafb6827", "Overall", "Admin", "Yes")
]
cursor.executemany('INSERT INTO "User" ("Name", "Password", "Company", "Role", "Working") VALUES (?, ?, ?, ?, ?)', sample_user_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("All tables seeded successfully.")