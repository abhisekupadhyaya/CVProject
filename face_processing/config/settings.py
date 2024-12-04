import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CROPPED_FACES_DIR = os.path.join(PROJECT_ROOT, "output", "cropped_faces")
PROCESSED_VIDEO_DIR = os.path.join(PROJECT_ROOT, "output", "processed_videos")

# Ensure output directories exist
os.makedirs(CROPPED_FACES_DIR, exist_ok=True)
os.makedirs(PROCESSED_VIDEO_DIR, exist_ok=True)

# Video processing settings
VIDEO_CODEC = 'mp4v'