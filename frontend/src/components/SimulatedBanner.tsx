import React from 'react';

interface SimulatedBannerProps {
  isLive: boolean;
  lastPolled: Date;
}

export const SimulatedBanner: React.FC<SimulatedBannerProps> = ({ isLive, lastPolled }) => {
  return (
    <div className="bg-amber-950/80 border-b border-amber-500/40 px-4 py-2 text-xs font-mono tracking-wider flex flex-wrap items-center justify-between text-amber-200">
      <div className="flex items-center space-x-2">
        <span className="bg-amber-500 text-slate-950 font-extrabold px-2 py-0.5 rounded text-[11px] uppercase tracking-normal">
          Simulated Data
        </span>
        <span className="font-medium text-amber-100">
          All transactions, bank reconciliation feeds, and customer records are simulated for hackathon demonstration.
        </span>
      </div>

      <div className="flex items-center space-x-4 mt-1 sm:mt-0">
        <div className="flex items-center space-x-1.5">
          <span className={`inline-block w-2 h-2 rounded-full ${isLive ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
          <span className="text-slate-300">
            {isLive ? 'Connected to FastAPI (:8000)' : 'Fixture Simulation Mode'}
          </span>
        </div>
        <span className="text-slate-400 hidden md:inline">
          Last polled: {lastPolled.toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
};
