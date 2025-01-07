import React from 'react';
import { Card } from './Card';
import type { ConfusionMatrixData } from '../types';

interface ConfusionMatrixProps {
  data: ConfusionMatrixData;
  darkMode?: boolean;
}

export function ConfusionMatrix({ data, darkMode = false }: ConfusionMatrixProps) {
  const total = data.truePositive + data.trueNegative + 
                data.falsePositive + data.falseNegative;

  const getPercentage = (value: number) => ((value / total) * 100).toFixed(1);

  return (
    <Card className="p-6" darkMode={darkMode}>
      <h2 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        Confusion Matrix
      </h2>
      <div className="grid grid-cols-2 gap-2">
        <div className={`${darkMode ? 'bg-green-900/30' : 'bg-green-100'} p-4 rounded`}>
          <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>True Positive</p>
          <p className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {getPercentage(data.truePositive)}%
          </p>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            {data.truePositive} cases
          </p>
        </div>
        <div className={`${darkMode ? 'bg-red-900/30' : 'bg-red-100'} p-4 rounded`}>
          <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>False Positive</p>
          <p className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {getPercentage(data.falsePositive)}%
          </p>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            {data.falsePositive} cases
          </p>
        </div>
        <div className={`${darkMode ? 'bg-red-900/30' : 'bg-red-100'} p-4 rounded`}>
          <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>False Negative</p>
          <p className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {getPercentage(data.falseNegative)}%
          </p>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            {data.falseNegative} cases
          </p>
        </div>
        <div className={`${darkMode ? 'bg-green-900/30' : 'bg-green-100'} p-4 rounded`}>
          <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>True Negative</p>
          <p className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {getPercentage(data.trueNegative)}%
          </p>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            {data.trueNegative} cases
          </p>
        </div>
      </div>
    </Card>
  );
}