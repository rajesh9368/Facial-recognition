import face_recognition
import cv2
import csv
from datetime import date
import time

cap = cv2.VideoCapture(0)
captured = 0
face_images = ["photos/ha.jpeg", "photos/hanuman.jpg", "photos\shiv.jpg"]
face_names = ["Name1", "Name2", "Name3"]

known_face_encodings = []
known_face_names = []

for face_image, face_name in zip(face_images, face_names):
    image = face_recognition.load_image_file(face_image)
    face_encoding = face_recognition.face_encodings(image)
    known_face_encodings.append(face_encoding)
    known_face_names.append(face_name)

csv_file = 'matches.csv'
csv_writer = csv.writer(open(csv_file, 'w'))

while captured < len(face_names):
    ret, frame = cap.read()
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        captured_image = frame.copy()
        filename = f"captured_{captured+1}.jpg"
        cv2.imwrite(filename, captured_image)
        # Display the captured image for 1 second
        cv2.imshow('Captured Image', captured_image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        captured += 1
        image1 = face_recognition.load_image_file(filename)
        face_encodings1 = face_recognition.face_encodings(image1)
        if len(face_encodings1) == 0:
            print(f"No face found in captured image {captured}.")
        else:
            face_encoding1 = face_encodings1[0]
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding1)
            if any(matches):
                matched_indices = [i for i, match in enumerate(matches) if match]
                for index in matched_indices:
                    matched_name = known_face_names[index]
                    matched_date = date.today().strftime('%Y-%m-%d')
                    csv_writer.writerow([matched_name, matched_date, "Present"])
                    print(f"Face matches with {matched_name}. Today's date is {matched_date}.")
                    known_face_encodings.pop(index)
                    known_face_names.pop(index)
            else:
                print(f"Face in captured image {captured} does not match with any of the known faces.")

# Write "Absent" for remaining names in the CSV file
for name in known_face_names:
    csv_writer.writerow([name, date.today().strftime('%Y-%m-%d'), "Absent"])

# Close the CSV file
# csv_writer.close()