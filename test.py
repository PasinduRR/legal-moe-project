# print file names in data/raw
import os
def list_files_in_directory(directory):
    try:
        # List all files in the specified directory
        files = os.listdir(directory)
        return files
    except FileNotFoundError:
        print(f"The directory {directory} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    directory = "data/raw"
    files = list_files_in_directory(directory)
    print("Files in directory:", files)