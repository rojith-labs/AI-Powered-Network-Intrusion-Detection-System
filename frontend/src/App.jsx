import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';

import DashboardPage from './pages/DashboardPage';
import TrafficPage from './pages/TrafficPage';
import AlertsPage from './pages/AlertsPage';
import DetectionsPage from './pages/DetectionsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ModelsPage from './pages/ModelsPage';
import PcapAnalysisPage from './pages/PcapAnalysisPage';
import SettingsPage from './pages/SettingsPage';

import { fetchHealth, fetchDashboard } from './services/api';
import { MonitoringWebSocket } from './services/websocket';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [health, setHealth] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [search, setSearch] = useState('');
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [wsInstance, setWsInstance] = useState(null);

  const loadData = async () => {
    try {
      const h = await fetchHealth();
      setHealth(h);
      const d = await fetchDashboard();
      setDashboardData(d);
    } catch (err) {
      console.error('Failed to load backend metrics:', err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);

  const toggleMonitoring = () => {
    if (isMonitoring) {
      if (wsInstance) wsInstance.disconnect();
      setIsMonitoring(false);
    } else {
      const ws = new MonitoringWebSocket(
        (data) => {
          // Received live flow
          loadData();
        },
        (err) => console.error('WS Error:', err),
        (status) => setIsMonitoring(status)
      );
      ws.connect();
      setWsInstance(ws);
    }
  };

  const handleSelectAlert = (alert) => {
    setSelectedAlert(alert);
    setActiveTab('alerts');
  };

  return (
    <div className="flex min-h-screen bg-[#0b0f17] text-slate-100 font-sans antialiased">
      {/* Sidebar */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        isMonitoring={isMonitoring} 
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar 
          health={health} 
          onRefresh={loadData} 
          isMonitoring={isMonitoring}
          toggleMonitoring={toggleMonitoring}
          search={search}
          setSearch={setSearch}
        />

        <main className="p-6 flex-1 overflow-y-auto">
          {activeTab === 'dashboard' && (
            <DashboardPage 
              data={dashboardData} 
              onSelectAlert={handleSelectAlert} 
              setActiveTab={setActiveTab} 
            />
          )}

          {activeTab === 'traffic' && (
            <TrafficPage search={search} />
          )}

          {activeTab === 'alerts' && (
            <AlertsPage 
              search={search} 
              selectedAlert={selectedAlert} 
              onSelectAlert={setSelectedAlert} 
            />
          )}

          {activeTab === 'detections' && (
            <DetectionsPage />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsPage />
          )}

          {activeTab === 'models' && (
            <ModelsPage />
          )}

          {activeTab === 'pcap' && (
            <PcapAnalysisPage />
          )}

          {activeTab === 'settings' && (
            <SettingsPage />
          )}
        </main>
      </div>
    </div>
  );
}
