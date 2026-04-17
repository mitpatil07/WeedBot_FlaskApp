import cv2

class Camera:
    def __init__(self, src=0):
        self.video = cv2.VideoCapture(src)
        
        # Set resolution to 1280x720 for high resolution feed
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        return image
        
    def get_stream_frame(self, frame=None):
        if frame is None:
            frame = self.get_frame()
            if frame is None:
                return None
                
        # Encode for HTTP stream
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
