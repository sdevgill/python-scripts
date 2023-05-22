import os
import re
from datetime import datetime
import sys


def is_already_renamed(filename):
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}-[\w-]+\.\w+$")
    return bool(pattern.match(filename))


def rename_files(path):
    for filename in os.listdir(path):
        if is_already_renamed(filename):
            continue

        # Get the file extension
        file_ext = os.path.splitext(filename)[1]

        # Clean the filename by replacing spaces and underscores with hyphens, removing special characters, and making it lowercase
        basename, file_ext = os.path.splitext(filename)
        clean_basename = (
            re.sub(r"[^\w\s-]", "", basename.replace(".", ""))
            .replace(" ", "-")
            .replace("_", "-")
            .lower()
        )
        clean_name = f"{clean_basename}{file_ext}"

        # Get the file creation date, last modified date, or current date
        creation_date = os.path.getctime(os.path.join(path, filename))
        modified_date = os.path.getmtime(os.path.join(path, filename))
        current_date = datetime.now().timestamp()

        if creation_date < modified_date:
            date_to_use = creation_date
        elif modified_date < creation_date:
            date_to_use = modified_date
        else:
            date_to_use = current_date

        # Format the date in yyyy-mm-dd format
        formatted_date = datetime.fromtimestamp(date_to_use).strftime("%Y-%m-%d")

        # Create the new filename with the date and cleaned filename
        new_filename = f"{formatted_date}-{clean_name}"

        # Rename the file
        os.rename(os.path.join(path, filename), os.path.join(path, new_filename))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        rename_files(directory)
    else:
        print("Please provide a directory path as an argument.")


# Todo
# Read EXIF metadata from images and use the date taken as the date to use
