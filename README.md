# youDupe

Script for finding and removing duplicate archived Youtube videos.  

**Files must end in their video_id and be .mkv**  
You can alter which extention the script looks for in the code by replacing all instances of '.mkv' with your desired extention.


Usage python dupe.py [OPTIONS] -d <DIRECTORY>

Options:

        -h, --help					Print this help text and exit  
        -a, --autoaccept				Accept deletions without prompting  
        -t, --trial					Print proposed deletions instead of deleting  
        -d, --directory PATH			The desired starting point of the recursive search  