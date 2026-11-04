import { useState, useEffect, useCallback, useRef } from 'react';
import { DashboardStats, Commitment, Incident, DemoStageKey } from './types';
import { pulseApi, getFixtureData } from './api';

export function useDashboardPolling(intervalMs: number = 2000) {
  const [mode, setMode] = useState<'auto' | 'fixtures' | 'live'>('auto');
  const [activeStage, setActiveStage] = useState<DemoStageKey>('swarm_detected');
  const [isLiveBackend, setIsLiveBackend] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastPolledAt, setLastPolledAt] = useState<Date>(new Date());

  const initialFixtures = getFixtureData('swarm_detected');
  const [stats, setStats] = useState<DashboardStats>(initialFixtures.dashboard as unknown as DashboardStats);
  const [commitments, setCommitments] = useState<Commitment[]>(initialFixtures.commitments as unknown as Commitment[]);
  const [incidents, setIncidents] = useState<Incident[]>(initialFixtures.incidents as unknown as Incident[]);

  const isPollingRef = useRef<boolean>(false);

  const fetchLive = useCallback(async () => {
    if (isPollingRef.current) return;
    isPollingRef.current = true;
    try {
      const [dashData, commData, incData] = await Promise.all([
        pulseApi.getDashboard(),
        pulseApi.getCommitments(),
        pulseApi.getIncidents(),
      ]);

      setStats(dashData);
      setCommitments(commData);
      setIncidents(incData);
      setIsLiveBackend(true);
      setError(null);
      setLastPolledAt(new Date());
    } catch (err: any) {
      if (mode === 'live') {
        setError(err.message || 'Failed to connect to backend :8000');
        setIsLiveBackend(false);
      } else {
        // Fall back gracefully to active fixture stage
        setIsLiveBackend(false);
        const fix = getFixtureData(activeStage);
        setStats(fix.dashboard as unknown as DashboardStats);
        setCommitments(fix.commitments as unknown as Commitment[]);
        setIncidents(fix.incidents as unknown as Incident[]);
        setError(null);
        setLastPolledAt(new Date());
      }
    } finally {
      setLoading(false);
      isPollingRef.current = false;
    }
  }, [mode, activeStage]);

  // Handle stage change in fixtures mode
  const switchFixtureStage = useCallback((stage: DemoStageKey) => {
    setActiveStage(stage);
    const fix = getFixtureData(stage);
    setStats(fix.dashboard as unknown as DashboardStats);
    setCommitments(fix.commitments as unknown as Commitment[]);
    setIncidents(fix.incidents as unknown as Incident[]);
    setLastPolledAt(new Date());
  }, []);

  useEffect(() => {
    if (mode === 'fixtures') {
      setIsLiveBackend(false);
      switchFixtureStage(activeStage);
      setLoading(false);
      return;
    }

    // Run first fetch immediately
    fetchLive();

    const timer = setInterval(() => {
      fetchLive();
    }, intervalMs);

    return () => clearInterval(timer);
  }, [mode, activeStage, intervalMs, fetchLive, switchFixtureStage]);

  return {
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
    refresh: fetchLive,
  };
}
