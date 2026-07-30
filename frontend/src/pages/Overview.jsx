import React, { useState, useEffect } from 'react';

const Overview = () => {
  const [kpiData, setKpiData] = useState(null);
  const [lcrData, setLcrData] = useState(null);

  useEffect(() => {
    fetch('/api/credit/kpis')
      .then(res => res.json())
      .then(data => setKpiData(data[0]));
      
    fetch('/api/alm/lcr')
      .then(res => res.json())
      .then(data => setLcrData(data[0]));
  }, []);

  const formatCurrency = (val) => {
    if (!val) return '$0';
    return '$' + (val / 1e9).toFixed(2) + 'B';
  };

  return (
    <div>
      <h1 className="text-gradient">Executive Overview</h1>
      <p className="text-secondary" style={{ marginBottom: '2rem' }}>
        High-level risk indicators across the entire banking book.
      </p>
      
      <div className="grid-cards">
        <div className="glass-panel">
          <div className="kpi-title">Total Credit Exposure</div>
          <div className="kpi-value">{kpiData ? formatCurrency(kpiData.Total_Exposure) : '...'}</div>
          <div className="kpi-trend trend-up">Current Portfolio</div>
        </div>
        
        <div className="glass-panel">
          <div className="kpi-title">Overall NPA Ratio</div>
          <div className="kpi-value">{kpiData ? (kpiData.Avg_NPA_Ratio * 100).toFixed(2) + '%' : '...'}</div>
          <div className="kpi-trend trend-down">Needs Attention</div>
        </div>

        <div className="glass-panel">
          <div className="kpi-title">Liquidity Coverage (LCR)</div>
          <div className="kpi-value">{lcrData ? (lcrData.lcr_ratio * 100).toFixed(2) + '%' : '...'}</div>
          <div className={`kpi-trend ${lcrData?.lcr_ratio < 1 ? 'trend-down' : 'trend-up'}`}>
            {lcrData?.lcr_status || '...'}
          </div>
        </div>
        
        <div className="glass-panel">
          <div className="kpi-title">Total Expected Credit Loss</div>
          <div className="kpi-value">{kpiData ? formatCurrency(kpiData.Total_Expected_Loss) : '...'}</div>
          <div className="kpi-trend trend-down">ECL Provision</div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
