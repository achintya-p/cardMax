import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { User, Card, Transaction, CardRecommendation } from '../types';

// For iOS simulator, use localhost
const API_URL = 'http://localhost:8000';  // We'll need to update this for production

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    await AsyncStorage.setItem('token', response.data.access_token);
    return response.data;
  },

  register: async (email: string, password: string) => {
    const response = await api.post('/auth/register', { email, password });
    await AsyncStorage.setItem('token', response.data.access_token);
    return response.data;
  },

  logout: async () => {
    await AsyncStorage.removeItem('token');
  },
};

export const cardsAPI = {
  getCards: async (): Promise<Card[]> => {
    const response = await api.get('/cards');
    return response.data;
  },

  addCard: async (cardId: string): Promise<void> => {
    await api.post('/wallet/cards', { cardId });
  },

  removeCard: async (cardId: string): Promise<void> => {
    await api.delete(`/wallet/cards/${cardId}`);
  },

  getRecommendation: async (
    amount: number,
    description: string,
    isForeign: boolean = false
  ): Promise<CardRecommendation> => {
    const response = await api.post('/cards/recommend', {
      amount,
      description,
      is_foreign: isForeign,
    });
    return response.data;
  },
};

export const transactionsAPI = {
  getTransactions: async (): Promise<Transaction[]> => {
    const response = await api.get('/transactions');
    return response.data;
  },

  addTransaction: async (transaction: Omit<Transaction, 'id' | 'createdAt'>): Promise<Transaction> => {
    const response = await api.post('/transactions', transaction);
    return response.data;
  },
}; 