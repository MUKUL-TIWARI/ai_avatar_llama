import cv2
import time

def capture_user_face():
    # Load Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    print("📸 Please face the camera — it will auto-capture when your face is detected.")
    face_detected_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Camera not detected!")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(faces) > 0:
            # Start timer once face detected
            if face_detected_time is None:
                face_detected_time = time.time()
            elif time.time() - face_detected_time >= 2:  # Wait 2 seconds of stable detection
                (x, y, w, h) = faces[0]
                face_only = frame[y:y+h, x:x+w]
                cv2.imwrite("face_scan.jpg", face_only)
                print("✅ Face automatically captured and saved as face_scan.jpg")
                break
        else:
            face_detected_time = None  # Reset timer if face lost

        cv2.imshow("Auto Face Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("❌ Capture canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    capture_user_face()
    
