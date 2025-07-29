import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { transactionsAPI } from '../../services/api';
import { Transaction } from '../../types';

export const TransactionsScreen = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const result = await transactionsAPI.getTransactions();
      setTransactions(result);
    } catch (error) {
      Alert.alert('Error', 'Failed to load transactions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const renderTransaction = ({ item: transaction }: { item: Transaction }) => (
    <View style={styles.transactionContainer}>
      <View style={styles.transactionHeader}>
        <Text style={styles.date}>
          {formatDate(transaction.createdAt)}
        </Text>
        <Text style={styles.amount}>
          ${transaction.amount.toFixed(2)}
        </Text>
      </View>

      <Text style={styles.description}>
        {transaction.description}
      </Text>

      <View style={styles.detailsContainer}>
        <Text style={styles.category}>
          Category: {transaction.category}
        </Text>
        {transaction.rewardValue && (
          <Text style={styles.reward}>
            Reward: {transaction.rewardValue.toFixed(2)}
          </Text>
        )}
      </View>

      {transaction.merchant && (
        <Text style={styles.merchant}>
          Merchant: {transaction.merchant}
        </Text>
      )}

      {transaction.location && (
        <Text style={styles.location}>
          Location: {transaction.location}
        </Text>
      )}

      {transaction.isForeign && (
        <Text style={styles.foreignTag}>
          Foreign Transaction
        </Text>
      )}
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
        data={transactions}
        renderItem={renderTransaction}
        keyExtractor={transaction => transaction.id}
        contentContainerStyle={styles.listContainer}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>
              No transactions yet.
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
  transactionContainer: {
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  transactionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  date: {
    fontSize: 14,
    color: '#666',
  },
  amount: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#000',
  },
  description: {
    fontSize: 16,
    color: '#000',
    marginBottom: 8,
  },
  detailsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  category: {
    fontSize: 14,
    color: '#666',
  },
  reward: {
    fontSize: 14,
    color: '#28a745',
    fontWeight: '600',
  },
  merchant: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  location: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  foreignTag: {
    fontSize: 12,
    color: '#dc3545',
    marginTop: 4,
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