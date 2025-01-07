import React from 'react';
import { Line } from 'react-chartjs-2';
import type { CurveData } from '../types';

interface PerformanceCurvesProps {
  rocData: CurveData[];
  prData: CurveData[];
  darkMode?: boolean;
}

export function PerformanceCurves({ rocData, prData, darkMode = false }: PerformanceCurvesProps) {
  const rocOptions = {
    scales: {
      x: { title: { display: true, text: 'False Positive Rate' } },
      y: { title: { display: true, text: 'True Positive Rate' } }
    },
    plugins: {
      legend: { display: true }
    }
  };

  const prOptions = {
    scales: {
      x: { title: { display: true, text: 'Recall' } },
      y: { title: { display: true, text: 'Precision' } }
    },
    plugins: {
      legend: { display: true }
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div>
        <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>ROC Curve</h3>
        <Line data={{ datasets: rocData }} options={rocOptions} />
      </div>
      <div>
        <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Precision-Recall Curve</h3>
        <Line data={{ datasets: prData }} options={prOptions} />
      </div>
    </div>
  );
}
