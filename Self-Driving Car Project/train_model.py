"""
load training data and process data, then use the data to train and test learning model

"""

import tensorflow as tf
import tensorflow.keras as keras

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
plt.ion()

import numpy as np
np.set_printoptions(formatter={'float_kind':lambda x: "%.4f" % x})

import cv2

#sklearn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

from imgaug import augmenters as img_aug
import pandas as pd
pd.set_option('display.width', 300)
pd.set_option('display.float_format', ':,.4f'.format)
pd.set_option('display.max_colwidth', 200)

from PIL import Image
import fnmatch
import os
import sys
import random
import logging

def get_training_data(path):
    if not os.path.exists(path):
        logging.error(f"Error, directory {path} does not exist")
        sys.exit()
    else:
        file_list = os.listdir(path)
        pattern = "*.jpg"
        for file in file_list:
            if fnmatch.fnmatch(file, pattern):
                image_paths.append(os.path.join(path, file))
                angle = int(file[-5])
                steering_angles.append(angle)

"""
don't forget to put x_train, x_valid, y_train, and y_valid in the correct order! :-)
"""
def process_training_data():
    x_train, x_valid, y_train, y_valid = train_test_split(image_paths, steering_angles, test_size = 0.2)
    #print('Training data: %d\nValidation data: %d' % (len(x_train), len(x_valid)))
    #print(x_train)
    return (x_train, y_train), (x_valid, y_valid)

