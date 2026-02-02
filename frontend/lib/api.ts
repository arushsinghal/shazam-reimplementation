import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Song {
  name: string;
  fingerprints_count: number;
  duration_seconds?: number;
}

export interface RecognitionResult {
  matched: boolean;
  song?: string;
  position_in_song?: string;
  confidence?: string;
  raw_score?: number;
  message?: string;
}

export interface AddSongResponse {
  success: boolean;
  song_name: string;
  fingerprints_count: number;
  message: string;
}

export const api = {
  // Add a new song to the database
  async addSong(songName: string, file: File): Promise<AddSongResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('song_name', songName);

    const response = await axios.post(`${API_BASE_URL}/api/songs/add`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      params: {
        song_name: songName,
      },
    });

    return response.data;
  },

  // Recognize a song from an audio clip
  async recognizeSong(file: File): Promise<RecognitionResult> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/api/songs/recognize`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  // Get list of all songs in the database
  async listSongs(): Promise<{ songs: Song[]; total_songs: number; total_hashes: number }> {
    const response = await axios.get(`${API_BASE_URL}/api/songs/list`);
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{ status: string; songs_count: number; hashes_count: number }> {
    const response = await axios.get(`${API_BASE_URL}/api/health`);
    return response.data;
  },
};
