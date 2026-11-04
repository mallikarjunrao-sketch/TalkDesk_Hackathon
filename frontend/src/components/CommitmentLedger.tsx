import React from 'react';
import { Commitment, CommitmentStatus } from '../types';
import { ShieldAlert, CheckCircle2, Clock, Eye, AlertCircle, ArrowUpRight } from 'lucide-react';

interface CommitmentLedgerProps {
  commitments: Commitment[];
  onSelectCommitment: (commitment: Commitment) => void;
}

const statusBadgeConfig: Record<CommitmentStatus, { label: string; className: string; icon: React.ReactNode }> = {
  VERIFIED: {
    label: 'VERIFIED',
    className: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40',
    icon: <CheckCircle2 className="w-3.5 h-3.5 mr-1" />,
  },
  AT_RISK: {
    label: 'AT_RISK',
    className: 'bg-red-500/20 text-red-300 border-red-500/50 animate-pulse font-extrabold',
    icon: <ShieldAlert className="w-3.5 h-3.5 mr-1 text-red-400" />,
  },
  AWAITING_VERIFICATION: {
    label: 'AWAITING_VERIFICATION',
    className: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/40',
    icon: <Clock className="w-3.5 h-3.5 mr-1 text-cyan-400" />,
  },
  ACKNOWLEDGED: {
    label: 'ACKNOWLEDGED',
    className: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/40',
    icon: <Clock className="w-3.5 h-3.5 mr-1 text-indigo-400" />,
  },
  APPROVAL_PENDING: {
    label: 'APPROVAL_PENDING',
    className: 'bg-amber-500/15 text-amber-300 border-amber-500/40',
    icon: <AlertCircle className="w-3.5 h-3.5 mr-1 text-amber-400" />,
  },
  REQUESTED: {
    label: 'REQUESTED',
    className: 'bg-blue-500/15 text-blue-300 border-blue-500/40',
    icon: <Clock className="w-3.5 h-3.5 mr-1" />,
  },
  PROPOSED: {
    label: 'PROPOSED',
    className: 'bg-slate-700/40 text-slate-300 border-slate-600',
    icon: null,
  },
  ESCALATED: {
    label: 'ESCALATED',
    className: 'bg-purple-500/20 text-purple-300 border-purple-500/50',
    icon: <AlertCircle className="w-3.5 h-3.5 mr-1" />,
  },
  DENIED: {
    label: 'DENIED',
    className: 'bg-rose-900/30 text-rose-300 border-rose-700',
    icon: null,
  },
};

export const CommitmentLedger: React.FC<CommitmentLedgerProps> = ({
  commitments,
  onSelectCommitment,
}) => {
  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl shadow-xl backdrop-blur overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>KEPT Commitments Ledger</span>
            <span className="text-xs font-mono font-normal bg-slate-800 text-slate-300 px-2 py-0.5 rounded-full">
              {commitments.length} records
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Immutable log of promises made by Talkdesk AI agent, independently verified against bank settlement.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
          <span className="flex items-center space-x-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span>Verified</span>
          </span>
          <span className="mx-1">•</span>
          <span className="flex items-center space-x-1">
            <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse" />
            <span>At Risk</span>
          </span>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-950/60 text-slate-400 text-xs uppercase font-mono border-b border-slate-800">
            <tr>
              <th className="px-6 py-3.5">Commitment ID</th>
              <th className="px-6 py-3.5">Customer & Case</th>
              <th className="px-6 py-3.5">Payment Ref</th>
              <th className="px-6 py-3.5">Amount</th>
              <th className="px-6 py-3.5">Action Ref</th>
              <th className="px-6 py-3.5">Status</th>
              <th className="px-6 py-3.5 text-right">Audit</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80 font-mono text-xs">
            {commitments.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-6 py-10 text-center text-slate-500 font-sans">
                  No commitments created yet. Waiting for Talkdesk agent conversation or seed data...
                </td>
              </tr>
            ) : (
              commitments.map((c) => {
                const isHero = c.payment_ref === 'TX-101' || c.case_ref === 'CASE-2041';
                const badge = statusBadgeConfig[c.status] || {
                  label: c.status,
                  className: 'bg-slate-800 text-slate-300 border-slate-700',
                  icon: null,
                };

                return (
                  <tr
                    key={c.id}
                    onClick={() => onSelectCommitment(c)}
                    className={`hover:bg-slate-800/40 transition cursor-pointer ${
                      c.status === 'AT_RISK' ? 'bg-red-950/15' : ''
                    }`}
                  >
                    {/* Commitment ID */}
                    <td className="px-6 py-4 font-bold text-slate-200">
                      <div className="flex items-center space-x-1.5">
                        <span>{c.id}</span>
                        {isHero && (
                          <span className="text-[10px] bg-indigo-500/30 text-indigo-300 border border-indigo-500/50 px-1.5 py-0.2 rounded font-sans font-bold">
                            HERO (Priya)
                          </span>
                        )}
                      </div>
                    </td>

                    {/* Customer & Case */}
                    <td className="px-6 py-4 font-sans">
                      <div className="font-medium text-slate-200">{c.customer_name || 'Customer'}</div>
                      <div className="text-[11px] font-mono text-slate-400">{c.case_ref}</div>
                    </td>

                    {/* Payment Ref */}
                    <td className="px-6 py-4 text-slate-300">
                      {c.payment_ref}
                    </td>

                    {/* Amount */}
                    <td className="px-6 py-4 text-white font-bold">
                      ₹{c.amount.toLocaleString()}
                    </td>

                    {/* Action Ref */}
                    <td className="px-6 py-4 text-cyan-300">
                      {c.action_ref || '—'}
                    </td>

                    {/* Status Badge */}
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-full text-[11px] border ${badge.className}`}
                      >
                        {badge.icon}
                        {badge.label}
                      </span>
                    </td>

                    {/* Audit / Action */}
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectCommitment(c);
                        }}
                        className="inline-flex items-center text-xs font-sans text-indigo-400 hover:text-indigo-300 bg-indigo-500/10 hover:bg-indigo-500/20 px-2.5 py-1 rounded border border-indigo-500/20 transition"
                      >
                        <Eye className="w-3.5 h-3.5 mr-1" />
                        Inspect Proof
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
