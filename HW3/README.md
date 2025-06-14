# **HW3 - Emotion Recognition**

## **File Structure**
```
parent_directory/
│── em3907/
│   │── Feature_Extraction_Analysis.ipynb          # Task1: Feature Analysis using Praat and Parselmouth
│   │── Classification.ipynb                       # Task2: Classification Experiments using openSMILE toolkit
│   │── response_em3907.pdf                        # Report with my responses to the questions
│   │── README.md                                  # Explanation of the code
│
│── opensmile/                                     # openSMILE toolkit directory
│── features/                                      # extracted openSMILE features
│── hw3_speech_files/                              # provided .wav file directory
│
└── Note: Only the em3907 directory is included in the submission.
```

## **Detail description of each file**
- `Feature_Extraction_Analysis.ipynb`  
  Scripts for feature extraction using Parselmouth and feature analysis.
- `Classification.ipynb`  
  Scripts for feature extraction using openSMILE toolkit and classification experiments using extracted features and leave-one-speaker-out cross-validation.
- `response_em3907.pdf`  
  Final report containing answers to feature analysis, classification experiments, and error analysis.
- `README.md`  
  This file. Documentation for code structure, feature extraction method, classification method, and execution instructions.


## Feature Extraction

### 1. Parselmouth-based Extraction
- **Tool**: Parselmouth (Python interface for Praat)
  
- **Extracted Features**: 
  - Pitch (raw pitch array): min, max, and mean pitch were extracted from the raw pitch array, after excluding zero and NaN values.
  - Intensity (raw intensity array): min, max, and mean intensity were also extracted from the raw intensity array, excluding zero and NaN values.
  
- **Settings**:
  - Pitch analysis range: 75–600 Hz (autocorrelation method)
  - Intensity analysis: pitch floor set to 75 Hz, and only channel 1 (left channel) was used.
  
- **Z-score Normalization across individual speakers**:
  - Speaker-wise z-score normalization was applied across all samples for each speaker.
      - 1. Extract raw feature values for all speech segments from speaker X.
        2. Concatenate all feature arrays from speaker X and calculate an overall mean (𝜇𝑋) and std (𝜎𝑋) of speaker X.
        3. Normalize each extracted feature array – for each value 𝒙 in an array, calculate the normalized 𝒙 as (𝒙 - 𝜇𝑋) / 𝜎𝑋.
        4. Finally, calculate the min, max, and mean of feature for each segment using the normalized feature array.
        5. *Note: obtain an overall pitch/intensity mean and std value for **each speaker instead of each feature**, in order to normalize by the speaker.


### 2. openSMILE-based Extraction
- **Tool**: openSMILE toolkit
- **Configuration**: IS09_emotion.conf (INTERSPEECH 2009 Emotion Challenge feature set)
- **Execution**:
  - Feature extraction performed **via terminal** using:
    1. Create a `features/` folder in the parent directory.
    2. Install and build the opensmile toolkit by executing the following commands from the parent directory:
    ```sh
    git clone https://github.com/audeering/opensmile.git
    cd opensmile/
    bash build.sh
    ```
    The `opensmile` directory will be created in the parent folder.
    
    3. Extract openSMILE features by running:
    ```sh
    find ../hw3_speech_files/ -type f -name "*.wav" -exec sh -c 'for file; do base=$(basename "$file" ".wav"); ./build/progsrc/smilextract/SMILExtract -l 1 -C ./config/is09-13/IS09_emotion.conf -I $file -csvoutput "../features/${base}.csv"; done' sh {} +
    ```
    The extracted feature files will be saved in the `features/` directory.

- **Normalization**:
  - Speaker-wise z-score normalization was applied before classification.
      - Unlike the feature analysis using Praat, openSMILE features provided precomputed statistical values. Thus, instead of aggregating and filtering raw feature arrays, mean and standard deviation were calculated directly from statistical values for each speaker.
      - 1. Compute the overall mean (𝜇𝑋) and standard deviation (𝜎𝑋) of each feature for speaker X.
        2. Normalize each feature value 𝒙, using the formula: z = (𝒙 - 𝜇𝑋) / 𝜎𝑋.
        3. Perform this normalization for all feature columns.


## Classification Experiments
- **Features**:
    - 180 total features selected using Random Forest feature importance.
    - Source features:
        - 384 openSMILE features
        - Additional features:
            - Speech-based features:
                - four normalized features from task 1 (`pitch_min_norm`, `pitch_max_norm`, `pitch_mean_norm`, `intensity_mean_norm`)
                - Additional extracted feature using Parselmouth and SpeechRecognition: `jitter`, `shimmer`, `HNR`, `ASR confidence score`
            - Text-based features:
                - `content_ratio = word_count / content_length`
                - `pitch_variation = pitch_mean_norm x word_counts`
                  
- **Classifier**: Support Vector Machine (SVM) with:
    - C=1.0, gamma="scale", kernel="rbf", random_state = 42, class_weight="balanced"
    
- **Validation**: Leave-One-Speaker-Out Cross-Validation

- **Evaluation Metrics**:
  - Per-speaker classification report (precision, recall, F1, support)
  - Aggregated accuracy and weighted F1 score across all speakers.

## How to Run
1. **Feature Extraction and Analysis**
   - Open `Feature_Extraction_Analysis.ipynb`
   - Execute all cells to reproduce feature extraction, normalization, and visualization.
   - Ensure Parselmouth is installed.
   - If Parselmouth is not installed, install it using:
     ```sh
     pip install praat-parselmouth
     ```
    
2. **Classification**
   - Open `Classification.ipynb`
   - Ensure openSMILE feature files are extracted and available under the `features/` directory.
   - Execute all cells to reproduce classification and evaluation.

3. **Directory Structure Requirements**
   - `hw3_speech_files/`, `features/`, and `opensmile/` directories must be located in the **parent folder** of `em3907/`.


## Special Notes
- **openSMILE feature extraction was performed outside Jupyter notebooks, using terminal commands.**
- **Ensure that the input and output paths are correctly configured when running openSMILE manually. In particular, both the `hw3_speech_files/` and `features/` directories must exist in the parent directory of the `em3907/` folder for the `classification.ipynb` script to function properly.**
- The final report (`response_em3907.pdf`) provides a complete summary of feature analysis, classification experiments, and improvement ideas based on the results.

