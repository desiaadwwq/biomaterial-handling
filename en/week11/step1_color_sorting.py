import cv2
import numpy as np
import os

def main():
    # 1. Load Image
    # Set the image path relative to the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, 'images', 'sample_tomatoes.png')
    
    # Read the image (Using numpy and imdecode to support Unicode paths)
    img_array = np.fromfile(image_path, np.uint8)
    image_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if image_bgr is None:
        print(f"Error: Could not find the image. Please check the path: {image_path}")
        return

    # Resize for better visibility and to fit in a 2x3 grid (400x300)
    image_bgr = cv2.resize(image_bgr, (400, 300))
    
    # 2. Color Space Conversion (BGR -> HSV, BGR -> CIE Lab)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    image_lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)

    # 3. Red Color Masking using HSV Space
    # In OpenCV, Hue(H) ranges from 0-179. Red is distributed around both 0 and 179.
    # Lower Red range (0-10)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    # Upper Red range (170-179)
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([179, 255, 255])

    mask_hsv1 = cv2.inRange(image_hsv, lower_red1, upper_red1)
    mask_hsv2 = cv2.inRange(image_hsv, lower_red2, upper_red2)
    mask_hsv_final = cv2.bitwise_or(mask_hsv1, mask_hsv2)

    # Apply the mask to the original image
    result_hsv = cv2.bitwise_and(image_bgr, image_bgr, mask=mask_hsv_final)

    # 4. Red Color Masking using CIE Lab Space
    # In OpenCV, L(0-255), a(0-255), b(0-255). Higher 'a' values indicate stronger Red characteristics.
    # L: 20-255, a: 140-255 (Red region), b: 0-255
    lower_lab = np.array([20, 140, 100])
    upper_lab = np.array([255, 255, 255])

    mask_lab = cv2.inRange(image_lab, lower_lab, upper_lab)
    
    # Apply the mask to the original image
    result_lab = cv2.bitwise_and(image_bgr, image_bgr, mask=mask_lab)
    
    # 5. Save Results (Using imencode to support Unicode paths)
    hsv_path = os.path.join(base_dir, 'images', 'result_hsv.png')
    lab_path = os.path.join(base_dir, 'images', 'result_lab.png')
    
    cv2.imencode('.png', result_hsv)[1].tofile(hsv_path)
    cv2.imencode('.png', result_lab)[1].tofile(lab_path)
    print("Results have been saved in the images folder.")

    # 6. Display Results (Merge into a single window for easy comparison)
    # Convert grayscale masks to 3-channel images to merge with color images
    mask_hsv_3c = cv2.cvtColor(mask_hsv_final, cv2.COLOR_GRAY2BGR)
    mask_lab_3c = cv2.cvtColor(mask_lab, cv2.COLOR_GRAY2BGR)

    # Function to add text to images
    def add_text(img, text):
        img_copy = img.copy()
        cv2.putText(img_copy, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        return img_copy

    # Add labels to each image
    img_orig = add_text(image_bgr, "Original")
    img_hsv_mask = add_text(mask_hsv_3c, "HSV Mask")
    img_hsv_res = add_text(result_hsv, "HSV Result")
    img_lab_mask = add_text(mask_lab_3c, "Lab Mask")
    img_lab_res = add_text(result_lab, "Lab Result")

    # Merge images into a 2x3 grid
    row1 = np.hstack([img_orig, img_hsv_mask, img_hsv_res])
    row2 = np.hstack([img_orig, img_lab_mask, img_lab_res])
    combined_image = np.vstack([row1, row2])

    cv2.imshow('Color Sorting Comparison', combined_image)

    print("Please check the popup window (OpenCV). If it's not visible, look for the Python icon on your taskbar.")
    print("While the popup window is selected, press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
