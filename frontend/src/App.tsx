import { useState } from 'react';
import axios from 'axios';
import { Activity, BarChart2, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Interfaces
interface FeatureWeights {
  [key: string]: number;
}

interface PredictionResponse {
  prediction: string;
  probability: number;
  rule_override: boolean;
  confidence_band: string;
  feature_weights: FeatureWeights;
}

const FEATURE_CONFIG = [
  { id: 'cgpa', label: 'CGPA', min: 5.5, max: 9.5, step: 0.1, default: 7.5 },
  { id: 'coding_score', label: 'Coding Score', min: 0, max: 100, step: 1, default: 60 },
  { id: 'aptitude_score', label: 'Aptitude Score', min: 0, max: 100, step: 1, default: 60 },
  { id: 'communication_score', label: 'Communication Score', min: 0, max: 100, step: 1, default: 60 },
  { id: 'skills_count', label: 'Technical Skills (Count)', min: 1, max: 10, step: 1, default: 3 },
  { id: 'projects_count', label: 'Projects (Count)', min: 0, max: 5, step: 1, default: 1 },
  { id: 'internships_count', label: 'Internships (Count)', min: 0, max: 3, step: 1, default: 0 },
  { id: 'backlogs', label: 'Active Backlogs', min: 0, max: 5, step: 1, default: 0 },
];

export default function App() {
  const [formData, setFormData] = useState<Record<string, number>>(() => {
    const initial: Record<string, number> = {};
    FEATURE_CONFIG.forEach(f => {
      initial[f.id] = f.default;
    });
    return initial;
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (id: string, value: number) => {
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await axios.post<PredictionResponse>(`${API_BASE}/v1/predict`, formData);
      setResult(res.data);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to prediction engine.');
    } finally {
      setLoading(false);
    }
  };

  const formatWeight = (val: number) => {
    return (val > 0 ? '+' : '') + val.toFixed(2);
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="text-brand-600 h-6 w-6" />
          <h1 className="text-xl font-bold text-slate-800 tracking-tight">PlaceIQ Analytics</h1>
        </div>
        <div className="text-sm font-medium text-slate-500">Readiness Prediction System</div>
      </header>

      {/* Main Content */}
      <main className="flex-1 p-6 lg:p-10 max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Inputs */}
        <div className="lg:col-span-5 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
          <div className="p-5 border-b border-slate-100 bg-slate-50">
            <h2 className="text-lg font-semibold text-slate-800">Student Profile</h2>
            <p className="text-sm text-slate-500 mt-1">Adjust the parameters to simulate readiness.</p>
          </div>
          <div className="p-5 flex-1 overflow-y-auto space-y-6">
            {FEATURE_CONFIG.map(feature => (
              <div key={feature.id}>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-medium text-slate-700">{feature.label}</label>
                  <span className="text-sm font-bold text-brand-600 bg-brand-50 px-2 py-0.5 rounded">
                    {formData[feature.id]}
                  </span>
                </div>
                <input
                  type="range"
                  min={feature.min}
                  max={feature.max}
                  step={feature.step}
                  value={formData[feature.id]}
                  onChange={(e) => handleChange(feature.id, parseFloat(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600"
                />
                <div className="flex justify-between mt-1">
                  <span className="text-xs text-slate-400">{feature.min}</span>
                  <span className="text-xs text-slate-400">{feature.max}</span>
                </div>
              </div>
            ))}
          </div>
          <div className="p-5 border-t border-slate-100 bg-slate-50">
            <button
              onClick={handlePredict}
              disabled={loading}
              className={cn(
                "w-full py-3 px-4 rounded-lg font-semibold text-white transition-all shadow-sm flex items-center justify-center gap-2",
                loading ? "bg-slate-400 cursor-not-allowed" : "bg-brand-600 hover:bg-brand-700 hover:shadow"
              )}
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing Profile...
                </>
              ) : (
                <>
                  <Activity className="w-5 h-5" />
                  Run Prediction Model
                </>
              )}
            </button>
            {error && <p className="text-sm text-red-600 mt-3 text-center">{error}</p>}
          </div>
        </div>

        {/* Right Column: Results */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          {!result ? (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex-1 flex flex-col items-center justify-center p-12 text-center text-slate-400">
              <BarChart2 className="w-16 h-16 mb-4 text-slate-300" />
              <h3 className="text-lg font-medium text-slate-600">No Prediction Data</h3>
              <p className="mt-2 text-sm max-w-sm">Run the prediction model to view placement probability and feature contributions.</p>
            </div>
          ) : (
            <>
              {/* Primary Result Widget */}
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 flex flex-col items-center relative overflow-hidden">
                {result.rule_override && (
                  <div className="absolute top-0 left-0 right-0 bg-red-50 border-b border-red-100 py-2 px-4 flex items-center justify-center gap-2 text-red-700 text-sm font-medium">
                    <AlertTriangle className="w-4 h-4" />
                    Deterministic Rule Triggered: Backlogs threshold exceeded.
                  </div>
                )}
                
                <div className={cn("mt-6 flex items-center justify-center w-20 h-20 rounded-full mb-4", 
                  result.probability >= 0.5 ? "bg-green-100 text-green-600" : "bg-red-100 text-red-600"
                )}>
                  {result.probability >= 0.5 ? <CheckCircle2 className="w-10 h-10" /> : <XCircle className="w-10 h-10" />}
                </div>

                <h2 className="text-3xl font-bold text-slate-800 tracking-tight">{result.prediction}</h2>
                <div className="mt-8 w-full max-w-md">
                  <div className="flex justify-between items-end mb-2">
                    <span className="text-sm font-medium text-slate-600">Placement Probability</span>
                    <span className="text-4xl font-black text-slate-800">
                      {(result.probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden flex">
                    <div 
                      className={cn(
                        "h-full transition-all duration-1000 ease-out",
                        result.probability >= 0.75 ? "bg-green-500" : 
                        result.probability >= 0.5 ? "bg-amber-500" : "bg-red-500"
                      )}
                      style={{ width: `${result.probability * 100}%` }}
                    />
                  </div>
                  <div className="flex justify-between mt-2 text-xs font-medium text-slate-400">
                    <span>0%</span>
                    <span>Confidence: {result.confidence_band.toUpperCase()}</span>
                    <span>100%</span>
                  </div>
                </div>
              </div>

              {/* Feature Weights / SHAP Widget */}
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex-1 flex flex-col">
                <div className="p-5 border-b border-slate-100 bg-slate-50 flex items-center gap-2">
                  <BarChart2 className="w-5 h-5 text-slate-500" />
                  <h3 className="text-lg font-semibold text-slate-800">Feature Contribution Analysis</h3>
                </div>
                <div className="p-6 flex-1 space-y-5">
                  {Object.entries(result.feature_weights)
                    .sort(([, a], [, b]) => Math.abs(b) - Math.abs(a)) // Sort by absolute impact
                    .map(([feature, weight]) => {
                      const maxAbsWeight = Math.max(...Object.values(result.feature_weights).map(Math.abs));
                      const percentage = (Math.abs(weight) / maxAbsWeight) * 100;
                      const isPositive = weight > 0;
                      const label = FEATURE_CONFIG.find(f => f.id === feature)?.label || feature;
                      
                      return (
                        <div key={feature} className="relative">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="font-medium text-slate-700">{label}</span>
                            <span className={cn(
                              "font-mono font-medium",
                              isPositive ? "text-green-600" : "text-red-600"
                            )}>
                              {formatWeight(weight)}
                            </span>
                          </div>
                          
                          {/* Centered Bar Chart */}
                          <div className="h-5 w-full bg-slate-50 flex relative">
                            {/* Center Line */}
                            <div className="absolute left-1/2 top-0 bottom-0 w-px bg-slate-300 z-10" />
                            
                            {/* Negative side */}
                            <div className="w-1/2 flex justify-end items-center pr-1">
                              {!isPositive && (
                                <div 
                                  className="h-full bg-red-400 rounded-l transition-all duration-700 ease-out"
                                  style={{ width: `${percentage}%` }}
                                />
                              )}
                            </div>
                            
                            {/* Positive side */}
                            <div className="w-1/2 flex justify-start items-center pl-1">
                              {isPositive && (
                                <div 
                                  className="h-full bg-green-400 rounded-r transition-all duration-700 ease-out"
                                  style={{ width: `${percentage}%` }}
                                />
                              )}
                            </div>
                          </div>
                        </div>
                      )
                    })}
                </div>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
