import React, { useState } from 'react';
import { predictFlow } from '../services/api';
import ThreatGauge from '../components/ThreatGauge';
import SeverityBadge from '../components/SeverityBadge';
import { Radar, Play, Cpu, HelpCircle, CheckCircle } from 'lucide-react';

export default function DetectionsPage() {
  const [formData, setFormData] = useState({
    flow_duration: 1.25,
    fwd_pkts_count: 150,
    bwd_pkts_count: 5,
    total_bytes: 6400,
    packet_rate: 124.0,
    bytes_per_sec: 5120.0,
    avg_pkt_size: 42.6,
    min_pkt_size: 32.0,
    max_pkt_size: 64.0,
    std_pkt_size: 12.0,
    fwd_pkt_len_mean: 42.6,
    fwd_pkt_len_std: 12.0,
    bwd_pkt_len_mean: 40.0,
    bwd_pkt_len_std: 5.0,
    syn_flag_cnt: 45,
    ack_flag_cnt: 0,
    fin_flag_cnt: 0,
    rst_flag_cnt: 2,
    psh_flag_cnt: 0,
    source_port: 48321,
    destination_port: 80,
    protocol: 6,
    flow_iat_mean: 0.008,
    flow_iat_std: 0.002,
    source_ip: '192.168.1.150',
    destination_ip: '10.0.0.1'
  });

  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await predictFlow(formData);
      setPredictionResult(res);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed. Make sure backend is online.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-wide">ML Detection & Explainable AI Engine</h1>
        <p className="text-xs text-slate-400 mt-1">Test real-time flow feature vector inference & inspect feature importance attributions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form Panel */}
        <div className="glass-panel p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-bold text-slate-200 text-sm flex items-center gap-2">
              <Radar className="w-4 h-4 text-indigo-400" />
              Input Flow Features (CIC-IDS2017 Schema)
            </h3>
            <span className="text-xs text-slate-400 font-mono">24 Parameters</span>
          </div>

          <form onSubmit={handlePredict} className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-slate-400 block mb-1">Flow Duration (sec)</label>
                <input
                  type="number"
                  step="0.001"
                  name="flow_duration"
                  value={formData.flow_duration}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Packet Rate (pkts/sec)</label>
                <input
                  type="number"
                  step="0.1"
                  name="packet_rate"
                  value={formData.packet_rate}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Forward Packets</label>
                <input
                  type="number"
                  name="fwd_pkts_count"
                  value={formData.fwd_pkts_count}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Backward Packets</label>
                <input
                  type="number"
                  name="bwd_pkts_count"
                  value={formData.bwd_pkts_count}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">SYN Flag Count</label>
                <input
                  type="number"
                  name="syn_flag_cnt"
                  value={formData.syn_flag_cnt}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">ACK Flag Count</label>
                <input
                  type="number"
                  name="ack_flag_cnt"
                  value={formData.ack_flag_cnt}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Destination Port</label>
                <input
                  type="number"
                  name="destination_port"
                  value={formData.destination_port}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Protocol (6=TCP, 17=UDP)</label>
                <input
                  type="number"
                  name="protocol"
                  value={formData.protocol}
                  onChange={handleChange}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono"
                />
              </div>
            </div>

            {error && <p className="text-xs text-rose-400 font-semibold">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs rounded-lg shadow-lg shadow-indigo-600/20 transition-all flex items-center justify-center gap-2"
            >
              <Play className="w-4 h-4 fill-white" />
              {loading ? 'Running ML Inference...' : 'Run ML Threat Inference'}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="space-y-6">
          {predictionResult ? (
            <div className="glass-panel p-6 rounded-xl border border-slate-800 space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <span className="text-xs text-slate-400 block">ML Prediction Result</span>
                  <h3 className={`text-xl font-extrabold ${predictionResult.prediction === 'BENIGN' ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {predictionResult.prediction}
                  </h3>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">Confidence Score</span>
                  <span className="text-lg font-bold text-indigo-300">
                    {(predictionResult.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Threat Gauge */}
              <ThreatGauge
                score={predictionResult.threat_score}
                severity={predictionResult.severity}
              />

              {/* Explainable AI Indicators */}
              <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-2">
                <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
                  <HelpCircle className="w-3.5 h-3.5 text-indigo-400" />
                  Model Detection Indicators (XAI)
                </h4>
                <ul className="space-y-1.5 text-xs text-slate-300">
                  {predictionResult.explanation.map((exp, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-indigo-400 font-bold">•</span>
                      <span>{exp}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Feature Importances List */}
              {predictionResult.feature_importance && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Top Feature Attributions</h4>
                  <div className="space-y-1.5">
                    {predictionResult.feature_importance.slice(0, 5).map((item, idx) => (
                      <div key={idx} className="flex items-center justify-between text-xs p-2 bg-slate-900/50 rounded border border-slate-800">
                        <span className="font-mono text-slate-300">{item.feature}</span>
                        <span className="font-bold text-purple-400">Importance: {(item.importance * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="glass-panel p-8 rounded-xl border border-slate-800 text-center text-slate-500 space-y-3">
              <Cpu className="w-10 h-10 text-slate-600 mx-auto" />
              <h3 className="font-bold text-slate-300 text-sm">Awaiting Flow Inference</h3>
              <p className="text-xs max-w-xs mx-auto">
                Fill out the flow feature parameters on the left and click "Run ML Threat Inference" to generate threat score and XAI indicators.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
