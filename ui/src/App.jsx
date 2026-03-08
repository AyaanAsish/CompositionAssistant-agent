import { useState, useRef, useEffect } from "react";

const API_URL = "http://localhost:8000";

// Icons as SVG components
const PlayIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
    <path fillRule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clipRule="evenodd" />
  </svg>
);

const PauseIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
    <path fillRule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clipRule="evenodd" />
  </svg>
);

const UploadIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-8 h-8">
    <path fillRule="evenodd" d="M11.47 2.47a.75.75 0 011.06 0l4.5 4.5a.75.75 0 01-1.06 1.06l-3.22-3.22V16.5a.75.75 0 01-1.5 0V4.81L8.03 8.03a.75.75 0 01-1.06-1.06l4.5-4.5zM3 15.75a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clipRule="evenodd" />
  </svg>
);

const MusicIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path fillRule="evenodd" d="M19.952 1.651a.75.75 0 01.298.599V16.303a3 3 0 01-2.176 2.884l-1.32.377a2.553 2.553 0 11-1.403-4.909l2.311-.66a1.5 1.5 0 001.088-1.442V6.994l-9 2.572v9.737a3 3 0 01-2.176 2.884l-1.32.377a2.553 2.553 0 11-1.402-4.909l2.31-.66a1.5 1.5 0 001.088-1.442V5.25a.75.75 0 01.544-.721l10.5-3a.75.75 0 01.658.122z" clipRule="evenodd" />
  </svg>
);

const SparklesIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path fillRule="evenodd" d="M9 4.5a.75.75 0 01.721.544l.813 2.846a3.75 3.75 0 002.576 2.576l2.846.813a.75.75 0 010 1.442l-2.846.813a3.75 3.75 0 00-2.576 2.576l-.813 2.846a.75.75 0 01-1.442 0l-.813-2.846a3.75 3.75 0 00-2.576-2.576l-2.846-.813a.75.75 0 010-1.442l2.846-.813A3.75 3.75 0 007.466 7.89l.813-2.846A.75.75 0 019 4.5zM18 1.5a.75.75 0 01.728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 010 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 01-1.456 0l-.258-1.036a2.625 2.625 0 00-1.91-1.91l-1.036-.258a.75.75 0 010-1.456l1.036-.258a2.625 2.625 0 001.91-1.91l.258-1.036A.75.75 0 0118 1.5zM16.5 15a.75.75 0 01.712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 010 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 01-1.422 0l-.395-1.183a1.5 1.5 0 00-.948-.948l-1.183-.395a.75.75 0 010-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0116.5 15z" clipRule="evenodd" />
  </svg>
);

const DownloadIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path fillRule="evenodd" d="M12 2.25a.75.75 0 01.75.75v11.69l3.22-3.22a.75.75 0 111.06 1.06l-4.5 4.5a.75.75 0 01-1.06 0l-4.5-4.5a.75.75 0 111.06-1.06l3.22 3.22V3a.75.75 0 01.75-.75zm-9 13.5a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clipRule="evenodd" />
  </svg>
);

const RefreshIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path fillRule="evenodd" d="M4.755 10.059a7.5 7.5 0 0112.548-3.364l1.903 1.903h-3.183a.75.75 0 100 1.5h4.992a.75.75 0 00.75-.75V4.356a.75.75 0 00-1.5 0v3.18l-1.9-1.9A9 9 0 003.306 9.67a.75.75 0 101.45.388zm15.408 3.352a.75.75 0 00-.919.53 7.5 7.5 0 01-12.548 3.364l-1.902-1.903h3.183a.75.75 0 000-1.5H2.984a.75.75 0 00-.75.75v4.992a.75.75 0 001.5 0v-3.18l1.9 1.9a9 9 0 0015.059-4.035.75.75 0 00-.53-.918z" clipRule="evenodd" />
  </svg>
);

