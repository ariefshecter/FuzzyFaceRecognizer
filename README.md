# FuzzyFaceRecognizer

## Description

FuzzyFaceRecognizer is a facial recognition system that integrates fuzzy logic technology to enhance accuracy and flexibility in the registration and attendance process. This project is designed to facilitate attendance management in various environments, such as schools, offices, or events, by leveraging facial recognition as a user identification method.

## Key Features

- **Face Registration**: Users can register by presenting their face to the camera. The system saves the registered face data in a file format for later use.
  
- **Real-Time Attendance**: Allows users to mark attendance through facial recognition directly. Attendance data is recorded in a CSV file that can be easily accessed and analyzed.

- **Fuzzy Logic**: Utilizes fuzzy logic to handle uncertainty in facial recognition, improving the system's ability to verify identities better under various lighting conditions and angles.

- **Data Management**: Facial data is stored in a separate folder with filenames corresponding to user names, and the system automatically deletes user entries if the face images are removed.

- **Simple Interface**: Provides an easy-to-use text-based user interface for interaction with the system.

## Technologies Used

- Python
- OpenCV
- face_recognition
- Pandas
- scikit-fuzzy

## Installation

To run this project, ensure that you have installed all the required libraries. Use the following command to install the necessary packages:

```bash
pip install opencv-python face_recognition pandas scikit-fuzzy
```
## Usage

1. **Run the program** and select the option for **registration** or **attendance**.
2. Follow the instructions displayed on the screen to complete the **registration** or **attendance** process.
3. Check the **CSV file** to view the recorded attendance logs.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, feel free to create an **issue** or submit a **pull request**.

