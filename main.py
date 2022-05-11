# Epochs objects are a data structure for representing and analyzing equal-duration chunks of the EEG/MEG signal. Epochs are
# most often used to represent data that is time-locked to repeated experimental events (such as stimulus onsets or subject button presses),
import mne
import json
import os
import matplotlib.pyplot as plt
from pathlib import Path
import tempfile
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

#workaround for -- _tkinter.TclError: invalid command name ".!canvas"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


import mne


# Current path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def epoch(param_meg,param_eeg,param_eog,param_ecg,param_emg,param_stim,raw, events, tmin, tmax):
    raw.pick_types(meg=param_meg,eeg=param_eeg,eog=param_eog,ecg=param_ecg,emg=param_emg, stim=param_stim).crop(tmax=60).load_data()


    report = mne.Report(title='Report')

    #raw
    report.add_raw(raw=raw, title='Raw', psd=False)  # omit PSD plot


    #events
    sfreq = raw.info['sfreq']
    report.add_events(events=events, title='Events', sfreq=sfreq)


    #epochs

    event_id = {
        'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,
        'visual/right': 4, 'face': 5, 'buttonpress': 32
    }

    metadata, _, _ = mne.epochs.make_metadata(
        events=events,
        event_id=event_id,
        tmin=tmin,
        tmax=tmax,
        sfreq=raw.info['sfreq']
    )
    epochs = mne.Epochs(
        raw=raw, events=events, event_id=event_id, metadata=metadata
    )

    report.add_epochs(epochs=epochs, title='Epochs from "epochs"')

    # == SAVE REPORT ==
    report.save('out_dir_report/report.html', overwrite=True)

    # == SAVE FILE ==
    epochs.save(os.path.join('out_dir', 'meg-epo.fif'), overwrite=True)







def main():
    # Load inputs from config.json
    with open('config.json') as config_json:
        config = json.load(config_json)

    # Read the meg file
    data_file = config.pop('fif')

    # Read the event time
    tmin = config.pop('t_min')
    tmax = config.pop('t_max')

    # crop() the Raw data to save memory:
    raw = mne.io.read_raw_fif(data_file, verbose=False).crop(tmax=60)

    i# f 'events' in config.keys():
       #  events_file = config.pop('events')
        # events = mne.read_events(events_file)
    # else:
        # extract an events array from Raw objects using mne.find_events():
        # reading experimental events from a “STIM” channel;
    events = mne.find_events(raw, stim_channel='STI 014')

    print(config['param_eeg'])
    epochs = epoch(config['param_meg'],config['param_eeg'],config['param_eog'], config['param_ecg'],config['param_emg'],config['param_stim'], raw, events, tmin=tmin, tmax=tmax)



if __name__ == '__main__':
    main()

