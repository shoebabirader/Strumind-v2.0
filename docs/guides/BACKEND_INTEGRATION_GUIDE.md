# 🔗 Backend Integration Guide

## Current Status

### ✅ **Already Connected**
1. **Authentication** - Fully working
2. **Analysis** - Fully working

### ⚠️ **Ready for Connection** (Structure in place)
3. **Node CRUD**
4. **Element CRUD**
5. **Material CRUD**
6. **Load Definition**
7. **Project Management**

---

## 🚀 **How to Complete Backend Integration**

### **Step 1: Add Backend Endpoints**

First, ensure your backend has these endpoints:

```python
# backend/main.py or backend/routers/

# Nodes
@app.post("/api/nodes/create")
@app.get("/api/nodes/list")
@app.put("/api/nodes/{node_id}")
@app.delete("/api/nodes/{node_id}")

# Elements
@app.post("/api/elements/create")
@app.get("/api/elements/list")
@app.put("/api/elements/{element_id}")
@app.delete("/api/elements/{element_id}")

# Materials
@app.post("/api/materials/create")
@app.get("/api/materials/list")
@app.put("/api/materials/{material_id}")
@app.delete("/api/materials/{material_id}")

# Loads
@app.post("/api/loads/create")
@app.get("/api/loads/list")
@app.put("/api/loads/{load_id}")
@app.delete("/api/loads/{load_id}")
```

---

### **Step 2: Update API Client**

Add the new endpoints to `frontend/src/lib/api.ts`:

```typescript
// Add to api.ts

// Node APIs
export const nodeAPI = {
  create: (data: any) => api.post('/api/nodes/create', data),
  list: () => api.get('/api/nodes/list'),
  update: (id: string, data: any) => api.put(`/api/nodes/${id}`, data),
  delete: (id: string) => api.delete(`/api/nodes/${id}`),
}

// Element APIs
export const elementAPI = {
  create: (data: any) => api.post('/api/elements/create', data),
  list: () => api.get('/api/elements/list'),
  update: (id: string, data: any) => api.put(`/api/elements/${id}`, data),
  delete: (id: string) => api.delete(`/api/elements/${id}`),
}

// Material APIs
export const materialAPI = {
  create: (data: any) => api.post('/api/materials/create', data),
  list: () => api.get('/api/materials/list'),
  update: (id: string, data: any) => api.put(`/api/materials/${id}`, data),
  delete: (id: string) => api.delete(`/api/materials/${id}`),
}

// Load APIs
export const loadAPI = {
  create: (data: any) => api.post('/api/loads/create', data),
  list: () => api.get('/api/loads/list'),
  update: (id: string, data: any) => api.put(`/api/loads/${id}`, data),
  delete: (id: string) => api.delete(`/api/loads/${id}`),
}
```

---

### **Step 3: Update ElementDialog**

```typescript
// frontend/src/components/dialogs/ElementDialog.tsx

import { elementAPI } from '@/lib/api'

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setLoading(true)
  setError('')
  
  try {
    const elementData = {
      ...formData,
      width: parseFloat(formData.width as any),
      height: parseFloat(formData.height as any),
    }
    
    // Save to backend
    await elementAPI.create(elementData)
    
    // Add to local state
    addElement(elementData)
    
    onClose()
    setFormData({ id: '', nodeI: '', nodeJ: '', type: 'beam', materialId: '', sectionType: 'rectangular', width: 0.3, height: 0.5 })
  } catch (err: any) {
    setError(err.response?.data?.detail || 'Failed to add element')
  } finally {
    setLoading(false)
  }
}
```

---

### **Step 4: Update MaterialDialog**

```typescript
// frontend/src/components/dialogs/MaterialDialog.tsx

import { materialAPI } from '@/lib/api'

const handleAddMaterial = async () => {
  if (newMaterial.id && newMaterial.name) {
    try {
      // Save to backend
      await materialAPI.create(newMaterial)
      
      // Add to local state
      addMaterial(newMaterial)
      
      setShowAddForm(false)
      setNewMaterial({ id: '', name: '', E: 0, nu: 0, density: 0, fy: 0, type: 'concrete' })
    } catch (error) {
      console.error('Failed to add material:', error)
    }
  }
}
```

---

### **Step 5: Update LoadDialog**

```typescript
// frontend/src/components/dialogs/LoadDialog.tsx

import { loadAPI } from '@/lib/api'

const handleAddNodalLoad = async (e: React.FormEvent) => {
  e.preventDefault()
  
  try {
    // Save to backend
    await loadAPI.create({
      type: 'nodal',
      ...nodalLoad
    })
    
    console.log('Nodal load added:', nodalLoad)
    onClose()
  } catch (error) {
    console.error('Failed to add load:', error)
  }
}
```

---

### **Step 6: Update NewProjectDialog**

```typescript
// frontend/src/components/dialogs/NewProjectDialog.tsx

import { projectAPI } from '@/lib/api'

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  
  try {
    // Create project in backend
    const response = await projectAPI.create(formData)
    
    // Pass to parent
    onCreateProject(response.data)
    
    onClose()
    setFormData({ name: '', description: '', units: 'metric', code: 'IS456', template: 'blank' })
  } catch (error) {
    console.error('Failed to create project:', error)
  }
}
```

---

### **Step 7: Load Data on Workspace Mount**

