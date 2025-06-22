# File Integrity Monitor: A Real-time File System Change Detector

## Description
A Python-based file integrity monitor that scans directories for any abnormal changes, including file modifications, deletions, and new additions. 
This tool helps ensure that important files and directories remain unaltered, providing a reliable way to track unauthorized changes and maintain data integrity.

## Functions:
- **Real-time Monitoring:** Periodically checks for changes in files and directories.
- **File Hashing:** Uses SHA-256 to generate file hashes for integrity verification.
- **Customizable Paths:** Allows users to specify directories to monitor, with options for monitoring the current working directory.
- **Change Detection:** Detects file modifications, deletions, and new files, providing real-time alerts on abnormal changes.
- **Baseline File Creation:** Generates and stores baseline file hashes for future comparisons, ensuring an easy way to verify file integrity over time.
- **Logging and Data Export:** Optionally logs changes and exports the baseline for later use.

## Test the Program:
To help you test the program, you can use the included "To Monitor" folder. It contains sample files. 
You can:
- Delete or modify these files.
- The program will alert you to any changes, deletions, or new additions, showing you how the integrity monitoring works in action.

## Installation:
Clone this repository and run the script with Python 3.10 or higher. The program will prompt you to select a directory for monitoring or will default to the current working directory.
Usage:
- Run the Program: Simply execute the script to start monitoring.
- User Interaction: You will be prompted to either select a directory or monitor the current working directory.
- Customizable Options: Configure the program to update the baseline or skip it, depending on your

## Example:
``` bash
git clone https://github.com/Cyber-Saif/File_Integrity_Monitor.git
cd File_Integrity_Monitor
python3 File_Integrity_Monitor.py
```


## Example Usage
You can clone the repository and run the program in the current directory to test the program. For testing example folder is attached "To Monitor"

![Monitor Example](https://github.com/user-attachments/assets/96ff99a4-0173-40e3-ad59-00783cbe110b)


## Important Notes:
- Ensure you have Python 3.10+ installed for compatibility with the file_digest method.
- You can enable logging to track changes by uncommenting the logging setup in the code.
