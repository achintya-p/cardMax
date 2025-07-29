import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Alert,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { cardsAPI } from '../../services/api';
import { CardRecommendation } from '../../types';

export const HomeScreen = () => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState<CardRecommendation | null>(null);

  const handleGetRecommendation = async () => {
    if (!amount || !description) {
      Alert.alert('Error', 'Please enter both amount and description');
      return;
    }

    try {
      setLoading(true);
      const result = await cardsAPI.getRecommendation(
        parseFloat(amount),
        description
      );
      setRecommendation(result);
    } catch (error) {
      Alert.alert('Error', 'Failed to get recommendation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Get Card Recommendation</Text>
        <Text style={styles.subtitle}>
          Enter your purchase details to find the best card
        </Text>
      </View>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Amount ($)"
          value={amount}
          onChangeText={setAmount}
          keyboardType="decimal-pad"
        />

        <TextInput
          style={styles.input}
          placeholder="Description (e.g., Restaurant, Gas)"
          value={description}
          onChangeText={setDescription}
        />

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleGetRecommendation}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? 'Getting recommendation...' : 'Get Recommendation'}
          </Text>
        </TouchableOpacity>
      </View>

      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
        </View>
      )}

      {recommendation && (
        <View style={styles.recommendationContainer}>
          <Text style={styles.recommendationTitle}>Recommended Card</Text>
          <View style={styles.cardContainer}>
            <Text style={styles.cardName}>{recommendation.card.name}</Text>
            <Text style={styles.cardIssuer}>{recommendation.card.issuer}</Text>
            <Text style={styles.rewardValue}>
              Estimated Reward: {recommendation.rewardValue.toFixed(2)}
            </Text>
            <Text style={styles.explanation}>{recommendation.explanation}</Text>
          </View>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    padding: 20,
    backgroundColor: '#f8f9fa',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
  form: {
    padding: 20,
  },
  input: {
    height: 50,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 15,
    fontSize: 16,
  },
  button: {
    height: 50,
    backgroundColor: '#007AFF',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  loadingContainer: {
    padding: 20,
    alignItems: 'center',
  },
  recommendationContainer: {
    padding: 20,
  },
  recommendationTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#000',
  },
  cardContainer: {
    backgroundColor: '#f8f9fa',
    padding: 20,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  cardName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 5,
  },
  cardIssuer: {
    fontSize: 16,
    color: '#666',
    marginBottom: 10,
  },
  rewardValue: {
    fontSize: 16,
    color: '#28a745',
    fontWeight: '600',
    marginBottom: 10,
  },
  explanation: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
}); 