import React from 'react';
import { 
  ShieldAlert, 
  LayoutDashboard, 
  Activity, 
  AlertTriangle, 
  Radar, 
  BarChart3, 
  Cpu, 
  FileSearch, 
  Settings,
  Radio
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, isMonitoring }) {
  const navItems = [
    { id: 'dashboard', label: 'SOC Dashboard', icon: LayoutDashboard },
    { id: 'traffic', label: 'Network Traffic', icon: Activity },
    { id: 'alerts', label: 'Alert Management', icon: AlertTriangle },
    { id: 'detections', label: 'ML Detections', icon: Radar },
    { id: 'analytics', label: 'Threat Analytics', icon: BarChart3 },
    { id: 'models', label: 'ML Models', icon: Cpu },
    { id: 'pcap', label: 'PCAP Analysis', icon: FileSearch },
    { id: 'settings', label: 'System Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#0f172a] border-r border-slate-800 flex flex-col justify-between h-screen sticky top-0 z-30">
      <div>
        {/* Brand Header */}
        <div className="p-5 flex items-center gap-3 border-b border-slate-800">
          <div className="p-2.5 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg shadow-indigo-500/20">
            <ShieldAlert className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-slate-100 text-lg tracking-wider">AI-NIDS</h1>
            <p className="text-xs text-slate-400 font-medium">SOC Defense Platform</p>
          </div>
        </div>

        {/* Live Status Pill */}
        <div className="px-4 py-3 border-b border-slate-800/60 bg-slate-900/40">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Engine Status</span>
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${isMonitoring ? 'bg-emerald-400 animate-ping' : 'bg-indigo-400'}`}></span>
              <span className={`text-xs font-semibold ${isMonitoring ? 'text-emerald-400' : 'text-indigo-400'}`}>
                {isMonitoring ? 'LIVE CAPTURE' : 'READY'}
              </span>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg font-medium text-sm transition-all duration-150 ${
                  isActive
                    ? 'bg-gradient-to-r from-indigo-600/90 to-purple-600/90 text-white shadow-md shadow-indigo-600/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/40 text-xs text-slate-500">
        <p className="font-semibold text-slate-400">Authorized Lab Use Only</p>
        <p className="mt-0.5">Defensive NIDS Engine v1.0.0</p>
      </div>
    </aside>
  );
}
