import React, { useState, useEffect } from 'react';
import { budgetService } from '../services/api';

const Budgets = () => {
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ category: '', amount: '', month: new Date().toISOString().slice(0, 7) });

  useEffect(() => { fetchBudgets(); }, []);

  const fetchBudgets = async () => {
    try { const res = await budgetService.getAll(); setBudgets(res.data); } 
    catch (error) { console.error('Error:', error); } 
    finally { setLoading(false); }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await budgetService.create({ ...formData, amount: parseFloat(formData.amount) });
      setShowForm(false);
      setFormData({ category: '', amount: '', month: new Date().toISOString().slice(0, 7) });
      fetchBudgets();
    } catch (error) { console.error('Error:', error); }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this budget?')) {
      await budgetService.delete(id);
      fetchBudgets();
    }
  };

  if (loading) return <div style={styles.loading}>Loading budgets...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}><h1>Budgets</h1><button onClick={() => setShowForm(true)} style={styles.createBtn}>+ Create Budget</button></div>
      {showForm && (
        <div style={styles.modal}>
          <div style={styles.modalContent}>
            <h3>Create New Budget</h3>
            <form onSubmit={handleSubmit}>
              <select value={formData.category} onChange={(e) => setFormData({...formData, category: e.target.value})} required>
                <option value="">Select Category</option>
                <option value="food_groceries">Food & Groceries</option><option value="transportation">Transportation</option>
                <option value="shopping">Shopping</option><option value="entertainment">Entertainment</option>
                <option value="utilities">Utilities</option><option value="housing">Housing</option>
              </select>
              <input type="number" placeholder="Amount" value={formData.amount} onChange={(e) => setFormData({...formData, amount: e.target.value})} required />
              <input type="month" value={formData.month} onChange={(e) => setFormData({...formData, month: e.target.value})} required />
              <div><button type="submit">Create</button><button type="button" onClick={() => setShowForm(false)}>Cancel</button></div>
            </form>
          </div>
        </div>
      )}
      <div style={styles.grid}>{budgets.map(b => (
        <div key={b.id} style={styles.card}>
          <div><h3>{b.category}</h3><button onClick={() => handleDelete(b.id)} style={styles.deleteBtn}>×</button></div>
          <p>Budget: ${b.amount}</p><p>Spent: ${b.spent || 0}</p><p>Remaining: ${b.remaining || b.amount}</p>
          <div style={styles.progress}><div style={{...styles.progressFill, width: `${Math.min((b.spent / b.amount) * 100, 100)}%` }} /></div>
          <small>{b.month}</small>
        </div>
      ))}</div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '1200px', margin: '0 auto' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' },
  createBtn: { padding: '0.5rem 1rem', background: '#4BC0C0', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' },
  card: { background: 'white', padding: '1rem', borderRadius: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  deleteBtn: { float: 'right', background: '#ff6384', color: 'white', border: 'none', borderRadius: '50%', width: '25px', height: '25px', cursor: 'pointer' },
  progress: { background: '#e0e0e0', borderRadius: '10px', height: '10px', margin: '1rem 0' },
  progressFill: { background: '#4BC0C0', borderRadius: '10px', height: '10px' },
  modal: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center' },
  modalContent: { background: 'white', padding: '2rem', borderRadius: '10px', width: '400px' },
  loading: { textAlign: 'center', padding: '2rem' },
};

export default Budgets;
