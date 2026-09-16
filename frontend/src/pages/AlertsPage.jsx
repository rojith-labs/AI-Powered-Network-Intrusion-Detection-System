import React, { useState, useEffect } from 'react';
import { fetchAlerts, updateAlertStatus } from '../services/api';
import SeverityBadge from '../components/SeverityBadge';
import AlertStatusBadge from '../components/AlertStatusBadge';
import { AlertTriangle, Filter, CheckCircle2, XCircle, Search, Clock } from 'lucide-react';

export default function AlertsPage({ search, selectedAlert, onSelectAlert }) {
  const [alerts, setAlerts] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [severity, setSeverity] = useState('');
  const [status, setStatus] = useState('');
  const [attackType, setAttackType] = useState('');
  const [loading, setLoading] = useState(false);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const res = await fetchAlerts({
        severity,
        status,
        attack_type: attackType,
        search,
        page,
        limit: 25,
      });
      setAlerts(res.items || []);
      setTotal(res.total || 0);
    } catch (err) {
      console.error('Failed to fetch alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, [page, severity, status, attackType, search]);

  const handleStatusUpdate = async (alertId, newStatus) => {
    try {
      await updateAlertStatus(alertId, newStatus);
      loadAlerts();
    } catch (err) {
      console.error('Failed to update alert status:', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-wide">Alert Management Center</h1>
          <p className="text-xs text-slate-400 mt-1">Investigate, triage, and resolve security detections</p>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
            <Filter className="w-3.5 h-3.5 text-indigo-400" />
            <span>Filter By:</span>
          </div>

          <select
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Severities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>

          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Statuses</option>
            <option value="New">New</option>
            <option value="Investigating">Investigating</option>
            <option value="Resolved">Resolved</option>
            <option value="False Positive">False Positive</option>
          </select>

          <select
            value={attackType}
            onChange={(e) => setAttackType(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Attack Types</option>
            <option value="DoS">DoS</option>
            <option value="DDoS">DDoS</option>
            <option value="Port Scan">Port Scan</option>
            <option value="Brute Force">Brute Force</option>
            <option value="Botnet">Botnet</option>
          </select>
        </div>

        <div className="text-xs text-slate-400 font-medium">
          Total Alerts: <span className="text-rose-400 font-bold">{total}</span>
        </div>
      </div>

      {/* Alerts Table */}
      <div className="glass-panel rounded-xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider bg-slate-900/50">
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Source IP</th>
                <th className="py-3 px-4">Target IP:Port</th>
                <th className="py-3 px-4">Attack Vector</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Threat Score</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {alerts.length > 0 ? (
                alerts.map((alert) => (
                  <tr
                    key={alert.id}
                    className="hover:bg-slate-800/50 transition-colors"
                  >
                    <td className="py-3 px-4 font-mono text-slate-400">
                      {alert.timestamp ? new Date(alert.timestamp).toLocaleString() : 'N/A'}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-200">{alert.source_ip}</td>
                    <td className="py-3 px-4 font-mono text-slate-300">
                      {alert.destination_ip}:{alert.destination_port}
                    </td>
                    <td className="py-3 px-4 font-bold text-rose-400">{alert.attack_type}</td>
                    <td className="py-3 px-4 text-slate-300">{(alert.confidence * 100).toFixed(1)}%</td>
                    <td className="py-3 px-4 font-extrabold text-white">{alert.threat_score}</td>
                    <td className="py-3 px-4"><SeverityBadge severity={alert.severity} /></td>
                    <td className="py-3 px-4"><AlertStatusBadge status={alert.status} /></td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        {alert.status === 'New' && (
                          <button
                            onClick={() => handleStatusUpdate(alert.id, 'Investigating')}
                            className="px-2 py-1 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 rounded text-[11px] font-semibold border border-amber-500/30"
                          >
                            Investigate
                          </button>
                        )}
                        {alert.status !== 'Resolved' && (
                          <button
                            onClick={() => handleStatusUpdate(alert.id, 'Resolved')}
                            className="px-2 py-1 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 rounded text-[11px] font-semibold border border-emerald-500/30"
                          >
                            Resolve
                          </button>
                        )}
                        {alert.status !== 'False Positive' && (
                          <button
                            onClick={() => handleStatusUpdate(alert.id, 'False Positive')}
                            className="px-2 py-1 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded text-[11px] font-semibold border border-slate-600"
                          >
                            False Pos
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="9" className="py-8 text-center text-slate-500">
                    No security alerts found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="p-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400 bg-slate-900/40">
          <span>Page {page} of {Math.ceil(total / 25) || 1}</span>
          <div className="flex gap-2">
            <button
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
              className="px-3 py-1 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 text-slate-300 rounded border border-slate-700"
            >
              Previous
            </button>
            <button
              disabled={page * 25 >= total}
              onClick={() => setPage(page + 1)}
              className="px-3 py-1 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 text-slate-300 rounded border border-slate-700"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
