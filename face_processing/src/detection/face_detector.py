import cv2
from retinaface import RetinaFace
import os

class FaceDetector:
    @staticmethod
    def detect_and_save_faces(video_path, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            detections = RetinaFace.detect_faces(frame)

            for key, face_info in detections.items():
                facial_area = face_info["facial_area"]
                cropped_face = frame[facial_area[1]:facial_area[3], 
                                   facial_area[0]:facial_area[2]]

                face_output_path = os.path.join(output_dir, 
                                              f"frame_{frame_count}_face_{key}.jpg")
                cv2.imwrite(face_output_path, cropped_face)

            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()