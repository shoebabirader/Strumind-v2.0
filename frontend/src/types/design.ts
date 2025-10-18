// Design Configuration
export interface DesignConfig {
  element_id: number;
  design_code: 'IS456' | 'IS800' | 'ACI318' | 'AISC360' | 'EUROCODE2' | 'EUROCODE3';
  material_grade: string;
  design_type: 'flexure' | 'shear' | 'torsion' | 'compression' | 'tension' | 'combined';
  load_combination_id?: number;
}

// Concrete Design (IS456)
export interface ConcreteDesignConfig {
  code: 'IS456' | 'ACI318' | 'EUROCODE2';
  concrete_grade: string; // M20, M25, M30, etc.
  steel_grade: string; // Fe415, Fe500, etc.
  cover: number; // mm
  member_type: 'beam' | 'column' | 'slab';
  dimensions: {
    width: number;
    depth: number;
    length?: number;
  };
  loads: {
    moment: number;
    shear: number;
    axial?: number;
    torsion?: number;
  };
}

// Steel Design (IS800)
export interface SteelDesignConfig {
  code: 'IS800' | 'AISC360' | 'EUROCODE3';
  steel_grade: string; // Fe250, Fe410, etc.
  section_type: string;
  member_type: 'beam' | 'column' | 'tension' | 'compression';
  length: number;
  loads: {
    axial?: number;
    moment_major?: number;
    moment_minor?: number;
    shear?: number;
  };
  end_conditions?: string;
}

// Foundation Design
export interface FoundationDesignConfig {
  foundation_type: 'isolated' | 'combined' | 'mat' | 'pile';
  loads: {
    vertical: number;
    horizontal_x: number;
    horizontal_y: number;
    moment_x: number;
    moment_y: number;
  };
  soil_bearing_capacity: number;
  depth: number;
  concrete_grade: string;
  steel_grade: string;
}

// Design Results
export interface DesignResults {
  status: 'pass' | 'fail' | 'warning';
  utilization_ratio: number;
  reinforcement?: {
    main_bars: string;
    stirrups: string;
    area_required: number;
    area_provided: number;
  };
  section_capacity?: {
    moment_capacity: number;
    shear_capacity: number;
    axial_capacity?: number;
  };
  checks: Array<{
    check_name: string;
    status: 'pass' | 'fail';
    value: number;
    limit: number;
    ratio: number;
  }>;
  warnings?: string[];
  errors?: string[];
}
