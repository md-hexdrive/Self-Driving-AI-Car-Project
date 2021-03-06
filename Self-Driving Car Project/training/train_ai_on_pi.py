# -*- coding: utf-8 -*-
"""Train my AI based on DeepPiCar AI lane following example code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g1RdYstwwC9sDoE5_IOo--DnhDIoxbF2

# End-to-End Lane Navigation via Nvidia Model
Original Author: David Tian

Date: 2020-02-12

This code is described in the [DeepPiCar - Part 5: Autonomous Lane Navigation via Deep Learning](https://medium.com/@dctian/deeppicar-part-5-lane-following-via-deep-learning-d93acdce6110?source=your_stories_page---------------------------) Blog.
"""

# Commented out IPython magic to ensure Python compatibility.
#imports

# python standard libraries
import os
import random
import fnmatch
import datetime
import pickle
from time import sleep

# data processing
import numpy as np
np.set_printoptions(formatter={'float_kind':lambda x: "%.4f" % x})

import pandas as pd
pd.set_option('display.width', 300)
pd.set_option('display.float_format', ':,.4f'.format)
pd.set_option('display.max_colwidth', 200)

#tensorflow
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

print(f'tf.__version__: {tf.__version__}')
print(f'keras.__version__: {keras.__version__}')

#sklearn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

#imaging
import cv2
from imgaug import augmenters as img_aug
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
from PIL import Image

#import images
#!cd /content
#!git clone https://github.com/dctian/DeepPiCar

#!ls

model_name = "Table-Day-Model"
model_output_dir = '/home/pi/Desktop/models/' + model_name
if not os.path.exists(model_output_dir):
  os.makedirs(model_output_dir)


data_dir = "/home/pi/Desktop/recordings/Table-Day-Data"
file_list = os.listdir(data_dir)
image_paths = []
steering_angles = []
pattern = '*.jpg'
for filename in file_list:
  if fnmatch.fnmatch(filename, pattern):
    image_paths.append(os.path.join(data_dir, filename))
    try:
      angle = int(filename[-5])
      
    except ValueError:
      angle = int(filename[-6])
    
    steering_angles.append(angle)

image_index = 20
plt.imshow(Image.open(image_paths[image_index]))
print("image_path: %s" % image_paths[image_index])
print("steering_angle %i" % steering_angles[image_index])

df = pd.DataFrame()
df['ImagePath'] = image_paths
df['Angle'] = steering_angles

# Look at the distribution of the steering angle
num_of_bins = 8
samples_per_bin = 400
hist, bins = np.histogram(df['Angle'], num_of_bins)

fig, axes = plt.subplots(1,1, figsize=(12,4))
axes.hist(df['Angle'], bins=num_of_bins, width=1, color='blue')

x_train, x_valid, y_train, y_valid = train_test_split(image_paths, steering_angles, test_size=0.2)
print('Training data: %d\n Validation data: %d' % (len(x_train), len(x_valid)))

#plot distributions of train and valid data to ensure consistency
fig, axes = plt.subplots(1,2, figsize=(12,4))
axes[0].hist(y_train, bins=num_of_bins, width=1, color='blue')
axes[0].set_title('Training data')
axes[1].hist(y_valid, bins=num_of_bins, width=1, color='red')
axes[1].set_title('Validation data')

"""# Augment Images"""

def my_imread(image_path):
  image = cv2.imread(image_path)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  return image

def zoom(image):
  zoom = img_aug.Affine(scale=(1, 1.3))
  image = zoom.augment_image(image)
  return image

fig, axes = plt.subplots(1,2, figsize=(15,10))
image_orig = my_imread(image_paths[image_index])
image_zoom = zoom(image_orig)
axes[0].imshow(image_orig)
axes[0].set_title("original")
axes[1].imshow(image_zoom)
axes[1].set_title("zoomed")

def compare_images(text1 = 'original', text2 = 'modified', modifier_function = my_imread, image1 = my_imread(image_paths[image_index])):
  fig, axes = plt.subplots(1,2, figsize=(15,10))
  image_orig = image1
  image_modified = modifier_function(image_orig)
  axes[0].imshow(image_orig)
  axes[0].set_title(text1)
  axes[1].imshow(image_modified)
  axes[1].set_title(text2)

compare_images('original', 'zoomed', zoom)

def pan(image):
  # pan left / right / up / down, about 10%
  pan = img_aug.Affine(translate_percent= {'x': (-0.1, 0.1), 'y': (-0.1, 0.1)})
  image = pan.augment_image(image)
  return image

compare_images('original', 'panned', pan)

def adjust_brightness(image):
  # increase or decrease brightness by 30%
  brightness = img_aug.Multiply((0.7, 1.3))
  image = brightness.augment_image(image)
  return image

compare_images('original', 'brightness adjusted', adjust_brightness)

def blur(image):
  kernel_size = random.randint(1, 5) # kernel largeer than 5 would make the image way to blurry
  image = cv2.blur(image,(kernel_size, kernel_size))
  return image

