# Image Processing Techniques Assignment

This repository contains the code for an image processing assignment, demonstrating various techniques using Python.

## Assignment Tasks

1. Binary Mask and Filters
   - Create a binary mask for a region of interest
   - Apply low-pass filters (Gaussian and Average)
   - Apply high-pass filters (Laplacian and Prewitt)

2. Dithering Algorithms
   - Implement Floyd-Steinberg dithering
   - Implement Jarvis-Judice-Ninke dithering
   - Compare results from both methods

3. Kuwahara Filter
   - Explain the Kuwahara filter
   - Implement and apply the Kuwahara filter

4. Fourier Transform and Frequency Domain Filters
   - Apply Fourier Transform to an image
   - Implement Butterworth filter
   - Implement Gaussian filter

5. Image Quantization
   - Quantize an image to 32 grayscale levels using only the imresize function
   - Document the steps followed in the process

## Requirements

- Python 3.x
- NumPy
- Pillow (PIL)
- Matplotlib
- OpenCV (cv2)
- scikit-image

## Usage

Each task is implemented in a separate section of the code. To run a specific task:

1. Ensure all required libraries are installed.
2. Update the `image_path` variable with the path to your input image.
3. Run the corresponding code section for the desired task.

## Notes

- The code is designed for grayscale images. Color images will be converted to grayscale.
- Results are visualized using Matplotlib.
- Some techniques may be computationally intensive for large images.

## Student Information

Mani Teja Rayana
Z23740179
