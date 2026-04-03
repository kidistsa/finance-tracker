import React, { useState, useEffect } from 'react';
import { recurringService } from '../services/recurringService';
import { useTheme } from '../context/themeContext';
import BackButton from '../components/BackButton';

const Recurring = () => {
  const { darkMode } = useTheme();
  const [recurring, setRecurring] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    amount: '',
    category: 'food_groceries',
    transaction_type: 'expense',
    frequency: 'monthly',
    start_date: new Date().toISOString().slice(0, 10),
    active: true
  });

  useEffect(() => { fetchRecurring(); }, []);

  const fetchRecurring = async () => {
    try { const res = await recurringService.getAll(); setRecurring(res.data); } 
    catch (error) { console.error('Error:', error); } 
    finally { setLoading(false); }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await recurringService.create({ ...formData, amount: parseFloat(formData.amount) });
      setShowForm(false);
      setFormData({ name: '', amount: '', category: 'food_groceries', transaction_type: 'expense', frequency: 'monthly', start_date: new Date().toISOString().slice(0, 10), active: true });
      fetchRecurring();
    } catch (error) { console.error('Error:', error); }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this recurring transaction?')) {
      await recurringService.delete(id);
      fetchRecurring();
    }
  };

  const frequencyLabels = { daily: 'Daily', weekly: 'Weekly', monthly: 'Monthly', yearly: 'Yearly' };

  if (loading) return <div style={styles.loading}>Loading recurring transactions...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <BackButton defaultPath="/dashboard" />
        <h1 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>Recurring Transactions</h1>
        <button onClick={() => setShowForm(true)} style={styles.createBtn}>+ Add Recurring</button>
      </div>

      {showForm && (
        <div style={styles.modal}>
          <div style={{ ...styles.modalContent, background: darkMode ? '#16213e' : 'white' }}>
            <h3>Add Recurring Transaction</h3>
            <form onSubmit={handleSubmit}>
              <input type="text" placeholder="Name" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} required style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }} />
              <input type="number" placeholder="Amount" value={formData.amount} onChange={(e) => setFormData({...formData, amount: e.target.value})} required style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }} />
              <select value={formData.transaction_type} onChange={(e) => setFormData({...formData, transaction_type: e.target.value})} style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }}>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
              <select value={formData.category} onChange={(e) => setFormData({...formData, category: e.target.value})} style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }}>
                <option value="food_groceries">Food & Groceries</option>
                <option value="transportation">Transportation</option>
                <option value="housing">Housing</option>
                <option value="utilities">Utilities</option>
              </select>
              <select value={formData.frequency} onChange={(e) => setFormData({...formData, frequency: e.target.value})} style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }}>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
              <input type="date" value={formData.start_date} onChange={(e) => setFormData({...formData, start_date: e.target.value})} required style={{ ...styles.input, background: darkMode ? '#0f3460' : 'white', color: darkMode ? '#fff' : '#333' }} />
              <div style={styles.modalButtons}>
                <button type="submit" style={styles.saveBtn}>Create</button>
                <button type="button" onClick={() => setShowForm(false)} style={styles.cancelBtn}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div style={styles.grid}>
        {recurring.map(r => (
          <div key={r.id} style={{ ...styles.card, background: darkMode ? '#16213e' : 'white' }}>
            <div style={styles.cardHeader}>
              <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>{r.name}</h3>
              <button onClick={() => handleDelete(r.id)} style={styles.deleteBtn}>×</button>
            </div>
            <div><strong>Amount:</strong> <span style={{ color: r.transaction_type === 'income' ? '#4bc0c0' : '#ff6384' }}>Br {r.amount}</span></div>
            <div><strong>Category:</strong> {r.category.replace('_', ' ').toUpperCase()}</div>
            <div><strong>Frequency:</strong> {frequencyLabels[r.frequency]}</div>
            <div><strong>Next:</strong> {new Date(r.next_occurrence).toLocaleDateString()}</div>
            <div><strong>Status:</strong> <span style={{ color: r.active ? '#4bc0c0' : '#ff6384' }}>{r.active ? 'Active' : 'Inactive'}</span></div>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '1200px', margin: '0 auto' },
  header: { display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' },
  createBtn: { padding: '0.5rem 1rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', marginLeft: 'auto' },
  modal: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 },
  modalContent: { padding: '2rem', borderRadius: '12px', width: '90%', maxWidth: '400px' },
  input: { width: '100%', padding: '0.75rem', marginBottom: '1rem', border: '1px solid #ddd', borderRadius: '8px', boxSizing: 'border-box' },
  modalButtons: { display: 'flex', gap: '1rem', justifyContent: 'flex-end' },
  saveBtn: { padding: '0.5rem 1rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' },
  cancelBtn: { padding: '0.5rem 1rem', background: '#e2e8f0', color: '#4a5568', border: 'none', borderRadius: '5px', cursor: 'pointer' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem' },
  card: { borderRadius: '12px', padding: '1rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' },
  deleteBtn: { background: '#ffebee', color: '#ff6384', border: 'none', width: '30px', height: '30px', borderRadius: '50%', cursor: 'pointer', fontSize: '1.2rem' },
  loading: { textAlign: 'center', padding: '2rem' }
};

export default Recurring;


