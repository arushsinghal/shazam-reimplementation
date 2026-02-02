#!/usr/bin/env python3
import sys
import os
import argparse
import json
import numpy as np
import librosa
import soundfile as sf
import tempfile
from datetime import datetime
from tqdm import tqdm

# Add backend to path to import helpers
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from research_helpers import (
        generate_noise_profile,
        add_noise_at_snr,
        simulate_codec_degradation,
        simulate_microphone_degradation
    )
    from service import get_service
    from config import DEFAULT_CONFIG
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you are running this script from the project root.")
    sys.exit(1)

class ResearchExperimentRunner:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.service = get_service()
        self.results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "config": DEFAULT_CONFIG
            },
            "experiments": {
                "noise": {},
                "codecs": {},
                "microphone": {}
            }
        }

    def _evaluate_audio(self, audio_data: np.ndarray, sr: int) -> dict:
        """Helper to run recognition on audio data buffer."""
        # Service expects a file path
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, audio_data, sr)
            tmp_name = tmp.name

        try:
            result = self.service.recognize_audio(tmp_name)
            # Normalize result
            return {
                "matched": result.get("matched", False) and result.get("song_name") is not None,
                "score": result.get("score", 0.0),
                "detected_song": result.get("song_name")
            }
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    def run_noise_robustness_test(self, audio_path: str, num_clips: int = 3):
        print("\n=== Running Noise Robustness Tests ===")
        y, sr = librosa.load(audio_path, sr=DEFAULT_CONFIG["sr"])

        noise_types = ["white", "pink", "cafe", "street", "club"]
        snr_levels = [20, 15, 10, 5, 0]

        for noise_type in tqdm(noise_types, desc="Noise Types"):
            self.results["experiments"]["noise"][noise_type] = {}
            noise_profile = generate_noise_profile(noise_type, len(y))

            for snr in snr_levels:
                # Run multiple clips if audio is long enough, else just 1
                # For simplicity here, we test the full song (or truncated) once
                # effectively acting as 1 large clip, or we could slice it.
                # The prompt asks to extract 3 clips.

                clip_results = []
                clip_len = 10 * sr # 10 seconds

                starts = np.linspace(0, len(y) - clip_len, num_clips + 2)[1:-1]
                if len(y) < clip_len:
                    starts = [0]

                for start in starts:
                    start_idx = int(start)
                    y_clip = y[start_idx : start_idx + int(clip_len)]
                    if len(y_clip) < clip_len and len(y) > clip_len: continue

                    # Generate fresh noise for this clip segment to ensure randomness
                    # Or slice the large profile
                    noise_clip = noise_profile[start_idx : start_idx + len(y_clip)]

                    noisy_clip = add_noise_at_snr(y_clip, noise_clip, snr)

                    res = self._evaluate_audio(noisy_clip, sr)
                    clip_results.append(res)

                # Aggregate
                matches = [r["matched"] for r in clip_results]
                accuracy = sum(matches) / len(matches) if matches else 0
                avg_score = np.mean([r["score"] for r in clip_results]) if matches else 0

                self.results["experiments"]["noise"][noise_type][f"snr_{snr}_db"] = {
                    "accuracy": accuracy,
                    "avg_score": float(avg_score),
                    "num_tests": len(matches)
                }

    def run_codec_robustness_test(self, audio_path: str):
        print("\n=== Running Codec Robustness Tests ===")
        y, sr = librosa.load(audio_path, sr=DEFAULT_CONFIG["sr"])

        codecs = [
            ("mp3", 320), ("mp3", 128), ("mp3", 64),
            ("aac", 256), ("opus", 96), ("opus", 32),
            ("original", 0)
        ]

        for codec, bitrate in tqdm(codecs, desc="Codecs"):
            # Same clip extraction logic
            clip_results = []
            clip_len = 10 * sr
            starts = np.linspace(0, len(y) - clip_len, 3 + 2)[1:-1]
            if len(y) < clip_len: starts = [0]

            for start in starts:
                start_idx = int(start)
                y_clip = y[start_idx : start_idx + int(clip_len)]
                if len(y_clip) == 0: continue

                processed = simulate_codec_degradation(y_clip, codec, bitrate)
                res = self._evaluate_audio(processed, sr)
                clip_results.append(res)

            matches = [r["matched"] for r in clip_results]
            accuracy = sum(matches) / len(matches) if matches else 0
            avg_score = np.mean([r["score"] for r in clip_results]) if matches else 0

            key = f"{codec}_{bitrate}kbps" if codec != "original" else "original"
            self.results["experiments"]["codecs"][key] = {
                "accuracy": accuracy,
                "avg_score": float(avg_score)
            }

    def run_microphone_robustness_test(self, audio_path: str):
        print("\n=== Running Microphone Robustness Tests ===")
        y, sr = librosa.load(audio_path, sr=DEFAULT_CONFIG["sr"])

        mics = ["iphone", "android", "laptop", "headset", "loud_env", "studio"]

        for mic in tqdm(mics, desc="Microphones"):
            clip_results = []
            clip_len = 10 * sr
            starts = np.linspace(0, len(y) - clip_len, 3 + 2)[1:-1]
            if len(y) < clip_len: starts = [0]

            for start in starts:
                start_idx = int(start)
                y_clip = y[start_idx : start_idx + int(clip_len)]
                if len(y_clip) == 0: continue

                processed = simulate_microphone_degradation(y_clip, mic)
                res = self._evaluate_audio(processed, sr)
                clip_results.append(res)

            matches = [r["matched"] for r in clip_results]
            accuracy = sum(matches) / len(matches) if matches else 0
            avg_score = np.mean([r["score"] for r in clip_results]) if matches else 0

            self.results["experiments"]["microphone"][mic] = {
                "accuracy": accuracy,
                "avg_score": float(avg_score)
            }

    def save_results(self):
        with open(self.output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {self.output_path}")

def main():
    parser = argparse.ArgumentParser(description="Run Audio Fingerprinting Robustness Experiments")
    parser.add_argument("--audio", required=True, help="Path to source audio file to test")
    parser.add_argument("--output", default="research_results.json", help="Path to save JSON results")

    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"Error: Audio file {args.audio} not found.")
        sys.exit(1)

    runner = ResearchExperimentRunner(args.output)

    try:
        runner.run_noise_robustness_test(args.audio)
        runner.run_codec_robustness_test(args.audio)
        runner.run_microphone_robustness_test(args.audio)
        runner.save_results()
    except KeyboardInterrupt:
        print("\nTests interrupted.")
        runner.save_results()
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
