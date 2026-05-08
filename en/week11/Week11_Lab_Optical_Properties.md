# Week 11 Lab: Optical Properties I - Fundamentals of Color Engineering and Quality Grading

## 🎯 Lab Objectives

- **Understanding Color Spaces**: Comparative analysis of RGB, HSV, and CIE Lab models
- **Implementation of Object Extraction Algorithm**: Utilization of Python and OpenCV library
- **Application of Automated Quality Sorting**: Classification of agricultural product (tomato) maturity via Masking technique

---

## 📸 1. Lab Environment and Materials

- **Software**: Python 3.x, OpenCV (`cv2`), NumPy
- **Lab Data**: `images/sample_tomatoes.png` (Tomato images with varying maturity levels)
- **Development Environment**: VS Code, Google Colab, or Antigravity IDE

---

## 🎨 2. Summary of Color Space Theory

| Color Space | Channel Composition | Characteristics in Agriculture/Vision |
|-------------|---------------------|---------------------------------------|
| **RGB** | Red, Green, Blue | Primary colors of light. Highly vulnerable to illumination changes. Difficult for color separation. |
| **HSV** | Hue, Saturation, Value | Separation of color and brightness. Advantageous for object tracking and masking. |
| **CIE Lab** | L (Lightness), a (Red-Green), b (Yellow-Blue) | Most similar to human visual perception. Standard for precise color difference analysis. |

---

## 💻 3. Implementation Steps

### 3-1. Image Loading and Preprocessing

- Image loading using OpenCV (`cv2.imread`)
- Understanding BGR format characteristics (OpenCV default load method)
- Image resizing for monitor display (`cv2.resize`)

### 3-2. Color Space Conversion

- Conversion of original BGR image to target color spaces required
- `cv2.cvtColor(image, cv2.COLOR_BGR2HSV)`: HSV space conversion
- `cv2.cvtColor(image, cv2.COLOR_BGR2LAB)`: CIE Lab space conversion

### 3-3. Red Masking: HSV Based

- Red exists across **around 0** and **around 179** in the Hue range (0~179)
- Creation of two region masks (Lower Red, Upper Red) and combination via `cv2.bitwise_or` required
- **Advantage**: Intuitive color threshold setting possible

### 3-4. Red Masking: CIE Lab Based

- Ignore L (Lightness) or set to a wide range
- Easy extraction of red when **a channel** (Red-Green) value is set high (e.g., 140~255)
- **Advantage**: Robust to illumination changes and precise for visual quality grading

### 3-5. Result Display and Saving

- Masked image synthesis with original image via `cv2.bitwise_and` function
- Result comparison: Visual inspection of Original, HSV Result, and CIE Lab Result
- Analysis result saving via `cv2.imwrite` function completed

---

## 📝 4. Discussion and Evaluation Criteria

- Comparative analysis of extraction performance (noise, edge clarity) between HSV mask and CIE Lab mask required
- Threshold resetting experiment (Hue or a/b channel) for sorting orange (Partially ripe) tomatoes recommended
- Discussion on application limitations in actual industrial fields (e.g., conveyor belts) with non-uniform lighting conditions
