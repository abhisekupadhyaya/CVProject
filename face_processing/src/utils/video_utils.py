import cv2

class VideoUtils:
    @staticmethod
    def get_video_properties(video_path):
        cap = cv2.VideoCapture(video_path)
        properties = {
            'fps': int(cap.get(cv2.CAP_PROP_FPS)),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        }
        cap.release()
        return properties