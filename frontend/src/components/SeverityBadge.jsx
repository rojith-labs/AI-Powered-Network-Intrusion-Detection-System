import React from 'react';

export default function SeverityBadge({ severity }) {
  const styles = {
    Normal: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
    Low: 'bg-blue-500/15 text-blue-400 border-blue-500/30',
    Medium: 'bg-yellow-500/15 text-yellow-400 border-yellow-500/30',
    High: 'bg-orange-500/15 text-orange-400 border-orange-500/30',
    Critical: 'bg-rose-500/15 text-rose-400 border-rose-500/30 animate-pulse',
  };

  const currentStyle = styles[severity] || 'bg-slate-500/15 text-slate-400 border-slate-500/30';

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${currentStyle}`}>
      {severity || 'Normal'}
    </span>
  );
}
