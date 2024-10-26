import asyncio
import os
import subprocess
import random
import time
from typing import List

class YouTubeDownloader:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        self.retry_delays = [1, 2, 4, 8, 16]

    async def download_video(self, video_url: str, output_dir: str) -> None:
        tools_dir = os.path.expanduser("local_tools")
        ffmpeg_path = os.path.join(tools_dir, "ffmpeg")
        yt_dlp_path = os.path.join(tools_dir, "yt-dlp")
        
        video_folder = os.path.join(output_dir, video_url.split('/')[-1])
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)
        
        for attempt, delay in enumerate(self.retry_delays):
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
                    "--user-agent", random.choice(self.user_agents),
                    "--sleep-interval", "2",
                    "--max-sleep-interval", "5",
                    video_url
                ]
                
                # Modified subprocess call with proper arguments
                process = await asyncio.create_subprocess_exec(
                    *command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0:
                    print(f"Successfully downloaded: {video_url}")
                    break
                else:
                    raise subprocess.CalledProcessError(process.returncode, command)
                
            except subprocess.CalledProcessError as e:
                if attempt < len(self.retry_delays) - 1:
                    print(f"Attempt {attempt + 1} failed for {video_url}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    print(f"Error downloading {video_url} after all attempts: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

async def process_batch(downloader: YouTubeDownloader, links: List[str], 
                       output_dir: str, batch_size: int = 3) -> None:
    total_links = len(links)
    for i in range(0, total_links, batch_size):
        # Get the current batch, handling the last partial batch correctly
        current_batch = links[i:min(i + batch_size, total_links)]
        tasks = [downloader.download_video(link, output_dir) for link in current_batch]
        await asyncio.gather(*tasks)
        
        # Add delay between batches, but only if there are more links to process
        remaining_links = total_links - (i + batch_size)
        if remaining_links > 0:
            await asyncio.sleep(5)

def read_youtube_links(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as file:
            links = [line.strip() for line in file if line.strip()]
        return links
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

async def main():
    output_directory = os.path.expanduser("youtube_downloads")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    links_file = "YouTubeLinks.txt"
    youtube_links = read_youtube_links(links_file)
    
    if not youtube_links:
        print("No links found in the file or file could not be read.")
        return
    
    downloader = YouTubeDownloader()
    await process_batch(downloader, youtube_links, output_directory)

if __name__ == "__main__":
    asyncio.run(main())