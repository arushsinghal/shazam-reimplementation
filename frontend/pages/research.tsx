import React, { useState } from 'react';
import Head from 'next/head';
import {
  Upload,
  Activity,
  Mic,
  FileAudio,
  Music,
  Play,
  CheckCircle,
  XCircle,
  Database
} from 'lucide-react';

export default function Research() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [activeTab, setActiveTab] = useState<'noise' | 'codec' | 'mic'>('noise');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Noise Parameters
  const [noiseType, setNoiseType] = useState('white');
  const [snrDb, setSnrDb] = useState(10);

  // Codec Parameters
  const [codec, setCodec] = useState('mp3');
  const [bitrate, setBitrate] = useState(128);

  // Mic Parameters
  const [micType, setMicType] = useState('iphone');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const runTest = async () => {
    if (!selectedFile) {
      setError("Please select an audio file first.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    let endpoint = '';

    if (activeTab === 'noise') {
      endpoint = 'http://localhost:8000/api/research/test-noise';
      formData.append('noise_type', noiseType);
      formData.append('snr_db', snrDb.toString());
    } else if (activeTab === 'codec') {
      endpoint = 'http://localhost:8000/api/research/test-codec';
      formData.append('codec', codec);
      formData.append('bitrate', bitrate.toString());
    } else {
      endpoint = 'http://localhost:8000/api/research/test-microphone';
      formData.append('mic_type', micType);
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Test failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An error occurred during testing");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans selection:bg-purple-900 selection:text-white">
      <Head>
        <title>Research & Robustness | Shazam Clone</title>
      </Head>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <header className="mb-10 text-center">
          <div className="inline-flex items-center justify-center p-3 bg-gray-800 rounded-full mb-4 ring-1 ring-gray-700">
            <Activity className="w-8 h-8 text-purple-400" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-white mb-2">
            Robustness Research Testing
          </h1>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Test audio fingerprinting accuracy under simulated real-world conditions including environmental noise, compression artifacts, and microphone degradation.
          </p>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">

          {/* Left Column: Configuration */}
          <div className="lg:col-span-1 space-y-6">

            {/* File Upload */}
            <div className="bg-gray-800 rounded-xl p-6 ring-1 ring-gray-700 shadow-xl">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FileAudio className="w-5 h-5 text-purple-400" />
                Input Source
              </h2>

              <div className="relative group cursor-pointer">
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept="audio/*"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className={`
                  border-2 border-dashed rounded-lg p-6 text-center transition-all duration-300
                  ${selectedFile ? 'border-green-500 bg-green-900/10' : 'border-gray-600 hover:border-purple-500 hover:bg-gray-700/50'}
                `}>
                  {selectedFile ? (
                    <div>
                      <Music className="w-8 h-8 text-green-400 mx-auto mb-2" />
                      <p className="text-sm font-medium text-green-300 truncate">
                        {selectedFile.name}
                      </p>
                      <p className="text-xs text-green-500 mt-1">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  ) : (
                    <div>
                      <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2 group-hover:text-purple-400 transition-colors" />
                      <p className="text-sm font-medium text-gray-300">
                        Click to upload audio
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        MP3, WAV, M4A supported
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Test Configuration */}
            <div className="bg-gray-800 rounded-xl overflow-hidden ring-1 ring-gray-700 shadow-xl">
              <div className="flex border-b border-gray-700">
                <button
                  onClick={() => setActiveTab('noise')}
                  className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'noise' ? 'bg-purple-900/30 text-purple-300 border-b-2 border-purple-500' : 'text-gray-400 hover:bg-gray-700'}`}
                >
                  Noise
                </button>
                <button
                  onClick={() => setActiveTab('codec')}
                  className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'codec' ? 'bg-purple-900/30 text-purple-300 border-b-2 border-purple-500' : 'text-gray-400 hover:bg-gray-700'}`}
                >
                  Codec
                </button>
                <button
                  onClick={() => setActiveTab('mic')}
                  className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'mic' ? 'bg-purple-900/30 text-purple-300 border-b-2 border-purple-500' : 'text-gray-400 hover:bg-gray-700'}`}
                >
                  Mic
                </button>
              </div>

              <div className="p-6 space-y-4">
                {activeTab === 'noise' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-1">Noise Environment</label>
                      <select
                        value={noiseType}
                        onChange={(e) => setNoiseType(e.target.value)}
                        className="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="white">White Noise (Gaussian)</option>
                        <option value="pink">Pink Noise (1/f)</option>
                        <option value="cafe">Café Environment</option>
                        <option value="street">Street Traffic</option>
                        <option value="club">Nightclub (Bass Heavy)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-1">
                        Signal-to-Noise Ratio: <span className="text-white">{snrDb} dB</span>
                      </label>
                      <input
                        type="range"
                        min="0"
                        max="30"
                        step="5"
                        value={snrDb}
                        onChange={(e) => setSnrDb(parseInt(e.target.value))}
                        className="w-full accent-purple-500 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                      />
                      <div className="flex justify-between text-xs text-gray-500 mt-1">
                        <span>Noisy (0dB)</span>
                        <span>Clean (30dB)</span>
                      </div>
                    </div>
                  </>
                )}

                {activeTab === 'codec' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-1">Diff Codec</label>
                      <select
                        value={codec}
                        onChange={(e) => setCodec(e.target.value)}
                        className="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="mp3">MP3</option>
                        <option value="aac">AAC</option>
                        <option value="opus">Opus</option>
                        <option value="flac">FLAC (Lossless)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-1">
                        Bitrate: <span className="text-white">{bitrate} kbps</span>
                      </label>
                      <input
                        type="range"
                        min="32"
                        max="320"
                        step="32"
                        value={bitrate}
                        onChange={(e) => setBitrate(parseInt(e.target.value))}
                        className="w-full accent-purple-500 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                  </>
                )}

                {activeTab === 'mic' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-1">Microphone Type</label>
                      <select
                        value={micType}
                        onChange={(e) => setMicType(e.target.value)}
                        className="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="iphone">iPhone Field Record</option>
                        <option value="android">Generic Android Mic</option>
                        <option value="laptop">Laptop Webinar Mic</option>
                        <option value="headset">Bluetooth Headset</option>
                        <option value="loud_env">Loud Environment (Clipping)</option>
                        <option value="studio">Studio Condenser</option>
                      </select>
                    </div>
                  </>
                )}

                <button
                  onClick={runTest}
                  disabled={loading || !selectedFile}
                  className={`
                    w-full py-3 px-4 rounded-lg font-bold flex items-center justify-center gap-2 transition-all
                    ${loading || !selectedFile
                      ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                      : 'bg-purple-600 hover:bg-purple-500 text-white shadow-lg shadow-purple-900/50'}
                  `}
                >
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Play className="w-5 h-5 fill-current" />
                      Run Experiment
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: Results */}
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Database className="w-5 h-5 text-purple-400" />
              Experiment Results
            </h2>

            {result ? (
              <div className="bg-gray-800 rounded-xl p-8 ring-1 ring-gray-700 shadow-xl animate-in fade-in slide-in-from-bottom-4">
                <div className="flex items-center justify-between mb-8">
                  <div>
                    <h3 className="text-2xl font-bold text-white mb-1">
                      {result.matched ? "Successful Identification" : "Identification Failed"}
                    </h3>
                    <p className="text-gray-400">
                      Score: <span className="text-white font-mono">{result.score.toFixed(2)}</span>
                    </p>
                    {result.detected_song && (
                       <p className="text-purple-400 mt-1">
                         Detected: <span className="font-semibold">{result.detected_song}</span>
                       </p>
                    )}
                  </div>
                  <div className={`p-4 rounded-full ${result.matched ? 'bg-green-900/30 ring-1 ring-green-500' : 'bg-red-900/30 ring-1 ring-red-500'}`}>
                    {result.matched ? (
                      <CheckCircle className="w-12 h-12 text-green-500" />
                    ) : (
                      <XCircle className="w-12 h-12 text-red-500" />
                    )}
                  </div>
                </div>

                <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-700">
                  <h4 className="text-sm font-uppercase text-gray-500 font-bold tracking-wider mb-4">TEST PARAMETERS</h4>
                  <div className="grid grid-cols-2 gap-4">
                    {result.noise_type && (
                      <div className="bg-gray-800 p-3 rounded border border-gray-700">
                        <span className="text-gray-400 text-xs block">Noise Type</span>
                        <span className="text-white capitalize">{result.noise_type}</span>
                      </div>
                    )}
                    {result.snr_db !== undefined && (
                      <div className="bg-gray-800 p-3 rounded border border-gray-700">
                        <span className="text-gray-400 text-xs block">SNR</span>
                        <span className={`font-bold ${
                          result.snr_db < 5 ? 'text-red-400' :
                          result.snr_db < 15 ? 'text-yellow-400' : 'text-green-400'
                        }`}>
                          {result.snr_db} dB
                        </span>
                      </div>
                    )}
                    {result.codec && (
                      <div className="bg-gray-800 p-3 rounded border border-gray-700">
                        <span className="text-gray-400 text-xs block">Codec</span>
                        <span className="text-white uppercase">{result.codec}</span>
                      </div>
                    )}
                    {result.bitrate && (
                      <div className="bg-gray-800 p-3 rounded border border-gray-700">
                        <span className="text-gray-400 text-xs block">Bitrate</span>
                        <span className="text-white">{result.bitrate} kbps</span>
                      </div>
                    )}
                     {result.microphone && (
                      <div className="bg-gray-800 p-3 rounded border border-gray-700">
                        <span className="text-gray-400 text-xs block">Microphone</span>
                        <span className="text-white capitalize">{result.microphone}</span>
                      </div>
                    )}
                    <div className="bg-gray-800 p-3 rounded border border-gray-700">
                      <span className="text-gray-400 text-xs block">Timestamp</span>
                      <span className="text-gray-300 text-sm">
                        {new Date().toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-6 text-center">
                   <p className="text-gray-500 text-sm mb-4">
                     This result contributes to the "Noise Robustness Analysis" study.
                   </p>
                </div>
              </div>
            ) : (
              <div className="bg-gray-800/50 rounded-xl p-12 ring-1 ring-gray-700 border-dashed border-2 border-gray-700 flex flex-col items-center justify-center text-center h-full min-h-[400px]">
                <Activity className="w-16 h-16 text-gray-700 mb-4" />
                <h3 className="text-xl font-medium text-gray-400">Ready to Test</h3>
                <p className="text-gray-500 max-w-sm mt-2">
                  Configure your experiment parameters on the left and upload an audio file to begin robustness testing.
                </p>
              </div>
            )}

            {/* Error Message */}
            {error && (
               <div className="bg-red-900/20 border border-red-800 text-red-200 p-4 rounded-lg flex items-center gap-3">
                 <XCircle className="w-5 h-5 flex-shrink-0" />
                 <p>{error}</p>
               </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
