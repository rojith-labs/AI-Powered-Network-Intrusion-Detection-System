import React, { useState, useEffect } from 'react';
import { fetchModelsInfo } from '../services/api';
import { Cpu, CheckCircle2, Terminal, Award, FileCode } from 'lucide-react';

export default function ModelsPage() {
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    fetchModelsInfo()
      .then(setModelInfo)
      .catch((err) => console.error('Failed to load model metadata:', err));
  }, []);

  if (!modelInfo) {
    return (
      <div className="p-8 text-center text-slate-400">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        <p>Loading Machine Learning Model Performance Metrics...</p>
      </div>
    );
  }

  const { status, active_model, models } = modelInfo;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-wide">Machine Learning Models Management</h1>
        <p className="text-xs text-slate-400 mt-1">Evaluated classifier models, validation metrics & dataset benchmarks</p>
      </div>

      {/* Active Model Status Card */}
      <div className="glass-panel p-6 rounded-xl border border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded-xl">
            <Cpu className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h3 className="font-bold text-slate-100 text-lg">{active_model}</h3>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                {status}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">Trained on CIC-IDS2017 Benchmark Flow Features</p>
          </div>
        </div>

        <div className="text-right">
          <span className="text-xs text-slate-500 block">Saved Model Location</span>
          <span className="font-mono text-xs text-slate-300">backend/models/nids_model.joblib</span>
        </div>
      </div>

      {/* Models List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {models && models.length > 0 ? (
          models.map((m, idx) => (
            <div key={idx} className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <h4 className="font-bold text-slate-200 text-sm">{m.model_name}</h4>
                  <span className="text-[11px] text-slate-400 font-mono">Dataset: {m.dataset_name}</span>
                </div>
                <Award className="w-5 h-5 text-amber-400" />
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-2.5 bg-slate-900/80 rounded border border-slate-800">
                  <span className="text-slate-500 block">Accuracy</span>
                  <span className="font-extrabold text-emerald-400 text-base">{(m.accuracy * 100).toFixed(2)}%</span>
                </div>
                <div className="p-2.5 bg-slate-900/80 rounded border border-slate-800">
                  <span className="text-slate-500 block">F1 Score</span>
                  <span className="font-extrabold text-indigo-400 text-base">{(m.f1_score * 100).toFixed(2)}%</span>
                </div>
                <div className="p-2.5 bg-slate-900/80 rounded border border-slate-800">
                  <span className="text-slate-500 block">Precision</span>
                  <span className="font-bold text-slate-200">{(m.precision * 100).toFixed(2)}%</span>
                </div>
                <div className="p-2.5 bg-slate-900/80 rounded border border-slate-800">
                  <span className="text-slate-500 block">Recall</span>
                  <span className="font-bold text-slate-200">{(m.recall * 100).toFixed(2)}%</span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-3 p-8 glass-panel text-center text-slate-500">
            Model not trained yet.
          </div>
        )}
      </div>

      {/* Retraining Instructions Terminal Box */}
      <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-3">
        <h3 className="font-bold text-slate-200 text-sm flex items-center gap-2">
          <Terminal className="w-4 h-4 text-indigo-400" />
          Model Retraining Command
        </h3>
        <p className="text-xs text-slate-400">
          To retrain and evaluate Random Forest, XGBoost, and Logistic Regression models on a new dataset:
        </p>
        <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 font-mono text-xs text-emerald-400">
          python ml/training/train.py --dataset path/to/dataset.csv
        </div>
      </div>
    </div>
  );
}
