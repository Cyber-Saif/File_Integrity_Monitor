# File Integrity Monitor: A Real-time File System Change Detector

## Description
A Python-based file integrity monitor that scans directories for any abnormal changes, including file modifications, deletions, and new additions. 
This tool helps ensure that important files and directories remain unaltered, providing a reliable way to track unauthorized changes and maintain data integrity.

## Functions:
- Real-time Monitoring: Periodically checks for changes in files and directories.
- File Hashing: Uses SHA-256 to generate file hashes for integrity verification.
- Customizable Paths: Allows users to specify directories to monitor, with options for monitoring the current working directory.
- Change Detection: Detects file modifications, deletions, and new files, providing real-time alerts on abnormal changes.
- Baseline File Creation: Generates and stores baseline file hashes for future comparisons, ensuring an easy way to verify file integrity over time.
- Logging and Data Export: Optionally logs changes and exports the baseline for later use.

## Example Usage
![Monitor Example](https://github.com/user-attachments/assets/96ff99a4-0173-40e3-ad59-00783cbe110b)


## Important Notes:
- Ensure you have Python 3.10+ installed for compatibility with the file_digest method.
- You can enable logging to track changes by uncommenting the logging setup in the code.
