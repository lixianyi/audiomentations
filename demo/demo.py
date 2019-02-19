import os

import numpy as np
from scipy.io import wavfile
from tqdm import tqdm

from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift

SAMPLE_RATE = 16000
CHANNELS = 1


def load_wav_file(sound_file_path):
    sample_rate, sound_np = wavfile.read(sound_file_path)
    if sample_rate != SAMPLE_RATE:
        raise Exception(
            "Unexpected sample rate {} (expected {})".format(sample_rate, SAMPLE_RATE)
        )

    assert sound_np.dtype == np.int16

    sound_np = sound_np / 32767  # ends up roughly between -1 and 1
    return sound_np


augmenter = Compose(
    [
        AddGaussianNoise(),
        TimeStretch(),
        PitchShift(),
    ]
)

current_dir = os.path.dirname(__file__)
output_dir = os.path.join(current_dir, "output")
os.makedirs(output_dir, exist_ok=True)

samples = load_wav_file(os.path.join(current_dir, "acoustic_guitar_0.wav"))
for i in tqdm(range(20)):
    output_file_path = os.path.join(output_dir, "{:03d}.wav".format(i))
    augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
    wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)
