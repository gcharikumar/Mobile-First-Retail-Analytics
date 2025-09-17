// frontend/src/components/Dashboard.jsx
/**
 * Dashboard: Top products chart, alerts.
 * Uses Recharts for viz, React Query for fetch.
 * Offline: Cache with service worker.
 */
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';
import api from '../services/api';  // Axios instance

const Dashboard = () => {
  const { data: topProducts, isLoading } = useQuery({
    queryKey: ['top-products'],
    queryFn: () => api.get('/analytics/top-products').then(res => res.data),
    staleTime: 5 * 60 * 1000  // Cache 5min
  });

  if (isLoading) return <div className="text-center">Loading...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">  {/* Mobile stack */}
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-lg font-semibold mb-2">Top 5 Products</h2>
        <BarChart width={300} height={200} data={topProducts}>
          <XAxis dataKey="product" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="this_week" fill="#8884d8" />
          <Bar dataKey="last_week" fill="#82ca9d" />
        </BarChart>
      </div>
      <div className="bg-yellow-100 p-4 rounded">  {/* Alert */}
        <p>Festival Alert: Navratri demand for silk sarees rising!</p>
      </div>
    </div>
  );
};

export default Dashboard;

// package.json deps: react: ^18.3.1, @tanstack/react-query: ^5.59.0, recharts: ^2.12.7, i18next: ^23.15.1, vite-plugin-pwa: ^0.20.5