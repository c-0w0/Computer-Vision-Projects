# Strawberry Detection with YOLOv11n
This project implements a YOLOv11n model to detect strawberries in images. It includes data preparation, model training, evaluation, and visualization of results.

## Dataset
The dataset consists of many different fruits but only `strawberry` is selected for this project, which is stored in `_Inputs` folder.

- In `_Inputs/strawberry`, `train`, `valid` and `test` folders are provided alongside `data.yaml` file that specifies the pathing for training, validation and testing respectively.
- In `train`, `valid` and `test`, there are `images` and `labels` which are the images and the annotation labels for every image.

Dataset Source: [deepNIR 11 Fruits annotations](https://www.kaggle.com/datasets/enddl22/deepnir-11fruits)

## Features
- Dataset analysis (train/val/test split)
- YOLOv11n model training on custom strawberry annotations dataset
- Performance metrics visualization (loss curves, mAP, confusion matrix)
- Inference on test images with bounding box visualization

## Requirements
- Python 3.x
- Ultralytics YOLO
- OpenCV
- Pandas
- Matplotlib
- Seaborn

## Results
![val_batch0_pred](https://github.com/user-attachments/assets/d371cd8e-f826-4943-9cfe-896938eceb50)

### Metrics
![confusion_matrix_normalized](https://github.com/user-attachments/assets/23936528-fa94-49c4-bc61-c1a375e5c4db)
![results](https://github.com/user-attachments/assets/74cc4efe-9b6d-49e8-aafd-a6879c0f05c3)

|YOLO evaluation metrics| Value |
| :-------------------: | ----- |
| mAP50-95              | 0.696 |
| mAP50                 | 0.955 |
| mAP75                 | 0.731 |
