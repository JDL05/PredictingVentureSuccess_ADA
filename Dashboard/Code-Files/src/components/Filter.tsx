import React, { useState } from 'react';

interface FiltersProps {
  onFilterChange: (filters: { confidence: number; date: string; model: string }) => void;
  darkMode?: boolean;
}

export function Filters({ onFilterChange, darkMode = false }: FiltersProps) {
  const [confidence, setConfidence] = useState(0);
  const [date, setDate] = useState('');
  const [model, setModel] = useState('');

  const handleApplyFilters = () => {
    onFilterChange({ confidence, date, model });
  };

  return (
    <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-gray-200'}`}>
      <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Filters</h3>
      <div className="space-y-4">
        <div>
          <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Confidence Threshold:</label>
          <input
            type="number"
            className="w-full mt-1 rounded-lg"
            value={confidence}
            onChange={(e) => setConfidence(Number(e.target.value))}
          />
        </div>
        <div>
          <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Date:</label>
          <input
            type="date"
            className="w-full mt-1 rounded-lg"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>
        <div>
          <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Model:</label>
          <input
            type="text"
            className="w-full mt-1 rounded-lg"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          />
        </div>
        <button onClick={handleApplyFilters} className="bg-blue-600 text-white px-4 py-2 rounded-lg">Apply Filters</button>
      </div>
    </div>
  );
}
