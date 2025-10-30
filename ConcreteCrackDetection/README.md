A deep learning model to classify concrete surfaces as **"Cracked" (Positive)** or **"Not Cracked" (Negative)** using convolutional neural networks (CNN).

## Dataset
The dataset consists of concrete surface images divided into two classes:
- **Negative**: Images without cracks
- **Positive**: Images with cracks

Dataset Source: [Concrete Crack Images for Classification on Kaggle](https://www.kaggle.com/datasets/sdubey1/concrete-crack-images-for-classification)

## Model Architecture
The CNN model consists of:
- **4 Convolutional Blocks** (Conv2D + BatchNorm + ReLU + MaxPooling)
- **Flatten Layer** followed by **Dropout (0.5)**
- **Dense Layers** (512 neurons with ReLU, 1 neuron with Sigmoid)

```python
Sequential([
    Input(shape=(100, 100, 1)),
    Conv2D(32, (3, 3)),
    BatchNormalization(),
    Activation('relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3)),
    BatchNormalization(),
    Activation('relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (3, 3)),
    BatchNormalization(),
    Activation('relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (3, 3)),
    BatchNormalization(),
    Activation('relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])