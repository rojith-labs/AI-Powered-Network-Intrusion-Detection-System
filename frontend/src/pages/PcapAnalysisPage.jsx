import React, { useState } from 'react';
import { analyzePcapFile } from '../services/api';
import SeverityBadge from '../components/SeverityBadge';
import ThreatGauge from '../components/ThreatGauge';
import { FileSearch, Upload, CheckCircle2, AlertCircle, FileText, Download } from 'lucide-react';

export default function PcapAnalysisPage() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a .pcap or .pcapng file first.');
      return;
    }

    setLoading(true);
    setProgress(10);
    setError('');

    try {
      const data = await analyzePcapFile(file, (progressEvent) => {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setProgress(percent);
      });
      setReport(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'PCAP analysis failed. Ensure valid .pcap format.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-wide">PCAP / PCAPNG Network Traffic Analysis</h1>
        <p className="text-xs text-slate-400 mt-1">Upload packet capture files to extract flow features, run ML threat detection, and audit results</p>
      </div>

      {/* Upload Zone */}
      <div className="glass-panel p-8 rounded-xl border border-dashed border-slate-700 text-center space-y-4">
        <Upload className="w-10 h-10 text-indigo-400 mx-auto animate-bounce" />
        <div>
          <h3 className="font-bold text-slate-200 text-base">Upload Network Capture File</h3>
          <p className="text-xs text-slate-400 mt-1">Supported formats: .pcap, .pcapng (Max size: 50MB)</p>
        </div>

        <input
          type="file"
          id="pcapInput"
          accept=".pcap,.pcapng"
          onChange={handleFileChange}
          className="hidden"
        />

        <div className="flex items-center justify-center gap-3">
          <label
            htmlFor="pcapInput"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 cursor-pointer transition-colors"
          >
            {file ? file.name : 'Select PCAP File'}
          </label>

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="px-5 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 text-white text-xs font-bold rounded-lg shadow-lg shadow-indigo-600/20 transition-all"
          >
            {loading ? `Analyzing (${progress}%)...` : 'Run Deep Analysis'}
          </button>
        </div>

        {error && <p className="text-xs text-rose-400 font-semibold">{error}</p>}
      </div>

      {/* Analysis Report View */}
      {report && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
            <div className="glass-panel p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400 block">Total Packets Parsed</span>
              <span className="text-2xl font-bold text-slate-100 mt-1 block">{report.total_packets}</span>
            </div>
            <div className="glass-panel p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400 block">Extracted Flows</span>
              <span className="text-2xl font-bold text-indigo-400 mt-1 block">{report.total_flows}</span>
            </div>
            <div className="glass-panel p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400 block">Normal vs Suspicious</span>
              <span className="text-lg font-bold text-emerald-400 mt-1 block">
                {report.normal_flows} <span className="text-slate-400 text-xs">Normal</span> / <span className="text-rose-400">{report.suspicious_flows}</span> <span className="text-slate-400 text-xs">Anomalous</span>
              </span>
            </div>
            <div className="glass-panel p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400 block">Overall Severity</span>
              <div className="mt-1">
                <SeverityBadge severity={report.overall_severity} />
              </div>
            </div>
          </div>

          {/* Detailed Flows Table */}
          <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
            <h3 className="font-bold text-slate-200 text-sm">Flow Classification Results</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider bg-slate-900/50">
                    <th className="py-2.5 px-3">Timestamp</th>
                    <th className="py-2.5 px-3">Source IP</th>
                    <th className="py-2.5 px-3">Destination IP</th>
                    <th className="py-2.5 px-3">Protocol</th>
                    <th className="py-2.5 px-3">Prediction</th>
                    <th className="py-2.5 px-3">Confidence</th>
                    <th className="py-2.5 px-3">Threat Score</th>
                    <th className="py-2.5 px-3">Severity</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {report.flows.map((flow, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/50">
                      <td className="py-2 px-3 text-slate-400">{flow.timestamp ? new Date(flow.timestamp).toLocaleTimeString() : 'N/A'}</td>
                      <td className="py-2 px-3 text-slate-200">{flow.source_ip}:{flow.source_port}</td>
                      <td className="py-2 px-3 text-slate-200">{flow.destination_ip}:{flow.destination_port}</td>
                      <td className="py-2 px-3 text-indigo-300">{flow.protocol}</td>
                      <td className={`py-2 px-3 font-bold ${flow.prediction === 'BENIGN' ? 'text-emerald-400' : 'text-rose-400'}`}>{flow.prediction}</td>
                      <td className="py-2 px-3 text-slate-300">{(flow.confidence * 100).toFixed(1)}%</td>
                      <td className="py-2 px-3 font-bold text-slate-100">{flow.threat_score}</td>
                      <td className="py-2 px-3"><SeverityBadge severity={flow.severity} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
