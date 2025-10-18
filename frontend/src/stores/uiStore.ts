import { create } from 'zustand';

type DialogType = 
  | 'project' | 'node' | 'element' | 'material' | 'load' | 'section'
  | 'analysis' | 'seismic' | 'wind' | 'design' | 'foundation'
  | 'login' | 'register' | 'disclaimer'
  | null;

interface UIState {
  theme: 'light' | 'dark';
  activeDialog: DialogType;
  leftPanelOpen: boolean;
  rightPanelOpen: boolean;
  bottomPanelOpen: boolean;
  loading: boolean;
  
  setTheme: (theme: 'light' | 'dark') => void;
  openDialog: (dialog: DialogType) => void;
  closeDialog: () => void;
  toggleLeftPanel: () => void;
  toggleRightPanel: () => void;
  toggleBottomPanel: () => void;
  setLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  theme: 'light',
  activeDialog: null,
  leftPanelOpen: true,
  rightPanelOpen: true,
  bottomPanelOpen: false,
  loading: false,
  
  setTheme: (theme) => set({ theme }),
  openDialog: (dialog) => set({ activeDialog: dialog }),
  closeDialog: () => set({ activeDialog: null }),
  toggleLeftPanel: () => set((state) => ({ leftPanelOpen: !state.leftPanelOpen })),
  toggleRightPanel: () => set((state) => ({ rightPanelOpen: !state.rightPanelOpen })),
  toggleBottomPanel: () => set((state) => ({ bottomPanelOpen: !state.bottomPanelOpen })),
  setLoading: (loading) => set({ loading }),
}));
