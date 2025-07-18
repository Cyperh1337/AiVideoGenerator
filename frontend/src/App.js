import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const VideoGenerator = () => {
  const [checkpoints, setCheckpoints] = useState([]);
  const [loras, setLoras] = useState([]);
  const [formData, setFormData] = useState({
    prompt: "",
    checkpoint: "",
    lora: "",
    width: 512,
    height: 512,
    frames: 16,
    duration_type: "short"
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationHistory, setGenerationHistory] = useState([]);
  const [comfyuiStatus, setComfyuiStatus] = useState("checking");
  const [currentGeneration, setCurrentGeneration] = useState(null);
  const [comfyuiUrl, setComfyuiUrl] = useState("http://127.0.0.1:8188");
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    await loadComfyUIConfig();
    await checkComfyUIStatus();
    await loadCheckpoints();
    await loadLoras();
    await loadGenerationHistory();
  };

  const loadComfyUIConfig = async () => {
    try {
      const response = await axios.get(`${API}/comfyui/config`);
      setComfyuiUrl(response.data.base_url);
    } catch (error) {
      console.error("Error loading ComfyUI config:", error);
    }
  };

  const updateComfyUIConfig = async (newUrl) => {
    try {
      await axios.post(`${API}/comfyui/config`, {
        base_url: newUrl
      });
      setComfyuiUrl(newUrl);
      setShowSettings(false);
      // Refresh status and models
      await checkComfyUIStatus();
      await loadCheckpoints();
      await loadLoras();
    } catch (error) {
      console.error("Error updating ComfyUI config:", error);
    }
  };

  const checkComfyUIStatus = async () => {
    try {
      const response = await axios.get(`${API}/comfyui/status`);
      setComfyuiStatus(response.data.status);
    } catch (error) {
      console.error("Error checking ComfyUI status:", error);
      setComfyuiStatus("error");
    }
  };

  const loadCheckpoints = async () => {
    try {
      const response = await axios.get(`${API}/comfyui/checkpoints`);
      setCheckpoints(response.data.checkpoints || []);
    } catch (error) {
      console.error("Error loading checkpoints:", error);
    }
  };

  const loadLoras = async () => {
    try {
      const response = await axios.get(`${API}/comfyui/loras`);
      setLoras(response.data.loras || []);
    } catch (error) {
      console.error("Error loading LoRAs:", error);
    }
  };

  const loadGenerationHistory = async () => {
    try {
      const response = await axios.get(`${API}/generate/history`);
      setGenerationHistory(response.data || []);
    } catch (error) {
      console.error("Error loading generation history:", error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleDurationTypeChange = (type) => {
    let frames;
    switch (type) {
      case "short":
        frames = 16; // TikTok short
        break;
      case "medium":
        frames = 60; // Medium video
        break;
      case "long":
        frames = 120; // Long video
        break;
      default:
        frames = 16;
    }
    
    setFormData(prev => ({
      ...prev,
      duration_type: type,
      frames: frames
    }));
  };

  const generateVideo = async () => {
    if (!formData.prompt || !formData.checkpoint) {
      alert("Please enter a prompt and select a checkpoint");
      return;
    }

    setIsGenerating(true);
    setCurrentGeneration(null);

    try {
      const response = await axios.post(`${API}/generate/video`, formData);
      
      if (response.data.success) {
        const videoId = response.data.video_id;
        setCurrentGeneration({
          id: videoId,
          status: "processing",
          prompt: formData.prompt
        });
        
        // Poll for status updates
        pollGenerationStatus(videoId);
      }
    } catch (error) {
      console.error("Error generating video:", error);
      setIsGenerating(false);
      alert("Error generating video: " + (error.response?.data?.detail || error.message));
    }
  };

  const pollGenerationStatus = async (videoId) => {
    try {
      const response = await axios.get(`${API}/generate/status/${videoId}`);
      const generation = response.data;
      
      setCurrentGeneration(generation);
      
      if (generation.status === "completed" || generation.status === "failed") {
        setIsGenerating(false);
        await loadGenerationHistory();
      } else if (generation.status === "processing") {
        // Continue polling
        setTimeout(() => pollGenerationStatus(videoId), 3000);
      }
    } catch (error) {
      console.error("Error polling generation status:", error);
      setIsGenerating(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "connected":
        return "text-green-500";
      case "disconnected":
        return "text-red-500";
      case "error":
        return "text-red-500";
      default:
        return "text-yellow-500";
    }
  };

  const getGenerationStatusColor = (status) => {
    switch (status) {
      case "completed":
        return "text-green-500";
      case "failed":
        return "text-red-500";
      case "processing":
        return "text-yellow-500";
      default:
        return "text-gray-500";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            ComfyUI Video Generator
          </h1>
          <p className="text-xl text-gray-300">
            Crea video straordinari con i tuoi checkpoint e LoRA personalizzati
          </p>
          <div className="mt-4 flex justify-center items-center space-x-2">
            <span className="text-sm text-gray-400">ComfyUI Status:</span>
            <span className={`text-sm font-semibold ${getStatusColor(comfyuiStatus)}`}>
              {comfyuiStatus}
            </span>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Generation Form */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-xl p-6 shadow-2xl">
              <h2 className="text-2xl font-bold mb-6 text-purple-300">Genera Video</h2>
              
              {/* Prompt */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Prompt
                </label>
                <textarea
                  name="prompt"
                  value={formData.prompt}
                  onChange={handleInputChange}
                  className="w-full h-32 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Descrivi il video che vuoi generare..."
                  rows="4"
                />
              </div>

              {/* Checkpoint Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Checkpoint
                </label>
                <select
                  name="checkpoint"
                  value={formData.checkpoint}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white"
                >
                  <option value="">Seleziona un checkpoint</option>
                  {checkpoints.map((checkpoint, index) => (
                    <option key={index} value={checkpoint}>
                      {checkpoint}
                    </option>
                  ))}
                </select>
              </div>

              {/* LoRA Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  LoRA (Opzionale)
                </label>
                <select
                  name="lora"
                  value={formData.lora}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white"
                >
                  <option value="">Nessun LoRA</option>
                  {loras.map((lora, index) => (
                    <option key={index} value={lora}>
                      {lora}
                    </option>
                  ))}
                </select>
              </div>

              {/* Duration Type */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Tipo di Video
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { type: "short", label: "Short (TikTok)", frames: 16 },
                    { type: "medium", label: "Medium", frames: 60 },
                    { type: "long", label: "Long (YouTube)", frames: 120 }
                  ].map((option) => (
                    <button
                      key={option.type}
                      onClick={() => handleDurationTypeChange(option.type)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        formData.duration_type === option.type
                          ? "bg-purple-600 text-white"
                          : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Video Parameters */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Larghezza
                  </label>
                  <input
                    type="number"
                    name="width"
                    value={formData.width}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white"
                    min="256"
                    max="1024"
                    step="64"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Altezza
                  </label>
                  <input
                    type="number"
                    name="height"
                    value={formData.height}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white"
                    min="256"
                    max="1024"
                    step="64"
                  />
                </div>
              </div>

              {/* Frames */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Frames: {formData.frames}
                </label>
                <input
                  type="range"
                  name="frames"
                  value={formData.frames}
                  onChange={handleInputChange}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                  min="8"
                  max="600"
                  step="8"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>8</span>
                  <span>600</span>
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateVideo}
                disabled={isGenerating || comfyuiStatus !== "connected"}
                className={`w-full py-3 px-6 rounded-lg font-semibold text-lg transition-all duration-300 ${
                  isGenerating || comfyuiStatus !== "connected"
                    ? "bg-gray-600 cursor-not-allowed"
                    : "bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 transform hover:scale-105"
                }`}
              >
                {isGenerating ? "Generando..." : "Genera Video"}
              </button>
            </div>
          </div>

          {/* Status and History */}
          <div className="space-y-6">
            {/* Current Generation */}
            {currentGeneration && (
              <div className="bg-gray-800 rounded-xl p-6 shadow-2xl">
                <h3 className="text-xl font-bold mb-4 text-purple-300">Generazione Corrente</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Status:</span>
                    <span className={`font-semibold ${getGenerationStatusColor(currentGeneration.status)}`}>
                      {currentGeneration.status}
                    </span>
                  </div>
                  <div className="text-sm text-gray-300">
                    <strong>Prompt:</strong> {currentGeneration.prompt}
                  </div>
                  {currentGeneration.status === "processing" && (
                    <div className="mt-4">
                      <div className="animate-pulse flex space-x-4">
                        <div className="rounded-full bg-purple-500 h-3 w-3"></div>
                        <div className="flex-1 space-y-2 py-1">
                          <div className="h-2 bg-purple-500 rounded w-3/4"></div>
                          <div className="h-2 bg-purple-500 rounded w-1/2"></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Generation History */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-2xl">
              <h3 className="text-xl font-bold mb-4 text-purple-300">Storico Generazioni</h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {generationHistory.length === 0 ? (
                  <p className="text-gray-400 text-center py-4">Nessuna generazione ancora</p>
                ) : (
                  generationHistory.map((generation, index) => (
                    <div key={index} className="bg-gray-700 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex-1">
                          <div className="text-sm text-gray-300 truncate">
                            {generation.prompt}
                          </div>
                          <div className="text-xs text-gray-500 mt-1">
                            {generation.checkpoint}
                            {generation.lora && ` • ${generation.lora}`}
                          </div>
                        </div>
                        <span className={`text-xs font-semibold ${getGenerationStatusColor(generation.status)}`}>
                          {generation.status}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(generation.created_at).toLocaleDateString("it-IT", {
                          year: "numeric",
                          month: "short",
                          day: "numeric",
                          hour: "2-digit",
                          minute: "2-digit"
                        })}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <VideoGenerator />
    </div>
  );
}

export default App;