import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { ArrowLeft, Upload, Loader, CheckCircle, AlertCircle, Music, Database } from 'lucide-react';
import { api } from '@/lib/api';

export default function AddSongs() {
  const [file, setFile] = useState<File | null>(null);
  const [songName, setSongName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string; count?: number } | null>(null);
  const [mounted, setMounted] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      if (!songName) {
        const filename = e.target.files[0].name;
        const nameWithoutExt = filename.replace(/\.[^/.]+$/, '');
        setSongName(nameWithoutExt);
      }
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type.startsWith('audio/')) {
        setFile(droppedFile);
        if (!songName) {
          const filename = droppedFile.name;
          const nameWithoutExt = filename.replace(/\.[^/.]+$/, '');
          setSongName(nameWithoutExt);
        }
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !songName) return;

    setUploading(true);
    setResult(null);

    try {
      const response = await api.addSong(songName, file);
      setResult({
        success: true,
        message: response.message,
        count: response.fingerprints_count,
      });
      setFile(null);
      setSongName('');
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (error: any) {
      setResult({
        success: false,
        message: error.response?.data?.detail || 'Failed to add song. Please try again.',
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <Head>
        <title>Add Songs - Shazam Clone</title>
      </Head>

      <main className="relative min-h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
        {/* Animated Background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-0 -left-4 w-96 h-96 bg-gray-700 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float"></div>
          <div className="absolute top-0 -right-4 w-96 h-96 bg-gray-600 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style={{ animationDelay: '2s' }}></div>
          <div className="absolute -bottom-8 left-1/2 w-96 h-96 bg-gray-700 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style={{ animationDelay: '4s' }}></div>

          {mounted && Array.from({ length: 15 }).map((_, i) => (
            <div
              key={i}
              className="particle absolute rounded-full bg-gray-400"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                width: `${Math.random() * 3 + 1}px`,
                height: `${Math.random() * 3 + 1}px`,
                animationDelay: `${Math.random() * 6}s`,
                animationDuration: `${Math.random() * 10 + 8}s`,
                opacity: 0.3,
              }}
            />
          ))}
        </div>

        <div className="relative z-10 container mx-auto px-4 py-8">
          {/* Back Button */}
          <Link href="/">
            <button className="flex items-center text-gray-300 hover:text-white transition-colors mb-8 glass rounded-full px-6 py-3 hover-lift group border border-gray-700">
              <ArrowLeft className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" />
              <span className="font-medium">Back to Home</span>
            </button>
          </Link>

          {/* Main Card */}
          <div className={`max-w-3xl mx-auto ${mounted ? 'animate-bounce-in' : 'opacity-0'}`}>
            <div className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-gray-600 to-gray-700 rounded-3xl blur opacity-30 group-hover:opacity-50 transition duration-500"></div>

              <div className="relative glass-dark rounded-3xl p-8 md:p-12 border border-gray-700">
                {/* Header */}
                <div className="text-center mb-10">
                  <div className="flex justify-center mb-6">
                    <div className="relative">
                      <div className="absolute inset-0 bg-gray-600 rounded-full blur-2xl opacity-40 animate-pulse"></div>
                      <div className="relative bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl p-5 animate-float border border-gray-600">
                        <Database className="w-12 h-12 text-gray-200" />
                      </div>
                    </div>
                  </div>
                  <h1 className="text-5xl font-black text-white mb-3">
                    Expand Your Library
                  </h1>
                  <p className="text-gray-400 text-lg">Build your personalized audio fingerprint database</p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Song Name Input */}
                  <div className={mounted ? 'animate-slide-up' : 'opacity-0'}>
                    <label htmlFor="song-name" className="block text-sm font-bold text-gray-300 mb-3 flex items-center gap-2">
                      <Music className="w-4 h-4" />
                      Song Name
                    </label>
                    <div className="relative">
                      <input
                        id="song-name"
                        type="text"
                        value={songName}
                        onChange={(e) => setSongName(e.target.value)}
                        className="w-full px-6 py-4 glass-dark text-white border-2 border-gray-700 rounded-2xl focus:border-gray-500 focus:outline-none transition-all placeholder-gray-500 font-medium"
                        placeholder="Enter song name..."
                        required
                      />
                    </div>
                  </div>

                  {/* File Upload */}
                  <div className={mounted ? 'animate-slide-up' : 'opacity-0'} style={{ animationDelay: '0.1s' }}>
                    <label htmlFor="file-input" className="block text-sm font-bold text-gray-300 mb-3 flex items-center gap-2">
                      <Upload className="w-4 h-4" />
                      Audio File
                    </label>
                    <div className="relative">
                      <input
                        id="file-input"
                        type="file"
                        onChange={handleFileChange}
                        accept="audio/*"
                        className="hidden"
                        required
                      />
                      <label
                        htmlFor="file-input"
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                        className={`relative flex items-center justify-center w-full px-6 py-12 border-2 border-dashed rounded-2xl cursor-pointer transition-all overflow-hidden ${
                          dragActive
                            ? 'border-gray-500 bg-gray-800/50 scale-105'
                            : 'border-gray-700 glass hover:border-gray-600 hover:bg-gray-800/30'
                        }`}
                      >
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-700/10 to-transparent animate-shimmer"></div>

                        <div className="relative text-center z-10">
                          <div className={`mx-auto mb-4 transition-transform ${dragActive ? 'scale-125' : ''}`}>
                            {file ? (
                              <CheckCircle className="w-16 h-16 text-green-400 mx-auto" />
                            ) : (
                              <div className="relative">
                                <div className="absolute inset-0 bg-gray-600 rounded-full blur-xl opacity-30"></div>
                                <Upload className="relative w-16 h-16 text-gray-400 mx-auto" />
                              </div>
                            )}
                          </div>
                          <p className="text-lg font-bold text-white mb-2">
                            {file ? file.name : dragActive ? 'Drop it here!' : 'Drop audio or click to upload'}
                          </p>
                          <p className="text-sm text-gray-500">
                            MP3, WAV, FLAC, or any audio format • Max 50MB
                          </p>
                        </div>
                      </label>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={!file || !songName || uploading}
                    className={`relative w-full py-5 rounded-2xl font-bold text-lg transition-all overflow-hidden group disabled:opacity-40 disabled:cursor-not-allowed ${mounted ? 'animate-slide-up' : 'opacity-0'}`}
                    style={{ animationDelay: '0.2s' }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-gray-700 to-gray-600 opacity-100 group-hover:opacity-90 transition-opacity"></div>
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-500/20 to-transparent animate-shimmer"></div>

                    <div className="relative flex items-center justify-center text-white">
                      {uploading ? (
                        <>
                          <Loader className="w-6 h-6 mr-3 animate-spin" />
                          <span>Processing Audio...</span>
                        </>
                      ) : (
                        <>
                          <Database className="w-6 h-6 mr-3" />
                          <span>Add to Database</span>
                        </>
                      )}
                    </div>
                  </button>
                </form>

                {/* Result Message */}
                {result && (
                  <div className={`mt-8 animate-bounce-in`}>
                    <div className={`glass rounded-2xl p-6 border-2 ${
                      result.success
                        ? 'border-green-600/50 bg-green-900/20'
                        : 'border-red-600/50 bg-red-900/20'
                    }`}>
                      <div className="flex items-start gap-4">
                        <div className={`flex-shrink-0 ${result.success ? 'text-green-400' : 'text-red-400'}`}>
                          {result.success ? (
                            <CheckCircle className="w-8 h-8 animate-bounce-in" />
                          ) : (
                            <AlertCircle className="w-8 h-8 animate-bounce-in" />
                          )}
                        </div>
                        <div className="flex-1">
                          <p className={`font-bold text-lg mb-1 ${result.success ? 'text-green-300' : 'text-red-300'}`}>
                            {result.success ? '✨ Success!' : '⚠️ Error'}
                          </p>
                          <p className={`text-sm mb-2 ${result.success ? 'text-green-200' : 'text-red-200'}`}>
                            {result.message}
                          </p>
                          {result.count && (
                            <div className="flex items-center gap-2 mt-3">
                              <div className="glass rounded-full px-4 py-2 border border-gray-700">
                                <p className="text-xs font-bold text-white">
                                  🎵 {result.count.toLocaleString()} Fingerprints Extracted
                                </p>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
