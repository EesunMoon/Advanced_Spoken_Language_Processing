import parselmouth
from parselmouth.praat import call
import numpy as np
import pandas as pd
import os
from IPython.display import Audio
import speech_recognition as sr

class Extract_Feature:
    def __init__(self, file_path):
        # parselmouth.Sound: A fragment of audio, represented by one or multiple channels of floating point values between -1 and 1, sampled at a fixed sampling frequency.
        self.sound = parselmouth.Sound(file_path)
        self.transcript = self.get_transcript(file_path)
        self.features = {}
        self.features["Speech File"] = file_path
        self.columns = ["Speech File", "Min Pitch" ,"Max Pitch", "Mean Pitch" ,"Sd Pitch", 
                        "Min Intensity", "Max Intensity" ,"Mean Intensity", "Sd Intensity",
                        "Speaking Rate" ,"Jitter", "Shimmer" ,"HNR"]

    def extract_features(self):
        """
            Feature Extraction Notes
            1. Pass praat script commands into the parselmouth.pratt.call() function for feature extraction
                Do Not use numpy functions or built-in methods of the form to_feature()
            2. For pitch extraction, set pitch floor to 75Hz, and pitch ceiling to 600Hz.
                Avoid using autocorrelation
            3. For intensity extraction, set the pitch floor to 100Hz.
                Use 'energy' averaging method to get mean intensity
            4. For jitter, extract local jitter only, and set period floor to 0.0001s,
                period ceiling to 0.02s, and maximum period factor to 1.3.
            5. For shimmer, extract local shimmer only, and set period floor to 0.0001s,
                period ceiling to 0.02s, maximum period factor to 1.3, 
                and maximum amplitude factor to 1.6.
            6. To calculate HNR, extract harmonicity (cc) first.
                Set time step to 0.01 minimum pitch to 75Hz, silence threshold to 0.1,
                and number of periods per window 1.0.
            7. Speaking rate can be approximated with #words/duration.
                Please indicate which method you use in your submission and how you obtain the result
                e.g. transcripts, helper scripts.
        """
        # call feature extractions function
        self.extract_pitch()
        self.extract_intensity()
        self.get_speaking_rate(self.transcript)
        self.extract_jitter()
        self.extract_shimmer()
        self.extract_hnr()
        
        return [self.features[key] for key in self.columns]

    def extract_pitch(self, time_step = 0.01, pitch_floor = 75, pitch_ceiling=600):
        """
            input: pitch extraction parameter
            output: pitch minimum, pitch maximum, pitch mean, pitch std
        """
        self.point_process = call(self.sound, "To PointProcess (periodic, cc)", 
                                pitch_floor, pitch_ceiling)
        
        # pitch: pitch floor = 75, pitch ceiling = 600
        pitch = call(self.sound, "To Pitch", time_step, pitch_floor, pitch_ceiling)
        
        min_time, max_time, unit, interpolation_method = 0.0, 0.0, "Hertz", "Parabolic"
        pitch_min = call(pitch, "Get minimum", min_time, max_time, unit, interpolation_method)
        pitch_max = call(pitch, "Get maximum", min_time, max_time, unit, interpolation_method)
        pitch_mean = call(pitch, "Get mean", min_time, max_time, unit)
        pitch_std = call(pitch, "Get standard deviation", min_time, max_time, unit)

        self.features["Min Pitch"] = pitch_min
        self.features["Max Pitch"] = pitch_max
        self.features["Mean Pitch"] = pitch_mean
        self.features["Sd Pitch"] = pitch_std

        print("**Pitch**")
        print(f"pitch min:{pitch_min:.2f} Hz, pitch max: {pitch_max:.2f} Hz, pitch_mean: {pitch_mean:.2f} Hz, pitch std: {pitch_std:.2f} Hz")
        return pitch_min, pitch_max, pitch_mean, pitch_std

    def extract_intensity(self, time_step = 0.01, pitch_floor = 100):
        """
            input: intensity extraction parameter
            output: intensity_min, intensity_max, intensity_mean, intensity_std
        """
        # intensity: pitch floor = 100, energy averaging method to get mean intensity
        subtract_mean = "yes"
        intensity = call(self.sound, "To Intensity", pitch_floor, time_step, subtract_mean)
        
        min_time, max_time, interpolation_method, averaging_method = 0.0, 0.0, 'Parabolic', "energy"
        intensity_min = call(intensity, "Get minimum", min_time, max_time, interpolation_method)
        intensity_max = call(intensity, "Get maximum", min_time, max_time, interpolation_method)
        intensity_mean = call(intensity, "Get mean", min_time, max_time, averaging_method) # energy averaging
        intensity_std = call(intensity, "Get standard deviation", min_time, max_time) 

        self.features["Min Intensity"] = intensity_min
        self.features["Max Intensity"] = intensity_max
        self.features["Mean Intensity"] = intensity_mean
        self.features["Sd Intensity"] = intensity_std

        print("**Intensity**")
        print(f"intensity min:{intensity_min:.2f} dB, intensity max: {intensity_max:.2f} dB, intensity_mean: {intensity_mean:.2f} dB, intensity std: {intensity_std:.2f} dB")
        return intensity_min, intensity_max, intensity_mean, intensity_std

    def extract_jitter(self, period_floor=0.0001, period_ceiling=0.02, maximum_period_factor=1.3):
        # jitter: local jitter, period floor = 0.0001, period ceiling = 0.02, maximum period = 1.3
        min_time, max_time = 0.0, 0.0
        jitter = call(self.point_process, "Get jitter (local)", 
                      min_time, max_time, period_floor, period_ceiling, maximum_period_factor)
        self.features["Jitter"] = jitter

        print("**Jitter**")
        print(f"Jitter:{jitter:.6f}")
        return jitter

    def extract_shimmer(self, period_floor=0.0001, period_ceiling=0.02, maximum_period_factor=1.3, maximum_amplitude=1.6):
        # Shimmer: local shimmer, period floor = 0.0001, period ceiling = 0.02, maximum period = 1.3, maximum amplitude = 1.6
        min_time, max_time = 0.0, 0.0
        shimmer = call([self.sound, self.point_process], "Get shimmer (local)", 
                       min_time, max_time, period_floor,period_ceiling, maximum_period_factor, maximum_amplitude)
        self.features["Shimmer"] = shimmer

        print("**Shimmer**")
        print(f"Shimmer:{shimmer:.6f}")
        return shimmer

    def extract_hnr(self,time_step = 0.01, minimum_pitch = 75, silence_threshold = 0.1, periods = 1.0):
        # HNR: cc first, time step = 0.01, minimum pitch = 75, silence threshold = 0.1, periods = 1.0
        hnr = call(self.sound, "To Harmonicity (cc)",
                    time_step, minimum_pitch, silence_threshold, periods)
        min_time, max_time = 0.0, 0.0
        hnr_value = call(hnr, "Get mean", min_time, max_time)
        
        self.features["HNR"] = hnr

        print("**HNR**")
        print(f"mean HNR:{hnr_value:.2} dB")
        return hnr
    
    def get_transcript(self, filename):
        speech_to_text = sr.Recognizer()

        with sr.AudioFile(filename) as source:
            speech_to_text.adjust_for_ambient_noise(source, duration=0.3)
            audio = speech_to_text.record(source)
        transcript = speech_to_text.recognize_google(audio)
        print("Transcript:", transcript)

        return transcript


    def get_speaking_rate(self, transcript):
        # duration = self.sound.get_total_duration()
        duration = call(self.sound, "Get total duration")
        print("Duration:", duration)

        word_count = len(transcript.split())
        speaking_rate = word_count / duration

        self.features["Speaking Rate"] = speaking_rate

        print("**Speaking Rate**")
        print(f"Speaking Rate: {speaking_rate:.2f} word/sec")
        return speaking_rate


    def sound_manipulation(self, time_step = 0.01, pitch_floor = 75, pitch_ceiling=600):
        """
            neurtal -> happy
                pitch: high pitch
                speed: high speed
        """

        manipulation = call(self.sound, "To Manipulation", 
                            time_step, pitch_floor, pitch_ceiling)

        # high pitch
        pitch_val = 1.5
        pitch_tier = call(manipulation, "Extract pitch tier")
        call(pitch_tier, "Multiply frequencies", self.sound.xmin, self.sound.xmax, pitch_val)
        call(pitch_tier, "Shift frequencies", self.sound.xmin, self.sound.xmax, 30, "Hertz")
        call([pitch_tier, manipulation], "Replace pitch tier")
        # call(manipulation, "Replace pitch tier", pitch_tier)

        # duration: faster speed
        speed_val = 1.1
        starting_point, ending_point = 0.000, 1.0/speed_val
        duration_tier = call(manipulation, "Extract duration tier")
        call(duration_tier, "Add point", starting_point, ending_point)
        call(duration_tier, "Add point", self.sound.xmax, ending_point)
        call([duration_tier, manipulation], "Replace duration tier")

        # save object
        call(manipulation, "Save as text file", "HW1/bonus.Manipulation")

        # save to wav file
        sound_happy = call(manipulation, "Get resynthesis (overlap-add)")
        Audio(data=sound_happy.values, rate=sound_happy.sampling_frequency)
        sound_happy.save("HW1/bonus.wav", "WAV")

