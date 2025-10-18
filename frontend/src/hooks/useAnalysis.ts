import { useMutation } from '@tanstack/react-query';
import { analysisApi, advancedAnalysisApi, seismicApi, windApi } from '@/lib/api';
import type { AnalysisConfig } from '@/types/analysis';

// SECURITY FIX: Use Record<string, unknown> for flexible but type-safe data
// This prevents code injection while allowing dynamic properties
export function useAnalysis() {
  const runAnalysisMutation = useMutation({
    mutationFn: (data: AnalysisConfig) => analysisApi.run(data),
  });

  const timeHistoryMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => advancedAnalysisApi.timeHistory(data as any),
  });

  const bucklingMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => advancedAnalysisApi.buckling(data as any),
  });

  const seismicMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => seismicApi.calculateBaseShear(data as any),
  });

  const windMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => windApi.calculateDesignPressure(data as any),
  });

  return {
    runAnalysis: runAnalysisMutation.mutateAsync,
    runTimeHistory: timeHistoryMutation.mutateAsync,
    runBuckling: bucklingMutation.mutateAsync,
    runSeismic: seismicMutation.mutateAsync,
    runWind: windMutation.mutateAsync,
    isLoading: runAnalysisMutation.isPending || timeHistoryMutation.isPending || bucklingMutation.isPending,
  };
}
