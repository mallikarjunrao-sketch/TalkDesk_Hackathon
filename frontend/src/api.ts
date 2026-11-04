import { DashboardStats, Commitment, Incident } from './types';
import fixturesData from './fixtures.json';

const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  isLive: boolean;
}

export const pulseApi = {
  async getDashboard(): Promise<DashboardStats> {
    const res = await fetch(`${API_BASE}/dashboard`);
    if (!res.ok) throw new Error(`Dashboard fetch failed: ${res.statusText}`);
    return res.json();
  },

  async getCommitments(): Promise<Commitment[]> {
    const res = await fetch(`${API_BASE}/commitments`);
    if (!res.ok) throw new Error(`Commitments fetch failed: ${res.statusText}`);
    const data = await res.json();
    return Array.isArray(data) ? data : data.commitments || [];
  },

  async getIncidents(): Promise<Incident[]> {
    const res = await fetch(`${API_BASE}/incidents`);
    if (!res.ok) throw new Error(`Incidents fetch failed: ${res.statusText}`);
    const data = await res.json();
    return Array.isArray(data) ? data : data.incidents || [];
  },

  async setSettlementMode(mode: 'NOT_FOUND' | 'FOUND'): Promise<{ success: boolean; mode: string }> {
    const res = await fetch(`${API_BASE}/admin/settlement-mode`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode }),
    });
    if (!res.ok) throw new Error(`Set settlement mode failed: ${res.statusText}`);
    return res.json();
  },

  async resetDemoState(): Promise<{ success: boolean; message: string }> {
    const res = await fetch(`${API_BASE}/admin/reset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`Reset failed: ${res.statusText}`);
    return res.json();
  },

  async triggerVerification(commitmentId?: string): Promise<any> {
    const body = commitmentId ? { commitment_id: commitmentId } : {};
    const res = await fetch(`${API_BASE}/verification/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`Verification run failed: ${res.statusText}`);
    return res.json();
  },

  async ingestEvent(event: { type: string; payment_ref: string; ts?: string }): Promise<any> {
    const res = await fetch(`${API_BASE}/events/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...event,
        ts: event.ts || new Date().toISOString(),
      }),
    });
    if (!res.ok) throw new Error(`Event ingest failed: ${res.statusText}`);
    return res.json();
  },
};

export function getFixtureData(stage: keyof typeof fixturesData.stages = 'at_risk') {
  return fixturesData.stages[stage] || fixturesData.stages.at_risk;
}
