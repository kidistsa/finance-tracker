import React from 'react';
import { useTheme } from '../context/themeContext';
import ReceiptScanner from '../components/ReceiptScanner';

const ReceiptScannerPage = () => {
  const { darkMode } = useTheme();

  return (
    <div>
      <ReceiptScanner />
    </div>
  );
};

export default ReceiptScannerPage;

