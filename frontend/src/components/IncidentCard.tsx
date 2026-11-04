import React from 'react';
import { Incident } from '../types';
import { Flame, Activity, ShieldCheck, Clock, Users, ArrowUpRight } from 'lucide-react';

interface IncidentCardProps {
  incident: Incident | null;
  affectedTransactions: number;
  contactedSupport: number;
  timeToDetectSeconds?: number | null;
}

export const IncidentCard: React.FC<IncidentCardProps> = ({
  incident,
  affectedTransactions,
  contactedSupport,
  timeToDetectSeconds,
}) => {
  if (!incident) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-lg backdrop-blur flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-slate-200">No Active Incident Detected</h3>
            <p className="text-sm text-slate-400">
              Autonomous verifier running. Event correlation signature threshold not triggered (&lt; 5 events / 120s).
            </p>
          </div>
        </div>
        <div className="text-right">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            SYSTEM NOMINAL
          </span>
        </div>
      </div>
    );
  }

  const isResolving = incident.status === 'RESOLVING';

  return (
    <div
      className={`border rounded-xl p-5 shadow-2xl backdrop-blur transition-all duration-300 relative overflow-hidden ${
        isResolving
          ? 'bg-amber-950/20 border-amber-500/40 shadow-amber-900/20'
          : 'bg-red-950/25 border-red-500/60 shadow-red-950/40 ring-1 ring-red-500/40'
      }`}
    >
      {/* Background glow banner indicator */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-red-500/5 rounded-full blur-3xl pointer-events-none" />

      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Left: Incident info & Signature */}
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <div className={`p-2.5 rounded-lg ${isResolving ? 'bg-amber-500/20 text-amber-400' : 'bg-red-500/20 text-red-400 animate-pulse'}`}>
              <Flame className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-mono text-xs uppercase px-2 py-0.5 rounded font-bold bg-red-500/20 text-red-300 border border-red-500/40">
                  {incident.status}
                </span>
                <span className="font-mono text-sm font-bold text-slate-100 tracking-wide">
                  {incident.id}
                </span>
              </div>
              <h2 className="text-xl font-bold text-white tracking-tight mt-0.5">
                Mass Mismatch: {incident.signature}
              </h2>
            </div>
          </div>

          <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg px-3.5 py-2 text-sm text-slate-300 max-w-2xl font-mono">
            <span className="text-amber-400 font-semibold">Talkdesk GUIDE Broadcast: </span>
            &ldquo;{incident.public_message}&rdquo;
          </div>
        </div>

        {/* Right: Key Incident Metrics */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="bg-slate-950/70 border border-slate-800 rounded-lg px-4 py-2.5 min-w-[130px]">
            <div className="text-xs text-slate-400 font-medium flex items-center space-x-1">
              <Activity className="w-3.5 h-3.5 text-red-400" />
              <span>Affected TXs</span>
            </div>
            <div className="text-2xl font-bold font-mono text-red-400 mt-0.5">
              {affectedTransactions || incident.affected_count || 50}
            </div>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg px-4 py-2.5 min-w-[130px]">
            <div className="text-xs text-slate-400 font-medium flex items-center space-x-1">
              <Users className="w-3.5 h-3.5 text-blue-400" />
              <span>Contacted Help</span>
            </div>
            <div className="text-2xl font-bold font-mono text-blue-400 mt-0.5">
              {contactedSupport || incident.contacted_count || 8}
            </div>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg px-4 py-2.5 min-w-[130px]">
            <div className="text-xs text-slate-400 font-medium flex items-center space-x-1">
              <Clock className="w-3.5 h-3.5 text-emerald-400" />
              <span>Time to Detect</span>
            </div>
            <div className="text-2xl font-bold font-mono text-emerald-400 mt-0.5">
              {timeToDetectSeconds ? `${timeToDetectSeconds}s` : '47s'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
