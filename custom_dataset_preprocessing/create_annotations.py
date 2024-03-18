# -*- coding: utf-8 -*-

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
root = 'CustomTestDataset/Videos'

n_folds=1
folds = [[[0,1,2,3],[4,5,6,7],[8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]]
for fold in range(n_folds):
        fold_ids = folds[fold]
        test_ids, val_ids, train_ids = fold_ids
	
#annotation_file = 'annotations_croppad_fold'+str(fold+1)+'.txt'
annotation_file = os.path.join(script_dir, 'annotations.txt')

for video in os.listdir(os.path.join(script_dir, root)):
    if not video.endswith('.npy') or 'croppad' not in video:
        continue
    
    try:
        label = str(int(video.split('_')[2]))
    except:
        label = str(int(video.split('-')[2]))

    audio = '03' + video.split('_face')[0][2:] + '_croppad.wav'
    
    with open(annotation_file, 'a') as f:
        f.write(os.path.join(script_dir, root, video) + ';' + os.path.join(script_dir, "CustomTestDataset", "Audio", audio) + ';'+ label + ';testing' + '\n')
		
