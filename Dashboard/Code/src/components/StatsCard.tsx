import React from 'react';
import { Card } from './Card';

interface StatsCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  darkMode?: boolean;
}

export function StatsCard({ title, value, icon, darkMode = false }: StatsCardProps) {
  return (
    <Card className="flex items-center p-6 space-x-4" darkMode={darkMode}>
      <div className={`p-3 ${darkMode ? 'bg-blue-900/30' : 'bg-blue-100'} rounded-lg`}>
        {icon}
      </div>
      <div>
        <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>{title}</p>
        <p className={`text-2xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          {(value * 100).toFixed(2)}%
        </p>
      </div>
    </Card>
  );
}