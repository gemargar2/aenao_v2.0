# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 9:35:51 2023

@author: stylelev
"""

import os
import numpy as np
import pandas as pd
from scipy import stats
import joblib
import scipy
import tensorflow
from datetime import datetime

os.chdir("/home/raspberry/Desktop")

THRESHOLD = 0.0021

raw_scale = 1               # Multiply raw values to fit into integers
sensor_sample_rate = 200    # Hz
desired_sample_rate = 50    # Hz
sample_time = 1           # Time (sec) length of each sample
samples_per_file = 500      # Expected number of measurements in each file (truncate to this)
max_measurements = int(sample_time * sensor_sample_rate)

def create_feature_set_val(path): 
     test = np.array([path])   
    
     x_out = []
     for file in test:
         sample = np.genfromtxt(file, delimiter=',') # read file, delimiter separate
         features = extract_features(sample, max_measurements, raw_scale)
         x_out.append(features)
        
     return np.array(x_out)

# ======================================= FEATURES EXTRACTION ==========================================================

# Function: extract specified features (variances, MAD) from sample
def extract_features(sample, max_measurements=0, scale=1):
    
    features = []
#    dummy_indices = []
    
    # Truncate sample
    if max_measurements == 0:
        max_measurements = sample.shape[0]
    sample = sample[0:max_measurements]
    
    # Scale sample
    sample = scale * sample

#    # Variance
    features.append(np.var(sample, axis=0))
#    dummy_indices.append(1)

# extract shannon entropy (cut signals to 500 bins)
    
    entropy = []
    df = pd.DataFrame(sample)  # Convert 'sample' to a pandas DataFrame

    for col in df.columns:
        bins = pd.cut(df[col], bins=500)
        entropy.append(scipy.stats.entropy(bins.value_counts()))

    features.append(np.array(entropy))
#    dummy_indices.append(2)
    
#    # Crest Factor
    crest_factor = np.max(np.abs(sample), axis=0) / np.sqrt(np.mean(sample ** 2, axis=0))
    features.append(crest_factor)
#    dummy_indices.append(3)
    
#   # extract peak-to-peak features
    features.append(np.array(np.max(np.abs(sample), axis=0) + np.min(np.abs(sample), axis=0)))
#    dummy_indices.append(4)

#    # Root mean square value (RMS)
    # features.append(np.sqrt(np.mean(sample ** 2, axis=0)))
    # dummy_indices.append(5)
    
#     # Kurtosis
    features.append(stats.kurtosis(sample))
#    dummy_indices.append(6)
    
#     # Skew
    features.append(stats.skew(sample))
#    dummy_indices.append(7)
   
    # # Median absolute deviation (MAD)
    # features.append(stats.median_abs_deviation(sample))
    # dummy_indices.append(8) 

    return np.array(features).flatten()#, dummy_indices


#-------------------------------------------- MODEL ------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------

def run_vibes_validation():

    scaler = joblib.load('scaler_data2')
    #instance = create_feature_set_val('./ShawnHymel tinyml-example-anomaly-detection master datasets/ceiling-fan/fan_0_low_1_weight/0329.csv')
    instance = create_feature_set_val('aenao_data/vibration/vib_sample2.csv')
    instance = scaler.transform(instance)
    instance = instance.reshape(instance.shape[0], 1, instance.shape[1])


    model = tensorflow.keras.models.load_model('vibration_AE.h5')
    print(model.summary())
    predictions = model.predict(instance)
    mse = np.mean(np.mean(np.square(instance - predictions), axis=1))

    if mse < THRESHOLD:
        #print("Normal Vibrations")
        message = "OK"
    else:
        #print("Abnormal Vibrations")
        message = "NOT OK"
        
    return message









