import React, { useState, useEffect } from 'react';
import { budgetService } from '../services/api';
import { useTheme } from '../context/themeContext';
import BackButton from '../components/BackButton';

const Budgets = () => {
  const { darkMode } = useTheme();
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    category: '',
    amount: '',
    month: new Date().toISOString().slice(0, 7),
    notification_threshold: 80,
    rollover_enabled: false
  });

  useEffect(() => {
    fetchBudgets();
  }, []);

  const fetchBudgets = async () => {
    try {
      const response = await budgetService.getAll();
      setBudgets(response.data);
    } catch (error) {
      console.error('Error fetching budgets:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await budgetService.create({
        ...formData,
        amount: parseFloat(formData.amount)
      });
      setShowForm(false);
      setFormData({
        category: '',
        amount: '',
        month: new Date().toISOString().slice(0, 7),
        notification_threshold: 80,
        rollover_enabled: false
      });
      fetchBudgets();
    } catch (error) {
      console.error('Error creating budget:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this budget?')) {
      await budgetService.delete(id);
      fetchBudgets();
    }
  };

  if (loading) return <div style={{ ...styles.loading, color: darkMode ? '#fff' : '#1a2a4f' }}>Loading budgets...</div>;

  return (
    
    <div style={styles.container}>
      <div style={styles.header}>
        <BackButton defaultPath="/dashboard" />
        <h1 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Budgets</h1>
        <button onClick={() => setShowForm(true)} style={styles.createBtn}>+ Create Budget</button>
      </div>

      {showForm && (
        <div style={styles.modal}>
          <div style={{ ...styles.modalContent, background: darkMode ? '#16213e' : 'white', color: darkMode ? '#eee' : '#333' }}>
            <h2 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Create New Budget</h2>
            <form onSubmit={handleSubmit}>
              <div style={styles.formGroup}>
                <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  required
                  style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#e2e8f0' }}
                >
                  <option value="">Select Category</option>
                  <option value="food_groceries">Food & Groceries</option>
                  <option value="transportation">Transportation</option>
                  <option value="shopping">Shopping</option>
                  <option value="entertainment">Entertainment</option>
                  <option value="utilities">Utilities</option>
                  <option value="housing">Housing</option>
                  <option value="healthcare">Healthcare</option>
                </select>
              </div>
              <div style={styles.formGroup}>
                <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Budget Amount (Br)</label>
                <input
                  type="number"
                  step="0.01"
                  placeholder="Enter amount"
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                  required
                  style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#e2e8f0' }}
                />
              </div>
              <div style={styles.formGroup}>
                <label style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Month</label>
                <input
                  type="month"
                  value={formData.month}
                  onChange={(e) => setFormData({ ...formData, month: e.target.value })}
                  required
                  style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333', borderColor: darkMode ? '#2d3748' : '#e2e8f0' }}
                />
              </div>
              <div style={styles.modalActions}>
                <button type="submit" style={styles.submitBtn}>Create Budget</button>
                <button type="button" onClick={() => setShowForm(false)} style={styles.cancelBtn}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div style={styles.grid}>
        {budgets.length === 0 ? (
          <div style={{ ...styles.emptyState, background: darkMode ? '#16213e' : 'white', color: darkMode ? '#eee' : '#718096' }}>
            <p>No budgets yet. Click "Create Budget" to get started!</p>
          </div>
        ) : (
          budgets.map(b => {
            const percentage = Math.min((b.spent / b.amount) * 100, 100);
            return (
              <div key={b.id} style={{ ...styles.card, background: darkMode ? '#16213e' : 'white' }}>
                <div style={styles.cardHeader}>
                  <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>{b.category.replace('_', ' ').toUpperCase()}</h3>
                  <button onClick={() => handleDelete(b.id)} style={styles.deleteBtn}>×</button>
                </div>
                <div style={styles.budgetDetails}>
                  <div style={styles.budgetRow}>
                    <span style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Budget:</span>
                    <strong style={{ color: darkMode ? '#fff' : '#333' }}>Br {b.amount}</strong>
                  </div>
                  <div style={styles.budgetRow}>
                    <span style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Spent:</span>
                    <strong style={{ color: percentage > 80 ? '#ff6384' : '#4bc0c0' }}>Br {b.spent || 0}</strong>
                  </div>
                  <div style={styles.budgetRow}>
                    <span style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>Remaining:</span>
                    <strong style={{ color: darkMode ? '#fff' : '#333' }}>Br {(b.remaining || b.amount) - (b.spent || 0)}</strong>
                  </div>
                </div>
                <div style={styles.progressBar}>
                  <div style={{ ...styles.progressFill, width: `${percentage}%`, background: percentage > 80 ? '#ff6384' : '#4bc0c0' }} />
                </div>
                <div style={styles.cardFooter}>
                  <span style={{ ...styles.month, background: darkMode ? '#2d3748' : '#edf2f7', color: darkMode ? '#e2e8f0' : '#4a5568' }}>{b.month}</span>
                  <span style={{ color: darkMode ? '#a0aec0' : '#718096' }}>{percentage.toFixed(0)}% used</span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '1400px', margin: '0 auto' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' },
  createBtn: { padding: '0.75rem 1.5rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '500' },
  modal: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 },
  modalContent: { padding: '2rem', borderRadius: '12px', width: '90%', maxWidth: '500px' },
  formGroup: { marginBottom: '1rem' },
  input: { width: '100%', padding: '0.75rem', border: '1px solid', borderRadius: '6px', fontSize: '1rem', boxSizing: 'border-box' },
  modalActions: { display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '1.5rem' },
  submitBtn: { padding: '0.75rem 1.5rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' },
  cancelBtn: { padding: '0.75rem 1.5rem', background: '#e2e8f0', color: '#4a5568', border: 'none', borderRadius: '6px', cursor: 'pointer' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem' },
  emptyState: { textAlign: 'center', padding: '3rem', borderRadius: '12px' },
  card: { borderRadius: '12px', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', transition: 'transform 0.2s' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' },
  deleteBtn: { background: '#ffebee', color: '#ff6384', border: 'none', width: '30px', height: '30px', borderRadius: '50%', cursor: 'pointer', fontSize: '1.2rem' },
  budgetDetails: { marginBottom: '1rem' },
  budgetRow: { display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.9rem' },
  progressBar: { background: '#e2e8f0', borderRadius: '10px', height: '8px', margin: '1rem 0' },
  progressFill: { borderRadius: '10px', height: '100%', transition: 'width 0.3s' },
  cardFooter: { display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginTop: '0.5rem' },
  month: { padding: '0.25rem 0.5rem', borderRadius: '4px' },
  loading: { textAlign: 'center', padding: '2rem', fontSize: '1.2rem' }
};

export default Budgets;

