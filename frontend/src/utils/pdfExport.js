import jsPDF from 'jspdf';

export const exportTransactionsToPDF = (transactions, summary, period, periodStart, periodEnd) => {
  const doc = new jsPDF();
  
  // Header
  doc.setFillColor(214, 77, 175);
  doc.rect(0, 0, 210, 35, 'F');
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(20);
  doc.text('Birr Finance Tracker', 14, 20);
  
  // Title
  doc.setTextColor(0, 0, 0);
  doc.setFontSize(16);
  doc.text('Transaction Report', 14, 50);
  
  // Summary
  doc.setFontSize(11);
  doc.text(`Total Income: Br ${summary.total_income?.toFixed(2) || 0}`, 14, 70);
  doc.text(`Total Expenses: Br ${summary.total_expenses?.toFixed(2) || 0}`, 14, 78);
  doc.text(`Net Savings: Br ${summary.net_savings?.toFixed(2) || 0}`, 14, 86);
  doc.text(`Transactions: ${summary.transaction_count || 0}`, 14, 94);
  
  // Simple table using text
  let y = 110;
  doc.setFontSize(10);
  doc.text('Date', 14, y);
  doc.text('Description', 50, y);
  doc.text('Amount', 160, y);
  y += 6;
  
  transactions.slice(0, 20).forEach(t => {
    if (y > 270) {
      doc.addPage();
      y = 20;
    }
    doc.text(new Date(t.date).toLocaleDateString(), 14, y);
    doc.text(t.description.substring(0, 25), 50, y);
    const amount = `${t.transaction_type === 'income' ? '+' : '-'}Br ${t.amount}`;
    doc.text(amount, 160, y);
    y += 6;
  });
  
  // Footer
  doc.setFontSize(8);
  doc.setTextColor(150, 150, 150);
  doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 290);
  
  doc.save(`report_${new Date().toISOString().slice(0, 10)}.pdf`);
};