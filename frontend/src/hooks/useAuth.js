// frontend/src/hooks/useAuth.js
/**
 * Auth Hook: JWT storage, login/logout, consent check.
 * Uses localStorage for token; React Query for mutations.
 * DPDP: Track consent in storage, prompt if missing.
 */
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import api from '../services/api';  // Axios

export const useAuth = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [hasConsent, setHasConsent] = useState(localStorage.getItem('consent') === 'true');
  const queryClient = useQueryClient();

  const loginMutation = useMutation({
    mutationFn: async ({ email, password }) => {
      const { data } = await api.post('/auth/token', { username: email, password });
      localStorage.setItem('token', data.access_token);
      setToken(data.access_token);
      return data;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user'] }),
  });

  const grantConsent = useMutation({
    mutationFn: async (purposes) => {
      // POST /auth/consent
      await api.post('/auth/consent', { purposes });
      localStorage.setItem('consent', 'true');
      setHasConsent(true);
    },
  });

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('consent');
    setToken(null);
    setHasConsent(false);
    queryClient.clear();
  };

  useEffect(() => {
    if (!token) {
      api.defaults.headers.common['Authorization'] = '';
    } else {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, [token]);

  return {
    token,
    hasConsent,
    login: loginMutation.mutate,
    grantConsent: grantConsent.mutate,
    logout,
    isLoading: loginMutation.isPending || grantConsent.isPending,
  };
};