import os
import shutil
import random
import asyncio

# Define the folder containing the video files
folder_path = "VideoFlash"
audio_folder_path = "AudioWAV"
destination_folder = "CustomTestDataset"
destination_video_path = os.path.join(destination_folder, "Videos")
destination_audio_path = os.path.join(destination_folder, "Audio")

# Define the mapping between abbreviations and emotion classes
emotion_mapping = {
    'NEU': 'Neutral',
    'HAP': 'Happy',
    'SAD': 'Sad',
    'ANG': 'Anger',
    'FEA': 'Fear',
    'DIS': 'Disgust'
}

emotion_mapping_numb = {
    'Neutral': '01',
    'Happy': '02',
    'Sad': '03',
    'Anger': '04',
    'Fear': '05',
    'Disgust': '06',
    # 'Surprised': '07'
}

file_type_mapping = {
    'Video_Audio': '01',
    'Video_Only': '02',
    'Audio': '03'
}

vocal_type = {
    'Speech': '01',
    'Song': '02'
}

emotion_intensity = {
    'XX': '01',
    'LO': '01',
    'MD': '02',
    'HI': '02'
}

# Define the number of samples per class
samples_per_class = 22

# Create a dictionary to store the counts of samples per class
samples_count = {emotion: 0 for emotion in emotion_mapping.values()}

# Retrieve all the filenames in the folder
filenames = os.listdir(folder_path)

# Sort the filenames alphabetically
filenames.sort()

# Number of shuffles to perform
num_shuffles = 10

# Perform multiple shuffles
for _ in range(num_shuffles):
    random.shuffle(filenames)

async def copy_files(source_file, destination_file):
    await asyncio.sleep(0)  # Simulate I/O operation
    try:
        shutil.copy(source_file, destination_file)
        return True
    except Exception as e:
        print(f"Failed to copy file: {source_file} to {destination_file}. Error: {str(e)}")
        return False

length = 0  
# Loop through each file in the folder
async def process_files():
    global length
    for filename in filenames:
        # Extract the emotion class from the filename
        emotion_abbr = filename.split('_')[-2]
        emotion_int = (filename.split('_')[-1]).split('.')[0]
        name = filename.split('.')[0]

        emotion = emotion_mapping.get(emotion_abbr)

        # Check if the number of samples for the current class is less than the desired count
        if samples_count[emotion] < samples_per_class:
            # Move the file to a new directory or perform any desired action
            source_file = os.path.join(folder_path, filename)
            source_audio_file = os.path.join(audio_folder_path, f"{name}.wav")

            destination_video_file_name = f"{file_type_mapping.get('Video_Audio')}_{vocal_type.get('Speech')}_{emotion_mapping_numb.get(emotion)}_{emotion_intensity.get(emotion_int)}_03_03_{length}.flv"
            destination_audio_file_name = f"{file_type_mapping.get('Audio')}_{vocal_type.get('Speech')}_{emotion_mapping_numb.get(emotion)}_{emotion_intensity.get(emotion_int)}_03_03_{length}.wav"

            destination_file = os.path.join(destination_video_path, destination_video_file_name)
            destination_audio_file = os.path.join(destination_audio_path, destination_audio_file_name)
            # Create the destination folder if it doesn't exist
            if not os.path.exists(destination_video_path):
                os.makedirs(destination_video_path)

            # Create the destination folder if it doesn't exist
            if not os.path.exists(destination_audio_path):
                os.makedirs(destination_audio_path)

            # Move the file asynchronously
            if not await copy_files(source_file, destination_file):
                print(f"Video: {filename}")
                continue
            
            if not await copy_files(source_audio_file, destination_audio_file):
                print(filename)
                continue

            # Increment the count for the current class
            samples_count[emotion] += 1
            length += 1

        # Check if the number of samples for all classes is equal to or greater than the desired count
        if all(count >= samples_per_class for count in samples_count.values()):
            break

# Run the asynchronous processing
asyncio.run(process_files())

# Print the counts of samples per class
for emotion, count in samples_count.items():
    print(f"{emotion}: {count} samples extracted.")


while True:
    if len(os.listdir(destination_video_path)) == 22 * 6 and len(os.listdir(destination_audio_path)) == 22 * 6:
        break
    else:
        print("Length of videos: ", len(os.listdir(destination_video_path)))
        print("Length of audios: ", len(os.listdir(destination_audio_path)))