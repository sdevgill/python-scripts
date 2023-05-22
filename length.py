import os
import subprocess
import sys


def get_media_file_duration(file_path):
    """
    Returns the duration of a media file using ffprobe.
    """
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            return float(result.stdout)
        except ValueError:
            pass
    return 0


def get_total_duration(directory):
    """
    Returns the total duration of all media files in a directory.
    """
    total_duration = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".mp3", ".mp4", ".m4a", ".wav")):
                file_path = os.path.join(root, file)
                duration = get_media_file_duration(file_path)
                total_duration += duration

    return total_duration


def validate_directory_path(directory_path):
    """
    Validates the directory path provided as a command-line argument.
    """
    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        sys.exit(1)


def validate_command_line_arguments():
    """
    Validates the command-line arguments.
    """
    if len(sys.argv) < 2:
        print("Please provide the path to the directory.")
        sys.exit(1)


# Validate the command-line arguments
validate_command_line_arguments()

# Get the directory path from the command-line arguments
directory_path = sys.argv[1]

# Validate the directory path
validate_directory_path(directory_path)

# Get the total duration of all media files in the directory
total_duration = get_total_duration(directory_path)

# Convert the total duration to hours, minutes, and seconds
hours = int(total_duration / 3600)
minutes = int((total_duration % 3600) / 60)
seconds = int(total_duration % 60)

# Print the total duration of all media files in the directory
print(
    f"The total duration of media files in the directory is: {hours:02d}h:{minutes:02d}m:{seconds:02d}s."
)