## Data Augmentation for YOLOv5 Training and the result of the new training 

## Overview
This data augmentation was performed to enhance the YOLOv5 model training using a small initial dataset . 
This process expanded the dataset to 60 images by applying various augmentation techniques.
The augmented dataset aimed to improve the model’s performance, given the limited original dataset size.

---

## Augmentation Techniques
The following augmentation methods were applied:

1. **Random Flipping:**
   - Horizontal and vertical flips to create diverse orientations.

2. **Rotation:**
   - Images were rotated within a range of -15 to +15 degrees.

3. **Scaling:**
   - Random scaling adjustments to simulate different object sizes.

4. **Shifting:**
   - Horizontal and vertical shifts to create positional variations.

5. **Brightness and Contrast Adjustments:**
   - Random changes in brightness and contrast to simulate varied lighting conditions.

6. **Gaussian Noise:**
   - Adding random noise to simulate sensor imperfections.

---

## Tools and Libraries Used
### Prerequisites
- **Python 3.x**
- Install the required libraries:
  ```bash
  pip install albumentations opencv-python
  ```
### Steps

1. **Prepare Directories**:
    `dataset/images/train`
    `augmented_images`

2. **Adjust Parameters**:
   - Modify `num_augmented_per_image` to control the number of augmented images 
3. **Run the Script**:
   ```bash
   python data_aug.py
   ```
4. **Result**:
   - The dataset size was increased (from 5 to 60 images for my case)
   - Augmented images retained the YOLO-format annotation compatibility.

---
## training Command :
   ```bash
    python train.py --img 640 --batch 16 --epochs 300 --data pool_dataset.yaml --weights yolov5m.pt --hyp hyp.scratch-med.yaml 
   ```

## Observations
- Improved training performance was observed:
  - Increased **Precision** to 91.7%.
  - Improved **Recall** to 87.5%.
  - Achieved an mAP@0.5 of 92.1% and mAP@0.5:0.95 of 43.6% after training.

---

