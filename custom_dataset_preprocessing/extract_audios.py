# -*- coding: utf-8 -*-

import librosa
import os
import soundfile as sf
import numpy as np

#audiofile = 'E://OpenDR_datasets//RAVDESS//Actor_19//03-01-07-02-01-02-19.wav'
##this file preprocess audio files to ensure they are of the same length. if length is less than 3.6 seconds, it is padded with zeros in the end. otherwise, it is equally cropped from 
##both sides

script_dir = os.path.dirname(os.path.abspath(__file__))
# root = './Caucasian_CustomTestDataset/Audio'
# root = './Asian_CustomTestDataset/Audio'
root = './AfricanAmerican_CustomTestDataset/Audio'
target_time = 3.6 #sec

for audiofile in os.listdir(os.path.join(script_dir, root)):
    if not audiofile.endswith('.wav') or 'croppad' in audiofile:
        continue
    audios = librosa.core.load(os.path.join(script_dir, root, audiofile), sr=22050)

    y = audios[0]
    sr = audios[1]
    target_length = int(sr * target_time)
    if len(y) < target_length:
        y = np.array(list(y) + [0 for i in range(target_length - len(y))])
    else:
        remain = len(y) - target_length
        y = y[remain//2:-(remain - remain//2)]
    
    sf.write(os.path.join(script_dir, root, audiofile[:-4]+'_croppad.wav'), y, sr)

	
