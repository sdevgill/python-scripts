import subprocess
import sys
from pathlib import Path


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
        str(file_path),
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        result.check_returncode()
        return float(result.stdout)
    except (subprocess.CalledProcessError, ValueError):
        print(f"An error occurred while processing {file_path}.")
        return 0


def get_total_duration(directory):
    """
    Returns the total duration of all media files in a directory.
    """
    media_files = (
        f
        for f in directory.glob("**/*")
        if f.suffix.lower() in (".mp3", ".mp4", ".m4a", ".wav", ".m4v")
    )
    total_duration = sum(get_media_file_duration(file) for file in media_files)
    return total_duration


def validate_directory_path(directory_path):
    """
    Validates the directory path provided as a command-line argument.
    """
    if not directory_path.is_dir():
        print("Invalid directory path.")
        raise SystemExit(1)


def validate_command_line_arguments():
    """
    Validates the command-line arguments.
    """
    if len(sys.argv) < 2:
        print("Please provide the path to the directory.")
        raise SystemExit(1)


def main():
    # Validate the command-line arguments
    validate_command_line_arguments()

    # Get the directory path from the command-line arguments
    directory_path = Path(sys.argv[1])

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


if __name__ == "__main__":
    main()
