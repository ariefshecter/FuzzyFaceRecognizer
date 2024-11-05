import cv2
import face_recognition
import os
import pickle
import numpy as np
from datetime import datetime
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Folder untuk menyimpan foto wajah
PHOTO_FOLDER = 'face_data'

# Fungsi untuk menyimpan data wajah
def save_face_encoding(name, encoding):
    if not os.path.exists(PHOTO_FOLDER):
        os.makedirs(PHOTO_FOLDER)
    
    # Simpan encoding wajah dalam pickle
    with open(os.path.join(PHOTO_FOLDER, f'{name}_encoding.pkl'), 'wb') as f:
        pickle.dump(encoding, f)

# Fungsi untuk melakukan evaluasi kecocokan wajah menggunakan logika fuzzy
def fuzzy_evaluation(similarity_score):
    # Fuzzy set untuk kecocokan wajah
    similarity = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'similarity')
    registration = ctrl.Consequent(np.arange(0, 11, 1), 'registration')

    similarity.automf(3)  # Menghasilkan 3 kategori: poor, average, good
    registration.automf(3)

    rule1 = ctrl.Rule(similarity['poor'], registration['poor'])
    rule2 = ctrl.Rule(similarity['average'], registration['average'])
    rule3 = ctrl.Rule(similarity['good'], registration['good'])

    registration_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    registration_simulator = ctrl.ControlSystemSimulation(registration_ctrl)

    registration_simulator.input['similarity'] = similarity_score
    registration_simulator.compute()

    return registration_simulator.output['registration']

# Fungsi untuk registrasi wajah dengan logika fuzzy
def register():
    name = input("Masukkan nama: ")
    cap = cv2.VideoCapture(0)
    print("Arahkan wajah Anda ke kamera untuk registrasi...")

    face_detected = False
    while not face_detected:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Registrasi", frame)
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if len(face_encodings) > 0:
            face_detected = True
            face_encoding = face_encodings[0]

            # Evaluasi kecocokan wajah dengan logika fuzzy
            similarity_scores = []
            for user in os.listdir(PHOTO_FOLDER):
                if user.endswith('_encoding.pkl'):
                    try:
                        with open(os.path.join(PHOTO_FOLDER, user), 'rb') as f:
                            stored_encoding = pickle.load(f)
                            similarity = face_recognition.face_distance([stored_encoding], face_encoding)[0]
                            similarity_scores.append(similarity)
                    except FileNotFoundError:
                        continue

            if similarity_scores:
                min_similarity_score = min(similarity_scores)
                fuzzy_score = fuzzy_evaluation(1 - min_similarity_score)  # Ubah similarity menjadi nilai antara 0 dan 1

                # Jika nilai fuzzy_score cukup tinggi, registrasi berhasil
                if fuzzy_score >= 7:  # Anda dapat mengubah nilai ini untuk memodifikasi tingkat kecocokan
                    print(f"Registrasi berhasil untuk {name}")
                    save_face_encoding(name, face_encoding)
                else:
                    print("Wajah terlalu mirip dengan wajah yang sudah terdaftar, silakan coba lagi.")
            else:
                print(f"Registrasi berhasil untuk {name}")
                save_face_encoding(name, face_encoding)

    cap.release()
    cv2.destroyAllWindows()
