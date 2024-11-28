import cv2
import requests
import numpy as np
import mysql.connector
from datetime import datetime
from ultralytics import YOLO
from collections import Counter
import time


class ESP32ObjectDetector:
    def __init__(self, camera_url, model_path, db_config, conf_threshold=0.5):
        """Initialize the object detector."""
        print("Initializing ESP32 Object Detector...")

        self.camera_url = camera_url
        self.conf_threshold = conf_threshold
        print("Loading YOLO model...")
        self.model = YOLO(model_path)
        print("YOLO model loaded successfully.")

        self.db_config = db_config
        self.class_names = self.model.names
        self.colors = self.generate_colors(len(self.class_names))

        print("Connecting to database...")
        self.db_connection = self.connect_database()
        print("Database connection established.")

        print("Creating detection table if it doesn't exist...")
        self.create_detection_table()
        print("Initialization complete.")

        self.paused = False

    def connect_database(self):
        """Connect to the MySQL database."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            print("Database connected successfully!")
            return conn
        except mysql.connector.Error as err:
            print(f"Failed to connect to database: {err}")
            raise

    def create_detection_table(self):
        """Create a table for storing detection results."""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detections (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME,
                    class_name VARCHAR(255),
                    detected_count INT
                )
            """)
            self.db_connection.commit()
            print("Table 'detections' is ready.")
        except mysql.connector.Error as err:
            print(f"Failed to create table: {err}")
            raise

    def insert_detection(self, class_name, count):
        """Insert detection results into the database."""
        try:
            if not self.db_connection.is_connected():
                self.db_connection = self.connect_database()
            cursor = self.db_connection.cursor()
            timestamp = datetime.now()
            cursor.execute("""
                INSERT INTO detections (timestamp, class_name, detected_count)
                VALUES (%s, %s, %s)
            """, (timestamp, class_name, count))
            self.db_connection.commit()
            print(f"Inserted detection: {class_name} with count {count}.")
        except mysql.connector.Error as err:
            print(f"Failed to insert data: {err}")

    def generate_colors(self, num_classes):
        """Generate distinct colors for each class."""
        np.random.seed(42)
        return np.random.randint(0, 255, size=(num_classes, 3), dtype='uint8')

    def start_stream(self):
        """Start the MJPEG video stream and detect objects."""
        print("Starting MJPEG video stream...")
        while True:
            try:
                response = requests.get(self.camera_url, stream=True, timeout=10)
                print(f"Stream response status: {response.status_code}")

                if response.status_code != 200:
                    print(f"Failed to connect to the camera. HTTP Status: {response.status_code}")
                    time.sleep(1)
                    continue

                bytes_data = bytes()

                for chunk in response.iter_content(chunk_size=1024):
                    bytes_data += chunk
                    a = bytes_data.find(b'\xff\xd8')  # Start of JPEG
                    b = bytes_data.find(b'\xff\xd9')  # End of JPEG
                    if a != -1 and b != -1:
                        jpg = bytes_data[a:b+2]
                        bytes_data = bytes_data[b+2:]

                        # Ensure the extracted JPEG is valid
                        if not jpg:
                            print("Extracted JPEG buffer is empty. Skipping this frame...")
                            continue

                        # Decode the JPEG to a frame
                        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                        if frame is None or frame.size == 0:
                            print("Decoded frame is invalid. Skipping this frame...")
                            continue

                        # Perform object detection
                        print("Running object detection...")
                        frame = self.detect_objects(frame)

                        # Display the detection results
                        cv2.imshow("YOLOv11 ESP32-CAM Stream", frame)

                        # Handle keyboard input for pausing or quitting
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('p'):  # Pause
                            print("Stream paused. Press 'p' to resume or 'q' to quit.")
                            cv2.waitKey(0)  # Wait indefinitely for user input
                        elif key == ord('q'):  # Quit
                            print("Exiting stream...")
                            break

            except requests.exceptions.RequestException as e:
                print(f"Stream error: {e}")
                time.sleep(1)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                cv2.destroyAllWindows()

    def detect_objects(self, frame):
        """Detect objects in the frame."""
        print("Running object detection on frame...")
        results = self.model.predict(frame, conf=self.conf_threshold)
        detections = results[0].boxes.data.cpu().numpy()

        # Count
        class_counter = Counter()
        for d in detections:
            class_id = int(d[5])
            class_counter[class_id] += 1

        # Insert
        for class_id, count in class_counter.items():
            class_name = self.class_names[class_id]
            self.insert_detection(class_name, count)

        # Visualize
        print("Visualizing detections...")
        return self.visualize_detections(frame, results)

    def visualize_detections(self, frame, results):
        """Visualize detection results on the frame."""
        detections = results[0].boxes.data.cpu().numpy()
        for d in detections:
            x1, y1, x2, y2, conf, class_id = map(int, d[:6])
            label = f"{self.class_names[class_id]}: {conf:.2f}"
            color = [int(c) for c in self.colors[class_id]]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame


if __name__ == "__main__":
    print("Starting ESP32 Object Detector...")

    
    CAMERA_URL = "http://#url#/stream"  # ESP32-CAM stream URL
    MODEL_PATH = r"D:\\Airost Intership Project\\Object_Detection\\train3\\best.pt"
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'object_detection'
    }

    try:
        
        detector = ESP32ObjectDetector(CAMERA_URL, MODEL_PATH, DB_CONFIG)
        print("Detector initialized. Starting stream...")
        detector.start_stream()
    except Exception as e:
        print(f"Fatal error: {e}")
