/* frontend/test/pos_form.test.jsx */

/**
 * Vitest tests for PosForm component.
 * Mocks axios for API calls.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import PosForm from '../src/components/PosForm';
import api from '../src/services/api';
import { I18nextProvider } from 'react-i18next';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslation from '../src/i18n/en.json';

i18n.use(initReactI18next).init({
  resources: { en: { translation: enTranslation } },
  lng: 'en',
});

vi.mock('../src/services/api');

test('PosForm adds item and submits', async () => {
  api.post.mockResolvedValue({ data: {} });
  render(
    <I18nextProvider i18n={i18n}>
      <PosForm />
    </I18nextProvider>
  );

  fireEvent.change(screen.getByPlaceholderText('Product Name (e.g., saree)'), {
    target: { value: 'saree' },
  });
  fireEvent.click(screen.getByText('Add Item'));
  expect(screen.getByText('saree')).toBeInTheDocument();

  fireEvent.click(screen.getByText('Checkout'));
  expect(api.post).toHaveBeenCalledWith('/pos/bills', {
    line_items: [{ product_name: 'saree', quantity: 1, price: 100.0 }],
    customer_phone: null,
    consent_given: false,
  });
});