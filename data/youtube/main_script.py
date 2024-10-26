import os
import subprocess

def download_video_and_transcripts(video_url, output_dir):
    # Use local paths for both ffmpeg and yt-dlp
    tools_dir = os.path.expanduser("local_tools")
    ffmpeg_path = os.path.join(tools_dir, "ffmpeg")
    yt_dlp_path = os.path.join(tools_dir, "yt-dlp")
    
    # Create subfolder named after video URL
    video_folder = os.path.join(output_dir, video_url.split('/')[-1])
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    
    try:
        command = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_path,
            "-o", f"{video_folder}/%(title)s.%(ext)s",
            "--no-mtime",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "--write-auto-sub",
            "--write-sub",
            "--sub-lang", "en,hi",
            "--sub-format", "ttml",
            "--convert-subs", "srt",
            video_url
        ]
        subprocess.run(command, check=True)
        print(f"Successfully downloaded: {video_url}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_url}: {e}")
    except Exception as e:
        print(f"Error: {e}")

def read_youtube_links(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read lines and remove whitespace, empty lines
            links = [line.strip() for line in file if line.strip()]
        return links
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def main():
    # Create main directory in user's home folder
    output_directory = os.path.expanduser("youtube_downloads")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Path to the file containing YouTube links
    links_file = "YouTubeLinks.txt"
    
    # Read YouTube links from file
    youtube_links = read_youtube_links(links_file)
    
    if not youtube_links:
        print("No links found in the file or file could not be read.")
        return
    
    # Download each video
    for i, link in enumerate(youtube_links, 1):
        print(f"\nProcessing video {i} of {len(youtube_links)}")
        download_video_and_transcripts(link, output_directory)

if __name__ == "__main__":
    main()