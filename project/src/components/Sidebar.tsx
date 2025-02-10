import React from 'react';
import { Database, LineChart, Terminal, Brain } from 'lucide-react';

interface SidebarProps {
  activeModule: string;
  onModuleChange: (module: string) => void;
  subModule?: string;
  onSubModuleChange?: (subModule: string) => void;
}

export function Sidebar({ activeModule, onModuleChange, subModule, onSubModuleChange }: SidebarProps) {
  const mainModules = [
    { id: 'dataProfiler', name: 'Data Profiling', icon: Database },
    { id: 'anomaly', name: 'Anomaly Detection', icon: LineChart },
    { id: 'sqlGenerator', name: 'SQL Generator', icon: Terminal },
    { id: 'nlp', name: 'Natural Language Processing', icon: Brain },
  ];

  const dataProfilingSubModules = [
    'Data Quality',
    'Column Correlation',
    'Fact Table And Dimension Table',
    'Primary Key Foreign Key Relation',
    'Statistical Analysis',
    'Business Rule Violations',
    'Data Granularity',
    'Data Frequency',
  ];

  return (
    <div className="w-64 bg-gray-800 text-white h-screen flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h1 className="text-2xl font-bold">SigmaDQ</h1>
      </div>
      <nav className="flex-1 overflow-y-auto">
        <ul className="p-2">
          {mainModules.map((module) => (
            <li key={module.id}>
              <button
                onClick={() => onModuleChange(module.id)}
                className={`w-full flex items-center p-2 rounded-md mb-1 ${
                  activeModule === module.id ? 'bg-blue-600' : 'hover:bg-gray-700'
                }`}
              >
                <module.icon className="w-5 h-5 mr-2" />
                {module.name}
              </button>
              {activeModule === 'dataProfiler' && module.id === 'dataProfiler' && onSubModuleChange && (
                <ul className="ml-4 mt-2 space-y-1">
                  {dataProfilingSubModules.map((subModuleName) => (
                    <li key={subModuleName}>
                      <button
                        onClick={() => onSubModuleChange(subModuleName)}
                        className={`w-full text-left p-2 rounded-md text-sm ${
                          subModule === subModuleName ? 'bg-gray-700' : 'hover:bg-gray-700'
                        }`}
                      >
                        {subModuleName}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}