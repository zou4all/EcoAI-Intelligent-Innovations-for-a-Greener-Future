import os
import cv2
import albumentations as A
from albumentations.core.composition import OneOf

# Define augmentation pipeline
def get_augmentation_pipeline():
    return A.Compose([
        A.HorizontalFlip(p=0.5),  # Horizontal Flip
        A.VerticalFlip(p=0.5),    # Vertical Flip
        A.RandomRotate90(p=0.5),  # Random 90-degree rotation
        A.Transpose(p=0.5),       # Transpose (swap axes)
        A.Affine(scale=(0.9, 1.1), translate_percent=(0.05, 0.1), rotate=(-15, 15), p=0.7),  # Affine Transformation
        A.RandomBrightnessContrast(p=0.5),  # Random Brightness & Contrast
        A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.5),  # Color adjustment
        A.Blur(blur_limit=3, p=0.3),        # Blur the image
        A.CLAHE(p=0.3),                     # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    ])

# Apply augmentations and save the images
def apply_augmentations(input_dir, output_dir, num_augmented_per_image=10):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load augmentation pipeline
    augmentations = get_augmentation_pipeline()

    # Iterate over all images in the input directory
    for image_file in os.listdir(input_dir):
        if not image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        # Read the image
        image_path = os.path.join(input_dir, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load {image_path}")
            continue

        # Apply augmentations
        for i in range(num_augmented_per_image):
            augmented = augmentations(image=image)
            augmented_image = augmented['image']

            # Save the augmented image
            output_file = f"{os.path.splitext(image_file)[0]}_aug_{i + 1}.jpg"
            cv2.imwrite(os.path.join(output_dir, output_file), augmented_image)

    print(f"Augmented images saved to {output_dir}")

# Main function to run the script
if __name__ == "__main__":
    input_dir = "dataset/images/train"  # Replace with the directory containing your original images
    output_dir = "augmented_images"  # Replace with the directory to save augmented images
    num_augmented_per_image = 20  # Number of augmented images to generate per original image

    apply_augmentations(input_dir, output_dir, num_augmented_per_image)
