import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { ArrowLeft, Upload, Music, CheckCircle, XCircle, Clock, Radio } from 'lucide-react';
import { api, RecognitionResult } from '@/lib/api';

export default function Recognize() {
  const [file, setFile] = useState<File | null>(null);
  const [recognizing, setRecognizing] = useState(false);
  const [result, setResult] = useState<RecognitionResult | null>(null);
  const [mounted, setMounted] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
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
        setResult(null);
      }
    }
  };

  const handleRecognize = async () => {
    if (!file) return;

    setRecognizing(true);
    setResult(null);

    try {
      const response = await api.recognizeSong(file);
      setResult(response);
    } catch (error: any) {
      setResult({
        matched: false,
        message: error.response?.data?.detail || 'Failed to recognize audio. Please try again.',
      });
    } finally {
      setRecognizing(false);
    }
  };

  const getConfidenceColor = (confidence?: string) => {
    if (!confidence) return { bg: 'bg-gray-600', text: 'text-gray-100', glow: 'rgba(156, 163, 175, 0.5)' };
    if (confidence === 'High confidence') return { bg: 'bg-green-600', text: 'text-white', glow: 'rgba(34, 197, 94, 0.6)' };
    if (confidence === 'Medium confidence') return { bg: 'bg-yellow-600', text: 'text-white', glow: 'rgba(234, 179, 8, 0.6)' };
    if (confidence === 'Low confidence') return { bg: 'bg-orange-600', text: 'text-white', glow: 'rgba(249, 115, 22, 0.6)' };
    return { bg: 'bg-gray-600', text: 'text-gray-100', glow: 'rgba(156, 163, 175, 0.5)' };
  };

  return (
    <div>
      <Head>
        <title>Recognize Music - Shazam Clone</title>
      </Head>

      <main className="relative min-h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
        {/* Animated Background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-0 -left-4 w-96 h-96 bg-gray-700 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float"></div>
          <div className="absolute top-0 -right-4 w-96 h-96 bg-gray-600 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style={{ animationDelay: '2s' }}></div>
          <div className="absolute -bottom-8 left-1/2 w-96 h-96 bg-gray-700 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style={{ animationDelay: '4s' }}></div>

          {mounted && Array.from({ length: 20 }).map((_, i) => (
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
                        <Radio className="w-12 h-12 text-gray-200" />
                      </div>
                    </div>
                  </div>
                  <h1 className="text-5xl font-black text-white mb-3">
                    Identify Any Track
                  </h1>
                  <p className="text-gray-400 text-lg">Analyze and recognize your audio instantly</p>
                </div>

                {/* Upload Section */}
                {!recognizing && !result && (
                  <div className="space-y-6">
                    <div className={mounted ? 'animate-slide-up' : 'opacity-0'}>
                      <input
                        id="file-input"
                        type="file"
                        onChange={handleFileChange}
                        accept="audio/*"
                        className="hidden"
                      />
                      <label
                        htmlFor="file-input"
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                        className={`relative flex items-center justify-center w-full px-6 py-16 border-2 border-dashed rounded-2xl cursor-pointer transition-all overflow-hidden ${
                          dragActive
                            ? 'border-gray-500 bg-gray-800/50 scale-105'
                            : 'border-gray-700 glass hover:border-gray-600 hover:bg-gray-800/30'
                        }`}
                      >
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-700/10 to-transparent animate-shimmer"></div>

                        <div className="relative text-center z-10">
                          <div className={`mx-auto mb-6 transition-transform ${dragActive ? 'scale-125' : ''}`}>
                            {file ? (
                              <CheckCircle className="w-20 h-20 text-green-400 mx-auto animate-bounce-in" />
                            ) : (
                              <div className="relative">
                                <div className="absolute inset-0 bg-gray-600 rounded-full blur-xl opacity-30 animate-pulse"></div>
                                <Upload className="relative w-20 h-20 text-gray-400 mx-auto" />
                              </div>
                            )}
                          </div>
                          <p className="text-2xl font-bold text-white mb-3">
                            {file ? file.name : dragActive ? 'Drop it here!' : 'Drop audio or click to upload'}
                          </p>
                          <p className="text-sm text-gray-500 mb-2">
                            5-10 second clips work best
                          </p>
                          <p className="text-xs text-gray-600">
                            MP3, WAV, FLAC, M4A, or any audio format
                          </p>
                        </div>
                      </label>
                    </div>

                    <button
                      onClick={handleRecognize}
                      disabled={!file}
                      className={`relative w-full py-5 rounded-2xl font-bold text-lg transition-all overflow-hidden group disabled:opacity-40 disabled:cursor-not-allowed ${mounted ? 'animate-slide-up' : 'opacity-0'}`}
                      style={{ animationDelay: '0.1s' }}
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-gray-700 to-gray-600 opacity-100 group-hover:opacity-90 transition-opacity"></div>
                      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-500/20 to-transparent animate-shimmer"></div>

                      <div className="relative flex items-center justify-center text-white">
                        <Music className="w-6 h-6 mr-3" />
                        <span>Identify Song</span>
                      </div>
                    </button>
                  </div>
                )}

                {/* Recognizing State */}
                {recognizing && (
                  <div className="text-center py-16 animate-bounce-in">
                    <div className="flex justify-center mb-8">
                      <div className="relative">
                        <div className="absolute inset-0 bg-gray-600 rounded-full animate-pulse-ring opacity-30"></div>
                        <div className="absolute inset-0 bg-gray-600 rounded-full animate-pulse-ring opacity-20" style={{ animationDelay: '0.5s' }}></div>

                        <div className="relative bg-gradient-to-br from-gray-700 to-gray-800 rounded-full p-8 border border-gray-600">
                          <Music className="w-16 h-16 text-gray-200 animate-float" />
                        </div>
                      </div>
                    </div>

                    <h3 className="text-3xl font-black text-white mb-3">
                      Listening...
                    </h3>
                    <p className="text-gray-400 text-lg mb-8">Analyzing spectral fingerprint</p>

                    {/* Animated Sound Waves */}
                    <div className="flex justify-center gap-3">
                      {[0, 1, 2, 3, 4, 5, 6].map((i) => (
                        <div
                          key={i}
                          className="w-2 bg-gradient-to-t from-gray-600 to-gray-400 rounded-full animate-wave"
                          style={{
                            height: `${40 + Math.random() * 20}px`,
                            animationDelay: `${i * 0.12}s`,
                          }}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Result */}
                {result && !recognizing && (
                  <div className="space-y-6 animate-bounce-in">
                    {result.matched ? (
                      <div className="text-center py-10">
                        <div className="flex justify-center mb-8">
                          <div className="relative">
                            <div className="absolute inset-0 bg-green-600 rounded-full blur-3xl opacity-40 animate-pulse"></div>
                            <div className="relative bg-gradient-to-br from-green-700 to-green-800 rounded-full p-8 border border-green-600">
                              <CheckCircle className="w-20 h-20 text-white" />
                            </div>
                          </div>
                        </div>

                        <div className="mb-6">
                          <div className="inline-block glass rounded-2xl px-4 py-2 mb-4 border border-gray-700">
                            <p className="text-sm font-bold text-green-400">✨ MATCH FOUND</p>
                          </div>
                        </div>

                        <h3 className="text-4xl font-black text-white mb-6 leading-tight">
                          {result.song}
                        </h3>

                        <div className="space-y-4">
                          {result.position_in_song && (
                            <div className="inline-flex items-center gap-3 glass rounded-full px-6 py-3 border border-gray-700">
                              <Clock className="w-5 h-5 text-gray-400" />
                              <span className="text-white font-semibold">Position: {result.position_in_song}</span>
                            </div>
                          )}

                          {result.confidence && (
                            <div className="flex justify-center">
                              <div
                                className={`${getConfidenceColor(result.confidence).bg} rounded-full px-8 py-3 font-bold text-lg shadow-lg`}
                                style={{
                                  boxShadow: `0 0 30px ${getConfidenceColor(result.confidence).glow}`
                                }}
                              >
                                {result.confidence}
                              </div>
                            </div>
                          )}

                          {result.raw_score && (
                            <div className="glass rounded-2xl px-6 py-3 inline-block border border-gray-700">
                              <p className="text-sm text-gray-400">
                                Match Score: <span className="font-bold text-white">{result.raw_score.toLocaleString()}</span>
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    ) : (
                      <div className="text-center py-10">
                        <div className="flex justify-center mb-8">
                          <div className="relative">
                            <div className="absolute inset-0 bg-red-600 rounded-full blur-3xl opacity-40 animate-pulse"></div>
                            <div className="relative bg-gradient-to-br from-red-700 to-red-800 rounded-full p-8 border border-red-600">
                              <XCircle className="w-20 h-20 text-white" />
                            </div>
                          </div>
                        </div>

                        <h3 className="text-3xl font-black text-white mb-4">No Match Found</h3>
                        <p className="text-gray-400 text-lg mb-3">
                          {result.message || 'Could not identify this song'}
                        </p>
                        <p className="text-sm text-gray-500">
                          Try uploading a longer clip or ensure the song is in the database
                        </p>
                      </div>
                    )}

                    {/* Try Again Button */}
                    <button
                      onClick={() => {
                        setFile(null);
                        setResult(null);
                        const fileInput = document.getElementById('file-input') as HTMLInputElement;
                        if (fileInput) fileInput.value = '';
                      }}
                      className="relative w-full py-5 rounded-2xl font-bold text-lg transition-all overflow-hidden group"
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-gray-700 to-gray-600 opacity-100 group-hover:opacity-90 transition-opacity"></div>
                      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-500/20 to-transparent animate-shimmer"></div>

                      <div className="relative flex items-center justify-center text-white">
                        <Music className="w-6 h-6 mr-3" />
                        <span>Try Another Song</span>
                      </div>
                    </button>
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
