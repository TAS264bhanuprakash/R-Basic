import React from 'react';
import { Database, GitBranch, Table2, Key, BarChart3, AlertCircle, Layers, Clock } from 'lucide-react';

interface DataProfilingOverviewProps {
  onSubModuleChange: (subModule: string) => void;
}

export function DataProfilingOverview({ onSubModuleChange }: DataProfilingOverviewProps) {
  const features = [
    {
      icon: Database,
      title: 'Data Quality',
      description: 'Analyze data completeness, accuracy, and consistency',
      color: 'from-blue-500 to-blue-600',
      module: 'Data Quality'
    },
    {
      icon: GitBranch,
      title: 'Column Correlation',
      description: 'Discover relationships between data columns',
      color: 'from-purple-500 to-purple-600',
      module: 'Column Correlation'
    },
    {
      icon: Table2,
      title: 'Fact & Dimension Tables',
      description: 'Identify and analyze table relationships',
      color: 'from-green-500 to-green-600',
      module: 'Fact Table And Dimension Table'
    },
    {
      icon: Key,
      title: 'Primary & Foreign Keys',
      description: 'Map key relationships across tables',
      color: 'from-yellow-500 to-yellow-600',
      module: 'Primary Key Foreign Key Relation'
    },
    {
      icon: BarChart3,
      title: 'Statistical Analysis',
      description: 'Get detailed statistical insights',
      color: 'from-pink-500 to-pink-600',
      module: 'Statistical Analysis'
    },
    {
      icon: AlertCircle,
      title: 'Business Rule Violations',
      description: 'Detect and analyze rule violations',
      color: 'from-red-500 to-red-600',
      module: 'Business Rule Violations'
    },
    {
      icon: Layers,
      title: 'Data Granularity',
      description: 'Analyze data at different levels',
      color: 'from-indigo-500 to-indigo-600',
      module: 'Data Granularity'
    },
    {
      icon: Clock,
      title: 'Data Frequency',
      description: 'Monitor data update patterns',
      color: 'from-cyan-500 to-cyan-600',
      module: 'Data Frequency'
    }
  ];

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Data Profiling</h1>
          <p className="text-lg text-gray-600">
            Comprehensive tools for analyzing and understanding your data structure and quality
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <button
              key={index}
              onClick={() => onSubModuleChange(feature.module)}
              className={`text-left bg-gradient-to-br ${feature.color} p-6 rounded-xl text-white transform transition-all duration-200 hover:scale-105 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-${feature.color.split('-')[1]}-400`}
            >
              <feature.icon className="w-10 h-10 mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-white/80">{feature.description}</p>
            </button>
          ))}
        </div>

        <div className="mt-12 bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-2xl font-bold mb-4">Getting Started</h2>
          <div className="space-y-4">
            <p className="text-gray-600">
              Click on any of the data profiling features above to begin analyzing your data.
              Each tool provides specific insights:
            </p>
            <ul className="list-disc list-inside space-y-2 text-gray-600 ml-4">
              <li>Use <span className="font-semibold">Data Quality</span> for basic quality metrics</li>
              <li>Check <span className="font-semibold">Column Correlation</span> to understand data relationships</li>
              <li>Analyze <span className="font-semibold">Fact & Dimension Tables</span> for data warehouse insights</li>
              <li>Review <span className="font-semibold">Business Rule Violations</span> to ensure data compliance</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}