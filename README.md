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
6. Mark non_flower and dead images using detect_non_flowers.py
7. use get_images.py to download images


