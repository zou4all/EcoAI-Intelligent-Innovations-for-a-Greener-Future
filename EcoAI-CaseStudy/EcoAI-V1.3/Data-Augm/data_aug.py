import os
import cv2
import albumentations as A
from glob import glob

def get_augmentation_pipeline():
    return A.Compose([
        A.HorizontalFlip(p=0.5),  
        A.VerticalFlip(p=0.5),    
        A.RandomRotate90(p=0.5),  
        A.Transpose(p=0.5),       
        A.Affine(scale=(0.9, 1.1), translate_percent=(0.05, 0.1), rotate=(-15, 15), p=0.7),  
        A.RandomBrightnessContrast(p=0.5),  
        A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.5),  
        A.Blur(blur_limit=3, p=0.3),  
        A.CLAHE(p=0.3),  
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.3))

def apply_augmentations(input_img_dir, input_label_dir, output_dir, num_augmented_per_image=10):
    output_image_dir = os.path.join(output_dir, "images")
    output_label_dir = os.path.join(output_dir, "labels")
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    augmentations = get_augmentation_pipeline()

    image_files = glob(os.path.join(input_img_dir, "*.jpg")) + glob(os.path.join(input_img_dir, "*.png"))

    for image_path in image_files:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Unable to load image {image_path}")
            continue

        label_path = image_path.replace(input_img_dir, input_label_dir).replace(".jpg", ".txt").replace(".png", ".txt")
        if not os.path.exists(label_path):
            print(f"Warning: No annotation file found for {image_path}, skipping...")
            continue

        with open(label_path, "r") as f:
            boxes = [list(map(float, line.strip().split())) for line in f.readlines()]

        class_labels = [b[0] for b in boxes]  # Extract class labels
        bboxes = [b[1:] for b in boxes]  # Extract bounding boxes (x_center, y_center, width, height)

        for i in range(num_augmented_per_image):
            augmented = augmentations(image=image, bboxes=bboxes, class_labels=class_labels)

            if not augmented["bboxes"]: 
                continue

            augmented_image = augmented["image"]
            augmented_bboxes = augmented["bboxes"]
            augmented_labels = augmented["class_labels"]

            aug_img_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_aug_{i+1}.jpg"
            aug_img_path = os.path.join(output_image_dir, aug_img_filename)
            cv2.imwrite(aug_img_path, augmented_image)

            aug_label_filename = aug_img_filename.replace(".jpg", ".txt").replace(".png", ".txt")
            aug_label_path = os.path.join(output_label_dir, aug_label_filename)

            with open(aug_label_path, "w") as f:
                for bbox, cls in zip(augmented_bboxes, augmented_labels):
                    x_center, y_center, width, height = bbox
                    if 0 < width <= 1 and 0 < height <= 1:  # Ensure valid YOLO bbox format
                        f.write(f"{int(cls)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    print(f"Augmented images and labels saved to {output_dir}.")

if __name__ == "__main__":
    input_img_dir = "dataset/images/train"  # Original image directory
    input_label_dir = "dataset/labels/train"  # YOLO label directory
    output_dir = "augmented_dataset"  # Where to save augmented images and labels
    num_augmented_per_image = 20  

    apply_augmentations(input_img_dir, input_label_dir, output_dir, num_augmented_per_image)
