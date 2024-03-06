import os
import shutil
import zipfile
import sys

def split_zip(input_zip, max_size=100):
    # Get the directory and filename from the input zip file
    input_dir, input_filename = os.path.split(input_zip)

    # Create output folder in the same directory as the input file
    output_folder = os.path.join(input_dir, 'output_folder')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the input zip file
    print("Opening zipped file...")
    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        # Get a list of all files in the zip file
        file_list = zip_ref.namelist()

        # Calculate the total size of the zip file
        total_size = sum(zip_ref.getinfo(file_name).file_size for file_name in file_list) / (1024 * 1024)

        # Check if splitting is needed
        if total_size <= max_size:
            print(f"The input file is already within the size limit. No need to split.")
            return

        # Initialize variables for splitting
        current_size = 0
        current_part = 1
        current_part_files = []

        # Iterate through each file in the zip
        for file_name in file_list:
            # Calculate the size of the current file in MB
            file_size = zip_ref.getinfo(file_name).file_size / (1024 * 1024)

            # Check if adding the current file exceeds half of the total size
            if current_size + file_size > total_size / 2:
                # Create a new zip file for the current part
                output_zip_name = f'{os.path.splitext(input_filename)[0]}_part_{current_part}.zip'
                output_zip = os.path.join(output_folder, output_zip_name)
                with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                    # Copy the content of the original zip file into the new zip
                    for part_file, arcname in current_part_files:
                        with zip_ref.open(part_file) as file:
                            new_zip.writestr(arcname, file.read())

                print(f'Created: {output_zip_name}')

                # Reset variables for the next part
                current_part += 1
                current_size = 0
                current_part_files = []

            # Add the current file to the list of files for the current part
            current_part_files.append((file_name, file_name))

            # Ensure the directory structure is created
            file_dir = os.path.dirname(file_name)
            if file_dir and not os.path.exists(os.path.join(output_folder, file_dir)):
                os.makedirs(os.path.join(output_folder, file_dir))

            current_size += file_size

        # Create the last part with the remaining files
        output_zip_name = f'{os.path.splitext(input_filename)[0]}_part_{current_part}.zip'
        output_zip = os.path.join(output_folder, output_zip_name)
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            # Copy the content of the original zip file into the new zip
            for part_file, arcname in current_part_files:
                with zip_ref.open(part_file) as file:
                    new_zip.writestr(arcname, file.read())

        print(f'Created: {output_zip_name}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_zip_file>")
        sys.exit(1)

    input_zip_file = sys.argv[1]

    split_zip(input_zip_file)