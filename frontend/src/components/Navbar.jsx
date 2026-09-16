import React from 'react';
import { Search, Bell, Shield, Radio, RefreshCw } from 'lucide-react';

export default function Navbar({ health, onRefresh, isMonitoring, toggleMonitoring, search, setSearch }) {
  const activeModel = health?.active_model || 'XGBoost';
  const isHealthy = health?.status === 'online';

  return (
    <header className="h-16 border-b border-slate-800 bg-[#0b0f17]/90 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Search Input */}
      <div className="relative w-72">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search IP, protocol, attack type..."
          className="w-full bg-slate-900/80 text-sm text-slate-200 placeholder-slate-500 rounded-lg pl-9 pr-4 py-1.5 border border-slate-800 focus:outline-none focus:border-indigo-500 transition-colors"
        />
      </div>

      {/* Action Buttons & Status Indicators */}
      <div className="flex items-center gap-4">
        {/* Real-time Monitoring Toggle */}
        <button
          onClick={toggleMonitoring}
          className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all shadow-sm ${
            isMonitoring
              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 hover:bg-emerald-500/30 animate-pulse'
              : 'bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700'
          }`}
        >
          <Radio className={`w-3.5 h-3.5 ${isMonitoring ? 'text-emerald-400' : 'text-slate-400'}`} />
          <span>{isMonitoring ? 'STOP MONITORING' : 'START MONITORING'}</span>
        </button>

        {/* Refresh button */}
        <button
          onClick={onRefresh}
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
          title="Refresh Data"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        {/* Active Model Pill */}
        <div className="flex items-center gap-2 px-3 py-1 bg-slate-900 border border-slate-800 rounded-lg text-xs">
          <Shield className="w-3.5 h-3.5 text-indigo-400" />
          <span className="text-slate-400">Model:</span>
          <span className="font-semibold text-indigo-300">{activeModel}</span>
        </div>

        {/* System Health Badge */}
        <div className="flex items-center gap-2 px-3 py-1 bg-slate-900 border border-slate-800 rounded-lg text-xs">
          <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-emerald-400' : 'bg-rose-500'}`}></span>
          <span className="text-slate-400">System:</span>
          <span className={`font-semibold ${isHealthy ? 'text-emerald-400' : 'text-rose-400'}`}>
            {isHealthy ? 'ONLINE' : 'OFFLINE'}
          </span>
        </div>
      </div>
    </header>
  );
}
