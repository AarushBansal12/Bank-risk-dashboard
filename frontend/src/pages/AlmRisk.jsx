import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const AlmRisk = () => {
  const [shockData, setShockData] = useState([]);
  const [portfolioData, setPortfolioData] = useState([]);

  useEffect(() => {
    fetch('/api/alm/rate-shocks')
      .then(res => res.json())
      .then(data => setShockData(data));
      
    fetch('/api/alm/portfolio')
      .then(res => res.json())
      .then(data => setPortfolioData(data));
  }, []);

  return (
    <div>
      <h1 className="text-gradient">ALM & Liquidity Risk (IRRBB)</h1>
      <p className="text-secondary" style={{ marginBottom: '2rem' }}>
        Interest Rate Risk in the Banking Book (IRRBB) simulated rate shocks and ALM portfolio metrics.
      </p>
      
      <div className="grid-charts">
        <div className="glass-panel" style={{ height: '400px' }}>
          <h3>Net Interest Income (NII) Sensitivities</h3>
          <p className="text-secondary" style={{ fontSize: '12px', marginBottom: '10px' }}>1-Year Gap Analysis under standard rate shocks (bps)</p>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={shockData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="shock_bps" tickFormatter={(val) => (val > 0 ? '+' : '') + val + ' bps'} />
              <YAxis tickFormatter={(val) => '$' + (val/1e6).toFixed(0) + 'M'} />
              <Tooltip formatter={(value) => '$' + (value/1e6).toFixed(2) + 'M'} />
              <ReferenceLine y={0} stroke="rgba(255,255,255,0.2)" />
              <Bar dataKey="nii_impact">
                {
                  shockData.map((entry, index) => (
                    <cell key={`cell-${index}`} fill={entry.nii_impact > 0 ? 'var(--accent-success)' : 'var(--accent-danger)'} />
                  ))
                }
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-panel" style={{ height: '400px' }}>
          <h3>ALM Portfolio Balances</h3>
          <p className="text-secondary" style={{ fontSize: '12px', marginBottom: '10px' }}>Assets vs Liabilities by Category</p>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={portfolioData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" angle={-45} textAnchor="end" height={60} />
              <YAxis tickFormatter={(val) => '$' + (val/1e9).toFixed(1) + 'B'} />
              <Tooltip formatter={(value) => '$' + (value/1e9).toFixed(2) + 'B'} />
              <Bar dataKey="total_balance" fill="var(--accent-warning)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AlmRisk;
