# Project get flower info from the internet
1. Get the names of the flowers that are the basis of our DB from WIKIPEDIA, + time of blooming
2. Get the names of the images from the net

# Steps
## Getting the data
1. mkdir data & data/images
2. run get_wikipedia_data.py
3. run get_flicker_images_urls.py
4. Download geckodriver for your system
5. run get_google_images.py. At some point you'll have to proove you are not a robot. As you are,
there's little you can do. Baaa
## Is this a flower model
1. Mark non_flower (faraway pics or just non flower pics) and dead images using detect_non_flowers.py (Use 1000 examples)
2. use is_non_flower_test_split.py to build a flower identifier
3. use get_images_for_is_flower.py
4. use is_non_flower_test_split.py
5. Use build_flower_detection_model.py
6. Use is_non_flower_test_split with option FP and FN (False positive and False negatives) changed in the file to examine the results of the model. This should catch falsly claimed non and not non flowers
7. Delete the data/image_is_flower directory
8. repeat starting from stage 8, until the is_non_flower model predicts well
## Build a flower identifier model
1. mkdir data/images
2. use get_images.py to download images
3. use apply_non_flower_model.py to separate all non flower images, and those we cannot load

