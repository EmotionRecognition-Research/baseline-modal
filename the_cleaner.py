import os

def delete_files_with_extension(folder_path, extensions):
    """
    Delete files with specified extensions in a given folder.

    Args:
    - folder_path (str): Path to the folder containing the files.
    - extensions (list): List of file extensions to delete.

    Returns:
    - None
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

# delete ravdess generated files
folder_path = "./ravdess_preprocessing/ravdess"
extensions = ['avi', 'npy']
delete_files_with_extension(folder_path, extensions)
