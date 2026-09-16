import React, { useState } from 'react';
import { Settings, Shield, Sliders, CheckCircle2, AlertOctagon } from 'lucide-react';

export default function SettingsPage() {
  const [threshold, setThreshold] = useState(20);
  const [autoAlert, setAutoAlert] = useState(true);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-wide">System & Security Settings</h1>
        <p className="text-xs text-slate-400 mt-1">Configure project-defined risk scoring parameters and interface parameters</p>
      </div>

      <div className="glass-panel p-6 rounded-xl border border-slate-800 space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
          <Sliders className="w-5 h-5 text-indigo-400" />
          <div>
            <h3 className="font-bold text-slate-200 text-sm">Threat Score Alert Threshold</h3>
            <p className="text-xs text-slate-400">Minimum threat score (0-100) required to automatically generate a security alert</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-300 font-medium">Alert Threshold Score</span>
            <span className="font-extrabold text-indigo-400 text-sm">{threshold} / 100</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            value={threshold}
            onChange={(e) => setThreshold(e.target.value)}
            className="w-full accent-indigo-500 bg-slate-900 h-2 rounded-lg cursor-pointer"
          />
          <div className="flex justify-between text-[11px] text-slate-500 font-mono">
            <span>0 (All Traffic)</span>
            <span>20 (Normal/Low)</span>
            <span>50 (Medium)</span>
            <span>80 (Critical Only)</span>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-5 flex items-center justify-between">
          <div>
            <h4 className="font-bold text-slate-200 text-xs">Automatic Alert Creation</h4>
            <p className="text-xs text-slate-400">Auto-persist alerts to SQLite database upon detecting high threat scores</p>
          </div>
          <button
            onClick={() => setAutoAlert(!autoAlert)}
            className={`w-12 h-6 rounded-full transition-colors p-1 flex items-center ${autoAlert ? 'bg-indigo-600 justify-end' : 'bg-slate-800 justify-start'}`}
          >
            <span className="w-4 h-4 rounded-full bg-white shadow-md"></span>
          </button>
        </div>

        <div className="border-t border-slate-800 pt-5 flex items-center justify-between">
          {saved ? (
            <span className="text-xs text-emerald-400 font-bold flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Settings Saved Successfully
            </span>
          ) : <div></div>}
          <button
            onClick={handleSave}
            className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-lg shadow-lg shadow-indigo-600/20 transition-colors"
          >
            Save Configuration
          </button>
        </div>
      </div>
    </div>
  );
}
