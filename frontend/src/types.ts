export type CommitmentStatus =
  | 'PROPOSED'
  | 'APPROVAL_PENDING'
  | 'REQUESTED'
  | 'ACKNOWLEDGED'
  | 'AWAITING_VERIFICATION'
  | 'VERIFIED'
  | 'AT_RISK'
  | 'ESCALATED'
  | 'DENIED';

export type PolicyDecision = 'ALLOW' | 'DENY' | 'NEEDS_APPROVAL';

export interface Commitment {
  id: string;
  case_ref: string;
  customer_name?: string;
  payment_ref: string;
  amount: number;
  currency: string;
  remedy: string;
  action_ref?: string | null;
  status: CommitmentStatus;
  policy_rule?: string;
  created_at: string;
  deadline?: string;
  evidence?: string;
  incident_id?: string | null;
  simulated?: boolean;
}

export interface Incident {
  id: string;
  status: string; // 'ACTIVE' | 'RESOLVING' | 'RESOLVED'
  signature: string;
  started_at?: string;
  affected_count?: number;
  contacted_count?: number;
  public_message: string;
}

export interface DashboardStats {
  incident: Incident | null;
  affected_transactions: number;
  contacted_support: number;
  commitments_created: number;
  verified: number;
  awaiting_or_at_risk: number;
  time_to_detect_seconds?: number | null;
  verified_resolution_rate?: number;
  simulated: boolean;
}

export interface SettlementModeRequest {
  mode: 'NOT_FOUND' | 'FOUND';
}

export type DemoStageKey = 'start' | 'at_risk' | 'swarm_detected' | 'resolved';
