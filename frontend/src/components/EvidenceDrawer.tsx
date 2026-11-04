import React from 'react';
import { Commitment } from '../types';
import { X, ShieldAlert, CheckCircle, Clock, FileText, ArrowRight, ShieldCheck, Terminal } from 'lucide-react';

interface EvidenceDrawerProps {
  commitment: Commitment | null;
  onClose: () => void;
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({ commitment, onClose }) => {
  if (!commitment) return null;

  const isVerified = commitment.status === 'VERIFIED';
  const isAtRisk = commitment.status === 'AT_RISK';

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/70 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-xl bg-slate-900 border-l border-slate-800 h-full p-6 shadow-2xl flex flex-col justify-between overflow-y-auto animate-in slide-in-from-right duration-300">
        
        {/* Header */}
        <div>
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div className="flex items-center space-x-2">
              <span className="font-mono text-xs px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-bold">
                {commitment.id}
              </span>
              <span className="text-lg font-bold text-white">KEPT Ledger Verification Audit</span>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Status Banner */}
          <div className="mt-5">
            {isAtRisk && (
              <div className="bg-red-950/40 border border-red-500/50 rounded-xl p-4 text-red-200">
                <div className="flex items-center space-x-2 text-red-400 font-bold text-sm">
                  <ShieldAlert className="w-5 h-5" />
                  <span>FALSE SUCCESS CAUGHT BY INDEPENDENT VERIFIER</span>
                </div>
                <p className="text-xs text-red-300/90 mt-1 leading-relaxed">
                  The Refund API returned <code>200 ACCEPTED</code>, but the autonomous verifier probed the bank settlement ledger and found <code>NOT_FOUND</code>.
                  PULSE refused to mark this commitment completed or tell the customer the money arrived.
                </p>
              </div>
            )}

            {isVerified && (
              <div className="bg-emerald-950/40 border border-emerald-500/50 rounded-xl p-4 text-emerald-200">
                <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm">
                  <ShieldCheck className="w-5 h-5" />
                  <span>INDEPENDENT SETTLEMENT PROVED & VERIFIED</span>
                </div>
                <p className="text-xs text-emerald-300/90 mt-1 leading-relaxed">
                  Funds have been verified directly in the clearing ledger. Customer can now be truthfully notified of completed refund.
                </p>
              </div>
            )}
          </div>

          {/* Metadata Grid */}
          <div className="grid grid-cols-2 gap-3 mt-5">
            <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              <span className="text-[11px] text-slate-400 uppercase font-mono block">Customer / Case</span>
              <span className="text-sm font-semibold text-white">{commitment.customer_name || 'Customer'}</span>
              <span className="text-xs font-mono text-slate-400 block">{commitment.case_ref}</span>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              <span className="text-[11px] text-slate-400 uppercase font-mono block">Transaction / Refund Amount</span>
              <span className="text-sm font-semibold text-white">₹{commitment.amount.toLocaleString()}</span>
              <span className="text-xs font-mono text-slate-400 block">{commitment.payment_ref}</span>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              <span className="text-[11px] text-slate-400 uppercase font-mono block">Action Reference</span>
              <span className="text-sm font-mono text-cyan-400">{commitment.action_ref || 'None (Pending)'}</span>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              <span className="text-[11px] text-slate-400 uppercase font-mono block">Policy Gate Decision</span>
              <span className="text-xs font-mono text-indigo-300">{commitment.policy_rule || 'Deterministic Rules R1-R5'}</span>
            </div>
          </div>

          {/* Audit Trail & Evidence */}
          <div className="mt-5">
            <span className="text-xs uppercase font-mono tracking-wider text-slate-400 block mb-2">
              Verifier Evidence & Cryptographic Audit String
            </span>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200 space-y-2">
              <div className="flex items-start space-x-2 text-emerald-400">
                <Terminal className="w-4 h-4 mt-0.5 shrink-0" />
                <span className="text-slate-400">Verifier Evidence:</span>
              </div>
              <p className="text-amber-300 pl-6 leading-relaxed bg-slate-900/50 p-2.5 rounded border border-slate-800/80">
                {commitment.evidence || 'No evidence recorded yet.'}
              </p>
              
              <div className="pt-2 border-t border-slate-800 text-[11px] text-slate-400 space-y-1">
                <div>Created: {new Date(commitment.created_at).toLocaleString()}</div>
                <div>Deadline: {commitment.deadline ? new Date(commitment.deadline).toLocaleString() : 'N/A'}</div>
                <div>Linked Incident: {commitment.incident_id || 'None'}</div>
              </div>
            </div>
          </div>

          {/* Golden Rule Callout */}
          <div className="mt-5 bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/50 text-xs text-slate-300 flex items-start space-x-2.5">
            <FileText className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-indigo-300">Hackathon Rule: </span>
              "Never claim 'completed' without VERIFIED. No code, prompt or slide may say a refund is done based only on an API 'accepted' response."
            </div>
          </div>
        </div>

        {/* Footer actions */}
        <div className="pt-6 border-t border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm font-medium transition"
          >
            Close Audit
          </button>
        </div>

      </div>
    </div>
  );
};
