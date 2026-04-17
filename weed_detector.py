import cv2
import numpy as np
import onnxruntime as ort

class WeedDetector:
    def __init__(self, model_path="weed_detector.onnx"):
        self.INPUT_SIZE = 640
        self.CONF_THRESHOLD = 0.61
        self.NMS_THRESHOLD = 0.45
        
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
        """
        if frame is None:
            return frame, None
            
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

        indices = cv2.dnn.NMSBoxes(boxes, scores, self.CONF_THRESHOLD, self.NMS_THRESHOLD)
        
        target_weed_center_x = None
        max_score = 0
        
        for i in indices:
            idx = int(i)
            x_box, y_box, w_box, h_box = boxes[idx]
            
            # Use the most confident detection for the arm
            if scores[idx] > max_score:
                max_score = scores[idx]
                target_weed_center_x = x_box + (w_box // 2)

            # Draw bounding box for visualization on stream
            cv2.rectangle(frame, (x_box, y_box), (x_box + w_box, y_box + h_box), (0, 255, 0), 2)
            cv2.putText(frame, "Weed", (x_box, y_box - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.circle(frame, (x_box + w_box // 2, y_box + h_box // 2), 5, (0, 0, 255), -1)
                
        return frame, target_weed_center_x
