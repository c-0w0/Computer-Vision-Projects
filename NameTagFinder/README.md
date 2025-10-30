## Introduction
The initial idea of this prototype was to find black area enclosed by white area.
This prototype started with the image cropped from the pdf file (passed), then moved to video processing (failed, probably due to blurry video).

## Assumption
1.	The name tag has a ratio of 4:1 (considering only the black keys area to the white key area), making it a criterion for filtering the candidate (overlap region of masks/contours).
   <img width="285" height="243" alt="image" src="https://github.com/user-attachments/assets/d0e16f30-c111-4ba7-b174-6266bdcc2830" />

## Workflow
1.	The program started by defining the HSV color ranges (upper_limit, lower_limit) for the black and white color.
2.	2 masks were created, namely ‘black_mask’ and ‘white_mask’, they detect black and white regions respectively.
3.	2 arrays of contours were created, namely ‘black_contours’ and ‘white_countours’, they store the data of bounding boxes of the regions found by masks.
4.	A nested for loop was designed to catch if any black regions were found in given white regions.
5.	Then, the passed regions are being tagged with their x, and y coordinates.

# Prototype2: YOLO
## Introduction
The idea of this prototype is to train the YOLO using annotated images.

## Workflow
1.	This prototype started with annotating the frames using CVAT.
2.	Then, the annotation labels were exported.
3.	In the program, extract the frames if the frames have annotation labels.
4.	YOLO model was trained.
5.	YOLO model was deployed to detect name tags in the video.
6.	The name tags were being tagged on the screen, and the output of coordinates were printed out in command line.
  <img width="940" height="736" alt="image" src="https://github.com/user-attachments/assets/6d67bac7-5a66-4d3d-824f-13ed77dada18" />

## Known issue
1.	Data leakage / Overfitting
Due to the training images used originated from the video itself. This will lead to overfitting of the model, as the model has pre-seen the result when the sample.mp4 is being used to test it.
