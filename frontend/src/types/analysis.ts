// Analysis Configuration
export interface AnalysisConfig {
  project_id: number;
  analysis_type: 'linear' | 'modal' | 'time_history' | 'pushover' | 'buckling' | 'pdelta';
  solver?: 'direct' | 'iterative';
  convergence_tolerance?: number;
  max_iterations?: number;
  load_cases?: string[];
}

// Analysis Results
export interface AnalysisResults {
  analysis_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: number;
  node_displacements?: Record<number, {
    dx: number;
    dy: number;
    dz: number;
    rx: number;
    ry: number;
    rz: number;
  }>;
  element_forces?: Record<number, {
    axial: number;
    shear_y: number;
    shear_z: number;
    torsion: number;
    moment_y: number;
    moment_z: number;
  }>;
  reactions?: Record<number, {
    fx: number;
    fy: number;
    fz: number;
    mx: number;
    my: number;
    mz: number;
  }>;
  modal_results?: {
    frequencies: number[];
    periods: number[];
    mode_shapes: any[];
  };
  error?: string;
}

// Seismic Analysis
export interface SeismicConfig {
  code: 'IS1893' | 'ASCE7' | 'EUROCODE8';
  zone: string;
  importance_factor: number;
  response_reduction_factor: number;
  soil_type: string;
  damping_ratio: number;
  seismic_weight: number;
  time_period?: number;
}

// Wind Analysis
export interface WindConfig {
  code: 'IS875' | 'ASCE7' | 'EUROCODE1';
  basic_wind_speed: number;
  terrain_category: number;
  structure_class: string;
  height: number;
  width?: number;
  depth?: number;
}

// Pushover Analysis
export interface PushoverConfig {
  load_pattern: 'uniform' | 'triangular' | 'modal';
  target_displacement?: number;
  max_steps?: number;
  displacement_increment?: number;
}

// P-Delta Analysis
export interface PDeltaConfig {
  include_pdelta: boolean;
  geometric_stiffness: boolean;
  max_iterations?: number;
  convergence_tolerance?: number;
}
