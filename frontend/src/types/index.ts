export interface User {
  id: string;
  email: string;
  isActive: boolean;
}

export interface Card {
  id: string;
  name: string;
  issuer: string;
  rewards: Record<Category, number>;
  rewardType: RewardType;
  annualFee: number;
  foreignTransactionFee: number;
  signUpBonus?: string;
}

export enum Category {
  DINING = 'dining',
  TRAVEL = 'travel',
  GROCERIES = 'groceries',
  GAS = 'gas',
  ENTERTAINMENT = 'entertainment',
  ONLINE_SHOPPING = 'online_shopping',
  OTHER = 'other'
}

export enum RewardType {
  POINTS = 'points',
  CASHBACK = 'cashback',
  MILES = 'miles'
}

export interface Transaction {
  id: string;
  description: string;
  amount: number;
  category: Category;
  cardId?: string;
  rewardValue?: number;
  isForeign: boolean;
  merchant?: string;
  location?: string;
  createdAt: string;
}

export interface CardRecommendation {
  card: Card;
  rewardValue: number;
  explanation: string;
} 