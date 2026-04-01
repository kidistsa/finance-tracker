import React, { useState, useEffect } from 'react';
import { transactionService } from '../services/api';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await transactionService.getAll({ limit: 100 });
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={styles.loading}>Loading transactions...</div>;

  return (
    <div style={styles.container}>
      <h1>Transactions</h1>
      <div style={styles.card}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th>Date</th><th>Description</th><th>Category</th><th>Type</th><th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map(t => (
              <tr key={t.id}>
                <td>{new Date(t.date).toLocaleDateString()}</td>
                <td>{t.description}</td>
                <td>{t.category}</td>
                <td>{t.transaction_type}</td>
                <td style={{ color: t.transaction_type === 'income' ? '#4BC0C0' : '#FF6384' }}>
                  ${t.amount}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '1200px', margin: '0 auto' },
  card: { background: 'white', padding: '1.5rem', borderRadius: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  table: { width: '100%', borderCollapse: 'collapse' },
  loading: { textAlign: 'center', padding: '2rem' },
};

export default Transactions;
