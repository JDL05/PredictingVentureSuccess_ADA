import React from 'react';
import { Card } from './Card';
import type { ShapData } from '../types';

interface ShapValuesProps {
  data: ShapData[];
  darkMode?: boolean;
}

// Funktion zum Formatieren von Variablennamen
const formatVariableName = (name: string) => {
  return name
    .replace(/_/g, ' ') // Unterstriche durch Leerzeichen ersetzen
    .toLowerCase() // Alles in Kleinbuchstaben umwandeln
    .replace(/\b\w/g, (char) => char.toUpperCase()); // Jeden ersten Buchstaben eines Wortes groß machen
};

export function ShapValues({ data, darkMode = false }: ShapValuesProps) {
  const topFeatures = [...data]
    .sort((a, b) => b.value - a.value) // Sortiere absteigend nach SHAP-Wert
    .slice(0, 5); // Wähle die Top-5 aus

  const maxValue = topFeatures[0]?.value || 1; // Sicherstellen, dass kein Fehler bei leerem Array auftritt

  return (
    <Card className="p-6" darkMode={darkMode}>
      <h2 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        SHAP Feature Importance
      </h2>
      <div className="space-y-3">
        {topFeatures.map((feature) => (
          <div key={feature.name} className="space-y-1">
            <div className="flex justify-between">
              <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                {formatVariableName(feature.name)} {/* Formatierter Variablenname */}
              </span>
              <span className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                {feature.value.toFixed(3)}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div
                className="bg-blue-600 h-2.5 rounded-full"
                style={{ width: `${(feature.value / maxValue) * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
