import time
import cv2
#import mss
import numpy as np
from pynput.keyboard import Key, Listener

def up():
    print("Go up")


def down():
    print("Go down")


def left():
    print("Go left")


def right():
    print("Go right")


def up_left():
    print("Go up_left")


def up_right():
    print("Go up_right")


def down_left():
    print("Go down_left")


def down_right():
    print("Go down_right")


def do_nothing():
    print("Do Nothing")


# Create a mapping of keys to function (use frozenset as sets are not hashable - so they can't be used as keys)

combination_to_function = {
    frozenset([Key.up]): up,  # No `()` after function_1 because
    # we want to pass the function, not the value of the function
    frozenset([Key.down, ]): down,
    frozenset([Key.left, ]): left,
    frozenset([Key.right, ]): right,
    frozenset([Key.up, Key.left]): up_left,
    frozenset([Key.up, Key.right]): up_right,
    frozenset([Key.down, Key.left]): down_left,
    frozenset([Key.down, Key.right]): down_right,
}

# Currently pressed keys
current_keys = set()


def on_press(key):
    # When a key is pressed, add it to the set we are keeping track of and check if this set is in the dictionary
    current_keys.add(key)
    if frozenset(current_keys) in combination_to_function:
        # If the current set of keys are in the mapping, execute the function
        combination_to_function[frozenset(current_keys)]()


def on_release(key):
    # When a key is released, remove it from the set of keys we are keeping track of
    if key in current_keys:
        current_keys.remove(key)


def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img


#with mss.mss() as sct:
    # Part of the screen to capture
    #monitor = {"top": 0, "left": 70, "width": 640, "height": 480}

while True:
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    last_time = time.time()
    # key_catcher = MockButton()
    # Get raw pixels from the screen, save it to a Numpy array
    #screen = np.array(sct.grab(monitor))
    #new_screen = process_img(original_img=screen)

    # Display the picture
    #cv2.imshow("Window", new_screen)

    # print("Loop took {} seconds".format(time.time() - last_time))
    # Press "q" to quit

    #k = cv2.waitKey(10)

    #if k & 0xFF == ord("q"):
    #    cv2.destroyAllWindows()
    #    break

    #listener.stop()
