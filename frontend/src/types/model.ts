// Project
export interface Project {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
  owner_id?: number;
}

// Node
export interface Node {
  id: number;
  project_id: number;
  x: number;
  y: number;
  z: number;
  restraints?: {
    dx: boolean;
    dy: boolean;
    dz: boolean;
    rx: boolean;
    ry: boolean;
    rz: boolean;
  };
  label?: string;
}

export type NodeCreate = Omit<Node, 'id'>;
export type NodeUpdate = Partial<NodeCreate>;

// Element
export interface Element {
  id: number;
  project_id: number;
  node_i: number;
  node_j: number;
  element_type: 'beam' | 'column' | 'truss' | 'cable' | 'shell' | 'plate';
  section_id?: number;
  material_id?: number;
  release_i?: string;
  release_j?: string;
  label?: string;
}

export type ElementCreate = Omit<Element, 'id'>;
export type ElementUpdate = Partial<ElementCreate>;

// Material
export interface Material {
  id: number;
  project_id: number;
  name: string;
  material_type: 'concrete' | 'steel' | 'timber' | 'aluminum' | 'custom';
  elastic_modulus: number; // MPa or ksi
  poissons_ratio: number;
  density: number; // kg/m³ or lb/ft³
  yield_strength?: number;
  ultimate_strength?: number;
  grade?: string;
}

// Section
export interface Section {
  id: number;
  project_id: number;
  name: string;
  section_type: 'rectangular' | 'circular' | 'I' | 'T' | 'L' | 'channel' | 'custom';
  properties: {
    area?: number;
    Ix?: number;
    Iy?: number;
    J?: number;
    depth?: number;
    width?: number;
    thickness?: number;
    [key: string]: any;
  };
}

// Load
export interface Load {
  id: number;
  project_id: number;
  load_case: string;
  load_type: 'nodal' | 'distributed' | 'point' | 'moment' | 'temperature';
  target_type: 'node' | 'element';
  target_id: number;
  values: {
    fx?: number;
    fy?: number;
    fz?: number;
    mx?: number;
    my?: number;
    mz?: number;
    w?: number; // distributed load
    direction?: string;
    [key: string]: any;
  };
  load_pattern?: string;
}

// Load Combination
export interface LoadCombination {
  id: number;
  name: string;
  combination_type: 'linear' | 'envelope';
  factors: Record<string, number>; // load_case: factor
  code?: string;
}
