import React, { useState } from 'react';
import { Login } from './components/Login';
import { Sidebar } from './components/Sidebar';
import { DataQuality } from './components/DataQuality';
import { Dashboard } from './components/Dashboard';
import { DataProfilingOverview } from './components/DataProfilingOverview';
import type { TableMetrics, User } from './types';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [activeModule, setActiveModule] = useState('');
  const [activeSubModule, setActiveSubModule] = useState('');

  const handleLogin = (email: string) => {
    setUser({ email });
  };

  const handleSubModuleChange = (subModule: string) => {
    setActiveSubModule(subModule);
  };

  const mockFetchData = async (): Promise<TableMetrics> => {
    // Simulating API call
    return {
      category1: {
        missing_values: {
          category_id: 0,
          category_name: 0
        },
        duplicate_rows: 0,
        null_values_percentage: {
          category_id: 0,
          category_name: 0
        },
        duplicate_percentage: 0,
        completeness_percentage: {
          category_id: 100,
          category_name: 100
        },
        uniqueness_percentage: {
          category_id: 100,
          category_name: 100
        }
      }
    };
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="flex">
      <Sidebar
        activeModule={activeModule}
        onModuleChange={setActiveModule}
        subModule={activeSubModule}
        onSubModuleChange={handleSubModuleChange}
      />
      <main className="flex-1 bg-gray-100 min-h-screen">
        {!activeModule && <Dashboard />}
        {activeModule === 'dataProfiler' && !activeSubModule && (
          <DataProfilingOverview onSubModuleChange={handleSubModuleChange} />
        )}
        {activeModule === 'dataProfiler' && activeSubModule === 'Data Quality' && (
          <DataQuality onFetchData={mockFetchData} />
        )}
        {activeModule === 'dataProfiler' && activeSubModule && activeSubModule !== 'Data Quality' && (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">{activeSubModule}</h2>
            <p className="text-gray-600">This feature is coming soon.</p>
          </div>
        )}
        {activeModule !== 'dataProfiler' && activeModule !== '' && (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Coming Soon</h2>
            <p className="text-gray-600">This feature is under development.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;