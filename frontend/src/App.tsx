import React, { useState } from 'react';
import { useDashboardPolling } from './useDashboardPolling';
import { SimulatedBanner } from './components/SimulatedBanner';
import { IncidentCard } from './components/IncidentCard';
import { KpiTiles } from './components/KpiTiles';
import { CommitmentLedger } from './components/CommitmentLedger';
import { EvidenceDrawer } from './components/EvidenceDrawer';
import { DemoControlBar } from './components/DemoControlBar';
import { Commitment } from './types';
import { Activity, RefreshCw, Radio, Layers, ShieldCheck, HelpCircle } from 'lucide-react';

export function App() {
  const {
    stats,
    commitments,
    incidents,
    isLiveBackend,
    loading,
    error,
    lastPolledAt,
    mode,
    setMode,
    activeStage,
    switchFixtureStage,
    refresh,
  } = useDashboardPolling(2000);

  const [selectedCommitment, setSelectedCommitment] = useState<Commitment | null>(null);

  // Active incident or fallback from stats
  const activeIncident = stats.incident || (incidents && incidents.length > 0 ? incidents[0] : null);

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* 1. Mandatory Simulated Data Banner */}
      <SimulatedBanner isLive={isLiveBackend} lastPolled={lastPolledAt} />

      {/* 2. Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-30 px-6 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
          
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-xl font-extrabold tracking-tight text-white font-mono">
                  PULSE
                </h1>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold">
                  TALKDESK INTEGRATION
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Autonomous Refund Verification & Incident Correlator
              </p>
            </div>
          </div>

          {/* Right Status Indicator */}
          <div className="flex items-center space-x-4 text-xs font-mono">
            <div className="flex items-center space-x-2 bg-slate-950/70 border border-slate-800 px-3 py-1.5 rounded-lg">
              <Radio className={`w-3.5 h-3.5 ${isLiveBackend ? 'text-emerald-400 animate-pulse' : 'text-amber-400'}`} />
              <span className="text-slate-300">
                {isLiveBackend ? 'POLLING LIVE (2s)' : 'FIXTURE PREVIEW'}
              </span>
            </div>

            <button
              onClick={() => refresh()}
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition"
              title="Manual refresh"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>

        </div>
      </header>

      {/* 3. Main Dashboard Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        
        {/* Demo Stage & Rehearsal Controller */}
        <DemoControlBar
          isLive={isLiveBackend}
          activeStage={activeStage}
          mode={mode}
          onSetMode={setMode}
          onSwitchStage={switchFixtureStage}
          onRefresh={refresh}
        />

        {/* Incident Detection Card */}
        <IncidentCard
          incident={activeIncident}
          affectedTransactions={stats.affected_transactions}
          contactedSupport={stats.contacted_support}
          timeToDetectSeconds={stats.time_to_detect_seconds}
        />

        {/* Projector-Ready KPI Tiles */}
        <KpiTiles
          commitmentsCreated={stats.commitments_created}
          verified={stats.verified}
          awaitingOrAtRisk={stats.awaiting_or_at_risk}
          resolutionRate={stats.verified_resolution_rate}
        />

        {/* KEPT Commitments Ledger */}
        <CommitmentLedger
          commitments={commitments}
          onSelectCommitment={setSelectedCommitment}
        />

      </main>

      {/* 4. Evidence Audit Flyout Drawer */}
      <EvidenceDrawer
        commitment={selectedCommitment}
        onClose={() => setSelectedCommitment(null)}
      />

      {/* 5. Footer Pitch */}
      <footer className="border-t border-slate-900 bg-slate-950/80 px-6 py-4 mt-auto text-xs text-slate-500 font-mono flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center space-x-2">
          <span className="text-slate-400 font-bold">PULSE Pitch:</span>
          <span className="text-slate-300">
            &ldquo;We make AI agents prove the refund actually arrived.&rdquo;
          </span>
        </div>
        <div className="text-slate-500">
          Talkdesk Hackathon • Person C (Incident, Frontend & QA)
        </div>
      </footer>
    </div>
  );
}
export default App;
