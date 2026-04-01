import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

interface Transaction {
  id: string;
  description: string;
  amount: number;
  date: Date;
  category?: string;
}

interface CategoryRule {
  patterns: RegExp[];
  category: string;
  subcategory?: string;
}

export class TransactionCategorizer {
  private rules: CategoryRule[] = [
    {
      patterns: [/uber/i, /lyft/i, /taxi/i, /transit/i, /metro/i],
      category: 'Transportation',
      subcategory: 'Rideshare'
    },
    {
      patterns: [/starbucks/i, /cafe/i, /restaurant/i, /dining/i, /grubhub/i, /doordash/i],
      category: 'Food & Dining',
      subcategory: 'Restaurants'
    },
    {
      patterns: [/walmart/i, /target/i, /kroger/i, /safeway/i, /grocery/i, /whole foods/i],
      category: 'Food & Dining',
      subcategory: 'Groceries'
    },
    {
      patterns: [/netflix/i, /hulu/i, /spotify/i, /apple music/i, /disney\+/i],
      category: 'Entertainment',
      subcategory: 'Subscriptions'
    },
    {
      patterns: [/amazon/i, /ebay/i, /etsy/i, /online shopping/i],
      category: 'Shopping',
      subcategory: 'Online'
    },
    {
      patterns: [/rent/i, /mortgage/i, /apartment/i],
      category: 'Housing',
      subcategory: 'Rent/Mortgage'
    },
    {
      patterns: [/electric/i, /water/i, /gas bill/i, /internet/i, /phone bill/i, /utility/i],
      category: 'Bills & Utilities',
      subcategory: 'Utilities'
    }
  ];

  public categorize(transaction: Transaction): Transaction {
    const description = transaction.description;
    
    for (const rule of this.rules) {
      for (const pattern of rule.patterns) {
        if (pattern.test(description)) {
          return {
            ...transaction,
            category: rule.category
          };
        }
      }
    }
    
    return {
      ...transaction,
      category: 'Uncategorized'
    };
  }

  public async batchCategorize(transactions: Transaction[]): Promise<Transaction[]> {
    return transactions.map(t => this.categorize(t));
  }

  public async learnFromHistory(userId: string): Promise<void> {
    // ML model training based on user's historical categorization
    // This would be called periodically to improve accuracy
    const db = admin.firestore();
    const transactions = await db.collection('transactions')
      .where('userId', '==', userId)
      .where('category', '!=', 'Uncategorized')
      .limit(1000)
      .get();
    
    // Extract features and train model
    // This is where you'd integrate with TensorFlow.js or similar
    functions.logger.info(`Learning from ${transactions.size} transactions for user ${userId}`);
  }
}