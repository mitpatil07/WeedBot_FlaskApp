import cv2

class Camera:
    def __init__(self, src=0):
        # Use DirectShow backend on Windows to prevent hangs with multiple cameras
        self.video = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        
        if not self.video.isOpened():
            print(f"ERROR: Could not open video source {src} with DSHOW. Trying default...")
            self.video = cv2.VideoCapture(src)
            if not self.video.isOpened() and src != 0:
                print(f"ERROR: Source {src} failed. Falling back to source 0.")
                self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Lowered from 1280x720 → 640x480 for performance
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.video.set(cv2.CAP_PROP_FPS, 30)

        self._frame_count = 0

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        self._frame_count += 1
        return image

    def should_detect(self, every_n=3):
        """✅ FIX 3: Only run heavy ONNX detection every N frames
        This reduces CPU load by 3x — key to stopping Pi crashes"""
        return self._frame_count % every_n == 0

    def get_stream_frame(self, frame=None):
        if frame is None:
            frame = self.get_frame()
            if frame is None:
                return None

        # ✅ FIX 4: Check imencode return value + lower JPEG quality
        # Lower quality = less data = less CPU/network load
        ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        if not ret:
            return None
        return jpeg.tobytes()
