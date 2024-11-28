# ESP32-CAM Object Detection and Inventory Management System

This project leverages **ESP32-CAM**, **YOLOv11**, and a **MySQL database (via XAMPP)** to create an object detection system. 
The system uses ESP32-CAMs to capture object streams, detects objects using a trained YOLOv11 model, and stores the results in a MySQL database. 
The detection results are accessible via a web interface.

---

## **Features**
- Real-time object detection using YOLOv11.
- Integration with ESP32-CAM for streaming video.
- Automatic data storage in a MySQL database.
- A web interface to view detection results.

---

## **Requirements**

### **Hardware**
1. ESP32-CAM module (at least 1; up to 3 recommended for multi-camera setups).
2. Laptop or desktop computer.

### **Software**
1. **XAMPP**: To set up a MySQL database and PHP environment.  
   Download from [https://www.apachefriends.org/download.html](https://www.apachefriends.org/download.html).
2. **Python 3.9 or later**: For running the object detection system.
3. **Ultralytics YOLOv8**: Pre-trained model for object detection.

---

## **Setup Guide**

### **1. Install Required Software**
- Download and install [XAMPP](https://www.apachefriends.org/download.html) for your operating system.
- Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### **2. Download All required files above and save in the same directory

### **3. Put the folder of object_detection_website in htdocs directory in XAMPP.

### **4. Run the Program and check the data in the link of http://localhost/object_detection_website/index.php

##Thats it! Feel free to contact me if any mistaken. TQVM