compare_images('original', 'blurred', blur)

def random_flip(image, steering_angle):
  """
  is_flip = random.randint(0, 1)
  if is_flip == 1:
    # randomly flip horizon
    image = cv2.flip(image,1)
    if (not steering_angle == 3):
      steering_angle = 2 - steering_angle
  """
  return image, steering_angle

fig, axes = plt.subplots(1,2, figsize=(15,10))
image_orig = my_imread(image_paths[image_index])
image_flip, steering_angle = random_flip(image_orig, steering_angles[image_index])
axes[0].imshow(image_orig)
axes[0].set_title('original, angle=%s' % (steering_angles[image_index]))
axes[1].imshow(image_flip)
axes[1].set_title('flipped, angle=%s' % steering_angle)

# put it together
def random_augment(image, steering_angle):
  if np.random.rand() < 0.5:
    image = pan(image)
  if np.random.rand() < 0.5:
    image = zoom(image)
  if np.random.rand() < 0.5:
    image = blur(image)
  if np.random.rand() < 0.5:
    image = adjust_brightness(image)
  image, steering_angle = random_flip(image, steering_angle)

  return image, steering_angle

# show a few randomly augmented images
ncol = 2
nrow = 10
fig, axes = plt.subplots(nrow, ncol, figsize=(15, 50))

for i in range(nrow):
  rand_index = random.randint(0, len(image_paths) - 1)
  image_path = image_paths[rand_index]
  steering_angle_orig = steering_angles[rand_index]

  image_orig = my_imread(image_path)
  image_aug, steering_angle_aug = random_augment(image_orig, steering_angle_orig)

  axes[i][0].imshow(image_orig)
  axes[i][0].set_title('original, angle=%s' % steering_angle_orig)
  axes[i][1].imshow(image_aug)
  axes[i][1].set_title('augmented, angle=%s' % steering_angle_aug)

"""# Preprocess Training Data for Nvidia Model"""

def img_preprocess(image):
  height, _, _ = image.shape
  #image = image[int(height/2):,:,:] # remove top half of the image, as it is not relavant for lane following
  image = image[:int(height-height//10),:,:] # remove bottom bit of image to eliminate displayed driving status visualization
  image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV) # Nvidia model said it best to use YUV color space
  image = cv2.GaussianBlur(image, (3,3), 0)
  image = cv2.resize(image, (85,64)) # input image size(200,66) Nvidia model
  image = image / 255 # normalizing, the processed image becomes black for some reason. Do we need this?
  return image

fig, axes = plt.subplots(1, 2, figsize=(15, 10))
image_orig = my_imread(image_paths[image_index])
image_processed = img_preprocess(image_orig)
axes[0].imshow(image_orig)
axes[0].set_title('original')
axes[1].imshow(image_processed)
axes[1].set_title('processed')

"""# Create and Train Model"""

# Experiment with smaller and hopefully faster models
def smaller_model():
  model = Sequential([
                      Conv2D(12, (5,5), input_shape=(64, 85, 3), activation='elu'),
                      #Conv2D(5, (5,5), activation='elu'),
                      Flatten(),
                      Dropout(0.2),
                      #Dense(10, activation='elu'),
                      Dense(4, activation='softmax')
  ], name="Smaller Model")

  model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model

def nvidia_model():

  # elu=Exponential Linear Unit, similar to leaky Relu
  # skipping 1st hidden layer (normalization layer), as we have normalized the data

  model = Sequential([
    # Convolution Layers
    Conv2D(24, (5, 5), strides=(2,2), input_shape=(64, 85, 3), activation='elu'),
    Conv2D(36, (5, 5), strides=(2,2), activation='elu'),
    Conv2D(48, (5, 5), strides=(2,2), activation='elu'),
    Conv2D(64, (3, 3), activation='elu'),
    Dropout(0.2), # not in original model. added for more robustness
    Conv2D(64, (3, 3), activation='elu'),

    # Fully Connected Layers
    Flatten(),
    Dropout(0.2), # not in original model. added for more robustness
    Dense(100, activation='elu'),
    Dense(50, activation='elu'),
    Dense(10, activation='elu'),

    # output layer: movement commands: go forward-left, forward-straight, forward-right, + stop
    Dense(4, activation='softmax')
  ], name='Nvidia_Model')

  # since this is a regression problem not classification problem,
  # we use MSE (Mean Squared Error) as loss function
  optimizer = Adam()#lr=1e-3) # lr is learning rate
  model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

  return model

model = nvidia_model()
print(model.summary())
# check that we will have 252,219 trainable parameters

def image_data_generator(image_paths, steering_angles, batch_size, is_training):
  while True:
    batch_images = []
    batch_steering_angles = []

    for i in range(batch_size):
      random_index = random.randint(0, len(image_paths) - 1)
      image_path = image_paths[random_index]
      image = my_imread(image_paths[random_index])
      steering_angle = steering_angles[random_index]
      if is_training:
        # training: augment image
        image, steering_angle = random_augment(image, steering_angle)
      
      image = img_preprocess(image)
      batch_images.append(image)
      batch_steering_angles.append(steering_angle)
    
    yield(np.asarray(batch_images), np.asarray(batch_steering_angles))

ncol = 2
nrow = 2

x_train_batch, y_train_batch = next(image_data_generator(x_train, y_train, nrow, True))
x_valid_batch, y_valid_batch = next(image_data_generator(x_valid, y_valid, nrow, False))

fig, axes = plt.subplots(nrow, ncol, figsize=(15, 6))
fig.tight_layout()

for i in range(nrow):
  axes[i][0].imshow(x_train_batch[i])
  axes[i][0].set_title("training, angle=%s" % y_train_batch[i])
  axes[i][1].imshow(x_valid_batch[i])
  axes[i][1].set_title("validation, angle=%s" % y_valid_batch[i])

# start Tensorboard before model fit, so we can see the epoch tick in Tensorboard
# Jupyter Notebook embedded Tensorboard is a new feature in TF 2.0!!

# clean up log folder for tensorboard
log_dir_root = f'{model_output_dir}/logs/'
#!rm -rf $log_dir_root

# this block prevents the training from starting if we tell Colab to Run All
# it works by throwing an error when Colab reaches this code cell, 
# preventing the code below from being run automatically
#DO_NOT_RUN_ALL

# save the model weights after each epoch if the validation loss decreased
checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=os.path.join(model_output_dir, model_name + '_check.h5'))

