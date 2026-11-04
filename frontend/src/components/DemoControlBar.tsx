import React, { useState } from 'react';
import { DemoStageKey } from '../types';
import { pulseApi } from '../api';
import { Play, RotateCcw, ShieldCheck, ToggleLeft, ToggleRight, Sparkles, Server, Check } from 'lucide-react';

interface DemoControlBarProps {
  isLive: boolean;
  activeStage: DemoStageKey;
  mode: 'auto' | 'fixtures' | 'live';
  onSetMode: (mode: 'auto' | 'fixtures' | 'live') => void;
  onSwitchStage: (stage: DemoStageKey) => void;
  onRefresh: () => void;
}

export const DemoControlBar: React.FC<DemoControlBarProps> = ({
  isLive,
  activeStage,
  mode,
  onSetMode,
  onSwitchStage,
  onRefresh,
}) => {
  const [settlementMode, setSettlementMode] = useState<'NOT_FOUND' | 'FOUND'>('NOT_FOUND');
  const [actionFeedback, setActionFeedback] = useState<string | null>(null);
  const [busy, setBusy] = useState<boolean>(false);

  const showFeedback = (msg: string) => {
    setActionFeedback(msg);
    setTimeout(() => setActionFeedback(null), 3000);
  };

  const handleReset = async () => {
    setBusy(true);
    try {
      if (isLive) {
        await pulseApi.resetDemoState();
        showFeedback('Reset API called: state returned to start');
      } else {
        onSwitchStage('start');
        showFeedback('Reset local fixture preview to Stage 1');
      }
      onRefresh();
    } catch (err: any) {
      showFeedback(`Error: ${err.message}`);
    } finally {
      setBusy(false);
    }
  };

  const handleToggleSettlement = async () => {
    setBusy(true);
    const nextMode = settlementMode === 'NOT_FOUND' ? 'FOUND' : 'NOT_FOUND';
    try {
      if (isLive) {
        await pulseApi.setSettlementMode(nextMode);
        setSettlementMode(nextMode);
        showFeedback(`Settlement toggle set to ${nextMode}`);
      } else {
        setSettlementMode(nextMode);
        if (nextMode === 'FOUND') {
          onSwitchStage('resolved');
        } else {
          onSwitchStage('at_risk');
        }
        showFeedback(`Simulated settlement mode: ${nextMode}`);
      }
      onRefresh();
    } catch (err: any) {
      showFeedback(`Error: ${err.message}`);
    } finally {
      setBusy(false);
    }
  };

  const handleRunVerification = async () => {
    setBusy(true);
    try {
      if (isLive) {
        await pulseApi.triggerVerification();
        showFeedback('Verification run complete');
      } else {
        showFeedback('Simulated verification run');
      }
      onRefresh();
    } catch (err: any) {
      showFeedback(`Error: ${err.message}`);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl text-xs">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        
        {/* Left: Rehearsal Stages */}
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span className="font-semibold text-slate-200 uppercase tracking-wider font-mono text-[11px]">
              Demo Rehearsal Stages (Section 10)
            </span>
          </div>
          
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => onSwitchStage('start')}
              className={`px-3 py-1.5 rounded-lg font-mono border transition ${
                activeStage === 'start'
                  ? 'bg-indigo-600 text-white border-indigo-500 font-bold'
                  : 'bg-slate-950/70 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              1. Start (Clean)
            </button>

            <button
              onClick={() => onSwitchStage('at_risk')}
              className={`px-3 py-1.5 rounded-lg font-mono border transition ${
                activeStage === 'at_risk'
                  ? 'bg-red-600 text-white border-red-500 font-bold'
                  : 'bg-slate-950/70 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              2. Priya AT_RISK (False Success)
            </button>

            <button
              onClick={() => onSwitchStage('swarm_detected')}
              className={`px-3 py-1.5 rounded-lg font-mono border transition ${
                activeStage === 'swarm_detected'
                  ? 'bg-amber-600 text-white border-amber-500 font-bold'
                  : 'bg-slate-950/70 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              3. Swarm / INC-0042 Active
            </button>

            <button
              onClick={() => onSwitchStage('resolved')}
              className={`px-3 py-1.5 rounded-lg font-mono border transition ${
                activeStage === 'resolved'
                  ? 'bg-emerald-600 text-white border-emerald-500 font-bold'
                  : 'bg-slate-950/70 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              4. Settlement FOUND (6 Verified)
            </button>
          </div>
        </div>

        {/* Right: Operational Actions (Reset, Settlement Toggle, Verification) */}
        <div className="flex flex-wrap items-center gap-2">
          {actionFeedback && (
            <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/80 px-2.5 py-1 rounded border border-emerald-500/30">
              {actionFeedback}
            </span>
          )}

          {/* Settlement Mode Toggle */}
          <button
            disabled={busy}
            onClick={handleToggleSettlement}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg font-mono border transition ${
              settlementMode === 'FOUND'
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/30'
                : 'bg-red-500/20 text-red-300 border-red-500/40 hover:bg-red-500/30'
            }`}
            title="Toggles whether bank settlement returns FOUND or NOT_FOUND"
          >
            {settlementMode === 'FOUND' ? (
              <ToggleRight className="w-4 h-4 text-emerald-400" />
            ) : (
              <ToggleLeft className="w-4 h-4 text-red-400" />
            )}
            <span>Settlement: {settlementMode}</span>
          </button>

          {/* Trigger Verification */}
          <button
            disabled={busy}
            onClick={handleRunVerification}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg font-mono bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
            <span>Run Verification</span>
          </button>

          {/* Reset Demo State */}
          <button
            disabled={busy}
            onClick={handleReset}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg font-mono bg-slate-800 hover:bg-slate-700 text-amber-300 border border-slate-700 transition"
            title="Reset system to start-of-demo state"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Reset Demo</span>
          </button>
        </div>

      </div>
    </div>
  );
};
