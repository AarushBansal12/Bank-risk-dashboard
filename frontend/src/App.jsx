import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { LayoutDashboard, ShieldAlert, BarChart3, Activity } from 'lucide-react';
import Overview from './pages/Overview';
import CreditRisk from './pages/CreditRisk';
import AlmRisk from './pages/AlmRisk';

function App() {
  return (
    <Router>
      <div className="dashboard-layout">
        <aside className="sidebar">
          <div>
            <h2 className="text-gradient" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldAlert size={28} />
              RiskEngine
            </h2>
            <p className="text-secondary" style={{ fontSize: '13px', marginTop: '4px' }}>
              Enterprise Risk Dashboard
            </p>
          </div>
          
          <nav className="nav-links">
            <NavLink to="/" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
              <LayoutDashboard size={20} />
              Overview
            </NavLink>
            <NavLink to="/credit" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
              <BarChart3 size={20} />
              Credit Risk
            </NavLink>
            <NavLink to="/alm" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
              <Activity size={20} />
              ALM & Liquidity
            </NavLink>
          </nav>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/credit" element={<CreditRisk />} />
            <Route path="/alm" element={<AlmRisk />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
