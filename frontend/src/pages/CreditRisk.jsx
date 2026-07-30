import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#ec4899'];

const CreditRisk = () => {
  const [sectorData, setSectorData] = useState([]);
  const [ratingData, setRatingData] = useState([]);

  useEffect(() => {
    fetch('/api/credit/sector-exposure')
      .then(res => res.json())
      .then(data => setSectorData(data));
      
    fetch('/api/credit/rating-dist')
      .then(res => res.json())
      .then(data => setRatingData(data));
  }, []);

  return (
    <div>
      <h1 className="text-gradient">Credit Risk Analysis</h1>
      <p className="text-secondary" style={{ marginBottom: '2rem' }}>
        Detailed breakdown of sector exposures, non-performing assets (NPA), and credit ratings.
      </p>
      
      <div className="grid-charts">
        <div className="glass-panel" style={{ height: '400px' }}>
          <h3>Sector Exposure</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={sectorData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" tickFormatter={(val) => '$' + (val/1e9).toFixed(1) + 'B'} />
              <YAxis dataKey="Sector" type="category" width={100} />
              <Tooltip formatter={(value) => '$' + (value/1e9).toFixed(2) + 'B'} />
              <Bar dataKey="Exposure" fill="var(--accent-primary)" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-panel" style={{ height: '400px' }}>
          <h3>Rating Distribution</h3>
          <ResponsiveContainer width="100%" height="90%">
            <PieChart>
              <Pie
                data={ratingData}
                dataKey="Exposure"
                nameKey="Credit_Rating"
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                fill="#82ca9d"
                label={({ Credit_Rating, percent }) => `${Credit_Rating} ${(percent * 100).toFixed(0)}%`}
              >
                {ratingData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => '$' + (value/1e9).toFixed(2) + 'B'} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default CreditRisk;
