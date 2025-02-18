import React from 'react';
import { Shield, Database, LineChart, Brain } from 'lucide-react';

export function Dashboard() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Welcome to SigmaDQ</h1>
        <p className="text-lg text-gray-600">Your comprehensive data quality management solution</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-8 rounded-2xl text-white">
          <Shield className="w-12 h-12 mb-4" />
          <h2 className="text-2xl font-bold mb-2">Secure Data Handling</h2>
          <p className="text-blue-100">Your data is protected with enterprise-grade security measures</p>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 p-8 rounded-2xl text-white">
          <Database className="w-12 h-12 mb-4" />
          <h2 className="text-2xl font-bold mb-2">Advanced Profiling</h2>
          <p className="text-purple-100">Comprehensive data profiling with detailed analytics</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-gradient-to-br from-green-500 to-green-600 p-8 rounded-2xl text-white">
          <LineChart className="w-12 h-12 mb-4" />
          <h2 className="text-2xl font-bold mb-2">Anomaly Detection</h2>
          <p className="text-green-100">Identify and analyze data anomalies with precision</p>
        </div>
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-8 rounded-2xl text-white">
          <Brain className="w-12 h-12 mb-4" />
          <h2 className="text-2xl font-bold mb-2">AI-Powered Analysis</h2>
          <p className="text-orange-100">Leverage machine learning for deeper insights</p>
        </div>
      </div>

      <div className="mt-12 text-center">
        <p className="text-gray-600">Select a module from the sidebar to get started</p>
      </div>
    </div>
  );
}