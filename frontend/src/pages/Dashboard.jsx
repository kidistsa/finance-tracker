import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/authContext';
import { transactionService } from '../services/api';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Dashboard = () => {
  const { token, logout } = useAuth();
  const [summary, setSummary] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [summaryRes, transactionsRes] = await Promise.all([
        transactionService.getSummary('month'),
        transactionService.getAll({ limit: 10 })
      ]);
      setSummary(summaryRes.data);
      setTransactions(transactionsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={styles.loading}>Loading dashboard...</div>;

  // Chart Data
  const categoryData = transactions.reduce((acc, t) => {
    if (t.transaction_type === 'expense') {
      acc[t.category] = (acc[t.category] || 0) + t.amount;
    }
    return acc;
  }, {});

  const doughnutData = {
    labels: Object.keys(categoryData),
    datasets: [{
      data: Object.values(categoryData),
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
    }],
  };

  const barData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      { label: 'Income', data: [1200, 1350, 1400, 1200], backgroundColor: '#4BC0C0' },
      { label: 'Expenses', data: [450, 520, 480, 600], backgroundColor: '#FF6384' },
    ],
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>Dashboard</h1>
        <button onClick={logout} style={styles.logoutBtn}>Logout</button>
      </div>

      <div style={styles.grid}>
        <div style={styles.card}><h3>Total Income</h3><p style={{...styles.amount, color: '#4BC0C0'}}></p></div>
        <div style={styles.card}><h3>Total Expenses</h3><p style={{...styles.amount, color: '#FF6384'}}></p></div>
        <div style={styles.card}><h3>Net Savings</h3><p style={{...styles.amount, color: '#36A2EB'}}></p></div>
        <div style={styles.card}><h3>Transactions</h3><p style={styles.amount}>{summary?.transaction_count || 0}</p></div>
      </div>

      <div style={styles.chartsGrid}>
        <div style={styles.chartCard}><h3>Spending by Category</h3><Doughnut data={doughnutData} /></div>
        <div style={styles.chartCard}><h3>Weekly Trend</h3><Bar data={barData} /></div>
      </div>

      <div style={styles.recentCard}>
        <h3>Recent Transactions</h3>
        <table style={styles.table}>
          <thead><tr><th>Date</th><th>Description</th><th>Category</th><th>Amount</th></tr></thead>
          <tbody>
            {transactions.map(t => (
              <tr key={t.id}>
                <td>{new Date(t.date).toLocaleDateString()}</td>
                <td>{t.description}</td>
                <td>{t.category}</td>
                <td style={{ color: t.transaction_type === 'income' ? '#4BC0C0' : '#FF6384' }}>
                  {t.transaction_type === 'income' ? '+' : '-'}
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
  container: { padding: '2rem', maxWidth: '1400px', margin: '0 auto' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' },
  logoutBtn: { padding: '0.5rem 1rem', background: '#ff6384', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '2rem' },
  card: { background: 'white', padding: '1.5rem', borderRadius: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  amount: { fontSize: '2rem', fontWeight: 'bold', marginTop: '0.5rem' },
  chartsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem', marginBottom: '2rem' },
  chartCard: { background: 'white', padding: '1.5rem', borderRadius: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  recentCard: { background: 'white', padding: '1.5rem', borderRadius: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  table: { width: '100%', borderCollapse: 'collapse', marginTop: '1rem' },
  loading: { textAlign: 'center', padding: '2rem', fontSize: '1.2rem' },
};

export default Dashboard;
