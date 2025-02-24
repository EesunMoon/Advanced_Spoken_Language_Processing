# **HW1 - Speech Feature Extraction & Manipulation**

## **Description**
This project extracts speech features from given `.wav` files and approximates the speaking rate using transcripts. Additionally, the **Neutral.wav** file is manipulated to sound more like **Happy.wav** by adjusting pitch and duration.

## **File Structure**
```
HW1/
│── Eesun_recordings/               # Provided speech recordings
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
    ```
    file_dirs = ['HW1/MSP_samples/','HW1/Eesun_recordings/']
    output_names = ['HW1/msp_features.csv','HW1/my_features.csv']
    ```
    and keey only:
    ```
    file_dirs = ['HW1/Eesun_recordings/']
    output_names = ['HW1/my_features.csv']
    ```
### **3. Run feature extraction & manipulation script**
```sh
python3 feature_extraction.py
```

### **4. Expected output**
- `myfeatures.csv`: Extracted features from `Eesun_recordings/`
- `bonus.wav`: Neutral speech transformed into Happy speech



## **Feature Extraction Details**
The script extracts the following speech features using **Praat (parselmouth)**:
- Pitch: Minimum, Maximum, Mean, Standard Deviation
- Intensity: Minimum, Maximum, Mean (energy-averaged), Standard Deviation
- Speaking Rate: Approximated as #words/duration, using Google Speech-to-Text for transcription.
- Jitter & Shimmer: Measures of voice perturbation.
- HNR (Harmonics-to-Noise Ratio): Extracted using `To Harmonicity (cc)`.

Speaking rate is estimated using:
```sh
word_count = len(transcript.split())
speaking_rate = word_count / duration
```
Since background noise can interfere with transcription, noise reduction is applied before speech recognition:
```sh
speech_to_text.adjust_for_ambient_noise(source, duration=0.3)
```

## **Speech Manipulation (Bonus)**
- `Eesun_recordings/Neutral.wav`: transformed into Happy speech by adjusting:
  - Pitch: Increased by 1.5x and shifted +30 Hz.
  - Speaking Rate: Increased by 1.1x (duration scaled to 0.91).

The manipulated speech file is saved as `bonus.wav`.


## **Additional Notes**
- `MSP_samples/` directory is referenced in the script but is NOT included in the submission, as per the assignment instructions.
- The script will still run correctly using `Eesun_recordings/`.
- If you want to include `MSP_samples`, make sure to place it in `HW1/`. Otherwise, remove related references in `feature_extraction.py`.
