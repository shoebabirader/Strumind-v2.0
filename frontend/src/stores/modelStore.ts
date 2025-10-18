import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import type { Project, Node, Element, Material, Load, Section } from '@/types/model';

interface ModelState {
  currentProject: Project | null;
  nodes: Node[];
  elements: Element[];
  materials: Material[];
  loads: Load[];
  sections: Section[];
  selectedNodes: number[];
  selectedElements: number[];
  
  // Actions
  setCurrentProject: (project: Project | null) => void;
  setNodes: (nodes: Node[]) => void;
  addNode: (node: Node) => void;
  updateNode: (id: number, data: Partial<Node>) => void;
  deleteNode: (id: number) => void;
  
  setElements: (elements: Element[]) => void;
  addElement: (element: Element) => void;
  updateElement: (id: number, data: Partial<Element>) => void;
  deleteElement: (id: number) => void;
  
  setMaterials: (materials: Material[]) => void;
  addMaterial: (material: Material) => void;
  
  setLoads: (loads: Load[]) => void;
  addLoad: (load: Load) => void;
  
  setSections: (sections: Section[]) => void;
  addSection: (section: Section) => void;
  
  setSelectedNodes: (ids: number[]) => void;
  setSelectedElements: (ids: number[]) => void;
  clearSelection: () => void;
}

export const useModelStore = create<ModelState>()(
  immer((set) => ({
    currentProject: null,
    nodes: [],
    elements: [],
    materials: [],
    loads: [],
    sections: [],
    selectedNodes: [],
    selectedElements: [],
    
    setCurrentProject: (project) => set({ currentProject: project }),
    
    setNodes: (nodes) => set({ nodes }),
    addNode: (node) => set((state) => { state.nodes.push(node); }),
    updateNode: (id, data) => set((state) => {
      const index = state.nodes.findIndex(n => n.id === id);
      if (index !== -1) {
        state.nodes[index] = { ...state.nodes[index], ...data };
      }
    }),
    deleteNode: (id) => set((state) => {
      state.nodes = state.nodes.filter(n => n.id !== id);
    }),
    
    setElements: (elements) => set({ elements }),
    addElement: (element) => set((state) => { state.elements.push(element); }),
    updateElement: (id, data) => set((state) => {
      const index = state.elements.findIndex(e => e.id === id);
      if (index !== -1) {
        state.elements[index] = { ...state.elements[index], ...data };
      }
    }),
    deleteElement: (id) => set((state) => {
      state.elements = state.elements.filter(e => e.id !== id);
    }),
    
    setMaterials: (materials) => set({ materials }),
    addMaterial: (material) => set((state) => { state.materials.push(material); }),
    
    setLoads: (loads) => set({ loads }),
    addLoad: (load) => set((state) => { state.loads.push(load); }),
    
    setSections: (sections) => set({ sections }),
    addSection: (section) => set((state) => { state.sections.push(section); }),
    
    setSelectedNodes: (ids) => set({ selectedNodes: ids }),
    setSelectedElements: (ids) => set({ selectedElements: ids }),
    clearSelection: () => set({ selectedNodes: [], selectedElements: [] }),
  }))
);
