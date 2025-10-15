import React, { useState } from 'react'
import { X, FileText, Download } from 'lucide-react'

interface ReportDialogProps {
  isOpen: boolean
  onClose: () => void
  onGenerate: (data: any) => void
}

export default function ReportDialog({ isOpen, onClose, onGenerate }: ReportDialogProps) {
  const [reportType, setReportType] = useState<'analysis' | 'calculation' | 'design'>('analysis')
  const [format, setFormat] = useState<'pdf' | 'excel' | 'word'>('pdf')
  const [options, setOptions] = useState({
    includeGraphs: true,
    includeDetailedResults: true,
    includeDesignChecks: true,
    includeMaterialTakeoff: false,
    includeDrawings: false
  })

  if (!isOpen) return null

  const handleGenerate = () => {
    onGenerate({
      type: reportType,
      format,
      options,
      timestamp: new Date().toISOString()
    })
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-green-400" />
            <h2 className="text-lg font-semibold">Generate Report</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Report Type</label>
              <select
                value={reportType}
                onChange={(e) => setReportType(e.target.value as any)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              >
                <option value="analysis">Analysis Report</option>
                <option value="calculation">Calculation Sheet</option>
                <option value="design">Design Report</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Export Format</label>
              <select
                value={format}
                onChange={(e) => setFormat(e.target.value as any)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              >
                <option value="pdf">PDF</option>
                <option value="excel">Excel</option>
                <option value="word">Word</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-3">Report Contents</label>
            <div className="space-y-2">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={options.includeGraphs}
                  onChange={(e) => setOptions({ ...options, includeGraphs: e.target.checked })}
                  className="rounded"
                />
                <span className="text-sm">Include Graphs and Charts</span>
              </label>
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={options.includeDetailedResults}
                  onChange={(e) => setOptions({ ...options, includeDetailedResults: e.target.checked })}
                  className="rounded"
                />
                <span className="text-sm">Include Detailed Results</span>
              </label>
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={options.includeDesignChecks}
                  onChange={(e) => setOptions({ ...options, includeDesignChecks: e.target.checked })}
                  className="rounded"
                />
                <span className="text-sm">Include Design Checks</span>
              </label>
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={options.includeMaterialTakeoff}
                  onChange={(e) => setOptions({ ...options, includeMaterialTakeoff: e.target.checked })}
                  className="rounded"
                />
                <span className="text-sm">Include Material Takeoff</span>
              </label>
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={options.includeDrawings}
                  onChange={(e) => setOptions({ ...options, includeDrawings: e.target.checked })}
                  className="rounded"
                />
                <span className="text-sm">Include Drawings</span>
              </label>
            </div>
          </div>

          <div className="bg-blue-900 bg-opacity-20 border border-blue-700 rounded p-4">
            <p className="text-sm text-blue-300">
              The report will be generated based on the current analysis results and model data.
            </p>
          </div>

          <div className="flex justify-end space-x-3 pt-4 border-t border-gray-700">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
            >
              Cancel
            </button>
            <button
              onClick={handleGenerate}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Generate Report</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
