# Self-Driving AI RC Car Project
 This is the Code and Documentation for the Self Driving RC Car for my final Project in the COMP 444 Embedded/Robotic Programming course at Athabasca University. A video of the project is located [here](https://youtu.be/rAWz5kUqRnQ).

**Note:** This project is a work in progress and the programming/documentation isn't complete.

## Credits:
For this project, I collaborated with my brother to build the car, and we discussed how to solve several problems together. My dad also made some wooden supports for the car to help secure and level hardware. I am very grateful for their advice/help.

I was aided in coding the car by consulting a number of online sources, particularly the Raspberry Pi, TensorFlow, and OpenCV documentation/tutorials; the [DeepPiCar tutorials](https://towardsdatascience.com/deeppicar-part-1-102e03c83f2c) and [code](https://github.com/dctian/DeepPiCar/blob/master/models/lane_navigation/code/); and [this tutorial](https://www.bluetin.io/dc-motors/motor-driver-raspberry-pi-tb6612fng/) and the [SparkFun TB6612FNG Hookup Guide](https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide/all) showed me how to interface the Raspberry Pi with the TB6612FNG motor controller. The code for training the AI is largely based on [end_to_end_lane_navigation.ipynb](https://github.com/dctian/DeepPiCar/blob/master/models/lane_navigation/code/end_to_end_lane_navigation.ipynb) from the DeepPiCar tutorials and some of the DeepPiCar programming helped me out in other places in my project, but I wrote most of the code myself. 

## Documentation:
The car was orginally a basic RC Lamborghini like what someone can buy from Amazon or Walmart. The car is powered by the Raspberry Pi 3B, which takes live camera and ultrasonic distance sensor feeds and processes them to determine appropriate actions to take while driving along an artificial track.

The programming is all in Python and some is in [Google Colab](https://colab.research.google.com/notebooks/intro.ipynb) notebooks.


This car can drive completely autonomously along any arbitrary track it has correct training data from.

The car uses a neural network that is trained by watching how a human driver navigates the track and uses the data provided by them to learn how to drive on its own.


## Source Code
The key code is contained in the [Self-Driving Car Project](https://github.com/md-hexdrive/Self-Driving-AI-Car-Project/tree/master/Self-Driving%20Car%20Project) directory.
The [misc](https://github.com/md-hexdrive/Self-Driving-AI-Car-Project/tree/master/misc) directory holds code that I experimented with over the course of creating the project. Some is based on tutorials I followed. The rest is code that I experimented with in direct relation to the car, but is not needed and has fallen by the wayside. For instance, I originally tried to use the Pygame Python module to provide user with real-time interactivity with the car using the keyboard, but it proved difficult to interface with OpenCV. I eventually used OpenCV's waitkey() method to capture keyboard input both when recording driving data to train the car and when the car was driving itself.

### Controlling GPIO hardware
The basic driving code is held in the driving.py file. This file handles the interaction between the Pi and the car's motors, which are controlled with the TB6612FNG motor controller from SparkFun. The ultrasonic distance sensor control code is in distance_sensor.py. Both interact with their respective devices through the Pi's GPIO (general purpose input-output) pins with the use of the Python GPIOZero library. 

### Autonomous Driving
The code for autonomous driving is held in drive_with_ai.py, but the code also relies on driving.py, record_driving.py, distance_monitoring.py, and interpret_frame.py.

The car uses a combination of a Convolutional Neural network and real-time sensor feedback to drive. The Neural network is trained with input images and driving commands that were recorded when a real driver drove the car along an artificial track (the actual training occurs on Google Colab, not on the car itself). The car's neural network takes as input live camera feed and outputs appropriate driving commands.

The neural network's decision can be overriden by either the car's ultrasonic distance sensor (if it detects an object too close, it will cause the car to stop) or the user can stop the car manually by hitting the spacebar. 
The neural network outputs an array of propbiblities which indicate to it how likely a certain command is to be the correct one to pass to the car in a given instance. Right now, commands are: drive forward and turn left, drive forward and straight ahead, drive forward and turn right, and stop. The four commands are represented interally as array positions 0, 1, 2, and 3 respectively. So if the network outputs `[3]`, it tells the car that it should stop. If the network outputs `[0]`, the car will turn left while driving forward, etc.

In terms of real cars, this car has automatic emergency braking and lane-keep-assist: It will automatically brake to avoid collisions or if it drives off the road, and it will stay in its lane automatically. 

### Collecting Training Data
The user connects to the Raspberry Pi over VNC. That way they can view semi real-time video from the car's camera, and they can manually control it with a keyboard. They can also control the Pi with a keyboard connected directly to the Pi either with a cord or wireless dongle (in theory). I didn't have a wireless keyboard, and connecting over vnc doesn't allow reliable real-time keyboard control (the Pi receives multiple key up/down events every second, or at least when you are pressing and holding a key the Pi doesn't interpret the key as being constantly held). Therefore, for collecting training data, I plugged a wired usb keyboard directly into the Pi and walked behind it while I drove it.
record_driving.py is the program that allows the user to drive the car while collecting training data.

