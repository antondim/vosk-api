#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import os
import pyaudio
import json
from array import array
import wave 
import time
import glob

WAV_SAVE_PATH = 'wav_folder/'  # add your path (e.g /home/f00/Desktop/wav_data/ or folder/)
DELETE_OLD_WAVS = True 
SAVE_MODE = True

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

def delete_old_wavs():
    # Deleting all previously saved .wav files
    wav_files = glob.glob(WAV_SAVE_PATH + '*.wav')
    for file in wav_files:
        os.unlink(file)

def wav_folder_creation():
    if not os.path.isdir(WAV_SAVE_PATH):
        os.makedirs(WAV_SAVE_PATH)
        print("created folder : ", WAV_SAVE_PATH)
    else:
        if DELETE_OLD_WAVS:
            delete_old_wavs()

def save_wav(path, sample_width, wav_data):
    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(16000)
    wave_file.writeframes(wav_data)
    wave_file.close()

def main():

    wav_sound_values = array('h') 
    model = Model("model")
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    sample_width = p.get_sample_size(pyaudio.paInt16)

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    while True:
        data = stream.read(4000, exception_on_overflow = False)
        sound_data = array('h', data)
        wav_sound_values.extend(sound_data)
        
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            txt = rec.FinalResult()
            print(txt)

            json2python_text = json.loads(txt)

            if json2python_text["text"] != '' and SAVE_MODE:
                save_wav(WAV_SAVE_PATH + 'vosk_api_mic_recording_' + str(time.time()) + '.wav', sample_width, wav_sound_values)
                wav_sound_values = array('h')
            else:   
                wav_sound_values = array('h') 
        else:
            print(rec.PartialResult())

if __name__ == "__main__":

    wav_folder_creation()
    main()

