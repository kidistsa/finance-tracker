import jsPDF from 'jspdf';
import 'jspdf-autotable';

export const exportTransactionsToPDF = (transactions, summary) => {
  const doc = new jsPDF();
  
  // Title
  doc.setFontSize(20);
  doc.text('Finance Tracker Report', 14, 22);
  
  // Summary
  doc.setFontSize(12);
  doc.text(`Period: ${new Date().toLocaleDateString()}`, 14, 35);
  doc.text(`Total Income: $${summary.total_income.toFixed(2)}`, 14, 42);
  doc.text(`Total Expenses: $${summary.total_expenses.toFixed(2)}`, 14, 49);
  doc.text(`Net Savings: $${summary.net_savings.toFixed(2)}`, 14, 56);
  
  // Transactions Table
  const tableData = transactions.map(t => [
    new Date(t.date).toLocaleDateString(),
    t.description,
    t.category,
    t.transaction_type,
    `$${t.amount.toFixed(2)}`
  ]);
  
  doc.autoTable({
    head: [['Date', 'Description', 'Category', 'Type', 'Amount']],
    body: tableData,
    startY: 70,
  });
  
  doc.save('finance-report.pdf');
};