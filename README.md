# Project Title
Video Similarity Detector
This program can compare videos to find similar one, even if they have been manipulated or altered. It extracts frames from videos, processes them, and uses perceptual hashing and fuzzy matching to determine the similarity between videos.



## Table of Contents:
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#howitworks)
- [License](#license)


## Features 
Frame Extraction: Extracts frames from videos at specified intervals.

Image Processing: Crops frames to focus on the central content.

Perceptual Hashing: Generates hashes for cropped frames to represent their visual content.

Similarity Comparison: Compares hashes using fuzzy matching to identify similar frames across videos.

Similarity Scoring: Calculates a final similarity score to determine if videos are likely the same.


## Dependencies
Ensure you have the following Python packages installed:

▫️ Python 3.6 or higher

▫️ pip

▫️ OpenCV (opencv-python)
pip install opencv-python

▫️ Pillow (Pillow)
pip install pillow

▫️ ImageHash
pip install opencv-python Pillow imagehash

▫️ RapidFuzz
pip install rapidfuzz


## Installation
1.Clone the Repository
'''bash
git clone https://github.com/Yasamanafshargh/https---github.com-Yasamanafshargh-video-similarity-detector.git
cd video-similarity-'''


2.Install Dependencies
Install the required Python packages if you haven't already (see Dependencies section).

3.Set Up the Environment (Optional)
Create a virtual environment to manage dependencies:
'''bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
'''


## Usage
1.Prepare Video Files

Place the videos you want to compare in a directory of your choice.

2.Configure Video Paths
In the script, set the paths to your video files:

'''python

# Define paths to your videos - you can add more paths as needed
video_paths = [
    'path/to/first_video.mp4',
    'path/to/second_video.mp4',
    # Add more paths if needed
]'''


3.Set Output Directory
Specify the base output directory where the processed frames will be saved:

python
base_output_folder = Path('path/to/output/directory')
base_output_folder.mkdir(parents=True, exist_ok=True)
Run the Script


4.Execute the script to start the video comparison:
bash
python video_similarity_detector.py


5.Interpret the Results

The script will output similarity scores and a conclusion indicating whether the videos are likely the same or different.


## Configuration
▫️Frame Extraction Rate (frame_rate)
Adjust the frame extraction rate by modifying the frame_rate parameter in the extract_and_crop_frame function. This determines every nth frame to process. Default is every 5th frame.
'''python
def extract_and_crop_frame(video_path, output_folder, frame_rate=5):
    # ...'''


▫️Similarity Thresholds
You can tweak the thresholds used to determine similarity:

-similarity_threshold: Minimum percentage similarity between two hashes to consider them a match. Default is 90%.
-final_score_threshold: Minimum percentage of high-similarity matches required to conclude that the videos are the same. Default is 70%.
-min_high_similarity_matches: Minimum number of high-similarity frame matches needed to directly conclude the videos are the same. Default is 10.

'''python

def compare_hashes_across_folders(
    folder_hashes,
    similarity_threshold=90,
    final_score_threshold=70,
    min_high_similarity_matches=10
):
    # ...'''


## How It Works
1.Extract and Crop Frames

▫️The script reads each video and extracts frames at intervals determined by the frame_rate.
▫️Each extracted frame is converted to a PIL image and cropped to focus on the middle third vertically, which helps in ignoring subtitles or watermarks that might be at the top or bottom.


2.Compute Perceptual Hashes

▫️A perceptual hash (phash) is calculated for each cropped frame using the imagehash library.
▫️These hashes represent the visual content of the frames in a way that is robust to minor changes.


3.Compare Hashes

▫️Hashes from different videos are compared using fuzzy matching provided by rapidfuzz.
▫️The similarity between hashes is quantified as a percentage.


4.Calculate Similarity Scores

▫️The script counts how many frame pairs have a similarity above the similarity_threshold.
▫️A final score is calculated based on the proportion of high-similarity matches relative to the total comparisons.


5.Determine Video Similarity

▫️If the number of high-similarity matches exceeds min_high_similarity_matches, the videos are likely the same.
▫️▫Otherwise, if the final score exceeds the final_score_threshold, the videos are considered likely the same.
▫️The conclusion is printed to the console.

## License
This project is licensed under the [MIT License](LICENSE).
