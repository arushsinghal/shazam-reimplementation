"""
Audio fingerprinting module for Shazam-style audio recognition.

This module implements:
- STFT spectrogram computation
- Constellation map generation via local spectral peak detection with frequency banding
- Anchor-target fan-out fingerprint generation
"""

from typing import List, Tuple
import numpy as np
import librosa
from scipy.ndimage import maximum_filter


def extract_fingerprints(
    y: np.ndarray,
    sr: int,
    n_fft: int,
    hop_ratio: int,
    freq_neighborhood: int,
    time_neighborhood: int,
    amplitude_threshold: float,
    num_bands: int,
    fanout: int,
    dt_min: int,
    dt_max_seconds: float,
) -> List[Tuple[int, int, int, int]]:
    """
    Extract audio fingerprints from a raw audio signal using constellation mapping.

    The fingerprinting process:
    1. Compute STFT spectrogram and convert to dB scale
    2. Detect local spectral peaks using frequency-banded maximum filtering
    3. Generate anchor-target fingerprint pairs with time-delta constraints

    Args:
        y: Audio time series (mono)
        sr: Sampling rate
        n_fft: FFT window size
        hop_ratio: Hop length as ratio of n_fft (hop_length = n_fft // hop_ratio)
        freq_neighborhood: Frequency axis neighborhood size for peak detection
        time_neighborhood: Time axis neighborhood size for peak detection
        amplitude_threshold: Minimum amplitude in dB for peak detection
        num_bands: Number of frequency bands for peak detection
        fanout: Maximum number of target peaks per anchor
        dt_min: Minimum time offset between anchor and target (in frames)
        dt_max_seconds: Maximum time offset between anchor and target (in seconds)

    Returns:
        List of fingerprints as (f1, f2, dt, t1) tuples where:
        - f1: anchor frequency bin
        - f2: target frequency bin
        - dt: time delta between anchor and target (frames)
        - t1: absolute time of anchor (frames)
    """
    hop_length = n_fft // hop_ratio

    # Compute STFT spectrogram
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    # Detect peaks using frequency-banded maximum filtering
    peaks = np.zeros_like(S_db, dtype=bool)
    freq_bins = S_db.shape[0]
    band_size = freq_bins // num_bands

    for b in range(num_bands):
        f_start = b * band_size
        f_end = freq_bins if b == num_bands - 1 else (b + 1) * band_size

        band = S_db[f_start:f_end, :]
        band_local_max = maximum_filter(
            band,
            size=(freq_neighborhood, time_neighborhood)
        )

        band_peaks = (band == band_local_max) & (band > amplitude_threshold)
        peaks[f_start:f_end, :] |= band_peaks

    # Extract peak coordinates
    freq_idx, time_idx = np.where(peaks)
    peak_list = list(zip(time_idx, freq_idx))
    peak_list.sort(key=lambda x: x[0])

    # Generate fingerprints using anchor-target fan-out
    dt_max = int(dt_max_seconds * sr / hop_length)
    fingerprints = []

    for i in range(len(peak_list)):
        t1, f1 = peak_list[i]
        count = 0

        for j in range(i + 1, len(peak_list)):
            t2, f2 = peak_list[j]
            dt = t2 - t1

            if dt < dt_min:
                continue
            if dt > dt_max:
                break

            fingerprints.append((f1, f2, dt, t1))
            count += 1

            if count >= fanout:
                break

    return fingerprints


def load_audio(audio_path: str, sr: int) -> Tuple[np.ndarray, int]:
    """
    Load audio file as mono signal at specified sampling rate.

    Args:
        audio_path: Path to audio file
        sr: Target sampling rate (will resample if necessary)

    Returns:
        Tuple of (audio_signal, sampling_rate)
    """
    y, sr_actual = librosa.load(audio_path, sr=sr, mono=True)
    return y, sr


def compute_snr_estimate(y: np.ndarray, n_fft: int = 2048, hop_length: int = 512) -> float:
    """
    Compute SNR estimate from audio signal.
    """
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    S_mean = np.mean(S, axis=1)

    # Estimate signal power as max mean spectral magnitude (or percentile)
    # and noise power as median (assuming noise is broadband/background)

    signal_power = np.max(S_mean)
    noise_power = np.median(S_mean)

    if noise_power == 0:
        return 100.0 # Clean

    snr = 10 * np.log10(signal_power / noise_power)
    return float(snr)


def analyze_peak_distribution(S_db: np.ndarray, peaks: np.ndarray) -> dict:
    """
    Analyze the distribution of spectral peaks.
    """
    peak_amplitudes = S_db[peaks]

    if len(peak_amplitudes) == 0:
        return {
            "total_peaks": 0,
            "mean_amplitude": 0.0,
            "std_amplitude": 0.0,
            "min_amplitude": 0.0,
            "max_amplitude": 0.0
        }

    return {
        "total_peaks": len(peak_amplitudes),
        "mean_amplitude": float(np.mean(peak_amplitudes)),
        "std_amplitude": float(np.std(peak_amplitudes)),
        "min_amplitude": float(np.min(peak_amplitudes)),
        "max_amplitude": float(np.max(peak_amplitudes))
    }


def extract_fingerprints_with_snr_info(
    y: np.ndarray,
    sr: int,
    n_fft: int,
    hop_ratio: int,
    freq_neighborhood: int,
    time_neighborhood: int,
    amplitude_threshold: float,
    num_bands: int,
    fanout: int,
    dt_min: int,
    dt_max_seconds: float,
) -> Tuple[List[Tuple[int, int, int, int]], float]:
    """
    Extract fingerprints and compute SNR.
    """
    fingerprints = extract_fingerprints(
        y, sr, n_fft, hop_ratio, freq_neighborhood,
        time_neighborhood, amplitude_threshold, num_bands,
        fanout, dt_min, dt_max_seconds
    )

    snr_db = compute_snr_estimate(y, n_fft=n_fft, hop_length=n_fft//hop_ratio)

    return fingerprints, snr_db_actual
