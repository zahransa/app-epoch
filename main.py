#Epochs objects are a data structure for representing and analyzing equal-duration chunks of the EEG/MEG signal. Epochs are
# most often used to represent data that is time-locked to repeated experimental events (such as stimulus onsets or subject button presses),
import mne
import json
import os



def epoch(raw,tmin,tmax):

    # extract an events array from Raw objects using mne.find_events():
    events = mne.find_events(raw, stim_channel='STI 014')
    epochs = mne.Epochs(raw, events, tmin=-tmin, tmax=tmax)

    epochs.save('out_dir/epochs-epo.fif', overwrite=True)



    return epochs




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
    # extract an events array from Raw objects using mne.find_events():
    # events = mne.find_events(raw, stim_channel='STI 014')
    #
    epochs = epoch(raw,tmin,tmax)







if __name__ == '__main__':
    main()