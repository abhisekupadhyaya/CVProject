import cv2
from retinaface import RetinaFace
from face_alignment import FaceAlignment, LandmarksType
import os

# Stage 1: Detect and Save Cropped Faces
def detect_and_save_faces(video_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces in the current frame
        detections = RetinaFace.detect_faces(frame)

        # Process detections and save cropped faces
        for key, face_info in detections.items():
            facial_area = face_info["facial_area"]
            cropped_face = frame[facial_area[1]:facial_area[3], facial_area[0]:facial_area[2]]

            # Save cropped face as an image file
            face_output_path = os.path.join(output_dir, f"frame_{frame_count}_face_{key}.jpg")
            cv2.imwrite(face_output_path, cropped_face)

        frame_count += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Stage 2: Align Facial Landmarks and Save Processed Frames
def align_faces_and_save(input_dir, output_video_path, frame_width, frame_height, fps):
    # Initialize Face Alignment Network (FAN)
    fa = FaceAlignment(LandmarksType.TWO_D, device='cuda' if cv2.cuda.getCudaEnabledDeviceCount() > 0 else 'cpu')

    # Initialize VideoWriter with desired dimensions
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Process each saved cropped face image
    for face_file in sorted(os.listdir(input_dir)):
        face_path = os.path.join(input_dir, face_file)
        face_image = cv2.imread(face_path)

        if face_image is None:
            continue

        # Detect facial landmarks using FAN
        landmarks = fa.get_landmarks(face_image)
        if landmarks is not None:
            # Optionally draw landmarks on the image (for visualization/debugging)
            for (x, y) in landmarks[0]:
                cv2.circle(face_image, (int(x), int(y)), 1, (0, 255, 0), -1)

        # Resize aligned face to match output dimensions if necessary
        resized_face = cv2.resize(face_image, (frame_width, frame_height))

        # Write processed frame to output video
        out.write(resized_face)

    # Release resources
    out.release()
    cv2.destroyAllWindows()

# Main Execution Flow
if __name__ == "__main__":
    video_path = "THE PERFECT BRIDE.mp4"  # Path to your input video file
    cropped_faces_dir = "cropped_faces"  # Directory to save cropped faces
    processed_video_path = "processed_video_new.mp4"  # Path to save the processed video

    # Get video properties for output video configuration
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    # Stage 1: Detect and save cropped faces
    detect_and_save_faces(video_path, cropped_faces_dir)

    # Stage 2: Align faces and save processed video
    align_faces_and_save(cropped_faces_dir, processed_video_path, frame_width, frame_height, fps)