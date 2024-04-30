# -*- coding: utf-8 -*-

import os
from sample_dataset import get_folds
script_dir = os.path.dirname(os.path.abspath(__file__))
root = 'CREMA-D/Videos'
	
#annotation_file = 'annotations_croppad_fold'+str(fold+1)+'.txt'
annotation_file = os.path.join(script_dir, 'annotations.txt')

train_files, test_files, val_files = get_folds()

for video in os.listdir(os.path.join(script_dir, root)):
    if not video.endswith('.npy') or 'croppad' not in video:
        continue
    
    try:
        label = str(int(video.split('_')[2]))
    except:
        label = str(int(video.split('-')[2]))

    fold = 'training'
    if video in test_files:
        fold = 'testing'
    elif video in val_files:
        fold = 'validation'
    elif video in train_files:
        fold = 'training'
    else:
        print("not recognized")
        continue

    audio = '03' + video.split('_face')[0][2:] + '_croppad.wav'
    
    with open(annotation_file, 'a') as f:
        f.write(os.path.join(script_dir, root, video) + ';' + os.path.join(script_dir, "CREMA-D", "Audio", audio) + ';'+ label + f';{fold}' + '\n')
		