"""Augment Images"""
def my_imread(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def zoom(image):
    zoom = img_aug.Affine(scale=(1, 1.3))
    image = zoom.augment_image(image)
    return image

def pan(image):
    # pan left / right / up / down, about 10%
    pan = img_aug.Affine(translate_percent={'x': (-0.1, 0.1), 'y': (-0.1, 0.2)})
    image = pan.augment_image(image)
    return image

def adjust_brightness(image):
    # increase or decrease brightness by 30%
    brightness = img_aug.Multiply((0.7,1.3))
    image = brightness.augment_image(image)
    return image

def blur(image):
    kernel_size = random.randint(1, 5) # kernel bigger than 5 would make the image way to blurry
    image = cv2.blur(image, (kernel_size, kernel_size))
    return image

def random_flip(image, steering_pos):
    flip_it = random.randint(0, 1)
    if flip_it == 1:
        image = cv2.flip(image,1)
        steering_pos = 2 - steering_pos # steering positions are 0, 1, and 2, so subtracting the position by two will flip its value
    
    return (image, steering_pos)

def random_augment(image, steering_pos):
    rand = random.randint(0, 1)
    if rand == 1:
        image == zoom(image)
        
    rand = random.randint(0, 1)
    if rand == 1:
        image == pan(image)
        
    rand = random.randint(0, 1)
    if rand == 1:
        image == adjust_brightness(image)
        
    rand = random.randint(0, 1)
    if rand == 1:
        image == blur(image)
    
    image, steering_pos = random_flip(image, steering_pos)
    
    return image, steering_pos

"""img_preprocess() preprocesses the images for use in the neural network""" 
def img_preprocess(image):
    height, _, _ = image.shape
    #image = image[int(height/2):,:,:]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.resize(image, (85, 64))
    image = image / 255
    return image

"""image_data_generator() generates random batches of images and their steering angles
for training and validation"""
def image_data_generator(image_paths, steering_angles, batch_size, is_training):
    while True:
        batch_images=[]
        batch_steering_angles=[]
        
        for i in range(batch_size):
            random_index = random.randint(0, len(image_paths) - 1)
            image_path = image_paths[random_index]
            image = my_imread(image_path)
            steering_angle = steering_angles[random_index]
            
            if is_training:
                image, steering_angle = random_augment(image, steering_angle)
            
            image = img_preprocess(image)
            batch_images.append(image)
            batch_steering_angles.append(steering_angle)
        
        yield(np.asarray(batch_images), np.asarray(batch_steering_angles))
    
"""
##################################################################################
Neural network models

DO NOT USE THE NIVIDIA MODEL ON THE RASPBERRY PI

"""
def nvidia_model():
    # elu= Exponential Linear Unit, similar to leaky Relu
    # skipping first hidden layer (normalization layer), as the image was previously normalized
    model = tf.keras.models.Sequential([
        # convolutional layers
        tf.keras.layers.Conv2D(24, (5, 5), strides=(2,2), input_shape=(85, 64, 3), activation='elu'),
        tf.keras.layers.Conv2D(36, (5, 5), strides=(2,2), activation='elu'),
        tf.keras.layers.Conv2D(48, (5, 5), strides=(2,2), activation='elu'),
        tf.keras.layers.Conv2D(64, (3, 3), activation = 'elu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Conv2D(64, (3, 3), activation = 'elu'),
        
        # Fully connected layers
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(100, activation = 'elu'),
        tf.keras.layers.Dense(50, activation = 'elu'),
        tf.keras.layers.Dense(10, activation = 'elu'),
        
        # output layer
        tf.keras.layers.Dense(1)
        ], name = "Nvidia_Model")
    
    model.compile(loss='mse', optimizer='adam')
    
    return model
        
"""
##################################################################################

Test Functions

"""
def check_data():
    
    plt.imshow(Image.open(image_paths[image_index]))
    print(image_paths[image_index])
    print(steering_angles[image_index])
    print(steering_angles.count(0))

    df = pd.DataFrame()
    df['ImagePath'] = image_paths
    df['Angle'] = steering_angles



def get_steering_angle_distribution():
    # look at steering angle distribution
    num_of_bins = 3
    samples_per_bin = 400
    hist, bins = np.histogram(df['Angle'], num_of_bins)

    fig, axes = plt.subplots(1,1, figsize=(8,4))
    axes.hist(df['Angle'], bins = num_of_bins, width = 1, color = 'green')
    print()

def compare_images(modifier_function=pan):
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    image_orig = my_imread(image_paths[image_index])
    image_aug = modifier_function(image_orig)
    axes[0].imshow(image_orig)
    axes[0].set_title('original')
    axes[1].imshow(image_aug)
    axes[1].set_title('modified')

def test_random_photo_augmentation(number_of_test_photos=2):
    # randomly augment a few images
    nrows = number_of_test_photos
    ncols = 2
    fix, axes = plt.subplots(nrows, ncols, figsize=(15, 50))

    for i in range(nrows):
        rand_index = random.randint(0, len(image_paths) - 1)
        image_path = image_paths[rand_index]
        steering_pos_orig = steering_angles[rand_index]
        
        image_orig = my_imread(image_path)
        image_aug, steering_pos_aug = random_augment(image_orig, steering_pos_orig)
        image_aug = img_preprocess(image_aug)
        axes[i][0].imshow(image_orig)
        axes[i][0].set_title(steering_pos_orig)
        axes[i][1].imshow(image_aug)
        axes[i][1].set_title(steering_pos_aug)

def test_image_data_generator():
    ncol = 2
    nrow = 2
    
    (x_train_batch, y_train_batch) = next(image_data_generator(image_paths, steering_angles, nrow, True))
    (x_test_batch, y_test_batch) = next(image_data_generator(image_paths, steering_angles, nrow, False))
    
    fig, axes = plt.subplots(nrow, ncol, figsize=(15, 6))
    fig.tight_layout()
    for i in range(nrow):
        axes[i][0].imshow(x_train_batch[i])
        axes[i][0].set_title("Training, angle=%s" % y_train_batch[i])
        axes[i][1].imshow(x_test_batch[i])
        axes[i][1].set_title("Validation, angle=%s" % y_test_batch[i])

logging.basicConfig(level = logging.ERROR)

image_paths = []
steering_angles = []
image_index = 24
specific_dir = "1582523922"
recording_path = "/home/pi/Desktop/recordings/" + specific_dir

get_training_data(recording_path)

(x_train, y_train), (x_valid, y_valid) = process_training_data()

model = nvidia_model()
print(model.summary())
test_image_data_generator()

print("\n\nDONE")