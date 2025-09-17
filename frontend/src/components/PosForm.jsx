/* frontend/src/components/PosForm.jsx */

/**
 * POS Form: Line item input, checkout.
 * Offline: Queues via service worker.
 * DPDP: Consent check for customer phone.
 */
import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '../services/api';
import { useTranslation } from 'react-i18next';

const PosForm = () => {
  const { t } = useTranslation();
  const [lineItems, setLineItems] = useState([]);
  const [productName, setProductName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [consentGiven, setConsentGiven] = useState(false);

  const mutation = useMutation({
    mutationFn: (data) => api.post('/pos/bills', data),
    onSuccess: () => {
      setLineItems([]);
      setCustomerPhone('');
      setConsentGiven(false);
    },
  });

  const addItem = () => {
    if (productName) {
      setLineItems([...lineItems, { product_name: productName, quantity: 1, price: 100.0 }]);
      setProductName('');
    }
  };

  const handleCheckout = () => {
    if (customerPhone && !consentGiven) {
      alert(t('consent_required'));
      return;
    }
    mutation.mutate({
      line_items: lineItems,
      customer_phone: customerPhone || null,
      consent_given: consentGiven,
    });
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4">{t('pos.title')}</h2>
      <input
        type="text"
        value={productName}
        onChange={(e) => setProductName(e.target.value)}
        placeholder={t('pos.product_name')}
        className="w-full p-2 mb-2 border rounded"
      />
      <button onClick={addItem} className="bg-blue-500 text-white p-2 rounded mb-2">
        {t('pos.add_item')}
      </button>
      {lineItems.map((item, index) => (
        <div key={index} className="flex justify-between mb-2">
          <span>{item.product_name}</span>
          <span>{item.quantity} x ₹{item.price}</span>
        </div>
      ))}
      <input
        type="text"
        value={customerPhone}
        onChange={(e) => setCustomerPhone(e.target.value)}
        placeholder={t('pos.customer_phone')}
        className="w-full p-2 mb-2 border rounded"
      />
      <label className="flex items-center mb-2">
        <input
          type="checkbox"
          checked={consentGiven}
          onChange={(e) => setConsentGiven(e.target.checked)}
        />
        <span className="ml-2">{t('pos.consent')}</span>
      </label>
      <button
        onClick={handleCheckout}
        className="bg-green-500 text-white p-2 rounded w-full"
        disabled={mutation.isPending}
      >
        {mutation.isPending ? t('pos.processing') : t('pos.checkout')}
      </button>
    </div>
  );
};

export default PosForm;
