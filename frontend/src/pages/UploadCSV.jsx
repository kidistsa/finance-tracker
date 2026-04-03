import React, { useState } from 'react';
import { transactionService } from '../services/api';

const UploadCSV = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please select a file');
      return;
    }
    setUploading(true);
    setMessage('');
    try {
      const response = await transactionService.uploadCSV(file);
      setMessage(`Success! Uploaded ${response.data.length} transactions`);
      setFile(null);
    } catch (error) {
      setMessage('Error uploading file: ' + (error.response?.data?.detail || 'Unknown error'));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Upload CSV</h1>
      <div style={styles.card}>
        <p>Upload your bank statement CSV file</p>
        <form onSubmit={handleSubmit}>
          <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} style={styles.input} />
          <button type="submit" disabled={uploading} style={styles.button}>
            {uploading ? 'Uploading...' : 'Upload CSV'}
          </button>
        </form>
        {message && <div style={styles.message}>{message}</div>}
        {/* <div style={styles.sample}>
          <h4>Sample CSV Format:</h4>
          <pre>date,amount,description,category,transaction_type
2024-03-25,50.00,Starbucks Coffee,food_groceries,expense
2024-03-25,1200.00,Salary Payment,other_income,income</pre>
        </div> */}
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '800px', margin: '0 auto' },
  card: { background: 'white', padding: '2rem', borderRadius: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  input: { display: 'block', margin: '1rem 0', padding: '0.5rem' },
  button: { background: 'linear-gradient(135deg, #d64daf 0%, #b83e8f 100%)', color: 'white', border: 'none', padding: '0.75rem 1.5rem', borderRadius: '5px', cursor: 'pointer' },
  message: { marginTop: '1rem', padding: '0.75rem', background: '#e8f5e9', color: '#2e7d32', borderRadius: '5px' },
  sample: { marginTop: '2rem', padding: '1rem', background: '#f5f5f5', borderRadius: '5px' },
};

export default UploadCSV;

