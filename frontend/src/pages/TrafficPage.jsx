import React, { useState, useEffect } from 'react';
import { fetchTrafficFlows } from '../services/api';
import { Search, Filter, RefreshCw, Layers } from 'lucide-react';

export default function TrafficPage({ search }) {
  const [flows, setFlows] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [protocol, setProtocol] = useState('');
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedFlow, setSelectedFlow] = useState(null);

  const loadFlows = async () => {
    setLoading(true);
    try {
      const res = await fetchTrafficFlows({
        protocol,
        prediction,
        search,
        page,
        limit: 25,
      });
      setFlows(res.items || []);
      setTotal(res.total || 0);
    } catch (err) {
      console.error('Failed to load traffic flows:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFlows();
  }, [page, protocol, prediction, search]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-wide">Network Traffic Logs</h1>
          <p className="text-xs text-slate-400 mt-1">Real-time and historical 5-tuple network flow aggregations</p>
        </div>
        <button
          onClick={loadFlows}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs rounded-lg border border-slate-700 flex items-center gap-2 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Flows
        </button>
      </div>

      {/* Filters Bar */}
      <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
            <Filter className="w-3.5 h-3.5 text-indigo-400" />
            <span>Filters:</span>
          </div>

          <select
            value={protocol}
            onChange={(e) => setProtocol(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Protocols</option>
            <option value="TCP">TCP</option>
            <option value="UDP">UDP</option>
            <option value="ICMP">ICMP</option>
          </select>

          <select
            value={prediction}
            onChange={(e) => setPrediction(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Traffic Classes</option>
            <option value="BENIGN">BENIGN (Normal)</option>
            <option value="DoS">DoS Attack</option>
            <option value="DDoS">DDoS Attack</option>
            <option value="Port Scan">Port Scan</option>
            <option value="Brute Force">Brute Force</option>
            <option value="Botnet">Botnet</option>
          </select>
        </div>

        <div className="text-xs text-slate-400 font-medium">
          Showing <span className="text-indigo-400 font-bold">{flows.length}</span> of <span className="text-slate-200 font-bold">{total}</span> flows
        </div>
      </div>

      {/* Flows Table */}
      <div className="glass-panel rounded-xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider bg-slate-900/50">
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Source IP : Port</th>
                <th className="py-3 px-4">Destination IP : Port</th>
                <th className="py-3 px-4">Protocol</th>
                <th className="py-3 px-4">Duration</th>
                <th className="py-3 px-4">Packets / Bytes</th>
                <th className="py-3 px-4">Classification</th>
                <th className="py-3 px-4">Threat Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {flows.length > 0 ? (
                flows.map((flow) => (
                  <tr
                    key={flow.id}
                    onClick={() => setSelectedFlow(flow)}
                    className="hover:bg-slate-800/50 cursor-pointer transition-colors"
                  >
                    <td className="py-3 px-4 font-mono text-slate-400">
                      {flow.timestamp ? new Date(flow.timestamp).toLocaleString() : 'N/A'}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-200">
                      {flow.source_ip}:<span className="text-slate-400">{flow.source_port}</span>
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-200">
                      {flow.destination_ip}:<span className="text-slate-400">{flow.destination_port}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-indigo-300 font-mono text-[11px]">
                        {flow.protocol}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-300">{flow.duration}s</td>
                    <td className="py-3 px-4 text-slate-300">
                      {flow.packet_count} pkts / {(flow.byte_count / 1024).toFixed(1)} KB
                    </td>
                    <td className="py-3 px-4 font-bold">
                      <span className={flow.prediction === 'BENIGN' ? 'text-emerald-400' : 'text-rose-400'}>
                        {flow.prediction}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-extrabold text-slate-100">{flow.threat_score}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="8" className="py-8 text-center text-slate-500">
                    No traffic flows matched the criteria.
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

      {/* Flow Detail Modal */}
      {selectedFlow && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel max-w-lg w-full rounded-xl border border-slate-700 p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-slate-100 text-lg flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-400" />
                Flow Detail #{selectedFlow.id}
              </h3>
              <button
                onClick={() => setSelectedFlow(null)}
                className="text-slate-400 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">Source IP:Port</span>
                <span className="font-mono text-slate-200 font-bold">{selectedFlow.source_ip}:{selectedFlow.source_port}</span>
              </div>
              <div className="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">Destination IP:Port</span>
                <span className="font-mono text-slate-200 font-bold">{selectedFlow.destination_ip}:{selectedFlow.destination_port}</span>
              </div>
              <div className="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">Protocol</span>
                <span className="font-mono text-indigo-300 font-bold">{selectedFlow.protocol}</span>
              </div>
              <div className="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">Duration</span>
                <span className="text-slate-200 font-bold">{selectedFlow.duration} seconds</span>
              </div>
              <div className="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">Packets Count</span>
                <span className="text-slate-200 font-bold">{selectedFlow.packet_count} packets</span>
              </div>
              <div className="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">Bytes Volume</span>
                <span className="text-slate-200 font-bold">{selectedFlow.byte_count} bytes</span>
              </div>
            </div>

            <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg flex items-center justify-between">
              <div>
                <span className="text-slate-400 text-xs block">ML Classification</span>
                <span className={`text-base font-extrabold ${selectedFlow.prediction === 'BENIGN' ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {selectedFlow.prediction}
                </span>
              </div>
              <div>
                <span className="text-slate-400 text-xs block">Threat Score</span>
                <span className="text-base font-extrabold text-white">{selectedFlow.threat_score} / 100</span>
              </div>
            </div>

            <button
              onClick={() => setSelectedFlow(null)}
              className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-lg transition-colors"
            >
              Close Detail
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
