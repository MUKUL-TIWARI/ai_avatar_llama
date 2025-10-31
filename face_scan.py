import cv2
import os

def scan_face(save_path="face_scan.jpg"):
    """📸 Capture a live face photo using webcam."""
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Face Scanner")

    print("\n🧍 Position your face in front of the camera. Press 's' to save or 'q' to quit.\n")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        cv2.imshow("Face Scanner", frame)

        k = cv2.waitKey(1)
        if k % 256 == 115:  # 's' key to save
            cv2.imwrite(save_path, frame)
            print(f"✅ Face image saved as {save_path}")
            break
        elif k % 256 == 113:  # 'q' key to quit
            print("❌ Capture cancelled by user.")
            save_path = None
            break

    cam.release()
    cv2.destroyAllWindows()
    return save_path
