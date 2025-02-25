# **HW1 - Speech Feature Extraction & Manipulation**

## **Description**
This project extracts speech features from two sets of `.wav` recordings:
1. **Eesun_recordings/**: These are self-recorded speech samples using Praat. The transcript for these recordings is:
    > "Oh my gosh, I can’t believe this happened. What am I supposed to do now?"
2. **MSP_samples/**: These are given recordings provided in the dataset.

Additionally, the Neutral.wav file from `Eesun_recordings` is manipulated to sound more like Happy.wav by adjusting pitch and duration.

## **File Structure**
```
HW1/
│── Eesun_recordings/               # Self-recorded speech samples
│   │── Afraid.wav
│   │── Angry.wav
│   │── Disgusted.wav
│   │── Happy.wav
│   │── Neutral.wav
│   │── Sad.wav
│   │── Surprised.wav
│
│── feature_extraction.py          # Main feature extraction & manipulation script
│── bonus.wav                      # Manipulated “Neutral.wav” (transformed to “Happy.wav”)
│── bonus.Manipulation             # Manipulation object for pitch & duration changes
│── HW1_response.docx              # Report including method explanations
│── msp_features.csv               # Extracted features from “MSP_samples”
│── my_features.csv                # Extracted features from “Eesun_recordings”
│── requirements.txt               # Required Python packages
│
└── Note: MSP_samples directory is not included in the submission.
        If you want to extract features from the MSP_samples dataset, place the MSP_samples directory inside HW1.
```

## **How to Run**
### **1. Install required dependencies**
```sh
pip install -r requirements.txt
```

### **2. Handle the MSP samples directory**
- If you want to execute features from the **MSP_samples dataset**, add the `MSP_samples/` directory inside `HW1`.
- Otherwise, modify `feature_extraction.py' by removing:
    ``` python
    file_dirs = ['HW1/MSP_samples/','HW1/Eesun_recordings/']
    output_names = ['HW1/msp_features.csv','HW1/my_features.csv']
    ```
    and keep only:
    ``` python
    file_dirs = ['HW1/Eesun_recordings/']
    output_names = ['HW1/my_features.csv']
    ```
### **3. Run feature extraction & manipulation script**
```sh
python feature_extraction.py
```

### **4. Expected output**
- `my_features.csv`: Extracted features from `Eesun_recordings/`
- `msp_features.csv`: Extracted features from `MSP_samples/`
- `bonus.wav`: Neutral speech transformed into Happy speech
- `bonus.Manipulation`: Manipulation object for pitch & duration changes

## **Feature Extraction Details**
The script extracts the following speech features using **Praat (parselmouth)**:
- Pitch: Minimum, Maximum, Mean, Standard Deviation
- Intensity: Minimum, Maximum, Mean (energy-averaged), Standard Deviation
- Speaking Rate: Approximated as #words/duration, using Google Speech-to-Text for transcription.
- Jitter & Shimmer: Measures of voice perturbation.
- HNR (Harmonics-to-Noise Ratio): Extracted using `To Harmonicity (cc)`.

### Speeking Rate Calculation
Speaking rate is estimated using:
```python
word_count = len(transcript.split())
speaking_rate = word_count / duration
```
Since background noise can interfere with transcription, noise reduction is applied before speech recognition:
```python
speech_to_text.adjust_for_ambient_noise(source, duration=0.3)
```

## **Speech Manipulation (Bonus)**
- `Eesun_recordings/Neutral.wav`: transformed into Happy speech by adjusting:
  - Pitch: Increased by 1.5x and shifted +30 Hz.
  - Speaking Rate: Increased by 1.1x (duration scaled to 0.91).

The manipulated speech file is saved as `bonus.wav` and `bonus.Manipulation`.


## **Additional Notes**
- `MSP_samples/` directory is referenced in the script but is NOT included in the submission, as per the assignment instructions.
- The script will still run correctly using `Eesun_recordings/`.
- If you want to include `MSP_samples`, make sure to place it in `HW1/`. Otherwise, remove related references in `feature_extraction.py`.

## **References**
- Parselmouth Praat API Documentation: [Parselmouth Praat Call](https://parselmouth.readthedocs.io/en/latest/api/parselmouth.praat.call.html)
- Parselmouth Library Documentation (PDF): Parselmouth Docs [PDF](https://parselmouth.readthedocs.io/_/downloads/en/stable/pdf/)
- MSP-Podcast Dataset: [MSP-Podcast Speech Corpus](https://ecs.utdallas.edu/research/researchlabs/msp-lab/MSP-Podcast.html)
- Praat Manual
