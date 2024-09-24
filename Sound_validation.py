import os
import numpy as np
import tensorflow
import librosa
from scipy import signal as sg
from datetime import datetime

def f_high(y,sr):
    b,a = sg.butter(10, 1000/(sr/2), btype='lowpass')
    yf = sg.lfilter(b,a,y)
    return yf

def load_librosa_sound_file(path, mono=False, channel=0):
    signal, sr = librosa.load(path, sr=None, mono=mono)
    if signal.ndim < 2:
        sound_file = signal, sr
    else:
        sound_file = signal[channel, :], sr

    return sound_file

def extract_signal_features_fhigh_and_stft(
    signal, sr, n_fft=1024, hop_length=512, n_mels=64, frames=5
):
    signal = f_high(signal, sr)
    sgram = librosa.stft(signal)
    sgram_mag, _ = librosa.magphase(sgram)
    
    mel_spectrogram = librosa.feature.melspectrogram(
        S=sgram_mag, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels
    )
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    features_vector_size = log_mel_spectrogram.shape[1] - frames + 1
    dims = frames * n_mels

    if features_vector_size < 1:
        return np.empty((0, dims), np.float32)

    features = np.zeros((features_vector_size, dims), np.float32)
    for time in range(frames):
        features[:, n_mels * time : n_mels * (time + 1)] = log_mel_spectrogram[
            :, time : time + features_vector_size
        ].T

    return features

def run_sound_validation(): 
    '''
    os.chdir("/home/raspberry/Desktop")
    # set hyperparameters

    n_fft = 2048
    hop_length = 512
    n_mels = 128
    frames = 5

    signal, sr = load_librosa_sound_file('aenao_v2.0/data/audio/audio_sample.wav') 
    instance = extract_signal_features_fhigh_and_stft(
        signal, sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels, frames=frames
    )

    model = tensorflow.keras.models.load_model('Sound_AE.h5')
    print(model.summary())

    predictions1 = model.predict(instance)
    mse = np.mean(np.mean(np.square(instance - predictions1), axis=1))
    '''

    mse = 0.8
    THRESHOLD = 1.211

    if mse < THRESHOLD:
        print("Normal sound")
        message = "OK" 
    else:
        print("Abnormal sound")
        message = "NOT OK" 
    
    return message

