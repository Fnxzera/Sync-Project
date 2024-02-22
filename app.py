import argparse
import os
import shutil
import time

def sync_folders(source_folder, replica_folder, log_file):
    # Verify if the source folder exists.
    if not os.path.exists(source_folder):
        print(f"The source folder '{source_folder}' doesnt exists.")
        return

    # Verify if the replic folder exists, otherwise create it.
    if not os.path.exists(replica_folder):
        print(f"The replica folder '{replica_folder}' doesnt exists. Creating...")
        os.makedirs(replica_folder)
    
    source_files = os.listdir(source_folder)
    replica_files = os.listdir(replica_folder)
    for file_name in source_files:
        #Get the files/folders names.
        source_path = os.path.join(source_folder, file_name)
        replica_path = os.path.join(replica_folder, file_name)       
        # Verify if some file on source isnt on replic.
        if file_name not in replica_files:
            # Write the copy source-replic operation on log_file.
            with open(log_file, 'a') as log:
                log.write(f"File copied: {file_name} from source.\n")
    try:
        # Copy all the folders and files from source folder to replic.
        shutil.copytree(source_folder, replica_folder, dirs_exist_ok=True)
        print(f"Folder syncronized: {source_folder} -> {replica_folder}")
        # Write the operation on log file.
        with open(log_file, 'a') as log:
            log.write(f"Folder syncronized: {source_folder} -> {replica_folder}\n")
        
    except Exception as e:
        print(f"Error to sync folder: {e}")

    # Delete folders or files on replic folder that isnt present in source folder.
    for item in os.listdir(replica_folder):
        replica_item = os.path.join(replica_folder, item)
        source_item = os.path.join(source_folder, item)
        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
                print(f"Folder deteled: {replica_item}")               
                with open(log_file, 'a') as log:
                    log.write(f"Folder deteled from replic: {replica_item}\n")
            else:
                os.remove(replica_item)
                print(f"File deteled: {replica_item}")       
                with open(log_file, 'a') as log:
                    log.write(f"File deleted: {replica_item}\n")

def main():
    # Define args on command line
    parser = argparse.ArgumentParser(description='Sync folders')
    parser.add_argument('source_folder', type=str, help='Path to source folder')
    parser.add_argument('replica_folder', type=str, help='Path to replica folder')
    parser.add_argument('--sync_interval', type=int, default=30, help='Sync interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to log file')
    args = parser.parse_args()

    print("Syncing folders...")
    while True:
        # Sync folders 
        sync_folders(args.source_folder, args.replica_folder, args.log_file)
        print("Sync completed. Waiting for next sync...")
        # Sync interval
        time.sleep(args.sync_interval)

if __name__ == "__main__":
    main()

