import numpy as np
from prony import prony
from shanks import shanks
from pade import pade
import soundfile as sf
from glob import glob
from scipy.signal import lfilter,decimate
import warnings

def load_ogg():
    data = dict()
    # Find all the .ogg files in vowels/ and read them into a dictionary
    for file in glob('vowels/*.ogg'):
        key = file[len('vowels/'):-len('.ogg')]
        data[key],samplerate = sf.read(file)

    return(data,samplerate)

def synthesize_vowel(data,vowel,p=12,q=0,freq=100,duration=1.5,samplerate=44100):

    # 12th order won't do high sample rate well, so decimate
    thresh_samplerate = 8000
    if samplerate > thresh_samplerate:

        # Define the new samplerate
        dec_factor = np.ceil(samplerate/thresh_samplerate).astype(int)
        samplerate0 = int(samplerate/dec_factor)
        # print('Decimated to samplerate of %d' % samplerate0)

        # # Decimate the signal - some future warnings to avoid here...
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=FutureWarning)
            sig = decimate(np.mean(data[vowel],axis=1),dec_factor)

    else:
        sig = np.mean(data[vowel],axis=1)
        samplerate0 = samplerate

    # The signal modeling!
    a,b,err = prony(sig,p,q)
    # a,b,err = shanks(np.mean(data[vowel],axis=1),p,q)
    # a,b = pade(np.mean(data[vowel],axis=1),p,q)

    # Find the sample period given the desired frequency (Hz)
    sampleperiod = np.floor(samplerate0/freq).astype(int)

    # Delta
    delta = np.zeros(sampleperiod)
    delta[0] = 1

    # Delta train given duration (s)
    reps = np.floor(duration*samplerate0/sampleperiod).astype(int)
    deltatrain = np.tile(delta,reps)

    # Filter using AR coeffs to get synthesized vowel sound, and normalize
    synth = lfilter([1],a,deltatrain)
    synth /= np.max(synth)
    return(synth,samplerate0)

def save(filename,data,save_dir='synth',samplerate=44100):
    savedfile = '%s/%s' % (save_dir,filename)
    sf.write(savedfile,data,samplerate)
    return(savedfile)

if __name__ == '__main__':

    # Grab our vowel sounds
    data,samplerate = load_ogg()

    # Synthesize each vowel
    for vowel in data.keys():
        synth = synthesize_vowel(data,vowel,freq=200,duration=1.5,samplerate=samplerate)
        save('%s_synth.ogg' % vowel,synth,samplerate=samplerate)
