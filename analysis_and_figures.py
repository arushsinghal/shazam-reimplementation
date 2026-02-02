import json
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def load_results(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def generate_noise_heatmap(data, output_path="figure1_noise_heatmap.png"):
    print("Generating Figure 1: Noise Robustness Heatmap...")
    noise_data = data["experiments"]["noise"]

    # Structure: noise_type -> snr_X_db -> accuracy
    rows = []

    # sort SNRs: 20, 15, 10, 5, 0
    snrs = [20, 15, 10, 5, 0]
    noise_types = list(noise_data.keys())

    matrix = []
    for nt in noise_types:
        row = []
        for snr in snrs:
            key = f"snr_{snr}_db"
            acc = noise_data[nt].get(key, {}).get("accuracy", 0)
            row.append(acc * 100) # Percentage
        matrix.append(row)

    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_style("whitegrid")

    ax = sns.heatmap(matrix, annot=True, fmt=".1f", cmap="RdYlGn",
                     xticklabels=[f"{s} dB" for s in snrs],
                     yticklabels=[n.capitalize() for n in noise_types],
                     vmin=0, vmax=100)

    plt.title("Audio Fingerprinting Accuracy vs Environmental Noise", fontsize=14, pad=20)
    plt.xlabel("Signal-to-Noise Ratio (SNR)", fontsize=12)
    plt.ylabel("Noise Environment", fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_codec_barchart(data, output_path="figure2_codec_robustness.png"):
    print("Generating Figure 2: Codec Degradation Bar Chart...")
    codec_data = data["experiments"]["codecs"]

    # Flatten to list
    items = []
    for k, v in codec_data.items():
        items.append({"Codec": k, "Accuracy": v["accuracy"] * 100})

    df = pd.DataFrame(items)

    # Sort roughly by strictness or just alpha
    # Order: Original, MP3 320, AAC 256, MP3 128, Opus 96, Opus 32
    order = ["original", "mp3_320kbps", "aac_256kbps", "mp3_128kbps", "opus_96kbps", "opus_32kbps"]
    # Filter only those present and sort
    df['sort_cat'] = pd.Categorical(df['Codec'], categories=order, ordered=True)
    df = df.sort_values('sort_cat')

    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_style("whitegrid")

    # Define colors based on accuracy
    colors = ['green' if x >= 95 else 'orange' if x >= 80 else 'red' for x in df['Accuracy']]

    ax = sns.barplot(x="Codec", y="Accuracy", data=df, palette=colors)

    plt.title("Audio Fingerprinting Robustness to Codec Compression", fontsize=14, pad=20)
    plt.ylabel("Accuracy (%)", fontsize=12)
    plt.xlabel("Codec Configuration", fontsize=12)
    plt.ylim(0, 105)

    # Add value labels
    for i, v in enumerate(df['Accuracy']):
        ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontweight='bold')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_summary_chart(data, output_path="figure3_summary.png"):
    print("Generating Figure 3: Summary Comparison...")

    # Extract specific conditions for summary
    conditions = []

    # 1. Clean (using original codec or high SNR white noise as proxy?)
    # Usually "original" from codecs is the baseline
    clean_acc = data["experiments"]["codecs"].get("original", {}).get("accuracy", 0) * 100
    conditions.append({"Condition": "Clean (Baseline)", "Accuracy": clean_acc})

    # 2. Cafe 10dB
    cafe_acc = data["experiments"]["noise"].get("cafe", {}).get("snr_10_db", {}).get("accuracy", 0) * 100
    conditions.append({"Condition": "Café Env (10dB SNR)", "Accuracy": cafe_acc})

    # 3. Street 10dB
    street_acc = data["experiments"]["noise"].get("street", {}).get("snr_10_db", {}).get("accuracy", 0) * 100
    conditions.append({"Condition": "Street Traffic (10dB SNR)", "Accuracy": street_acc})

    # 4. Club 10dB
    club_acc = data["experiments"]["noise"].get("club", {}).get("snr_10_db", {}).get("accuracy", 0) * 100
    conditions.append({"Condition": "Nightclub (10dB SNR)", "Accuracy": club_acc})

    # 5. MP3 128k
    mp3_acc = data["experiments"]["codecs"].get("mp3_128kbps", {}).get("accuracy", 0) * 100
    conditions.append({"Condition": "MP3 Compression (128kbps)", "Accuracy": mp3_acc})

    # 6. Opus 32k
    opus_acc = data["experiments"]["codecs"].get("opus_32kbps", {}).get("accuracy", 0) * 100
    conditions.append({"Condition": "Opus Low-Bitrate (32kbps)", "Accuracy": opus_acc})

    # 7. iPhone Mic
    mic_acc = data["experiments"]["microphone"].get("iphone", {}).get("accuracy", 0) * 100
    conditions.append({"Condition": "iPhone Microphone Sim", "Accuracy": mic_acc})

    df = pd.DataFrame(conditions)
    df = df.sort_values("Accuracy", ascending=True)

    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_style("whitegrid")

    norm = plt.Normalize(0, 100)
    colors = plt.cm.RdYlGn(norm(df["Accuracy"].values))

    ax = sns.barplot(x="Accuracy", y="Condition", data=df, palette=list(colors))

    plt.title("Audio Fingerprinting Robustness: Comprehensive Summary", fontsize=14, pad=20)
    plt.xlabel("Accuracy (%)", fontsize=12)
    plt.xlim(0, 105)

    # Add labels
    for i, v in enumerate(df['Accuracy']):
        ax.text(v + 1, i, f"{v:.1f}%", va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Generate Figures from Research Results")
    parser.add_argument("--input", default="research_results.json", help="Path to input JSON results")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Results file {args.input} not found.")
        return

    data = load_results(args.input)

    try:
        generate_noise_heatmap(data)
        generate_codec_barchart(data)
        generate_summary_chart(data)
        print("\nAll figures generated successfully.")
    except Exception as e:
        print(f"Error generating figures: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
