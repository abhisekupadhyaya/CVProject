#!/bin/bash

# Create a local directory
mkdir -p local_tools
cd local_tools

# Download yt-dlp
echo "Downloading yt-dlp..."
curl -L -o yt-dlp "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
chmod +x yt-dlp

# Download ffmpeg
echo "Downloading ffmpeg..."
# Determine OS architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    FFMPEG_URL="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
elif [ "$ARCH" = "aarch64" ]; then
    FFMPEG_URL="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linuxarm64-gpl.tar.xz"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

# Download and extract ffmpeg
wget -O ffmpeg-latest.tar.xz "$FFMPEG_URL"
tar xvf ffmpeg-latest.tar.xz
mv ffmpeg-master-latest-linux*/bin/ffmpeg ./ffmpeg
mv ffmpeg-master-latest-linux*/bin/ffprobe ./ffprobe
chmod +x ffmpeg ffprobe

# Clean up
rm -rf ffmpeg-master-latest-linux* ffmpeg-latest.tar.xz

echo "Installation complete! Tools installed in ~/local_tools/"