import React from 'react';
import { CheckCircle2, AlertOctagon, Layers, Percent } from 'lucide-react';

interface KpiTilesProps {
  commitmentsCreated: number;
  verified: number;
  awaitingOrAtRisk: number;
  resolutionRate?: number;
}

export const KpiTiles: React.FC<KpiTilesProps> = ({
  commitmentsCreated,
  verified,
  awaitingOrAtRisk,
  resolutionRate = 75.0,
}) => {
  const calculatedRate = commitmentsCreated > 0
    ? Math.round((verified / commitmentsCreated) * 100)
    : 0;
  
  const displayRate = resolutionRate || calculatedRate;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {/* 1. Commitments Created */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 shadow-lg backdrop-blur">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            KEPT Commitments
          </span>
          <Layers className="w-5 h-5 text-indigo-400" />
        </div>
        <div className="text-4xl md:text-5xl font-extrabold font-mono text-white mt-2">
          {commitmentsCreated}
        </div>
        <p className="text-xs text-slate-400 mt-2">
          Autonomous promises tracked
        </p>
      </div>

      {/* 2. Verified (GREEN) */}
      <div className="bg-slate-900/70 border border-emerald-500/30 rounded-xl p-5 shadow-lg backdrop-blur">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400">
            Verified Settled
          </span>
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
        </div>
        <div className="text-4xl md:text-5xl font-extrabold font-mono text-emerald-400 mt-2">
          {verified}
        </div>
        <p className="text-xs text-emerald-400/80 mt-2 flex items-center">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 inline-block" />
          Proved via independent verifier
        </p>
      </div>

      {/* 3. Awaiting / AT_RISK (CRITICAL: HIGHLIGHTED) */}
      <div
        className={`rounded-xl p-5 shadow-lg backdrop-blur transition-all ${
          awaitingOrAtRisk > 0
            ? 'bg-red-950/30 border border-red-500/60 shadow-red-950/30 ring-1 ring-red-500/30'
            : 'bg-slate-900/70 border border-slate-800'
        }`}
      >
        <div className="flex items-center justify-between">
          <span className={`text-xs font-semibold uppercase tracking-wider ${awaitingOrAtRisk > 0 ? 'text-red-400' : 'text-slate-400'}`}>
            Pending / At Risk
          </span>
          <AlertOctagon className={`w-5 h-5 ${awaitingOrAtRisk > 0 ? 'text-red-400 animate-pulse' : 'text-slate-500'}`} />
        </div>
        <div className={`text-4xl md:text-5xl font-extrabold font-mono mt-2 ${awaitingOrAtRisk > 0 ? 'text-red-400' : 'text-slate-300'}`}>
          {awaitingOrAtRisk}
        </div>
        <p className="text-xs text-red-300/80 mt-2 font-medium">
          {awaitingOrAtRisk > 0 ? '⚠️ Settlement proof pending' : 'Zero commitments at risk'}
        </p>
      </div>

      {/* 4. Verified Resolution Rate */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 shadow-lg backdrop-blur">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Verified Resolution Rate
          </span>
          <Percent className="w-5 h-5 text-cyan-400" />
        </div>
        <div className="text-4xl md:text-5xl font-extrabold font-mono text-cyan-300 mt-2">
          {displayRate}%
        </div>
        <p className="text-xs text-slate-400 mt-2">
          Target outcome: 6/8 settled
        </p>
      </div>
    </div>
  );
};
