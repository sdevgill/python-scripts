import re
import sys
import urllib.request
import subprocess


def download_wistia_video(video_id, filename, convert_to_mp3=False):
    base_url = "http://fast.wistia.net/embed/iframe/"
    full_url = base_url + video_id

    try:
        # Fetch the page content
        with urllib.request.urlopen(full_url) as response:
            page_content = response.read().decode("utf-8")

        # Regex to find the video URL
        video_url_pattern = re.compile(r'"type":"original".*?"url":"(http[^"]+\.bin)"')
        match = video_url_pattern.search(page_content)

        if match:
            video_url = match.group(1).replace("\\/", "/")
            video_url_mp4 = video_url.replace(".bin", ".mp4")

            # Download the video
            video_content = urllib.request.urlopen(video_url_mp4).read()
            temp_filename = (
                filename if not convert_to_mp3 else filename.replace(".mp3", ".mp4")
            )
            with open(temp_filename, "wb") as video_file:
                video_file.write(video_content)

            if convert_to_mp3:
                # Convert MP4 to MP3 using ffmpeg
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        temp_filename,
                        "-vn",
                        "-ab",
                        "128k",
                        "-ar",
                        "44100",
                        "-y",
                        filename,
                    ]
                )
                print(f"Converted to {filename} successfully.")
            else:
                print(f"Downloaded {filename} successfully.")
        else:
            print("Failed to extract video URL.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python download_wistia.py <video_id> <filename.mp4 or filename.mp3> <convert_to_mp3: true or false>"
        )
    else:
        video_id = sys.argv[1]
        filename = sys.argv[2]
        convert_to_mp3 = sys.argv[3].lower() == "true"
        download_wistia_video(video_id, filename, convert_to_mp3)


# Instructions to Run the Script

# Ensure ffmpeg is installed on your system. You can download it from FFmpeg's official website or install it through your system's package manager.
# Save the script in a file, e.g., download_wistia.py.
# Run the script with the desired options. For example, to download and convert to MP3:

# python download_wistia.py your_video_id_here output_filename.mp3 true
