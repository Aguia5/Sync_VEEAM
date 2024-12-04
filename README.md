Folder Synchronization Tool - Instructions
This tool synchronizes the contents of a source folder with a replica folder. It ensures the replica folder is an exact match of the source folder by copying, updating, and deleting files as necessary. Synchronization runs periodically at a specified interval.

Usage
To run the script, use the following command:

python <script_name>.py <source_path> <replica_path> <interval_in_seconds> <log_file_path>

Arguments
<source_path>
Path to the folder containing the original files (source folder).
Example: /home/user/source

<replica_path>
Path to the folder where the replica of the source will be created and updated.
Example: /home/user/replica

<interval_in_seconds>
The time interval (in seconds) between each synchronization.
Example: 60 (synchronizes every 60 seconds)

<log_file_path>
Path to the file where synchronization logs will be saved.
Example: /home/user/sync.log

Features
One-way synchronization: Changes in the source folder are reflected in the replica folder.
Handles missing files/folders: Automatically creates missing directories and files in the replica.
Cleans up extra files/folders: Deletes files and folders in the replica that no longer exist in the source.
Logging: All actions (file creation, updates, deletions) are logged to the console and the specified log file.
