/* frontend/src/components/ConsentModal.jsx */

/**
 * Consent Modal: DPDP compliance for data usage.
 * Shown on first load if no consent.
 */
import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { useTranslation } from 'react-i18next';

const ConsentModal = () => {
  const { hasConsent, grantConsent } = useAuth();
  const { t } = useTranslation();

  if (hasConsent) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded max-w-sm mx-auto">
        <h2 className="text-lg font-semibold mb-4">{t('consent.title')}</h2>
        <p className="mb-4">{t('consent.message')}</p>
        <button
          onClick={() => grantConsent(['loyalty', 'analytics'])}
          className="bg-blue-500 text-white p-2 rounded mr-2"
        >
          {t('consent.accept')}
        </button>
        <button
          onClick={() => localStorage.setItem('consent', 'false')}
          className="bg-gray-500 text-white p-2 rounded"
        >
          {t('consent.deny')}
        </button>
      </div>
    </div>
  );
};

export default ConsentModal;