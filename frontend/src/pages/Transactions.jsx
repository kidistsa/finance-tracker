import React, { useState, useEffect, useCallback } from 'react';
import { useTheme } from '../context/themeContext';
import BackButton from '../components/BackButton';

const Transactions = () => {
  const { darkMode } = useTheme();
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [filters, setFilters] = useState({
    start_date: '',
    end_date: '',
    category: '',
    limit: 20
  });

  const fetchTransactions = useCallback(async () => {
    try {
      setLoading(true);
      setError('');
      const token = localStorage.getItem('token');
      
      const params = new URLSearchParams();
      if (filters.start_date) params.append('start_date', filters.start_date);
      if (filters.end_date) params.append('end_date', filters.end_date);
      if (filters.category) params.append('category', filters.category);
      params.append('limit', filters.limit);
      params.append('offset', (page - 1) * filters.limit);
      
      const url = 'http://localhost:9000/api/transactions?' + params.toString();
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      
      if (!response.ok) throw new Error(HTTP );
      
      const data = await response.json();
      
      if (page === 1) {
        setTransactions(data);
      } else {
        setTransactions(prev => [...prev, ...data]);
      }
      setHasMore(data.length === filters.limit);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setError('Failed to load transactions. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [filters, page]);

  useEffect(() => {
    setPage(1);
    fetchTransactions();
  }, [filters]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
    setPage(1);
  };

  const resetFilters = () => {
    setFilters({
      start_date: '',
      end_date: '',
      category: '',
      limit: 20
    });
    setPage(1);
  };

  const loadMore = () => {
    if (hasMore && !loading) {
      setPage(prev => prev + 1);
    }
  };

  if (loading && page === 1) return <div style={{ ...styles.loading, color: darkMode ? '#fff' : '#1a2a4f' }}>Loading transactions...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <BackButton defaultPath="/dashboard" />
        <h1 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Transactions</h1>
      </div>

      <div style={{ ...styles.filtersCard, background: darkMode ? '#16213e' : 'white' }}>
        <div style={styles.filtersGrid}>
          <div style={styles.filterGroup}>
            <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Start Date</label>
            <input type="date" name="start_date" value={filters.start_date} onChange={handleFilterChange} style={{ ...styles.filterInput, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }} />
          </div>
          <div style={styles.filterGroup}>
            <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>End Date</label>
            <input type="date" name="end_date" value={filters.end_date} onChange={handleFilterChange} style={{ ...styles.filterInput, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }} />
          </div>
          <div style={styles.filterGroup}>
            <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Category</label>
            <select name="category" value={filters.category} onChange={handleFilterChange} style={{ ...styles.filterInput, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }}>
              <option value="">All Categories</option>
              <option value="food_groceries">Food & Groceries</option>
              <option value="transportation">Transportation</option>
              <option value="shopping">Shopping</option>
              <option value="entertainment">Entertainment</option>
              <option value="utilities">Utilities</option>
              <option value="housing">Housing</option>
            </select>
          </div>
          <div style={styles.filterGroup}>
            <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Limit</label>
            <select name="limit" value={filters.limit} onChange={handleFilterChange} style={{ ...styles.filterInput, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }}>
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
        <div style={styles.filterActions}>
          <button onClick={fetchTransactions} style={styles.applyBtn}>Apply Filters</button>
          <button onClick={resetFilters} style={styles.resetBtn}>Reset</button>
        </div>
      </div>

      <div style={{ ...styles.card, background: darkMode ? '#16213e' : 'white' }}>
        <div style={styles.tableHeader}>
          <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Transaction History</h3>
          <span style={{ color: darkMode ? '#a0aec0' : '#718096' }}>{transactions.length} transactions</span>
        </div>
        {transactions.length === 0 ? (
          <div style={{ ...styles.noData, color: darkMode ? '#a0aec0' : '#718096' }}>
            <p>No transactions found. Upload a CSV file to get started!</p>
          </div>
        ) : (
          <>
            <div style={styles.tableWrapper}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Date</th>
                    <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Description</th>
                    <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Category</th>
                    <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Type</th>
                    <th style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map(t => (
                    <tr key={t.id}>
                      <td style={{ color: darkMode ? '#eee' : '#2d3748' }}>{new Date(t.date).toLocaleDateString()}</td>
                      <td style={{ color: darkMode ? '#eee' : '#2d3748' }}>{t.description}</td>
                      <td><span style={{ ...styles.categoryBadge, background: darkMode ? '#2d3748' : '#edf2f7' }}>{t.category}</span></td>
                      <td><span style={{ ...styles.typeBadge, background: t.transaction_type === 'income' ? '#4bc0c0' : '#ff6384', color: 'white' }}>{t.transaction_type}</span></td>
                      <td style={{ color: t.transaction_type === 'income' ? '#4bc0c0' : '#ff6384', fontWeight: 'bold' }}>
                        {t.transaction_type === 'income' ? '+' : '-'}Br {t.amount}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {hasMore && (
              <div style={styles.loadMore}>
                <button onClick={loadMore} disabled={loading} style={styles.loadMoreBtn}>
                  {loading ? 'Loading...' : 'Load More'}
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '1400px', margin: '0 auto' },
  header: { display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' },
  filtersCard: { padding: '1.5rem', borderRadius: '12px', marginBottom: '2rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  filtersGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' },
  filterGroup: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  filterInput: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '6px', fontSize: '0.9rem' },
  filterActions: { display: 'flex', gap: '1rem', justifyContent: 'flex-end' },
  applyBtn: { padding: '0.5rem 1.5rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' },
  resetBtn: { padding: '0.5rem 1.5rem', background: '#e2e8f0', color: '#4a5568', border: 'none', borderRadius: '6px', cursor: 'pointer' },
  card: { borderRadius: '12px', overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  tableHeader: { padding: '1rem 1.5rem', borderBottom: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  tableWrapper: { overflowX: 'auto' },
  table: { width: '100%', borderCollapse: 'collapse' },
  categoryBadge: { padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' },
  typeBadge: { padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', textTransform: 'capitalize' },
  noData: { textAlign: 'center', padding: '3rem' },
  loading: { textAlign: 'center', padding: '2rem', fontSize: '1.2rem' },
  loadMore: { textAlign: 'center', padding: '1rem' },
  loadMoreBtn: { padding: '0.5rem 1.5rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }
};

export default Transactions;
