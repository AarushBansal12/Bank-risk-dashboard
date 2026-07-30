import React, { useState, useEffect } from 'react';

const Overview = () => {
  const [kpiData, setKpiData] = useState(null);
  const [lcrData, setLcrData] = useState(null);
  const [totalEcl, setTotalEcl] = useState(null);

  useEffect(() => {
    fetch('/api/credit/kpis')
      .then(res => res.json())
      .then(data => setKpiData(data[0]));
      
    fetch('/api/alm/lcr')
      .then(res => res.json())
      .then(data => setLcrData(data[0]));
      
    fetch('/api/credit/ecl-summary')
      .then(res => res.json())
      .then(data => {
        const sumEcl = data.reduce((acc, row) => acc + (row.approx_ECL || 0), 0);
        setTotalEcl(sumEcl);
      });
  }, []);

  const formatCurrency = (val) => {
    if (val === undefined || val === null) return '$0';
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
          <div className="kpi-value">{kpiData ? formatCurrency(kpiData.total_exposure) : '...'}</div>
          <div className="kpi-trend trend-up">Current Portfolio</div>
        </div>
        
        <div className="glass-panel">
          <div className="kpi-title">Overall NPA Ratio</div>
          <div className="kpi-value">{kpiData ? (kpiData.npa_percentage).toFixed(2) + '%' : '...'}</div>
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
          <div className="kpi-value">{totalEcl !== null ? formatCurrency(totalEcl) : '...'}</div>
          <div className="kpi-trend trend-down">ECL Provision</div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
