from pathlib import Path
from PIL import Image
import cv2
import imagehash
from concurrent.futures import ThreadPoolExecutor, as_completed
from rapidfuzz import fuzz

"""
This program is for comparing videos and finding similar videos.
Even if the video is manipulated or changed, it will recognise it.

"""

# Define paths to your videos - you can add many paths as you want
folder_dir1 = 'D:\\Downloads\\videos\\Waterscape_5 and Animal_4.mp4'
folder_dir2 = 'D:\\Downloads\\videos\\Animal_4.mp4'
video_paths = [folder_dir1, folder_dir2]

# Base output directory for saving frames
base_output_folder = Path('D:\\Downloads\\video.frames.cropped')
base_output_folder.mkdir(parents=True, exist_ok=True)



def extract_and_crop_frame(video_path, output_folder, frame_rate=5):
    """
    Extracts frames from videos and crops them into their middle third part
    and then it will calculate the every frame hash
    
    Parameters:
    video_path (path): The path where the input videos are
    frame_rate (integer): Extracts frame from given video files at intervals determined by (every nth frame)


    """
    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    hashes = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process frames at specified intervals (e.g., every 5th frame)
        if frame_num % frame_rate == 0:
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            width, height = pil_img.size

            # Crop to the middle third
            crop_x1, crop_x2 = 0, width
            crop_y1 = int(height * 0.333)
            crop_y2 = int(height * 0.666)
            cropped_img = pil_img.crop((crop_x1, crop_y1, crop_x2, crop_y2))

            # Save cropped frame
            output_path = output_folder / f"frame_{frame_num:04d}.jpg"
            cropped_img.save(output_path)

            # Calculate perceptual hash
            phash = imagehash.phash(cropped_img)
            hashes[output_path.name] = str(phash)  # Store hash as string for comparison

            print(f'Saved and hashed frame {frame_num} for {video_path}')

        frame_num += 1

    cap.release()
    return hashes



def process_videos(video_paths, base_output_folder):
    folder_hashes = {}

    for video_path in video_paths:
        video_name = Path(video_path).stem
        video_output_folder = base_output_folder / video_name
        video_output_folder.mkdir(parents=True, exist_ok=True)

        # Extract frames, crop, save, and hash
        print(f"Processing video: {video_name}")
        folder_hashes[video_name] = extract_and_crop_frame(video_path, video_output_folder)

    return folder_hashes



def compare_hashes_across_folders(folder_hashes, similarity_threshold=90, final_score_threshold=70, min_high_similarity_matches=10):
    """
    Compare hashes between folders using fuzzy matching and calculate the final score.

    Parameters:
    similarity_threshold: Minimum percentage similarity between two hashes to count as a match.
    final_score_threshold: Minimum percentage of matches required to conclude that the videos are the same.
    min_high_similarity_matches: Number of highly similar frame matches required to directly conclude the videos are the same.

    """
    folder_names = list(folder_hashes.keys())
    total_comparisons = 0  # Total number of comparisons made
    high_similarity_count = 0  # Count of comparisons with similarity >= threshold

    for i in range(len(folder_names)):
        for j in range(i + 1, len(folder_names)):
            folder1, folder2 = folder_names[i], folder_names[j]
            print(f"\nComparing frames from {folder1} to frames in {folder2}:")

            for name1, hash1 in folder_hashes[folder1].items():
                for name2, hash2 in folder_hashes[folder2].items():
                    similarity = fuzz.ratio(hash1, hash2)
                    total_comparisons += 1  # Increment total comparisons

                    if similarity >= similarity_threshold:
                        high_similarity_count += 1  # Increment high similarity count
                        print(f" {folder1}/{name1} and {folder2}/{name2} {similarity}% similarity")

            print(f"Comparison completed between {folder1} and {folder2}")

    # Check if high similarity count meets or exceeds 10 to directly conclude the videos are the same
    if high_similarity_count >= min_high_similarity_matches:
        print(f"\nConclusion: The videos are likely the same because there are {high_similarity_count} frame matches with similarity >= {similarity_threshold}%.")
    else:
        # Calculate the final score as the percentage of high similarity comparisons
        if total_comparisons > 0:
            final_score = (high_similarity_count / total_comparisons) * 100
            print(f"\nFinal Score: {final_score:.2f}% of frames have similarity >= {similarity_threshold}%")
            
            # Decision based on final score threshold
            if final_score >= final_score_threshold:
                print("Conclusion: The videos are likely the same.")
            else:
                print("Conclusion: The videos are likely different.")
        else:
            print("\nNo comparisons were made.")



# Process videos and extract frames
folder_hashes = process_videos(video_paths, base_output_folder)

# Compare hashes across folders and calculate the final score
compare_hashes_across_folders(folder_hashes)
