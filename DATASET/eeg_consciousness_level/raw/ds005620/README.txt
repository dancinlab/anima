# A Repeated Awakening Study Exploring the Capacity of Complexity Measures to Capture Dreaming During Propofol Sedation

## Description
This dataset contains EEG data from a study investigating the effects of propofol sedation on dreaming and the applicability of complexity measures in capturing this phenomenon. The study aims to understand the dynamics of consciousness during sedation and the potential for EEG complexity measures to reflect subjective experiences.

## Authors
- Imad J. Bajwa
- Andre S. Nilsen
- René Skukies
- Arnfinn Aamodt
- Gernot Ernst
- Johan F. Storm
- Bjørn E. Juel

## Ethics Statement
Approved by the Regional Committees for Medical Research Ethics South East Norway (REK), ref. 2015/1520.

## License
This dataset is licensed under CC-BY-4.0.

## File Structure

The dataset is organized by subject, with each subject's EEG files stored in a dedicated directory. Below is the structure for the EEG data associated with a sample subject (sub-1016).

### Directory Structure
```
/Volumes/IMADS SSD/Anesthesia_conciousness_paper/project_BIDS/
└── sub-1016/
    └── eeg/
        ├── sub-1016_task-awake_acq-EC_channels.tsv
        ├── sub-1016_task-awake_acq-EC_eeg.eeg
        ├── sub-1016_task-awake_acq-EC_eeg.json
        ├── sub-1016_task-awake_acq-EC_eeg.vhdr
        ├── sub-1016_task-awake_acq-EC_eeg.vmrk
        ├── sub-1016_task-awake_acq-EC_events.json
        ├── sub-1016_task-awake_acq-EC_events.tsv
        ├── ...
```

### File Naming Convention
EEG files are named in the format:
`sub-<subject_id>_task-<task_name>_acq-<acquisition>_run-<run_number>.<extension>`

### Example Filenames
- `sub-1016_task-awake_acq-EC_channels.tsv`
- `sub-1016_task-sed_acq-rest_run-1_eeg.eeg`

### Filename Components
- **sub-<subject_id>**: Identifier for the subject (e.g., `sub-1016`).
- **task-<task_name>**: Indicates the task condition:
  - `awake`: Wakefulness
  - `sed`: Sedation condition
  - `sed2`: One-minute resting EEG recorded just before an awakening
- **acq-<acquisition>**: Type of acquisition:
  - `EC`: Eyes Closed (during wakefulness)
  - `EO`: Eyes Open (during wakefulness)
  - `tms`: Session with Transcranial Magnetic Stimulation
  - `rest`: Rest condition (during sedation)
- **run-<run_number>**: Specifies the run number for the data collection:
  - `run-1`, `run-2`, `run-3` (indicating different awakenings in sedation)
- **.<extension>**: File extension indicating the type of file (e.g., `.eeg`, `.vhdr`, `.vmrk`, etc.).

### File Types
- **.eeg**: Raw EEG data.
- **.vhdr**: BrainVision header file.
- **.vmrk**: BrainVision marker file.
- **_events.json / _events.tsv**: Event markers.
- **_channels.tsv / _eeg.json**: Channel information and metadata.

## Usage Instructions
To analyze the data, you may need software such as Python with MNE-Python. Please refer to the MNE documentation for details on how to load and manipulate the datasets.

## Contact Information
For questions regarding this dataset, please contact:
Imad J. Bajwa  
Email: imadjb@uio.no

Bjørn E. Juel
Email: Bjorneju@gmail.com

## Acknowledgements
We thank the participants and the supporting research staff for their contributions to this study.

References
----------
Appelhoff, S., Sanderson, M., Brooks, T., Vliet, M., Quentin, R., Holdgraf, C., Chaumon, M., Mikulan, E., Tavabi, K., Höchenberger, R., Welke, D., Brunner, C., Rockhill, A., Larson, E., Gramfort, A. and Jas, M. (2019). MNE-BIDS: Organizing electrophysiological data into the BIDS format and facilitating their analysis. Journal of Open Source Software 4: (1896).https://doi.org/10.21105/joss.01896

Pernet, C. R., Appelhoff, S., Gorgolewski, K. J., Flandin, G., Phillips, C., Delorme, A., Oostenveld, R. (2019). EEG-BIDS, an extension to the brain imaging data structure for electroencephalography. Scientific Data, 6, 103.https://doi.org/10.1038/s41597-019-0104-8


