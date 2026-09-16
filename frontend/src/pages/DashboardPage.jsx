import React from 'react';
import { 
  Activity, 
  ShieldAlert, 
  ShieldCheck, 
  AlertOctagon, 
  Database,
  ArrowUpRight
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, BarChart, Bar
} from 'recharts';
import SeverityBadge from '../components/SeverityBadge';
import AlertStatusBadge from '../components/AlertStatusBadge';

const PIE_COLORS = ['#ef4444', '#f97316', '#eab308', '#3b82f6', '#8b5cf6', '#ec4899'];

export default function DashboardPage({ data, onSelectAlert, setActiveTab }) {
  if (!data || !data.summary) {
    return (
      <div className="p-8 text-center text-slate-400">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        <p>Loading SOC Dashboard metrics...</p>
      </div>
    );
  }

  const { summary, traffic_timeline, attack_distribution, severity_distribution, recent_alerts, top_source_ips, top_dest_ports } = data;

  const cards = [
    {
      title: 'Total Traffic Volume',
      value: `${(summary.total_traffic_bytes / (1024 * 1024)).toFixed(2)} MB`,
      sub: `${summary.total_flows} Total Flows Aggregated`,
      icon: Database,
      color: 'from-blue-500 to-indigo-600',
      textColor: 'text-blue-400'
    },
    {
      title: 'Normal Traffic Flows',
      value: summary.normal_traffic_count,
      sub: `${((summary.normal_traffic_count / Math.max(1, summary.total_flows)) * 100).toFixed(1)}% of total traffic`,
      icon: ShieldCheck,
      color: 'from-emerald-500 to-teal-600',
      textColor: 'text-emerald-400'
    },
    {
      title: 'Malicious Detections',
      value: summary.malicious_traffic_count,
      sub: `${((summary.malicious_traffic_count / Math.max(1, summary.total_flows)) * 100).toFixed(1)}% anomalous flows`,
      icon: ShieldAlert,
      color: 'from-orange-500 to-amber-600',
      textColor: 'text-orange-400'
    },
    {
      title: 'Critical Alerts',
      value: summary.critical_alerts_count,
      sub: `Threat Level: ${summary.active_threat_level}`,
      icon: AlertOctagon,
      color: 'from-rose-500 to-red-600',
      textColor: 'text-rose-400'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-wide">SOC Overview Dashboard</h1>
          <p className="text-xs text-slate-400 mt-1">Real-Time Threat Intelligence & Network Traffic Analytics</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={() => setActiveTab('pcap')}
            className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs rounded-lg shadow-lg shadow-indigo-600/25 transition-all flex items-center gap-2"
          >
            <ArrowUpRight className="w-4 h-4" />
            Analyze PCAP File
          </button>
        </div>
      </div>

      {/* Metric Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {cards.map((c, i) => {
          const Icon = c.icon;
          return (
            <div key={i} className="glass-panel glass-panel-hover p-5 rounded-xl border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{c.title}</p>
                <p className={`text-2xl font-black mt-1 ${c.textColor}`}>{c.value}</p>
                <p className="text-[11px] text-slate-500 mt-1">{c.sub}</p>
              </div>
              <div className={`p-3 bg-gradient-to-br ${c.color} rounded-xl text-white shadow-lg`}>
                <Icon className="w-5 h-5" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Traffic Timeline Area Chart */}
        <div className="lg:col-span-2 glass-panel p-5 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-200 text-sm">Traffic Timeline (Normal vs Malicious)</h3>
              <p className="text-xs text-slate-400">Flow volume over time</p>
            </div>
            <div className="flex items-center gap-4 text-xs font-medium">
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Normal
              </span>
              <span className="flex items-center gap-1.5 text-rose-400">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Malicious
              </span>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={traffic_timeline}>
                <defs>
                  <linearGradient id="normalGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.0}/>
                  </linearGradient>
                  <linearGradient id="maliciousGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="timestamp" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                />
                <Area type="monotone" dataKey="normal_flows" stroke="#10b981" fillOpacity={1} fill="url(#normalGrad)" />
                <Area type="monotone" dataKey="malicious_flows" stroke="#ef4444" fillOpacity={1} fill="url(#maliciousGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Attack Distribution Pie Chart */}
        <div className="glass-panel p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-slate-200 text-sm">Attack Category Distribution</h3>
            <p className="text-xs text-slate-400 mb-2">Classified threat vectors</p>
          </div>
          <div className="h-52 flex items-center justify-center">
            {attack_distribution.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={attack_distribution}
                    dataKey="count"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={3}
                  >
                    {attack_distribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-slate-500">No attack categories detected</p>
            )}
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {attack_distribution.slice(0, 6).map((item, idx) => (
              <div key={idx} className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: PIE_COLORS[idx % PIE_COLORS.length] }}></span>
                <span className="text-slate-300 font-medium truncate">{item.name}:</span>
                <span className="text-slate-400 font-bold">{item.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tables Row: Recent Security Alerts & Top Target Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Alerts Table */}
        <div className="lg:col-span-2 glass-panel p-5 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-200 text-sm">Recent Security Alerts</h3>
              <p className="text-xs text-slate-400">Live anomalous detection feed</p>
            </div>
            <button 
              onClick={() => setActiveTab('alerts')}
              className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
            >
              View All Alerts &rarr;
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  <th className="py-2.5 px-3">Timestamp</th>
                  <th className="py-2.5 px-3">Source IP</th>
                  <th className="py-2.5 px-3">Attack Type</th>
                  <th className="py-2.5 px-3">Threat Score</th>
                  <th className="py-2.5 px-3">Severity</th>
                  <th className="py-2.5 px-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-xs">
                {recent_alerts.slice(0, 7).map((alert) => (
                  <tr 
                    key={alert.id}
                    onClick={() => onSelectAlert && onSelectAlert(alert)}
                    className="hover:bg-slate-800/40 cursor-pointer transition-colors"
                  >
                    <td className="py-2.5 px-3 font-mono text-slate-400">
                      {alert.timestamp ? new Date(alert.timestamp).toLocaleTimeString() : 'N/A'}
                    </td>
                    <td className="py-2.5 px-3 font-mono text-slate-200">{alert.source_ip}</td>
                    <td className="py-2.5 px-3 font-semibold text-indigo-300">{alert.attack_type}</td>
                    <td className="py-2.5 px-3 font-bold text-slate-100">{alert.threat_score}</td>
                    <td className="py-2.5 px-3"><SeverityBadge severity={alert.severity} /></td>
                    <td className="py-2.5 px-3"><AlertStatusBadge status={alert.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Threat Sources & Target Ports */}
        <div className="space-y-6">
          <div className="glass-panel p-5 rounded-xl border border-slate-800">
            <h3 className="font-bold text-slate-200 text-sm mb-3">Top Attacker IPs</h3>
            <div className="space-y-2 text-xs">
              {top_source_ips.map((ip, idx) => (
                <div key={idx} className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="font-mono text-slate-300">{ip.name}</span>
                  <span className="font-bold text-indigo-400">{ip.count} flows</span>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel p-5 rounded-xl border border-slate-800">
            <h3 className="font-bold text-slate-200 text-sm mb-3">Top Target Ports</h3>
            <div className="space-y-2 text-xs">
              {top_dest_ports.map((port, idx) => (
                <div key={idx} className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="font-mono text-slate-300">{port.name}</span>
                  <span className="font-bold text-purple-400">{port.count} flows</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
