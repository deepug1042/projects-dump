#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the AlexNet model
def create_alexnet(input_shape, num_classes):
    model = Sequential([
        Conv2D(96, kernel_size=(11,11), strides=(4,4), activation='relu', input_shape=input_shape),
        MaxPooling2D(pool_size=(3,3), strides=(2,2)),
        Conv2D(256, kernel_size=(5,5), padding='same', activation='relu'),
        MaxPooling2D(pool_size=(3,3), strides=(2,2)),
        Conv2D(384, kernel_size=(3,3), padding='same', activation='relu'),
        Conv2D(384, kernel_size=(3,3), padding='same', activation='relu'),
        Conv2D(256, kernel_size=(3,3), padding='same', activation='relu'),
        MaxPooling2D(pool_size=(3,3), strides=(2,2)),
        Flatten(),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    return model

# Define input shape and number of classes
input_shape = (224, 224, 3)  # Example input shape
num_classes = 2  # Example number of classes for binary classification, adjust as needed

# Create the AlexNet model
alexnet_model = create_alexnet(input_shape, num_classes)

# Compile the model
alexnet_model.compile(optimizer=Adam(), loss=SparseCategoricalCrossentropy(), metrics=['accuracy'])

# Print model summary
alexnet_model.summary()

# Define data directories
train_dir = r'D:\Leaf\train'  # Path to your training dataset directory
validation_dir = r'D:\Leaf\val'  # Path to your validation dataset directory

# Define image dimensions and batch size
img_height, img_width = 224, 224  # Example dimensions, adjust as needed
batch_size = 32  # Example batch size, adjust as needed

# Create data generators with preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

# Load and preprocess train and validation datasets
train_dataset = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'  # Use 'categorical' for multi-class classification
)

validation_dataset = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'  # Use 'categorical' for multi-class classification
)

# Train the model
alexnet_model.fit(
    train_dataset,
    epochs=10,  # Example number of epochs
    validation_data=validation_dataset
)


# In[ ]:





# In[ ]:




