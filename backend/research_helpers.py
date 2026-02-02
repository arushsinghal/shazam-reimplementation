import numpy as np
import librosa
from scipy import signal
from typing import Dict, Any, Tuple
import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import DEFAULT_CONFIG
from service import get_service, AudioFingerprintingService

# 1. generate_noise_profile
def generate_noise_profile(noise_type: str, length: int) -> np.ndarray:
    """
    Generate synthetic noise profiles based on type.
    """
    np.random.seed(42)  # For reproducibility during generation

    if noise_type == "white":
        return np.random.randn(length)

    elif noise_type == "pink":
        # Pink noise: 1/f spectral power density
        # Simple approximation using filtered white noise
        b = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
        a = np.array([1, -2.494956002, 2.017265875, -0.522189400])
        white = np.random.randn(length + 1000)
        pink = signal.lfilter(b, a, white)
        return pink[1000:]

    elif noise_type == "cafe":
        # Overlapping sine waves (5 different frequencies 100-900 Hz) to simulate chatter hum
        t = np.arange(length)
        freqs = [100, 250, 400, 750, 900]
        noise = np.zeros(length)
        for f in freqs:
            # Varying phases
            phase = np.random.rand() * 2 * np.pi
            noise += np.sin(2 * np.pi * f * t / 44100 + phase)
        return noise / len(freqs)

    elif noise_type == "street":
        # Engine noise (150 Hz fundamental with harmonics)
        t = np.arange(length)
        f0 = 150
        noise = np.sin(2 * np.pi * f0 * t / 44100)
        # Add harmonics
        noise += 0.5 * np.sin(2 * np.pi * 2 * f0 * t / 44100)
        noise += 0.25 * np.sin(2 * np.pi * 3 * f0 * t / 44100)
        # Add some random rumble
        noise += 0.5 * np.random.randn(length)
        return noise

    elif noise_type == "club":
        # Bass + drums simulation (60 Hz + 100 Hz kick)
        t = np.arange(length)
        # Continuous sub bass
        bass = np.sin(2 * np.pi * 60 * t / 44100)
        # Periodic kick drum (approx every 0.5s)
        beat_len = int(0.5 * 44100)
        kick_env = np.exp(-np.linspace(0, 10, beat_len))
        kick = np.sin(2 * np.pi * 100 * np.arange(beat_len) / 44100) * kick_env

        # Tile kick
        num_beats = int(np.ceil(length / beat_len))
        kick_track = np.tile(kick, num_beats)[:length]

        return bass + kick_track

    else:
        # Default to white noise
        return np.random.randn(length)

# 2. add_noise_at_snr
def add_noise_at_snr(signal_data: np.ndarray, noise: np.ndarray, snr_db: int) -> np.ndarray:
    """
    Add noise to signal at specified SNR.
    """
    if len(noise) < len(signal_data):
        # Repeat noise if too short
        repeats = int(np.ceil(len(signal_data) / len(noise)))
        noise = np.tile(noise, repeats)[:len(signal_data)]
    else:
        # Crop noise if too long
        noise = noise[:len(signal_data)]

    # Calculate powers
    signal_power = np.mean(signal_data ** 2)
    noise_power = np.mean(noise ** 2)

    if noise_power == 0:
        return signal_data

    if signal_power == 0:
        return noise

    # Calculate required noise scalar
    # SNR_linear = P_signal / P_noise_scaled
    # P_noise_scaled = scalar^2 * P_noise
    # scalar = sqrt(P_signal / (SNR_linear * P_noise))

    snr_linear = 10 ** (snr_db / 10.0)
    noise_scale = np.sqrt(signal_power / (snr_linear * noise_power))

    return signal_data + (noise * noise_scale)

# 3. simulate_codec_degradation
def simulate_codec_degradation(audio: np.ndarray, codec: str, bitrate: int) -> np.ndarray:
    """
    Simulate audio codec artifacts.
    """
    sr = DEFAULT_CONFIG["sr"]

    if codec.lower() in ["mp3", "aac"]:
        # Simulate high-frequency loss based on bitrate
        # Lower bitrate = lower cutoff frequency
        if bitrate < 64:
            cutoff = 8000
        elif bitrate < 128:
            cutoff = 12000
        elif bitrate < 192:
            cutoff = 15000
        else:
            cutoff = 18000

        # Low-pass filter
        sos = signal.butter(10, cutoff, 'low', fs=sr, output='sos')
        filtered = signal.sosfilt(sos, audio)
        return filtered

    elif codec.lower() == "opus":
        # Simulate quantization noise
        # Lower bitrate = fewer quantization levels
        if bitrate < 32:
            levels = 256 # 8-bit like
        elif bitrate < 64:
            levels = 1024
        else:
            levels = 4096

        # Quantize
        audio_norm = audio / (np.max(np.abs(audio)) + 1e-9)
        quantized = np.round(audio_norm * levels) / levels
        return quantized * np.max(np.abs(audio))

    elif codec.lower() == "flac":
        return audio

    else:
        return audio

# 4. simulate_microphone_degradation
def simulate_microphone_degradation(audio: np.ndarray, mic_type: str) -> np.ndarray:
    """
    Simulate microphone frequency response and noise floor.
    """
    noise_levels = {
        "iphone": 0.01,
        "android": 0.015,
        "laptop": 0.008,
        "headset": 0.003,
        "loud_env": 0.05,
        "studio": 0.001
    }

    level = noise_levels.get(mic_type.lower(), 0.01)

    # Add random noise floor
    noise = np.random.randn(len(audio)) * level
    noisy_audio = audio + noise

    # Simple EQ simulation for mics (bandpass)
    sr = DEFAULT_CONFIG["sr"]
    if mic_type.lower() in ["laptop", "headset"]:
        # Tiny mics often have no bass
        sos = signal.butter(4, 200, 'high', fs=sr, output='sos')
        noisy_audio = signal.sosfilt(sos, noisy_audio)

    return noisy_audio

# Test Runners (Helper wrappers)

async def run_single_noise_test(audio_path: str, noise_type: str, snr_db: int) -> Dict[str, Any]:
    service = get_service()

    # Load audio
    y, sr = librosa.load(audio_path, sr=DEFAULT_CONFIG["sr"])

    # Generate and add noise
    noise = generate_noise_profile(noise_type, len(y))
    noisy_audio = add_noise_at_snr(y, noise, snr_db)

    import tempfile
    import soundfile as sf
    import os

    # Create temp file with proper cleanup
    fd, tmp_name = tempfile.mkstemp(suffix=".wav")
    try:
        sf.write(tmp_name, noisy_audio, sr)

        # Use service to identify
        result = service.recognize_audio(tmp_name)

        # Result format from service.recognize_audio:
        # { 'matched': bool, 'song_name': str, 'score': float, ... } or error dict

        return {
            "matched": result.get("matched", False) and result.get("song_name") is not None,
            "score": result.get("score", 0.0),
            "noise_type": noise_type,
            "snr_db": snr_db,
            "timestamp": "iso-time-placeholder", # Handled by route
            "detected_song": result.get("song_name")
        }
    finally:
        os.close(fd)
        os.unlink(tmp_name)

async def run_single_codec_test(audio_path: str, codec: str, bitrate: int) -> Dict[str, Any]:
    service = get_service()

    # Load audio
    y, sr = librosa.load(audio_path, sr=DEFAULT_CONFIG["sr"])

    # Simulate codec
    degraded_audio = simulate_codec_degradation(y, codec, bitrate)

    import tempfile
    import soundfile as sf
    import os

    fd, tmp_name = tempfile.mkstemp(suffix=".wav")
    try:
        sf.write(tmp_name, degraded_audio, sr)
        result = service.recognize_audio(tmp_name)

        return {
            "matched": result.get("matched", False) and result.get("song_name") is not None,
            "score": result.get("score", 0.0),
            "codec": codec,
            "bitrate": bitrate,
            "timestamp": "iso-time-placeholder",
            "detected_song": result.get("song_name")
        }
    finally:
        os.close(fd)
        os.unlink(tmp_name)

async def run_single_mic_test(audio_path: str, mic_type: str) -> Dict[str, Any]:
    service = get_service()

    # Load audio
    y, sr = librosa.load(audio_path, sr=DEFAULT_CONFIG["sr"])

    # Simulate mic
    degraded_audio = simulate_microphone_degradation(y, mic_type)

    import tempfile
    import soundfile as sf
    import os

    fd, tmp_name = tempfile.mkstemp(suffix=".wav")
    try:
        sf.write(tmp_name, degraded_audio, sr)
        result = service.recognize_audio(tmp_name)

        return {
            "matched": result.get("matched", False) and result.get("song_name") is not None,
            "score": result.get("score", 0.0),
            "microphone": mic_type,
            "timestamp": "iso-time-placeholder",
            "detected_song": result.get("song_name")
        }
    finally:
        os.close(fd)
        os.unlink(tmp_name)

