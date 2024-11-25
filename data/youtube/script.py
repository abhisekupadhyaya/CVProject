import cv2
from retinaface import RetinaFace

# Load video
video_path = "THE PERFECT BRIDE.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize VideoWriter with cropped face dimensions (adjust as needed)
output_path = 'processed_video.mp4'
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect faces in the current frame
    detections = RetinaFace.detect_faces(frame)

    # Process detections and write cropped faces to output video
    for key, face_info in detections.items():
        facial_area = face_info["facial_area"]
        cropped_face = frame[facial_area[1]:facial_area[3], facial_area[0]:facial_area[2]]
        
        # Resize cropped face to match output dimensions if necessary
        resized_face = cv2.resize(cropped_face, (frame_width, frame_height))
        
        # Write processed frame to output video
        out.write(resized_face)

    # Explicitly release memory for the current frame
    del frame

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()