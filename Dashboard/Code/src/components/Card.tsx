import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  darkMode?: boolean;
}

export function Card({ children, className = '', darkMode = false }: CardProps) {
  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md ${className}`}>
      {children}
    </div>
  );
}