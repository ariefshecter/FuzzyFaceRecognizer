import cv2
import face_recognition
import os
import pickle
import pandas as pd
from datetime import datetime

# Folder untuk menyimpan foto wajah
PHOTO_FOLDER = 'face_data'
ATTENDANCE_FILE = 'attendance.csv'

# Fungsi untuk menyimpan kehadiran ke file CSV
def save_attendance(name):
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=['user', 'attendance', 'time'])
        df.to_csv(ATTENDANCE_FILE, index=False)

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(ATTENDANCE_FILE)

    # Ganti df.append dengan pd.concat
    new_entry = pd.DataFrame({'user': [name], 'attendance': ['present'], 'time': [time]})
    df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(ATTENDANCE_FILE, index=False)
    print(f"Kehadiran tercatat untuk {name} pada {time}")


# Fungsi untuk absen menggunakan wajah
def attendance():
    cap = cv2.VideoCapture(0)
    print("Arahkan wajah Anda ke kamera untuk absen...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Absen", frame)
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            # Cek kecocokan wajah dengan pengguna yang terdaftar
            for user in os.listdir(PHOTO_FOLDER):
                if user.endswith('_encoding.pkl'):
                    try:
                        with open(os.path.join(PHOTO_FOLDER, user), 'rb') as f:
                            stored_encoding = pickle.load(f)
                            if face_recognition.compare_faces([stored_encoding], face_encoding)[0]:
                                name = user.split('_')[0]
                                save_attendance(name)
                                cap.release()
                                cv2.destroyAllWindows()
                                return
                    except FileNotFoundError:
                        continue

        # Tekan 'q' untuk keluar dari mode absen
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
