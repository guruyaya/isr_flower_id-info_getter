# Project get flower info from the internet
1. Get the names of the flowers that are the basis of our DB from WIKIPEDIA, + time of blooming
2. Get the names of the images from the net

# Steps
1. mkdir data & data/images
2. run get_wikipedia_data.py
3. run get_flicker_images_urls.py
4. Download geckodriver for your system
5. run get_google_images.py. At some point you'll have to proove you are not a robot. As you are,
there's little you can do. Baaa
6. Mark non_flower (faraway pics or just non flower pics) and dead images using detect_non_flowers.py (Use 1000 examples)
7. use is_non_flower_test_split.py to build a flower identifier
8. Use build_flower_detection_model.py
9. use get_images.py to download images


