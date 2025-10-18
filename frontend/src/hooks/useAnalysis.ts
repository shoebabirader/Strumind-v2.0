import { useMutation } from '@tanstack/react-query';
import { analysisApi, advancedAnalysisApi, seismicApi, windApi } from '@/lib/api';
import type { AnalysisConfig } from '@/types/analysis';

export function useAnalysis() {
  const runAnalysisMutation = useMutation({
    mutationFn: (data: AnalysisConfig) => analysisApi.run(data),
  });

  const timeHistoryMutation = useMutation({
    mutationFn: (data: any) => advancedAnalysisApi.timeHistory(data),
  });

  const bucklingMutation = useMutation({
    mutationFn: (data: any) => advancedAnalysisApi.buckling(data),
  });

  const seismicMutation = useMutation({
    mutationFn: (data: any) => seismicApi.calculateBaseShear(data),
  });

  const windMutation = useMutation({
    mutationFn: (data: any) => windApi.calculateDesignPressure(data),
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
