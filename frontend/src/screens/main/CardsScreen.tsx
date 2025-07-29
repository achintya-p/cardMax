import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { cardsAPI } from '../../services/api';
import { Card, Category } from '../../types';

export const CardsScreen = () => {
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCards();
  }, []);

  const loadCards = async () => {
    try {
      setLoading(true);
      const result = await cardsAPI.getCards();
      setCards(result);
    } catch (error) {
      Alert.alert('Error', 'Failed to load cards. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveCard = async (cardId: string) => {
    try {
      await cardsAPI.removeCard(cardId);
      setCards(cards.filter(card => card.id !== cardId));
      Alert.alert('Success', 'Card removed from your wallet');
    } catch (error) {
      Alert.alert('Error', 'Failed to remove card. Please try again.');
    }
  };

  const renderRewards = (rewards: Record<Category, number>) => {
    return Object.entries(rewards).map(([category, rate]) => (
      <Text key={category} style={styles.rewardText}>
        {category}: {rate}%
      </Text>
    ));
  };

  const renderCard = ({ item: card }: { item: Card }) => (
    <View style={styles.cardContainer}>
      <View style={styles.cardHeader}>
        <Text style={styles.cardName}>{card.name}</Text>
        <Text style={styles.cardIssuer}>{card.issuer}</Text>
      </View>

      <View style={styles.rewardsContainer}>
        <Text style={styles.sectionTitle}>Rewards</Text>
        {renderRewards(card.rewards)}
      </View>

      <View style={styles.feesContainer}>
        <Text style={styles.sectionTitle}>Fees</Text>
        <Text style={styles.feeText}>
          Annual Fee: ${card.annualFee.toFixed(2)}
        </Text>
        <Text style={styles.feeText}>
          Foreign Transaction: {card.foreignTransactionFee}%
        </Text>
      </View>

      {card.signUpBonus && (
        <Text style={styles.bonusText}>
          Sign-up Bonus: {card.signUpBonus}
        </Text>
      )}

      <TouchableOpacity
        style={styles.removeButton}
        onPress={() => handleRemoveCard(card.id)}
      >
        <Text style={styles.removeButtonText}>Remove from Wallet</Text>
      </TouchableOpacity>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={cards}
        renderItem={renderCard}
        keyExtractor={card => card.id}
        contentContainerStyle={styles.listContainer}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>
              No cards in your wallet yet.
            </Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContainer: {
    padding: 16,
  },
  cardContainer: {
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  cardHeader: {
    marginBottom: 12,
  },
  cardName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#000',
  },
  cardIssuer: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginBottom: 8,
  },
  rewardsContainer: {
    marginBottom: 12,
  },
  rewardText: {
    fontSize: 14,
    color: '#28a745',
    marginBottom: 4,
  },
  feesContainer: {
    marginBottom: 12,
  },
  feeText: {
    fontSize: 14,
    color: '#dc3545',
    marginBottom: 4,
  },
  bonusText: {
    fontSize: 14,
    color: '#007AFF',
    marginBottom: 12,
  },
  removeButton: {
    backgroundColor: '#dc3545',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  removeButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
}); 