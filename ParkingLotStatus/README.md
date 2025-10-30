## Introduction
This project features vehicle object detection within self defined bounding boxes.

## Idea
1. Extract the first frame of the video for bounding box plotting purpose.
2. Self define the bounding boxes for parking slots by plotting on the extracted image through `Tkinter` GUI.
3. Export the coordinate of the 4 plottings for every bounding box to a JSON file.
4. Deploy a pretrained `YOLO11s.pt` model to do the classification task, it predicts on the video frame(unprocessed one).
5. Retrieve the prediction data `detections`, and calculate every detected object's coordinate.
6. Use `cv2.pointPolygonTest()` to determine whether the predictions are located in the defined bounding boxes (parking slots).
7. Output a video `output.mp4` which shows the prediction results along with the occupancy of the parking lot.

## Screenshots
### Self defining bounding boxes
<img width="1277" height="787" alt="BBox Painter" src="https://github.com/user-attachments/assets/f9eb94dc-a470-49ee-b973-5622e360b349" />

### Output Video
<img width="1594" height="900" alt="image" src="https://github.com/user-attachments/assets/43326e08-3467-4ed5-b11b-38e4e604e456" />
