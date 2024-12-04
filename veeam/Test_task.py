import os
import shutil
import time
import logging
import argparse

# Function to set up logging for both console and log file
def setup_logging(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),  # Logs to a file
            logging.StreamHandler()        # Logs to the console
        ]
    )

# Function to synchronize the source and replica folders
def sync_folders(source, replica):
    # Traverse all directories and files in the source folder
    for root, dirs, files in os.walk(source):
        # Get the relative path to replicate folder structure
        relative_path = os.path.relpath(root, source)
        replica_dir = os.path.join(replica, relative_path)

        # Ensure the corresponding directory exists in the replica folder
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)
            logging.info(f"Created directory: {replica_dir}")

        # Synchronize files from source to replica
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_dir, file)

            # Copy the file if it doesn't exist in replica or has been updated
            if not os.path.exists(replica_file) or (
                os.path.getmtime(source_file) > os.path.getmtime(replica_file)
            ):
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied/Updated: {source_file} -> {replica_file}")

    # Traverse the replica folder to clean up files and directories not in source
    for root, dirs, files in os.walk(replica, topdown=False):
        # Get the relative path to compare with the source folder
        relative_path = os.path.relpath(root, replica)
        source_dir = os.path.join(source, relative_path)

        # Remove files from replica that are not in source
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_dir, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"Deleted file: {replica_file}")

        # Remove directories from replica that are not in source
        for dir in dirs:
            replica_dir = os.path.join(root, dir)
            source_dir = os.path.join(source_dir, dir)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                logging.info(f"Deleted directory: {replica_dir}")

def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization Tool")
    parser.add_argument("source", help="Path to the source folder")  # Source folder to sync from
    parser.add_argument("replica", help="Path to the replica folder")  # Replica folder to sync to
    parser.add_argument("interval", type=int, help="Sync interval in seconds")  # Time interval for sync
    parser.add_argument("log_file", help="Path to the log file")  # File to record sync logs
    args = parser.parse_args()

    # Initialize logs
    setup_logging(args.log_file)

    # Logs
    logging.info("Starting synchronization...")
    logging.info(f"Source: {args.source}")
    logging.info(f"Replica: {args.replica}")
    logging.info(f"Sync interval: {args.interval} seconds")

    # Infinite loop to sync folders based on the specified interval
    while True:
        try:
            sync_folders(args.source, args.replica)
        except Exception as e:
            # Log any errors that occur during synchronization
            logging.error(f"An error occurred during synchronization: {e}")
        time.sleep(args.interval)  # Wait for the specified interval before the next sync

if __name__ == "__main__":
    main()
