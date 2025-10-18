import { useMutation } from '@tanstack/react-query';
import { reportingApi } from '@/lib/api';

export function useReporting() {
  const analysisReportMutation = useMutation({
    mutationFn: (data: any) => reportingApi.generateAnalysisReport(data),
  });

  const calculationSheetMutation = useMutation({
    mutationFn: (data: any) => reportingApi.generateCalculationSheet(data),
  });

  return {
    generateAnalysisReport: analysisReportMutation.mutateAsync,
    generateCalculationSheet: calculationSheetMutation.mutateAsync,
    isLoading: analysisReportMutation.isPending || calculationSheetMutation.isPending,
  };
}
