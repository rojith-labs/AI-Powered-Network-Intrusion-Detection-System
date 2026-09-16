import React from 'react';

export default function ThreatGauge({ score, severity, label = "Threat Score" }) {
  // Score 0 to 100
  const normalizedScore = Math.max(0, Math.min(100, score || 0));

  const getColor = (sev) => {
    switch (sev) {
      case 'Normal': return { stroke: '#10b981', text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/30' };
      case 'Low': return { stroke: '#3b82f6', text: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/30' };
      case 'Medium': return { stroke: '#eab308', text: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30' };
      case 'High': return { stroke: '#f97316', text: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/30' };
      case 'Critical': return { stroke: '#ef4444', text: 'text-rose-400', bg: 'bg-rose-500/10', border: 'border-rose-500/30' };
      default: return { stroke: '#64748b', text: 'text-slate-400', bg: 'bg-slate-500/10', border: 'border-slate-500/30' };
    }
  };

  const style = getColor(severity);
  const strokeDashoffset = 283 - (283 * normalizedScore) / 100;

  return (
    <div className={`p-4 rounded-xl glass-panel ${style.bg} border ${style.border} flex items-center gap-4`}>
      {/* Circle Radial Progress */}
      <div className="relative w-20 h-20 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="45"
            className="stroke-slate-800"
            strokeWidth="8"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke={style.stroke}
            strokeWidth="8"
            strokeDasharray="283"
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-700 ease-out"
          />
        </svg>
        <span className={`absolute font-extrabold text-xl ${style.text}`}>
          {Math.round(normalizedScore)}
        </span>
      </div>

      <div>
        <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{label}</p>
        <p className={`text-lg font-bold mt-0.5 ${style.text}`}>{severity || 'Normal'}</p>
        <p className="text-[11px] text-slate-500 mt-0.5">Project-Defined Threat Score (0–100)</p>
      </div>
    </div>
  );
}
