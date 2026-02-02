"""
Configuration module for audio fingerprinting parameters.

These parameters control the fingerprinting algorithm's behavior.
DO NOT modify unless you understand their impact on recognition accuracy.
"""

# Default configuration matching the research notebook
DEFAULT_CONFIG = {
    # Audio processing
    "sr": 44100,                    # Target sampling rate (Hz)

    # STFT parameters
    "n_fft": 2048,                  # FFT window size (~46ms at 44.1kHz)
    "hop_ratio": 4,                 # Hop length = n_fft / hop_ratio (~11ms steps)

    # Peak detection
    "freq_neighborhood": 20,        # Frequency bins for local maximum filter
    "time_neighborhood": 20,        # Time frames for local maximum filter
    "amplitude_threshold": -35,     # Minimum peak amplitude in dB
    "num_bands": 6,                 # Number of frequency bands for peak distribution

    # Fingerprint generation
    "fanout": 10,                   # Maximum target peaks per anchor
    "dt_min": 2,                    # Minimum time delta between anchor and target (frames)
    "dt_max_seconds": 2.0,          # Maximum time delta (seconds)
}


def get_config():
    """Get a copy of the default configuration."""
    return DEFAULT_CONFIG.copy()


def validate_config(config: dict) -> bool:
    """
    Validate configuration parameters.

    Args:
        config: Configuration dictionary to validate

    Returns:
        True if valid, raises ValueError if invalid
    """
    required_keys = [
        "sr", "n_fft", "hop_ratio", "freq_neighborhood",
        "time_neighborhood", "amplitude_threshold", "num_bands",
        "fanout", "dt_min", "dt_max_seconds"
    ]

    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    # Validate ranges
    if config["sr"] <= 0:
        raise ValueError("sr must be positive")
    if config["n_fft"] <= 0 or config["n_fft"] & (config["n_fft"] - 1) != 0:
        raise ValueError("n_fft must be a positive power of 2")
    if config["hop_ratio"] <= 0:
        raise ValueError("hop_ratio must be positive")
    if config["num_bands"] <= 0:
        raise ValueError("num_bands must be positive")
    if config["fanout"] <= 0:
        raise ValueError("fanout must be positive")
    if config["dt_min"] < 0:
        raise ValueError("dt_min must be non-negative")
    if config["dt_max_seconds"] <= 0:
        raise ValueError("dt_max_seconds must be positive")

    return True
