import React, { useState } from 'react';
import { Activity, Target, Zap, BarChart, Moon, Sun, FileText } from 'lucide-react';
import { StatsCard } from './components/StatsCard';
import { ConfusionMatrix } from './components/ConfusionMatrix';
import { ResultsTable } from './components/ResultsTable';
import { ShapValues } from './components/ShapValues';
import type { ModelData } from './types';

const mockModels: ModelData[] = [
  {
    name: "Gradient Boosting",
    stats: {
      accuracy: 0.85,
      precision: 0.82,
      recall: 0.88,
      f1Score: 0.85
    },
    confusionMatrix: {
      truePositive: 150,
      trueNegative: 140,
      falsePositive: 30,
      falseNegative: 20
    },
    shapValues: [
      { name: "Feature 1", value: 0.42 },
      { name: "Feature 2", value: 0.38 },
      { name: "Feature 3", value: 0.25 },
      { name: "Feature 4", value: 0.18 },
      { name: "Feature 5", value: 0.15 }
    ],
    results: Array.from({ length: 20 }, (_, i) => ({
      id: `GB-${i + 1}`,
      actualLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      predictedLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      confidence: 0.7 + Math.random() * 0.3,
      timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString()
    })),
    paperUrl: "https://arxiv.org/abs/1603.02754"
  },
  {
    name: "Light GBM",
    stats: {
      accuracy: 0.88,
      precision: 0.86,
      recall: 0.89,
      f1Score: 0.87
    },
    confusionMatrix: {
      truePositive: 160,
      trueNegative: 145,
      falsePositive: 25,
      falseNegative: 15
    },
    shapValues: [
      { name: "Feature 1", value: 0.45 },
      { name: "Feature 2", value: 0.35 },
      { name: "Feature 3", value: 0.28 },
      { name: "Feature 4", value: 0.20 },
      { name: "Feature 5", value: 0.12 }
    ],
    results: Array.from({ length: 20 }, (_, i) => ({
      id: `LGB-${i + 1}`,
      actualLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      predictedLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      confidence: 0.7 + Math.random() * 0.3,
      timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString()
    })),
    paperUrl: "https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree"
  },
  {
    name: "Neural Network",
    stats: {
      accuracy: 0.82,
      precision: 0.80,
      recall: 0.84,
      f1Score: 0.82
    },
    confusionMatrix: {
      truePositive: 140,
      trueNegative: 135,
      falsePositive: 35,
      falseNegative: 25
    },
    shapValues: [
      { name: "Feature 1", value: 0.40 },
      { name: "Feature 2", value: 0.32 },
      { name: "Feature 3", value: 0.30 },
      { name: "Feature 4", value: 0.22 },
      { name: "Feature 5", value: 0.10 }
    ],
    results: Array.from({ length: 20 }, (_, i) => ({
      id: `NN-${i + 1}`,
      actualLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      predictedLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      confidence: 0.7 + Math.random() * 0.3,
      timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString()
    })),
    paperUrl: "https://arxiv.org/abs/1512.03385"
  },
  {
    name: "Logistic Regression",
    stats: {
      accuracy: 0.86,
      precision: 0.84,
      recall: 0.87,
      f1Score: 0.85
    },
    confusionMatrix: {
      truePositive: 155,
      trueNegative: 142,
      falsePositive: 28,
      falseNegative: 18
    },
    shapValues: [
      { name: "Feature 1", value: 0.38 },
      { name: "Feature 2", value: 0.35 },
      { name: "Feature 3", value: 0.28 },
      { name: "Feature 4", value: 0.15 },
      { name: "Feature 5", value: 0.08 }
    ],
    results: Array.from({ length: 20 }, (_, i) => ({
      id: `LR-${i + 1}`,
      actualLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      predictedLabel: Math.random() > 0.5 ? 'Positive' : 'Negative',
      confidence: 0.7 + Math.random() * 0.3,
      timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString()
    })),
    paperUrl: "https://arxiv.org/abs/1509.09169"
  }
];

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [selectedModel, setSelectedModel] = useState(0);
  const currentModel = mockModels[selectedModel];

  return (
    <div className={`min-h-screen transition-colors duration-200 ${darkMode ? 'dark bg-gray-900' : 'bg-gray-100'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Model Performance Dashboard
          </h1>
          <div className="flex items-center space-x-4">
            {currentModel.paperUrl && (
              <a
                href={currentModel.paperUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                  darkMode ? 'bg-gray-800 text-gray-200 hover:bg-gray-700' : 'bg-white text-gray-800 hover:bg-gray-50'
                } shadow-md transition-colors duration-200`}
              >
                <FileText className="w-5 h-5" />
                <span>Paper</span>
              </a>
            )}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`p-2 rounded-lg ${darkMode ? 'bg-gray-800 text-gray-200' : 'bg-white text-gray-800'} shadow-md`}
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </div>

        <div className="flex space-x-4 mb-8">
          {mockModels.map((model, index) => (
            <button
              key={model.name}
              onClick={() => setSelectedModel(index)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                selectedModel === index
                  ? 'bg-blue-600 text-white'
                  : darkMode
                  ? 'bg-gray-800 text-gray-200 hover:bg-gray-700'
                  : 'bg-white text-gray-800 hover:bg-gray-50'
              } shadow-md`}
            >
              {model.name}
            </button>
          ))}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard 
            title="Accuracy" 
            value={currentModel.stats.accuracy}
            icon={<Target className="w-6 h-6 text-blue-600" />}
            darkMode={darkMode}
          />
          <StatsCard 
            title="Precision" 
            value={currentModel.stats.precision}
            icon={<Zap className="w-6 h-6 text-blue-600" />}
            darkMode={darkMode}
          />
          <StatsCard 
            title="Recall" 
            value={currentModel.stats.recall}
            icon={<Activity className="w-6 h-6 text-blue-600" />}
            darkMode={darkMode}
          />
          <StatsCard 
            title="F1 Score" 
            value={currentModel.stats.f1Score}
            icon={<BarChart className="w-6 h-6 text-blue-600" />}
            darkMode={darkMode}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <ConfusionMatrix data={currentModel.confusionMatrix} darkMode={darkMode} />
          <ShapValues data={currentModel.shapValues} darkMode={darkMode} />
        </div>

        <div className="mb-8">
          <h2 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Latest Results
          </h2>
          <ResultsTable results={currentModel.results} darkMode={darkMode} />
        </div>
      </div>
    </div>
  );
}

export default App;