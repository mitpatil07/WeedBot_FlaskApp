import cv2
import numpy as np
import onnxruntime as ort
import os

class WeedDetector:
    def __init__(self, model_path=None):
        self.INPUT_SIZE = 640
        self.CONF_THRESHOLD = 0.61
        self.NMS_THRESHOLD = 0.45

        # ✅ FIXED: Use absolute path so it works regardless of working directory
        if model_path is None:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weed_detector.onnx")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX model not found at: {model_path}")

        # Load ONNX model
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name

    def preprocess(self, frame):
        img = cv2.resize(frame, (self.INPUT_SIZE, self.INPUT_SIZE))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2,0,1))
        img = np.expand_dims(img, axis=0)
        return img

    def detect(self, frame):
        """
        Detects weeds using the provided ONNX model.
        Returns the annotated frame and the center X coordinate of the most confident weed.
        Always runs so bounding boxes appear whenever the camera is on.
        """
        if frame is None:
            return frame, None

        try:
            img = self.preprocess(frame)
            outputs = self.session.run(None, {self.input_name: img})
            detections = outputs[0][0].T

            boxes = []
            scores = []

            for det in detections:
                x, y, w, h, conf = det

                if conf > self.CONF_THRESHOLD:
                    x1 = int((x - w/2) * frame.shape[1] / self.INPUT_SIZE)
                    y1 = int((y - h/2) * frame.shape[0] / self.INPUT_SIZE)
                    x2 = int((x + w/2) * frame.shape[1] / self.INPUT_SIZE)
                    y2 = int((y + h/2) * frame.shape[0] / self.INPUT_SIZE)

                    boxes.append([x1, y1, x2-x1, y2-y1])
                    scores.append(float(conf))

            target_weed_center_x = None
            max_score = 0

            if len(boxes) > 0:
                indices = cv2.dnn.NMSBoxes(boxes, scores, self.CONF_THRESHOLD, self.NMS_THRESHOLD)

                for i in indices:
                    idx = int(i)
                    x_box, y_box, w_box, h_box = boxes[idx]

                    # Track the most confident weed for arm targeting
                    if scores[idx] > max_score:
                        max_score = scores[idx]
                        target_weed_center_x = x_box + (w_box // 2)

                    # ✅ Draw bounding box with confidence score
                    cv2.rectangle(frame, (x_box, y_box), (x_box + w_box, y_box + h_box), (0, 255, 0), 2)
                    label = f"Weed {scores[idx]:.2f}"
                    cv2.putText(frame, label, (x_box, y_box - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.circle(frame, (x_box + w_box // 2, y_box + h_box // 2), 5, (0, 0, 255), -1)

        except Exception as e:
            # ✅ FIXED: Don't crash the stream on detection errors
            cv2.putText(frame, f"Detection error: {e}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            return frame, None

        return frame, target_weed_center_x
