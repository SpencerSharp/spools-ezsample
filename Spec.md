1 finish sample marking script
1 make script that downloads marked samples
    1 check if marker song length matches downloaded song length
1 make script that loads markers into ableton project
    1 cycle albums, rank by my rating and how sparsely album was tagged
    1 a ton of markers on one album won't clog if done right
1 create sample tagging/trimming workflow
    1 script to export clips
1 create sample demoing workflow

ezsample
    marks samples, builds marked sample table
music
    downloads marked samples, manages track lib
ableton
    loads marked samples into ableton
    exports files to sample library
        as a result, indirectly manages sample library

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