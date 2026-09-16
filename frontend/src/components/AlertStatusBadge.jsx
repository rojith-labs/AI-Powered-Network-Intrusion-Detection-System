import React from 'react';

export default function AlertStatusBadge({ status }) {
  const styles = {
    New: 'bg-indigo-500/15 text-indigo-400 border-indigo-500/30',
    Investigating: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
    Resolved: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
    'False Positive': 'bg-slate-500/15 text-slate-400 border-slate-500/30',
  };

  const currentStyle = styles[status] || 'bg-slate-500/15 text-slate-400 border-slate-500/30';

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${currentStyle}`}>
      {status || 'New'}
    </span>
  );
}
