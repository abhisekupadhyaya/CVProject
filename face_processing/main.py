import os
from src.detection.face_detector import FaceDetector
from src.alignment.face_aligner import FaceAligner
from src.utils.video_utils import VideoUtils
from config.settings import CROPPED_FACES_DIR, PROCESSED_VIDEO_DIR

def process_video(input_video_path):
    # Get video properties
    video_props = VideoUtils.get_video_properties(input_video_path)
    
    # Generate output paths
    video_name = os.path.splitext(os.path.basename(input_video_path))[0]
    faces_output_dir = os.path.join(CROPPED_FACES_DIR, video_name)
    aligned_faces_dir = os.path.join(PROCESSED_VIDEO_DIR, f"{video_name}_aligned")

    # Stage 1: Detect and save faces
    detector = FaceDetector()
    detector.detect_and_save_faces(input_video_path, faces_output_dir)

    # Stage 2: Align and save faces as images
    aligner = FaceAligner()
    aligner.align_faces_and_save(
        faces_output_dir,
        aligned_faces_dir,
        video_props['width'],
        video_props['height'],
        video_props['fps']
    )

if __name__ == "__main__":
    input_video = "THE PERFECT BRIDE.mp4"
    process_video(input_video)