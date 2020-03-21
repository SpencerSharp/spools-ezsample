
FILES
ableton.py
    create_sampling_set
        Opens ableton, opens the sample session project, adds the clips passed in as params
    save_sampling_set
        Saves existing ableton sampling set, clears out clips
img.py
    add_img
        Attempts to add an image to sample events
    scan_img
        Gets info from image at coordinates
mobile.py
    Loops through user's photo stream images, tries to add them to sample events via img.py's "add_img"


TABLES
sample_events
source_library
sample_library