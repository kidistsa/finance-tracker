import React, { createContext, useState, useContext, useEffect } from 'react';

const DataContext = createContext();

export const useData = () => useContext(DataContext);

export const DataProvider = ({ children }) => {
  const [summary, setSummary] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setLoading(false);
        return;
      }
      
      try {
        const [summaryRes, txRes] = await Promise.all([
          fetch('http://localhost:9000/api/transactions/summary?period=month', {
            headers: { 'Authorization': 'Bearer ' + token }
          }),
          fetch('http://localhost:9000/api/transactions?limit=50', {
            headers: { 'Authorization': 'Bearer ' + token }
          })
        ]);
        
        if (summaryRes.ok && txRes.ok) {
          const summaryData = await summaryRes.json();
          const txData = await txRes.json();
          setSummary(summaryData);
          setTransactions(txData);
        }
      } catch (err) {
        console.error('Error loading data:', err);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, []);

  return (
    <DataContext.Provider value={{ summary, transactions, loading }}>
      {children}
    </DataContext.Provider>
  );
};
