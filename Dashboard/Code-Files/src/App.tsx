import React, { useState, useEffect } from 'react';
import { Activity, Target, Zap, BarChart, Moon, Sun, FileText } from 'lucide-react';
import { StatsCard } from './components/StatsCard';
import { ConfusionMatrix } from './components/ConfusionMatrix';
import { ResultsTable } from './components/ResultsTable';
import { ShapValues } from './components/ShapValues';
import { Bar } from 'react-chartjs-2';
import type { ModelData } from './types';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [models, setModels] = useState<ModelData[]>([]);
  const [selectedTab, setSelectedTab] = useState("Model Comparison"); // Neuer State für Tabs

  useEffect(() => {
    fetch('/dashboard_data.json')
      .then((response) => response.json())
      .then((data) => setModels(data))
      .catch((error) => console.error('Fehler beim Laden der Daten:', error));
  }, []);

  if (models.length === 0) {
    return <div>Loading...</div>;
  }

  // Tab-Inhalte dynamisch rendern
  const renderContent = () => {
    if (selectedTab === "Model Comparison") {
      return (
        <div className="grid grid-cols-1 gap-8 mb-8">
          {/* Vergleichstabelle */}
          <div className="grid grid-cols-1 gap-4">
            <h2 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
    
            </h2>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className={`${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                  <th className="border-b border-gray-300 py-2">Model</th>
                  <th className="border-b border-gray-300 py-2">Accuracy</th>
                  <th className="border-b border-gray-300 py-2">Precision</th>
                  <th className="border-b border-gray-300 py-2">Recall</th>
                  <th className="border-b border-gray-300 py-2">F1-Score</th>
                </tr>
              </thead>
              <tbody>
                {models.map((model) => (
                  <tr key={model.name} className={`${darkMode ? 'text-gray-300' : 'text-gray-800'} hover:bg-gray-200 dark:hover:bg-gray-700`}>
                    <td className="py-2">{model.name}</td>
                    <td className="py-2">{(model.stats.accuracy * 100).toFixed(2)}%</td>
                    <td className="py-2">{(model.stats.precision * 100).toFixed(2)}%</td>
                    <td className="py-2">{(model.stats.recall * 100).toFixed(2)}%</td>
                    <td className="py-2">{(model.stats.f1Score * 100).toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Balkendiagramm */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
            <h2 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Metrics Comparison
            </h2>
            <Bar
              data={{
                labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                datasets: models.map((model, index) => ({
                  label: model.name,
                  data: [model.stats.accuracy, model.stats.precision, model.stats.recall, model.stats.f1Score],
                  backgroundColor: `rgba(${index * 50}, 99, 132, 0.5)`,
                }))
              }}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                    labels: {
                      color: darkMode ? 'white' : 'black',
                    },
                  },
                },
                scales: {
                  x: {
                    ticks: {
                      color: darkMode ? 'white' : 'black',
                    },
                  },
                  y: {
                    ticks: {
                      color: darkMode ? 'white' : 'black',
                    },
                  },
                },
              }}
            />
          </div>
        </div>
      );
    } else {
      const currentModel = models.find((model) => model.name === selectedTab);
      if (!currentModel) return null;

      return (
        <div>
          {/* Statistiken */}
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
          {/* Confusion Matrix & SHAP-Werte */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <ConfusionMatrix data={currentModel.confusionMatrix} darkMode={darkMode} />
            {currentModel.shapValues && (
              <ShapValues data={currentModel.shapValues} darkMode={darkMode} />
            )}
          </div>
          {/* Investment Opportunities */}
          <div className="mb-8">
            <h2 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Investment Opportunities
            </h2>
            <ResultsTable results={currentModel.results} darkMode={darkMode} />
          </div>
        </div>
      );
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-200 ${darkMode ? 'dark bg-gray-900' : 'bg-gray-100'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Model Performance Dashboard
          </h1>
          <div className="flex items-center space-x-4">
            {/* Der Paper-Button wird immer sichtbar */}
            <a
              href="https://arxiv.org" // Standard-Link oder allgemeine Referenz
              target="_blank"
              rel="noopener noreferrer"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                darkMode ? 'bg-gray-800 text-gray-200 hover:bg-gray-700' : 'bg-white text-gray-800 hover:bg-gray-50'
              } shadow-md transition-colors duration-200`}
            >
              <FileText className="w-5 h-5" />
              <span>Paper</span>
            </a>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`p-2 rounded-lg ${darkMode ? 'bg-gray-800 text-gray-200' : 'bg-white text-gray-800'} shadow-md`}
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </div>


        {/* Tabs */}
        <div className="flex space-x-4 mb-8">
          <button
            onClick={() => setSelectedTab("Model Comparison")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
              selectedTab === "Model Comparison"
                ? 'bg-blue-600 text-white'
                : darkMode
                ? 'bg-gray-800 text-gray-200 hover:bg-gray-700'
                : 'bg-white text-gray-800 hover:bg-gray-50'
            }`}
          >
            Model Comparison
          </button>
          {models.map((model) => (
            <button
              key={model.name}
              onClick={() => setSelectedTab(model.name)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                selectedTab === model.name
                  ? 'bg-blue-600 text-white'
                  : darkMode
                  ? 'bg-gray-800 text-gray-200 hover:bg-gray-700'
                  : 'bg-white text-gray-800 hover:bg-gray-50'
              }`}
            >
              {model.name}
            </button>
          ))}
        </div>

        {renderContent()}
      </div>
    </div>
  );
}

export default App;
