import cv2
from face_alignment import FaceAlignment, LandmarksType
import os

class FaceAligner:
    def __init__(self):
        self.fa = FaceAlignment(
            LandmarksType.TWO_D,
            device='cuda' if cv2.cuda.getCudaEnabledDeviceCount() > 0 else 'cpu'
        )

    def align_faces_and_save(self, input_dir, output_dir, frame_width, frame_height, fps):
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for face_file in sorted(os.listdir(input_dir)):
            face_path = os.path.join(input_dir, face_file)
            face_image = cv2.imread(face_path)

            if face_image is None:
                continue

            landmarks = self.fa.get_landmarks(face_image)
            if landmarks is not None:
                for (x, y) in landmarks[0]:
                    cv2.circle(face_image, (int(x), int(y)), 1, (0, 255, 0), -1)

            resized_face = cv2.resize(face_image, (frame_width, frame_height))
            
            # Save the aligned face with the same filename in the output directory
            output_path = os.path.join(output_dir, face_file)
            cv2.imwrite(output_path, resized_face)