Update `workspace.tsx` to load existing data:

```typescript
// frontend/src/pages/workspace.tsx

import { nodeAPI, elementAPI, materialAPI } from '@/lib/api'

useEffect(() => {
  const loadModelData = async () => {
    try {
      // Load nodes
      const nodesResponse = await nodeAPI.list()
      // Update context with nodes
      
      // Load elements
      const elementsResponse = await elementAPI.list()
      // Update context with elements
      
      // Load materials
      const materialsResponse = await materialAPI.list()
      // Update context with materials
    } catch (error) {
      console.error('Failed to load model data:', error)
    }
  }
  
  if (isAuthenticated) {
    loadModelData()
  }
}, [isAuthenticated])
```

---

### **Step 8: Add Delete Functionality**

Update tables to call delete APIs:

```typescript
// frontend/src/components/tables/NodesTable.tsx

import { nodeAPI } from '@/lib/api'

const handleDelete = async (nodeId: string) => {
  if (confirm('Delete this node?')) {
    try {
      await nodeAPI.delete(nodeId)
      // Remove from local state
      // Refresh table
    } catch (error) {
      console.error('Failed to delete node:', error)
    }
  }
}

// In the table:
<button
  onClick={() => handleDelete(node.id)}
  className="toolbar-button"
  title="Delete"
>
  <Trash2 className="w-3 h-3" />
</button>
```

---

## 🔄 **Data Flow with Backend**

### **Create Flow**
```
User fills dialog
    ↓
Submit form
    ↓
Call backend API (POST)
    ↓
Backend saves to database
    ↓
Backend returns success
    ↓
Update local state (Context)
    ↓
UI refreshes automatically
```

### **Read Flow**
```
Workspace loads
    ↓
Call backend API (GET)
    ↓
Backend returns data
    ↓
Update local state (Context)
    ↓
Tables/UI display data
```

### **Update Flow**
```
User clicks edit
    ↓
Dialog opens with data
    ↓
User modifies
    ↓
Call backend API (PUT)
    ↓
Backend updates database
    ↓
Update local state
    ↓
UI refreshes
```

### **Delete Flow**
```
User clicks delete
    ↓
Confirm dialog
    ↓
Call backend API (DELETE)
    ↓
Backend removes from database
    ↓
Remove from local state
    ↓
UI refreshes
```

---

## 🎯 **Testing Backend Integration**

### **Test Checklist**

1. **Authentication** ✅
   - [ ] Login works
   - [ ] Token is stored
   - [ ] Token is sent with requests
   - [ ] Logout works

2. **Node CRUD**
   - [ ] Create node → Backend saves
   - [ ] List nodes → Backend returns data
   - [ ] Update node → Backend updates
   - [ ] Delete node → Backend removes

3. **Element CRUD**
   - [ ] Create element → Backend saves
   - [ ] List elements → Backend returns data
   - [ ] Update element → Backend updates
   - [ ] Delete element → Backend removes

4. **Material CRUD**
   - [ ] Create material → Backend saves
   - [ ] List materials → Backend returns data
   - [ ] Update material → Backend updates
   - [ ] Delete material → Backend removes

5. **Analysis**
   - [ ] Run analysis → Backend processes
   - [ ] Results returned → UI displays

---

## 🐛 **Debugging Tips**

### **Check Network Tab**
```
1. Open browser DevTools (F12)
2. Go to Network tab
3. Perform action (e.g., add node)
4. Check request:
   - URL correct?
   - Method correct (POST/GET/PUT/DELETE)?
   - Headers include auth token?
   - Body has correct data?
5. Check response:
   - Status 200/201 = success
   - Status 400/401/500 = error
   - Read error message
```

### **Check Console**
```
1. Open browser Console
2. Look for errors
3. Check API calls
4. Verify data format
```

### **Check Backend Logs**
```
1. Check backend terminal
2. Look for incoming requests
3. Check for errors
4. Verify data processing
```

---

## 📝 **Quick Implementation Checklist**

### **Backend (Python/FastAPI)**
- [ ] Add node endpoints
- [ ] Add element endpoints
- [ ] Add material endpoints
- [ ] Add load endpoints
- [ ] Add project endpoints
- [ ] Test with Postman/curl

### **Frontend (React/TypeScript)**
- [ ] Add API functions to api.ts
- [ ] Update NodeDialog with API calls
- [ ] Update ElementDialog with API calls
- [ ] Update MaterialDialog with API calls
- [ ] Update LoadDialog with API calls
- [ ] Update NewProjectDialog with API calls
- [ ] Add delete handlers to tables
- [ ] Add data loading on mount
- [ ] Test all CRUD operations

---

## 🎉 **Result**

After completing these steps, you'll have:
- ✅ Full CRUD operations for all entities
- ✅ Data persistence in backend database
- ✅ Real-time sync between frontend and backend
- ✅ Complete production-ready application

---

## 💡 **Pro Tips**

1. **Error Handling**: Always wrap API calls in try-catch
2. **Loading States**: Show loading indicators during API calls
3. **Optimistic Updates**: Update UI immediately, rollback on error
4. **Caching**: Cache frequently accessed data
5. **Validation**: Validate on both frontend and backend

---

**Need Help?** Check the existing AnalysisDialog implementation - it's already fully connected to the backend and can serve as a reference! 🚀