def processing(data_dir, output_name):
    data = []
    for file in os.listdir(data_dir):
        if file.endswith(".wav"):
            file_path = os.path.join(data_dir, file)
            print(f"\n--{file_path} Processing--")
            EF = Extract_Feature(file_path=file_path)
            features = EF.extract_features()
            print(f"{file_path}'s result:", features)
            data.append(features)

    columns = ["Speech File", "Min Pitch" ,"Max Pitch", "Mean Pitch" ,"Sd Pitch", 
                "Min Intensity", "Max Intensity" ,"Mean Intensity", "Sd Intensity",
                "Speaking Rate" ,"Jitter", "Shimmer" ,"HNR"]
    df = pd.DataFrame(data, columns=columns)
    # print(f"--{output_name} Result--")
    # print(df)
    df.to_csv(output_name, index=False)


if __name__ == "__main__":
    file_dirs = ['HW1/MSP_samples/','HW1/Eesun_recordings/']
    output_names = ['HW1/msp_features.csv','HW1/my_features.csv']
    
    # Extract Features
    for file_dir, output_name in zip(file_dirs, output_names):
        print(f"---{file_dir} is Processing---")
        processing(file_dir, output_name)
    
    
    # [Bonus point] Manipulation (Neutral -> Happy)
    manipulation_file = "HW1/Eesun_recordings/Neutral.wav"
    EF = Extract_Feature(manipulation_file)
    EF.sound_manipulation()
    