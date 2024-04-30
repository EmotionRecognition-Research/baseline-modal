import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
root = 'CREMA-D/Videos'

def get_folds():
    files = []
    emotions = []
    for video in os.listdir(os.path.join(script_dir, root)):
        if not video.endswith('.npy') or 'croppad' not in video:
            continue
        files.append(video)
        emotions.append(video.split("_")[2])
    
    # Split the dataset into training (70%), testing (15%), and validation (15%)
    X_train, X_temp, y_train, y_temp = train_test_split(np.array(files), np.array(emotions), test_size=0.3, random_state=42)
    X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Create dictionaries to store the filenames for each set
    train_files = np.array(X_train)
    test_files = np.array(X_test)
    val_files = np.array(X_val)

    return train_files, test_files, val_files

if __name__ == "__main__":
    train_set, test_set, val_set = get_folds()
    print("Training set:")
    print(len(train_set))
    print(train_set[:5])
    print("\nTesting set:")
    print(len(test_set))
    print(test_set[:5])
    print("\nValidation set:")
    print(len(val_set))
    print(val_set[:5])