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
1. **ESP32-CAM module**.
2. **Laptop or desktop computer**.

### **Software**
1. **XAMPP**: To set up a MySQL database and PHP environment.  
   Download from [https://www.apachefriends.org/download.html](https://www.apachefriends.org/download.html).
2. **Python 3.9 or later**: For running the object detection system.  
   Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
3. **Ultralytics YOLOv11**: Pre-trained model for object detection.

---

## **Setup Guide**

### **1. Install Required Software**
- Download and install **XAMPP** for your operating system.
- Install **Python** from [here](https://www.python.org/downloads/).

### **2. Download All Required Files**
- Download all the necessary files for this project and place them in the same directory on your system.

### **3. Configure XAMPP**
- Place the folder `object_detection_website` inside the `htdocs` directory of your **XAMPP** installation:
  - Typically, the path to the `htdocs` directory will be `C:/xampp/htdocs/`.
  - Move the `object_detection_website` folder into `htdocs/`.

### **4. Run the Program**
- Run the Python program to start the object detection process.
- Access the results via the web interface by visiting:  
  [http://localhost/object_detection_website/index.php](http://localhost/object_detection_website/index.php)

---

## **That's it!**  
Feel free to contact me if you encounter any issues or errors. Thank you very much for using this project! 😊

