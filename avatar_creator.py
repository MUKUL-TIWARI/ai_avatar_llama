import cv2
from PIL import Image
import os

def capture_user_face():
    """Capture user's face from webcam and save as 'user_face.jpg'."""
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("📷 Capture Your Image (Press SPACE to Capture, ESC to Exit)")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to grab frame")
            break
        cv2.imshow("📷 Capture Your Image (Press SPACE to Capture, ESC to Exit)", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC pressed
            print("🛑 Capture cancelled.")
            cam.release()
            cv2.destroyAllWindows()
            return None
        elif k % 256 == 32:  # SPACE pressed
            img_name = "user_face.jpg"
            cv2.imwrite(img_name, frame)
            print(f"✅ Image captured and saved as {img_name}")
            cam.release()
            cv2.destroyAllWindows()
            return img_name

    cam.release()
    cv2.destroyAllWindows()
    return None


def cartoonize_image(image_path):
    """Convert an image into a cartoon-style avatar."""
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Could not load image for cartoonizing.")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )

    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    out_name = "user_avatar.png"
    cv2.imwrite(out_name, cartoon)
    print(f"🎨 Cartoon avatar saved as {out_name}")

    return out_name


def create_avatar():
    """Main function to capture face and convert it into cartoon avatar."""
    print("📸 Starting face capture...")
    face_img = capture_user_face()
    if not face_img:
        print("❌ No image captured.")
        return None

    print("🎨 Converting captured image to cartoon style...")
    avatar_img = cartoonize_image(face_img)

    if avatar_img:
        print("✅ Avatar creation complete!")
    else:
        print("⚠️ Avatar creation failed.")

    return avatar_img


if __name__ == "__main__":
    create_avatar()
