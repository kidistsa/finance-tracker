import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { useTheme } from '../context/themeContext';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const MonthlyComparison = () => {
  const { darkMode } = useTheme();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [months, setMonths] = useState(6);

  useEffect(() => {
    fetchMonthlyData();
  }, [months]);

  const fetchMonthlyData = async () => {
    try {
      const token = localStorage.getItem('token');
      const url = 'http://localhost:9000/api/analytics/monthly-comparison?months=' + months;
      const response = await fetch(url, {
        headers: { Authorization: 'Bearer ' + token }
      });
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Error fetching monthly data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={styles.loading}>Loading monthly comparison...</div>;

  const chartData = {
    labels: data.map(d => d.month),
    datasets: [
      {
        label: 'Income',
        data: data.map(d => d.income),
        backgroundColor: '#4BC0C0',
        borderRadius: 8,
      },
      {
        label: 'Expenses',
        data: data.map(d => d.expense),
        backgroundColor: '#FF6384',
        borderRadius: 8,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: darkMode ? '#fff' : '#333',
          font: { size: 12 }
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            label += 'Br ' + context.raw.toLocaleString();
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        ticks: {
          color: darkMode ? '#fff' : '#333',
          callback: function(value) {
            return 'Br ' + value.toLocaleString();
          }
        },
        grid: {
          color: darkMode ? '#2d3748' : '#e2e8f0'
        },
        title: {
          display: true,
          text: 'Amount (Br)',
          color: darkMode ? '#fff' : '#333'
        }
      },
      x: {
        ticks: {
          color: darkMode ? '#fff' : '#333'
        },
        grid: {
          color: darkMode ? '#2d3748' : '#e2e8f0'
        }
      }
    }
  };

  const totalIncome = data.reduce((sum, d) => sum + d.income, 0);
  const totalExpense = data.reduce((sum, d) => sum + d.expense, 0);
  const bestMonth = data.reduce((best, d) => d.savings > best.savings ? d : best, data[0] || { savings: 0 });

  return (
    <div style={{ ...styles.container, background: darkMode ? '#16213e' : 'white' }}>
      <div style={styles.header}>
        <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Monthly Income vs Expenses</h3>
        <select 
          value={months} 
          onChange={(e) => setMonths(parseInt(e.target.value))}
          style={{ ...styles.select, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#e2e8f0' }}
        >
          <option value="3">Last 3 Months</option>
          <option value="6">Last 6 Months</option>
          <option value="12">Last 12 Months</option>
        </select>
      </div>

      <div style={styles.chartContainer}>
        <Bar data={chartData} options={options} />
      </div>

      <div style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Total Income</span>
          <span style={{ ...styles.summaryValue, color: '#4BC0C0' }}>Br {totalIncome.toLocaleString()}</span>
        </div>
        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Total Expenses</span>
          <span style={{ ...styles.summaryValue, color: '#FF6384' }}>Br {totalExpense.toLocaleString()}</span>
        </div>
      </div>

      {bestMonth && bestMonth.savings !== undefined && (
        <div style={styles.bestMonth}>
          🏆 Best Month: {bestMonth.month} (Saved Br {bestMonth.savings.toLocaleString()})
        </div>
      )}
    </div>
  );
};

const styles = {
  container: { 
    padding: '1.5rem', 
    borderRadius: '12px', 
    marginBottom: '2rem',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
  },
  header: { 
    display: 'flex', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    marginBottom: '1.5rem',
    flexWrap: 'wrap',
    gap: '1rem'
  },
  select: { 
    padding: '0.5rem', 
    borderRadius: '8px', 
    border: '1px solid',
    cursor: 'pointer'
  },
  chartContainer: { height: '400px', marginBottom: '1.5rem' },
  summaryGrid: { 
    display: 'grid', 
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
    gap: '1rem', 
    marginTop: '1rem',
    marginBottom: '1rem'
  },
  summaryCard: { 
    display: 'flex', 
    justifyContent: 'space-between', 
    padding: '0.75rem', 
    background: 'rgba(0,0,0,0.03)', 
    borderRadius: '8px'
  },
  summaryLabel: { fontSize: '0.85rem', color: '#666' },
  summaryValue: { fontSize: '1rem', fontWeight: 'bold' },
  bestMonth: { 
    textAlign: 'center', 
    padding: '0.75rem', 
    background: 'rgba(75, 192, 192, 0.1)', 
    borderRadius: '8px',
    marginTop: '1rem',
    color: '#4BC0C0'
  },
  loading: { textAlign: 'center', padding: '2rem' }
};

export default MonthlyComparison;