model = load_model(f'{model_output_dir}/{model_name}_check.h5')
#SendEmail('lane nav train started')
for i in range(5):
    print("Epoch", i+1)
    history = model.fit_generator(image_data_generator(x_train, y_train, batch_size=30, is_training=True),
                          steps_per_epoch=30,
                          epochs=1,
                          validation_data = image_data_generator(x_valid, y_valid, batch_size=30,
                                                                 is_training=False),
                          validation_steps=20,
                          verbose=1,
                          shuffle=1,
                          callbacks=[checkpoint_callback])
    sleep(10)
# always save model output as soon as model finishes training
model.save(os.path.join(model_output_dir, model_name + '_final.h5'))

#date_str = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
history_path = os.path.join(model_output_dir,'history.pickle')
with open(history_path, 'wb') as f:
  pickle.dump(history.history, f, pickle.HIGHEST_PROTOCOL)

#SendEmail('lane nav train finished. val_loss from %.1f to %.1f' % (history.history['val_loss'][0], history.history['val_loss'][-1]))

#history.history

# always save model output as soon as model finishes training
model.save(os.path.join(model_output_dir, model_name + '_final.h5'))
history_path = os.path.join(model_output_dir,'history.pickle')
with open(history_path, 'wb') as f:
  pickle.dump(history.history, f, pickle.HIGHEST_PROTOCOL)

history_path = os.path.join(model_output_dir,'history.pickle')

# plot training a validation losses
# this should be the same as tensorboard
#history_path = os.path.join(model_output_dir,'history.pickle')
with open(history_path, 'rb') as f:
  history = pickle.load(f)

#history

#history
plt.plot(history['loss'],color='blue')
plt.plot(history['val_loss'],color='red')
plt.legend(['training loss', 'validation loss'])

#history
plt.plot(history['acc'], color='blue')
plt.plot(history['val_acc'], color='red')
plt.legend(['training accuracy', 'validation accuracy'])

model = load_model(f'{model_output_dir}/{model_name}_final.h5')
x_test, y_test = next(image_data_generator(image_paths, steering_angles, 1, False))
y_pred = np.argmax(model.predict(x_test))
print(y_pred)
print(y_test)

plt.imshow(x_test[0])

from sklearn.metrics import mean_squared_error, r2_score

def summarize_prediction(y_true, y_pred):

  mse = mean_squared_error(y_true, y_pred)
  r_squared = r2_score(y_true, y_pred)

  print(f'number of tests = {len(y_true)}')
  print(f'mse       = {mse:.2}')
  print(f'r_squared = {r_squared:.2%}')
  print()

def predict_and_summarize(x, y):
  model = load_model(f'{model_output_dir}/{model_name}_check.h5')
  predictions = model.predict(x)
  
  y_pred = []
  for prediction in predictions:
    y_pred.append(np.argmax(prediction))

  #print(y_pred)  
  #print(predictions)
  summarize_prediction(y, y_pred)
  return y_pred

n_tests = 100
x_test, y_test = next(image_data_generator(x_valid, y_valid, 100, False))

y_pred = predict_and_summarize(x_test, y_test)

n_tests_show = 10
fix, axes = plt.subplots(n_tests_show, 1, figsize=(10, 4 * n_tests_show))
for i in range(n_tests_show):
  axes[i].imshow(x_test[i])
  axes[i].set_title(f"actual angle={y_test[i]}, predicted angle={int(y_pred[i])}, diff = {int(y_pred[i])-y_test[i]}")