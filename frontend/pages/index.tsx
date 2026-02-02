import { useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { Music, Plus, Search, Zap, Shield, Waves } from 'lucide-react';

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div>
      <Head>
        <title>Shazam Clone - Audio Recognition</title>
        <meta name="description" content="Recognize music using audio fingerprinting" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
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

        <div className="relative z-10 container mx-auto px-4 py-12 md:py-20">
          {/* Header */}
          <div className={`text-center mb-16 md:mb-24 ${mounted ? 'animate-slide-up' : 'opacity-0'}`}>
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="absolute inset-0 rounded-full bg-gray-700 animate-pulse-ring opacity-20"></div>
                <div className="relative glass rounded-full p-8">
                  <Waves className="w-20 h-20 text-gray-200 animate-float" />
                </div>
              </div>
            </div>

            <h1 className="text-6xl md:text-8xl font-black mb-6 text-white">
              SoundWave
            </h1>
            <p className="text-2xl md:text-3xl text-gray-300 max-w-3xl mx-auto font-light mb-4 leading-relaxed">
              Audio Recognition Powered by
              <span className="font-bold text-gray-100"> Advanced DSP</span>
            </p>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Professional-grade spectral fingerprinting technology
            </p>
          </div>

          {/* Action Cards */}
          <div className={`grid md:grid-cols-2 gap-8 max-w-5xl mx-auto mb-20 ${mounted ? 'animate-bounce-in' : 'opacity-0'}`} style={{ animationDelay: '0.2s' }}>
            {/* Recognize Music Card */}
            <Link href="/recognize">
              <div className="relative group cursor-pointer">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-gray-600 to-gray-700 rounded-3xl blur opacity-30 group-hover:opacity-50 transition duration-500"></div>

                <div className="relative glass-dark rounded-3xl p-10 hover-lift overflow-hidden border border-gray-700">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-700/20 to-transparent animate-shimmer"></div>

                  <div className="relative z-10">
                    <div className="flex justify-center mb-8">
                      <div className="relative">
                        <div className="absolute inset-0 bg-gray-600 rounded-full blur-xl opacity-50 group-hover:opacity-75 transition-opacity"></div>
                        <div className="relative bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl p-6 transform group-hover:scale-110 transition-all duration-300 border border-gray-600">
                          <Search className="w-14 h-14 text-gray-200" />
                        </div>
                      </div>
                    </div>

                    <h2 className="text-4xl font-bold text-white mb-4 text-center group-hover:scale-105 transition-transform">
                      Recognize Music
                    </h2>
                    <p className="text-gray-300 text-center text-lg mb-6 leading-relaxed">
                      Upload audio clips and identify tracks instantly with precision fingerprinting
                    </p>

                    <div className="flex items-center justify-center gap-2 text-gray-400 font-semibold group-hover:gap-4 transition-all">
                      <span>Start Listening</span>
                      <span>→</span>
                    </div>
                  </div>
                </div>
              </div>
            </Link>

            {/* Add Songs Card */}
            <Link href="/add-songs">
              <div className="relative group cursor-pointer">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-gray-700 to-gray-600 rounded-3xl blur opacity-30 group-hover:opacity-50 transition duration-500"></div>

                <div className="relative glass-dark rounded-3xl p-10 hover-lift overflow-hidden border border-gray-700">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-700/20 to-transparent animate-shimmer"></div>

                  <div className="relative z-10">
                    <div className="flex justify-center mb-8">
                      <div className="relative">
                        <div className="absolute inset-0 bg-gray-600 rounded-full blur-xl opacity-50 group-hover:opacity-75 transition-opacity"></div>
                        <div className="relative bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl p-6 transform group-hover:scale-110 transition-all duration-300 border border-gray-600">
                          <Plus className="w-14 h-14 text-gray-200" />
                        </div>
                      </div>
                    </div>

                    <h2 className="text-4xl font-bold text-white mb-4 text-center group-hover:scale-105 transition-transform">
                      Add Songs
                    </h2>
                    <p className="text-gray-300 text-center text-lg mb-6 leading-relaxed">
                      Expand your audio library and build a comprehensive recognition database
                    </p>

                    <div className="flex items-center justify-center gap-2 text-gray-400 font-semibold group-hover:gap-4 transition-all">
                      <span>Build Library</span>
                      <span>→</span>
                    </div>
                  </div>
                </div>
              </div>
            </Link>
          </div>

          {/* Features */}
          <div className={`max-w-6xl mx-auto ${mounted ? 'animate-slide-up' : 'opacity-0'}`} style={{ animationDelay: '0.4s' }}>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="glass rounded-3xl p-8 text-center hover-lift group border border-gray-700">
                <div className="flex justify-center mb-6">
                  <div className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl p-5 group-hover:scale-110 transition-transform border border-gray-600">
                    <Zap className="w-10 h-10 text-gray-200" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">Lightning Fast</h3>
                <p className="text-gray-400 leading-relaxed">
                  Millisecond-level spectral analysis using optimized STFT algorithms
                </p>
              </div>

              <div className="glass rounded-3xl p-8 text-center hover-lift group border border-gray-700">
                <div className="flex justify-center mb-6">
                  <div className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl p-5 group-hover:scale-110 transition-transform border border-gray-600">
                    <Music className="w-10 h-10 text-gray-200" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">Ultra Accurate</h3>
                <p className="text-gray-400 leading-relaxed">
                  Advanced constellation mapping with time-shift invariant matching
                </p>
              </div>

              <div className="glass rounded-3xl p-8 text-center hover-lift group border border-gray-700">
                <div className="flex justify-center mb-6">
                  <div className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl p-5 group-hover:scale-110 transition-transform border border-gray-600">
                    <Shield className="w-10 h-10 text-gray-200" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">Privacy First</h3>
                <p className="text-gray-400 leading-relaxed">
                  100% local processing - your audio data never leaves your device
                </p>
              </div>
            </div>
          </div>

          {/* Footer Stats */}
          <div className="mt-20 text-center">
            <div className="glass rounded-3xl p-8 max-w-4xl mx-auto border border-gray-700">
              <div className="grid grid-cols-3 gap-8">
                <div>
                  <div className="text-4xl font-black text-white mb-2">99.9%</div>
                  <div className="text-gray-400 text-sm">Accuracy Rate</div>
                </div>
                <div>
                  <div className="text-4xl font-black text-white mb-2">&lt;2s</div>
                  <div className="text-gray-400 text-sm">Recognition Time</div>
                </div>
                <div>
                  <div className="text-4xl font-black text-white mb-2">∞</div>
                  <div className="text-gray-400 text-sm">Song Database</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