// Custom Audio Player Component
function AudioPlayer({ audioUrl, title = "Transformed Audio" }) {
  const audioRef = useRef(null);
  const progressRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
    const handleLoadedMetadata = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", handleTimeUpdate);
    audio.addEventListener("loadedmetadata", handleLoadedMetadata);
    audio.addEventListener("ended", handleEnded);

    return () => {
      audio.removeEventListener("timeupdate", handleTimeUpdate);
      audio.removeEventListener("loadedmetadata", handleLoadedMetadata);
      audio.removeEventListener("ended", handleEnded);
    };
  }, [audioUrl]);

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleProgressClick = (e) => {
    if (!progressRef.current || !audioRef.current) return;
    const rect = progressRef.current.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    audioRef.current.currentTime = percent * duration;
  };

  const formatTime = (time) => {
    if (isNaN(time)) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  };

  const progress = duration ? (currentTime / duration) * 100 : 0;

  return (
    <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
      <audio ref={audioRef} src={audioUrl} />
      
      {/* Title */}
      <div className="flex items-center gap-2 mb-4">
        <MusicIcon />
        <span className="text-sm font-medium text-slate-300">{title}</span>
      </div>

      {/* Waveform Visualization (Static bars) */}
      <div className="flex items-center justify-center gap-[2px] h-16 mb-4 px-4">
        {Array.from({ length: 50 }).map((_, i) => {
          const height = Math.sin(i * 0.3) * 30 + Math.random() * 20 + 20;
          const isActive = (i / 50) * 100 <= progress;
          return (
            <div
              key={i}
              className={`w-1 rounded-full transition-all duration-150 ${
                isActive 
                  ? "bg-gradient-to-t from-violet-500 to-fuchsia-400" 
                  : "bg-slate-600/50"
              }`}
              style={{ 
                height: `${height}%`,
                opacity: isPlaying ? (isActive ? 1 : 0.5) : 0.7
              }}
            />
          );
        })}
      </div>

      {/* Progress Bar */}
      <div
        ref={progressRef}
        onClick={handleProgressClick}
        className="h-2 bg-slate-700 rounded-full cursor-pointer mb-3 overflow-hidden"
      >
        <div
          className="h-full bg-gradient-to-r from-violet-500 to-fuchsia-500 rounded-full transition-all duration-100"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-400 font-mono">{formatTime(currentTime)}</span>
        
        <button
          onClick={togglePlay}
          className="w-14 h-14 rounded-full bg-gradient-to-br from-violet-500 to-fuchsia-600 hover:from-violet-400 hover:to-fuchsia-500 flex items-center justify-center shadow-lg shadow-violet-500/25 transition-all duration-200 hover:scale-105 active:scale-95"
        >
          {isPlaying ? <PauseIcon /> : <PlayIcon />}
        </button>
        
        <span className="text-xs text-slate-400 font-mono">{formatTime(duration)}</span>
      </div>
    </div>
  );
}

