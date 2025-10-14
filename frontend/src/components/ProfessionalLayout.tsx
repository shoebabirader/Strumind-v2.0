import { useState, ReactNode } from 'react'
import '../styles/professional.css'

interface ProfessionalLayoutProps {
  children: ReactNode
}

export default function ProfessionalLayout({ children }: ProfessionalLayoutProps) {
  const [leftPanelWidth, setLeftPanelWidth] = useState(280)
  const [rightPanelWidth, setRightPanelWidth] = useState(300)
  const [showLeftPanel, setShowLeftPanel] = useState(true)
  const [showRightPanel, setShowRightPanel] = useState(true)

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Top Menu Bar */}
      <div className="bg-gray-800 text-white px-4 py-1 flex items-center gap-6 text-sm">
        <div className="font-bold text-blue-400">StruMind</div>
        <div className="flex gap-4">
          <button className="hover:bg-gray-700 px-3 py-1 rounded">File</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Edit</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">View</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Define</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Assign</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Analyze</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Design</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Display</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Tools</button>
          <button className="hover:bg-gray-700 px-3 py-1 rounded">Help</button>
        </div>
      </div>

      {/* Toolbar */}
      <div className="toolbar">
        <div className="toolbar-group">
          <button className="toolbar-button" title="New Model">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span className="toolbar-label">New</span>
          </button>
          <button className="toolbar-button" title="Open Model">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
            </svg>
            <span className="toolbar-label">Open</span>
          </button>
          <button className="toolbar-button" title="Save Model">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
            <span className="toolbar-label">Save</span>
          </button>
        </div>

        <div className="toolbar-group">
          <button className="toolbar-button active" title="Select">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
            </svg>
            <span className="toolbar-label">Select</span>
          </button>
          <button className="toolbar-button" title="Draw Node">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span className="toolbar-label">Node</span>
          </button>
          <button className="toolbar-button" title="Draw Frame">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
            </svg>
            <span className="toolbar-label">Frame</span>
          </button>
          <button className="toolbar-button" title="Draw Shell">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V5z" />
            </svg>
            <span className="toolbar-label">Shell</span>
          </button>
        </div>

        <div className="toolbar-group">
          <button className="toolbar-button" title="Run Analysis">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span className="toolbar-label">Analyze</span>
          </button>
          <button className="toolbar-button" title="Design">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span className="toolbar-label">Design</span>
          </button>
        </div>

        <div className="toolbar-group">
          <button className="toolbar-button" title="3D View">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            <span className="toolbar-label">3D View</span>
          </button>
          <button className="toolbar-button" title="Zoom Extents">
            <svg className="toolbar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
            </svg>
            <span className="toolbar-label">Zoom</span>
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        {showLeftPanel && (
          <div className="sidebar" style={{ width: `${leftPanelWidth}px` }}>
            <div className="sidebar-section">
              <div className="sidebar-header">
                <span>Model Explorer</span>
                <button onClick={() => setShowLeftPanel(false)} className="text-gray-600 hover:text-gray-800">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="sidebar-content">
                <ul className="tree-view">
                  <li className="tree-item selected">
                    <svg className="tree-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                    </svg>
                    <span>Project 1</span>
                  </li>
                  <li className="tree-item ml-4">
                    <svg className="tree-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span>Nodes (24)</span>
                  </li>
                  <li className="tree-item ml-4">
                    <svg className="tree-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5h16M4 12h16M4 19h16" />
                    </svg>
                    <span>Frames (18)</span>
                  </li>
                  <li className="tree-item ml-4">
                    <svg className="tree-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V5z" />
                    </svg>
                    <span>Shells (12)</span>
                  </li>
                  <li className="tree-item ml-4">
                    <svg className="tree-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span>Loads (8)</span>
                  </li>
                </ul>
              </div>
            </div>

            <div className="sidebar-section">
              <div className="sidebar-header">
                <span>Analysis Cases</span>
              </div>
              <div className="sidebar-content">
                <ul className="tree-view">
                  <li className="tree-item">
                    <input type="checkbox" className="mr-2" checked readOnly />
                    <span>Dead Load</span>
                  </li>
                  <li className="tree-item">
                    <input type="checkbox" className="mr-2" checked readOnly />
                    <span>Live Load</span>
                  </li>
                  <li className="tree-item">
                    <input type="checkbox" className="mr-2" checked readOnly />
                    <span>Seismic X</span>
                  </li>
                  <li className="tree-item">
                    <input type="checkbox" className="mr-2" checked readOnly />
                    <span>Seismic Y</span>
                  </li>
                  <li className="tree-item">
                    <input type="checkbox" className="mr-2" />
                    <span>Wind X</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Center - Main Viewport */}
        <div className="flex-1 flex flex-col bg-gray-900">
          {/* Tab Bar */}
          <div className="tab-bar">
            <div className="tab active">3D View</div>
            <div className="tab">Plan View</div>
            <div className="tab">Elevation</div>
          </div>

          {/* Main Content */}
          <div className="flex-1 relative">
            {children}
          </div>
        </div>

        {/* Right Sidebar - Properties */}
        {showRightPanel && (
          <div className="sidebar" style={{ width: `${rightPanelWidth}px` }}>
            <div className="sidebar-section">
              <div className="sidebar-header">
                <span>Properties</span>
                <button onClick={() => setShowRightPanel(false)} className="text-gray-600 hover:text-gray-800">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="sidebar-content">
                <div className="property-grid">
                  <div className="property-row">
                    <div className="property-label">Object Type:</div>
                    <div className="property-value">
                      <input type="text" value="Frame" readOnly className="bg-gray-100" />
                    </div>
                  </div>
                  <div className="property-row">
                    <div className="property-label">Label:</div>
                    <div className="property-value">
                      <input type="text" value="B1" />
                    </div>
                  </div>
                  <div className="property-row">
                    <div className="property-label">Section:</div>
                    <div className="property-value">
                      <select>
                        <option>300x450</option>
                        <option>300x600</option>
                        <option>400x600</option>
                      </select>
                    </div>
                  </div>
                  <div className="property-row">
                    <div className="property-label">Material:</div>
                    <div className="property-value">
                      <select>
                        <option>M25</option>
                        <option>M30</option>
                        <option>M40</option>
                      </select>
                    </div>
                  </div>
                  <div className="property-row">
                    <div className="property-label">Length:</div>
                    <div className="property-value">
                      <input type="number" value="6000" /> mm
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="sidebar-section">
              <div className="sidebar-header">
                <span>Analysis Results</span>
              </div>
              <div className="sidebar-content">
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Moment:</span>
                    <span className="font-semibold">125.4 kNm</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Shear:</span>
                    <span className="font-semibold">45.2 kN</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Axial:</span>
                    <span className="font-semibold">320.8 kN</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Deflection:</span>
                    <span className="font-semibold">12.5 mm</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Status Bar */}
      <div className="status-bar">
        <div className="status-item">
          <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <circle cx="10" cy="10" r="8" className="text-green-500" />
          </svg>
          <span>Ready</span>
        </div>
        <div className="status-item">
          <span>Nodes: 24</span>
        </div>
        <div className="status-item">
          <span>Elements: 30</span>
        </div>
        <div className="status-item">
          <span>Load Cases: 5</span>
        </div>
        <div className="status-item">
          <span>Units: kN, m</span>
        </div>
        <div className="status-item">
          <span>Coord: X=0.00, Y=0.00, Z=0.00</span>
        </div>
      </div>
    </div>
  )
}
