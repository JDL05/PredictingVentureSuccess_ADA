import React from 'react';
import { Card } from './Card';
import type { Result } from '../types';

interface ResultsTableProps {
  results: Result[];
  darkMode?: boolean;
}

export function ResultsTable({ results, darkMode = false }: ResultsTableProps) {
  // Filtern Sie nur die True Positives
  const truePositiveResults = results.filter(
    (result) => result.actualLabel === 'Positive' && result.predictedLabel === 'Positive'
  );

  return (
    <Card className="p-6" darkMode={darkMode}>
      <h2 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        Investment Opportunities
      </h2>
      <table className="min-w-full text-left text-sm">
        <thead>
          <tr>
            <th className={`py-2 ${darkMode ? 'text-white' : 'text-gray-600'}`}>ID</th>
            <th className={`py-2 ${darkMode ? 'text-white' : 'text-gray-600'}`}>ACTUAL</th>
            <th className={`py-2 ${darkMode ? 'text-white' : 'text-gray-600'}`}>PREDICTED</th>
            <th className={`py-2 ${darkMode ? 'text-white' : 'text-gray-600'}`}>CONFIDENCE</th>
            <th className={`py-2 ${darkMode ? 'text-white' : 'text-gray-600'}`}>TIMESTAMP</th>
          </tr>
        </thead>
        <tbody>
          {truePositiveResults.map((result) => (
            <tr key={result.id} className="hover:bg-gray-100 dark:hover:bg-gray-800">
              <td className={`py-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>{result.id}</td>
              <td className={`py-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>{result.actualLabel}</td>
              <td className={`py-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>{result.predictedLabel}</td>
              <td className={`py-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>{result.confidence}</td>
              <td className={`py-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {new Date(result.timestamp).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {truePositiveResults.length === 0 && (
        <div className={`py-4 text-center ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
          No True Positives found.
        </div>
      )}
    </Card>
  );
}