// Tag Button Component
function TagButton({ word, isSelected, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 text-sm rounded-full transition-all duration-200 ${
        isSelected
          ? "bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white font-medium shadow-lg shadow-violet-500/25"
          : "bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 hover:text-white border border-slate-700/50"
      }`}
    >
      {word}
    </button>
  );
}

// Category Section Component
function CategorySection({ title, words, selectedTags, toggleTag }) {
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">{title}</h3>
      <div className="flex flex-wrap gap-2">
        {words.map((word) => (
          <TagButton
            key={word}
            word={word}
            isSelected={selectedTags.has(word)}
            onClick={() => toggleTag(word)}
          />
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [selectedTags, setSelectedTags] = useState(new Set());
  const [loading, setLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const [outputBlob, setOutputBlob] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [processingStep, setProcessingStep] = useState("");

  const categories = [
    {
      title: "Mood",
      words: ["happy", "joyful", "dark", "sad", "tender", "melancholic", "energetic", "calm", "mysterious", "romantic"],
    },
    {
      title: "Rhythm",
      words: ["faster", "slower", "upbeat", "syncopated", "steady", "swinging", "groovy", "laid-back"],
    },
    {
      title: "Melody",
      words: ["add notes", "remove notes", "simplify", "ornate", "flowing", "staccato", "arpeggiated", "minimalist"],
    },
    {
      title: "Genre",
      words: ["rock", "classical", "jazz", "pop", "electronic", "folk", "blues", "ambient", "orchestral"],
    },
  ];

  const toggleTag = (word) => {
    setSelectedTags((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(word)) {
        newSet.delete(word);
      } else {
        newSet.add(word);
      }
      return newSet;
    });
  };

  const handleFileSelect = (e) => {
    if (e.target.files?.[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const runAgent = async () => {
    if (!file) return alert("Please select a WAV file first");

    const finalPrompt = [
      prompt.trim(),
      ...Array.from(selectedTags),
    ].filter(Boolean).join(", ");

    if (!finalPrompt) return alert("Please enter a prompt or select at least one tag");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("prompt", finalPrompt);

    setLoading(true);
    setProcessingStep("Uploading audio...");

    try {
      setProcessingStep("Transcribing to MIDI...");
      await new Promise(r => setTimeout(r, 500));
      
      setProcessingStep("Analyzing with AI...");
      const resp = await fetch(`${API_URL}/process-wav/`, {
        method: "POST",
        body: formData,
      });

      if (!resp.ok) throw new Error("Processing failed");

      setProcessingStep("Generating new audio...");
      const data = await resp.json();
      const filename = data.filename;

      const audioResp = await fetch(`${API_URL}/download/${filename}`);
      const blob = await audioResp.blob();
      const url = URL.createObjectURL(blob);

      setAudioUrl(url);
      setOutputBlob(blob);
      setProcessingStep("");
    } catch (err) {
      alert("Processing failed: " + err.message);
    } finally {
      setLoading(false);
      setProcessingStep("");
    }
  };

  const reuseOutputAsInput = () => {
    if (!outputBlob) return;
    const newFile = new File([outputBlob], "transformed_audio.wav", { type: "audio/wav" });
    setFile(newFile);
    setAudioUrl(null);
  };

  const downloadAudio = () => {
    if (!audioUrl) return;
    const a = document.createElement("a");
    a.href = audioUrl;
    a.download = "composition_assistant_output.wav";
    a.click();
  };

  const clearAll = () => {
    setFile(null);
    setPrompt("");
    setSelectedTags(new Set());
    setAudioUrl(null);
    setOutputBlob(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Background gradient */}
      <div className="fixed inset-0 bg-gradient-to-br from-violet-950/20 via-slate-950 to-fuchsia-950/20 pointer-events-none" />
      
      {/* Animated background orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-fuchsia-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-violet-500/10 rounded-full border border-violet-500/20 mb-6">
            <SparklesIcon />
            <span className="text-sm text-violet-300">AI-Powered Music Transformation</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-white via-violet-200 to-fuchsia-200 bg-clip-text text-transparent">
            Ayaan's Composition Assistant
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Transform your music with natural language. Upload audio, describe your vision, and let AI create something new.
          </p>
        </header>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Sidebar - Tags */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50">
              <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-violet-500" />
                Quick Tags
              </h2>
              <div className="space-y-6">
                {categories.map((cat) => (
                  <CategorySection
                    key={cat.title}
                    title={cat.title}
                    words={cat.words}
                    selectedTags={selectedTags}
                    toggleTag={toggleTag}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Upload Area */}
            <div
              onDrop={handleDrop}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              className={`relative bg-slate-900/50 backdrop-blur-sm rounded-2xl p-8 border-2 border-dashed transition-all duration-200 ${
                dragActive
                  ? "border-violet-500 bg-violet-500/10"
                  : file
                  ? "border-green-500/50 bg-green-500/5"
                  : "border-slate-700 hover:border-slate-600"
              }`}
            >
              <input
                type="file"
                accept=".wav"
                onChange={handleFileSelect}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              
              <div className="text-center">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4 ${
                  file ? "bg-green-500/20 text-green-400" : "bg-slate-800 text-slate-400"
                }`}>
                  <UploadIcon />
                </div>
                
                {file ? (
                  <div>
                    <p className="text-lg font-medium text-green-400 mb-1">{file.name}</p>
                    <p className="text-sm text-slate-500">
                      {(file.size / 1024 / 1024).toFixed(2)} MB • Ready to process
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-lg font-medium text-slate-300 mb-1">
                      Drop your WAV file here
                    </p>
                    <p className="text-sm text-slate-500">
                      or click to browse
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Prompt Input */}
            <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50">
              <label className="block text-sm font-medium text-slate-400 mb-3">
                Describe your transformation
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g., Make it sound more dreamy and add some jazz influences..."
                rows={3}
                className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-transparent transition-all resize-none"
              />
              
              {/* Selected Tags Preview */}
              {selectedTags.size > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  <span className="text-xs text-slate-500">Selected:</span>
                  {Array.from(selectedTags).map((tag) => (
                    <span
                      key={tag}
                      className="text-xs px-2 py-1 bg-violet-500/20 text-violet-300 rounded-full"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={runAgent}
                disabled={loading || !file}
                className="flex-1 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-500 hover:to-fuchsia-500 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-xl shadow-lg shadow-violet-500/25 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>{processingStep || "Processing..."}</span>
                  </>
                ) : (
                  <>
                    <SparklesIcon />
                    <span>Transform Music</span>
                  </>
                )}
              </button>
              
              {(file || audioUrl) && (
                <button
                  onClick={clearAll}
                  className="px-6 py-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-xl transition-all"
                >
                  Clear
                </button>
              )}
            </div>

            {/* Loading State */}
            {loading && (
              <div className="bg-slate-900/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-800/50">
                <div className="flex items-center gap-4">
                  <div className="relative w-12 h-12">
                    <div className="absolute inset-0 rounded-full border-4 border-slate-700" />
                    <div className="absolute inset-0 rounded-full border-4 border-violet-500 border-t-transparent animate-spin" />
                  </div>
                  <div>
                    <p className="font-medium text-white">{processingStep}</p>
                    <p className="text-sm text-slate-400">This may take a moment...</p>
                  </div>
                </div>
                
                {/* Progress Steps */}
                <div className="mt-6 grid grid-cols-4 gap-2">
                  {["Upload", "Transcribe", "Transform", "Generate"].map((step, i) => (
                    <div key={step} className="text-center">
                      <div className={`h-1 rounded-full mb-2 ${
                        i <= ["Uploading", "Transcribing", "Analyzing", "Generating"].findIndex(s => processingStep.includes(s))
                          ? "bg-violet-500"
                          : "bg-slate-700"
                      }`} />
                      <span className="text-xs text-slate-500">{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Output Section */}
            {audioUrl && !loading && (
              <div className="space-y-4">
                <AudioPlayer audioUrl={audioUrl} title="Your Transformed Composition" />
                
                {/* Action Buttons */}
                <div className="flex gap-4">
                  <button
                    onClick={reuseOutputAsInput}
                    className="flex-1 bg-slate-800 hover:bg-slate-700 text-white font-medium py-3 px-6 rounded-xl transition-all flex items-center justify-center gap-2"
                  >
                    <RefreshIcon />
                    <span>Use as New Input</span>
                  </button>
                  
                  <button
                    onClick={downloadAudio}
                    className="flex-1 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-medium py-3 px-6 rounded-xl shadow-lg shadow-emerald-500/25 transition-all flex items-center justify-center gap-2"
                  >
                    <DownloadIcon />
                    <span>Download</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-slate-500 text-sm">
          <p>Made with ♥ by Ayaan • Powered by AI</p>
        </footer>
      </div>
    </div>
  );
}
