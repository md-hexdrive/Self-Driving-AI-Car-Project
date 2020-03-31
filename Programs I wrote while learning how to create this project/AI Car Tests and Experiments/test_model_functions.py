from train_model import *

"""
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
        #image_aug = img_preprocess(image_aug)
        axes[i][0].imshow(image_orig)
        axes[i][0].set_title(steering_pos_orig)
        axes[i][1].imshow(image_aug)
        axes[i][1].set_title(steering_pos_aug)

print('hello')