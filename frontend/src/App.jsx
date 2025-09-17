// frontend/src/App.jsx
/**
 * Main App: Routing, Auth, Localization.
 * Mobile-first: Tailwind classes for sm: breakpoints.
 */
import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';  // For Hindi/Tamil etc.
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PosForm from './components/PosForm';
import ConsentModal from './components/ConsentModal';

const queryClient = new QueryClient();

function App() {
  const { t, i18n } = useTranslation();  // Load lang: i18n.changeLanguage('hi')

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-100 p-4 sm:p-6">  {/* Mobile padding */}
          <header className="mb-4">
            <h1 className="text-2xl font-bold text-center">{t('app.title')}</h1>  {/* Localized */}
            <select onChange={(e) => i18n.changeLanguage(e.target.value)} className="ml-auto">
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
              <option value="ta">தமிழ்</option>
            </select>
          </header>
          <ConsentModal />  {/* DPDP: Show on load if no consent */}
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/pos" element={<PosForm />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;