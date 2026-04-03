import React, { useState, useRef } from 'react';
import { useTheme } from '../context/themeContext';
import BackButton from '../components/BackButton';

const ReceiptScanner = () => {
  const { darkMode } = useTheme();
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setExtractedData(null);
      setError('');
    }
  };

  const handleScan = async () => {
    if (!image) {
      setError('Please select a receipt image first');
      return;
    }

    setScanning(true);
    setError('');

    const formData = new FormData();
    formData.append('file', image);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:9000/api/receipt-scanner/scan', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token
        },
        body: formData
      });

      const data = await response.json();
      
      if (response.ok) {
        setResult(data);
        setExtractedData(data.extracted_data);
      } else {
        setError(data.detail || 'Failed to scan receipt');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setScanning(false);
    }
  };

  const handleCreateTransaction = async () => {
    if (!extractedData || !extractedData.total) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:9000/api/transactions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({
          amount: extractedData.total,
          description: extractedData.merchant || 'Receipt Purchase',
          category: 'shopping',
          transaction_type: 'expense',
          date: extractedData.date || new Date().toISOString(),
          source: 'receipt_scanner'
        })
      });

      if (response.ok) {
        alert('? Transaction created successfully!');
        setImage(null);
        setPreview(null);
        setResult(null);
        setExtractedData(null);
        if (fileInputRef.current) fileInputRef.current.value = '';
      } else {
        alert('Failed to create transaction');
      }
    } catch (err) {
      alert('Error creating transaction');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <BackButton defaultPath="/dashboard" />
        <h1 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>?? Receipt Scanner</h1>
      </div>

      <div style={{ ...styles.card, background: darkMode ? '#16213e' : 'white' }}>
        <p style={{ color: darkMode ? '#a0aec0' : '#4a5568', marginBottom: '1rem' }}>
          Take a photo of your receipt and we'll automatically extract the transaction details!
        </p>

        {/* Upload Area */}
        <div 
          style={styles.uploadArea}
          onClick={() => fileInputRef.current?.click()}
        >
          {preview ? (
            <img src={preview} alt="Receipt preview" style={styles.preview} />
          ) : (
            <div style={styles.uploadPlaceholder}>
              <span style={styles.uploadIcon}>??</span>
              <p>Click or tap to upload receipt image</p>
              <small>Supports JPG, PNG, PDF</small>
            </div>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            style={{ display: 'none' }}
          />
        </div>

        {error && <div style={styles.error}>{error}</div>}

        {preview && !result && (
          <button 
            onClick={handleScan} 
            disabled={scanning} 
            style={styles.scanBtn}
          >
            {scanning ? '?? Scanning...' : '?? Scan Receipt'}
          </button>
        )}

        {/* Results */}
        {extractedData && (
          <div style={styles.results}>
            <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>?? Extracted Data</h3>
            
            <div style={styles.resultRow}>
              <strong>Merchant:</strong> 
              <span>{extractedData.merchant || 'Not detected'}</span>
            </div>
            
            <div style={styles.resultRow}>
              <strong>Date:</strong> 
              <span>{extractedData.date || 'Not detected'}</span>
            </div>
            
            <div style={styles.resultRow}>
              <strong>Total Amount:</strong> 
              <span style={{ color: '#4bc0c0', fontWeight: 'bold' }}>
                Br {extractedData.total || 'Not detected'}
              </span>
            </div>
            
            {extractedData.items && extractedData.items.length > 0 && (
              <>
                <strong>Items:</strong>
                <div style={styles.itemsList}>
                  {extractedData.items.slice(0, 5).map((item, idx) => (
                    <div key={idx} style={styles.itemRow}>
                      <span>{item.description}</span>
                      <span>Br {item.amount}</span>
                    </div>
                  ))}
                </div>
              </>
            )}

            {extractedData.total && (
              <button onClick={handleCreateTransaction} style={styles.createBtn}>
                ? Create Transaction
              </button>
            )}
          </div>
        )}

        {result?.transaction && (
          <div style={{ ...styles.success, marginTop: '1rem' }}>
            ? Transaction created! Check your transactions page.
          </div>
        )}
      </div>

      <div style={{ ...styles.card, background: darkMode ? '#16213e' : 'white', marginTop: '1rem' }}>
        <h3 style={{ color: darkMode ? '#fff' : '#1a2a4f' }}>?? Tips for Best Results</h3>
        <ul style={{ color: darkMode ? '#a0aec0' : '#4a5568' }}>
          <li>Take photo in good lighting</li>
          <li>Keep the receipt flat and centered</li>
          <li>Make sure the total amount is clearly visible</li>
          <li>Avoid shadows or glare on the receipt</li>
        </ul>
      </div>
    </div>
  );
};

const styles = {
  container: { padding: '2rem', maxWidth: '800px', margin: '0 auto' },
  header: { display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' },
  card: { padding: '1.5rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  uploadArea: { 
    border: '2px dashed #d64daf', 
    borderRadius: '12px', 
    padding: '2rem', 
    textAlign: 'center',
    cursor: 'pointer',
    marginBottom: '1rem',
    transition: 'all 0.2s'
  },
  uploadPlaceholder: { color: '#a0aec0' },
  uploadIcon: { fontSize: '3rem', display: 'block', marginBottom: '0.5rem' },
  preview: { maxWidth: '100%', maxHeight: '300px', borderRadius: '8px' },
  scanBtn: { width: '100%', padding: '0.75rem', background: '#d64daf', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '1rem' },
  results: { marginTop: '1rem', padding: '1rem', background: 'rgba(0,0,0,0.03)', borderRadius: '8px' },
  resultRow: { display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #e2e8f0' },
  itemsList: { marginTop: '0.5rem', padding: '0.5rem', background: 'rgba(0,0,0,0.02)', borderRadius: '8px' },
  itemRow: { display: 'flex', justifyContent: 'space-between', padding: '0.25rem 0' },
  createBtn: { width: '100%', padding: '0.75rem', marginTop: '1rem', background: '#4bc0c0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' },
  error: { background: '#ffebee', color: '#c62828', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem' },
  success: { background: '#e8f5e9', color: '#2e7d32', padding: '0.75rem', borderRadius: '8px' }
};

export default ReceiptScanner;

