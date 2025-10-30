## Introduction
This is a simple human face blurring project.

It takes the input of image, video, or webcam, and output respective file format (except webcam) with the face blurred.

## Steps
1. Read input file (image, video, webcam).
2. Make use of library [Mediapipe](https://mediapipe.readthedocs.io/en/latest/solutions/face_detection.html)'s Face Detection Solution to find out bounding box of human faces. 
3. Blur the area.

## Output
<img width="576" height="324" alt="output" src="https://github.com/user-attachments/assets/1c467272-c19a-40c5-ab5b-fb4b34c454b2" />
Output from image input

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/ba53310b-6d8a-4ba9-8181-4d771ea16791" />
Output from video input

## Pending task
1. Instead of using a blurring rectangle, blur the face at the polygonal detail level.
