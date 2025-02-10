import React, { useState, useEffect } from 'react';
import type { TableMetrics } from '../types';

interface DataQualityProps {
  onFetchData: () => Promise<TableMetrics>;
}

export function DataQuality({ onFetchData }: DataQualityProps) {
  const [data, setData] = useState<TableMetrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [tables, setTables] = useState<string[]>([]);
  const [selectedTables, setSelectedTables] = useState<string[]>([]);
  const [loadingTables, setLoadingTables] = useState(false);

  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = async () => {
    setLoadingTables(true);
    try {
      const response = await fetch('http://127.0.0.1:8089/list-tables/');
      const data = await response.json();
      setTables(data);
    } catch (error) {
      console.error('Error fetching tables:', error);
    } finally {
      setLoadingTables(false);
    }
  };

  const handleTableSelection = (tableName: string) => {
    setSelectedTables(prev => {
      if (prev.includes(tableName)) {
        return prev.filter(t => t !== tableName);
      }
      return [...prev, tableName];
    });
  };

  const handleFetchData = async () => {
    if (selectedTables.length === 0) {
      alert('Please select at least one table');
      return;
    }

    setLoading(true);
    try {
      const result = await onFetchData();
      setData(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getColorClass = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Data Quality Analysis</h2>
        
        {loadingTables ? (
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
            <span className="text-gray-600">Loading tables...</span>
          </div>
        ) : (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold mb-4">Select Tables for Analysis</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-6">
              {tables.map((table) => (
                <label
                  key={table}
                  className={`flex items-center p-3 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                    selectedTables.includes(table)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={selectedTables.includes(table)}
                    onChange={() => handleTableSelection(table)}
                    className="form-checkbox h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2 text-gray-700">{table}</span>
                </label>
              ))}
            </div>
            <button
              onClick={handleFetchData}
              disabled={loading || selectedTables.length === 0}
              className={`bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2`}
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <span>Analyze Selected Tables</span>
                  <span className="text-sm">({selectedTables.length} selected)</span>
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {data && (
        <div className="space-y-8">
          {Object.entries(data).map(([tableName, metrics]) => (
            <div key={tableName} className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold mb-4">{tableName}</h3>
              
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-semibold">Completeness Percentage</h4>
                  {Object.entries(metrics.completeness_percentage).map(([column, value]) => (
                    <div key={column} className="space-y-1">
                      <div className="flex justify-between text-sm">
                        <span>{column}</span>
                        <span>{value}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`${getColorClass(value)} h-2 rounded-full transition-all duration-500`}
                          style={{ width: `${value}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="space-y-4">
                  <h4 className="font-semibold">Uniqueness Percentage</h4>
                  {Object.entries(metrics.uniqueness_percentage).map(([column, value]) => (
                    <div key={column} className="space-y-1">
                      <div className="flex justify-between text-sm">
                        <span>{column}</span>
                        <span>{value}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`${getColorClass(value)} h-2 rounded-full transition-all duration-500`}
                          style={{ width: `${value}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-6 grid grid-cols-2 gap-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">Duplicate Percentage</h4>
                  <div className="text-2xl font-bold">
                    {metrics.duplicate_percentage}%
                  </div>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">Missing Values</h4>
                  <div className="space-y-1">
                    {Object.entries(metrics.missing_values).map(([column, value]) => (
                      <div key={column} className="flex justify-between">
                        <span>{column}:</span>
                        <span>{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}