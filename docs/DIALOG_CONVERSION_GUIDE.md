# 🔄 Dialog Conversion Guide - Modern to Classic Style

## Pattern to Follow

### Step 1: Update Imports

**REMOVE:**
```typescript
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
```

**ADD:**
```typescript
import {
  ClassicDialog,
  ClassicDialogContent,
  ClassicDialogHeader,
  ClassicDialogTitle,
  ClassicDialogBody,
  ClassicDialogFooter,
} from '@/components/ui/classic-dialog';
```

### Step 2: Update Dialog Structure

**BEFORE:**
```typescript
<Dialog open={isOpen} onOpenChange={closeDialog}>
  <DialogContent className="sm:max-w-[500px]">
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
    </DialogHeader>
    
    <div className="space-y-4 py-4">
      {/* Content */}
    </div>
    
    <DialogFooter>
      <Button variant="outline" onClick={closeDialog}>Cancel</Button>
      <Button onClick={handleSubmit}>OK</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

**AFTER:**
```typescript
<ClassicDialog open={isOpen} onOpenChange={closeDialog}>
  <ClassicDialogContent>
    <ClassicDialogHeader>
      <ClassicDialogTitle>Title</ClassicDialogTitle>
    </ClassicDialogHeader>
    
    <ClassicDialogBody>
      {/* Content */}
    </ClassicDialogBody>
    
    <ClassicDialogFooter>
      <button onClick={closeDialog}>Cancel</button>
      <button onClick={handleSubmit} style={{
        background: "var(--accent-blue)",
        color: "var(--text-white)",
        borderColor: "var(--accent-blue)"
      }}>OK</button>
    </ClassicDialogFooter>
  </ClassicDialogContent>
</ClassicDialog>
```

### Step 3: Update Form Elements

**Labels:**
```typescript
// BEFORE
<Label htmlFor="field">Field Name</Label>

// AFTER
<label className="form-label">Field Name</label>
```

**Inputs:**
```typescript
// BEFORE
<Input id="field" type="number" value={value} onChange={onChange} />

// AFTER
<input className="form-input" type="number" value={value} onChange={onChange} />
```

**Selects:**
```typescript
// BEFORE
<Select value={value} onValueChange={setValue}>
  <SelectTrigger><SelectValue /></SelectTrigger>
  <SelectContent>
    <SelectItem value="opt1">Option 1</SelectItem>
  </SelectContent>
</Select>

// AFTER
<select className="form-input" value={value} onChange={(e) => setValue(e.target.value)}>
  <option value="opt1">Option 1</option>
</select>
```

**Checkboxes:**
```typescript
// BEFORE
<Checkbox checked={checked} onCheckedChange={setChecked} />

// AFTER
<input type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} />
```

### Step 4: Update Layout Classes

**Form Groups:**
```typescript
<div className="form-group">
  <label className="form-label">Label</label>
  <input className="form-input" />
</div>
```

**Form Rows (side by side):**
```typescript
<div className="form-row">
  <div className="form-group">...</div>
  <div className="form-group">...</div>
</div>
```

---

## Quick Reference

### All Dialogs to Convert (44 total)

1. ❌ NodeDialog.tsx
2. ❌ ElementDialog.tsx
3. ❌ MaterialDialog.tsx
4. ❌ LoadDialog.tsx
5. ✅ AnalysisDialog.tsx (DONE)
6. ❌ ConcreteDesignDialog.tsx
7. ❌ AIAssistantDialog.tsx
8. ❌ DetailingDialog.tsx
9. ❌ GenerativeDesignDialog.tsx
10. ❌ OptimizationDialog.tsx
11. ❌ WorkflowDialog.tsx
12. ❌ ConnectionsDialog.tsx
13. ❌ SectionDialog.tsx
14. ❌ SeismicDialog.tsx
15. ❌ WindDialog.tsx
16. ❌ LoadCombinationsDialog.tsx
17. ❌ SlabDesignDialog.tsx
18. ❌ DynamicAnalysisDialog.tsx
19. ❌ FoundationDialog.tsx
20. ❌ ServiceabilityDialog.tsx
21. ❌ ParallelAnalysisDialog.tsx
22. ❌ AdvancedAnalysisDialog.tsx
23. ❌ PushoverDialog.tsx
24. ❌ SpecializedDesignDialog.tsx
25. ❌ AdvancedElementsDialog.tsx
26. ❌ NonlinearDialog.tsx
27. ❌ PDeltaDialog.tsx
28. ❌ DesignExtendedDialog.tsx
29. ❌ MLDialog.tsx
30. ❌ ResultsDialog.tsx
31. ❌ VersioningDialog.tsx
32. ❌ TemplatesDialog.tsx
33. ❌ CacheDialog.tsx
34. ❌ PluginsDialog.tsx
35. ❌ ProjectDialog.tsx
36. ❌ BIMDialog.tsx
37. ❌ LearningDialog.tsx
38. ❌ GeometryDialog.tsx
39. ❌ UnitsDialog.tsx
40. ❌ ReportingDialog.tsx
41. ❌ ModelDialog.tsx
42. ❌ CollaborationDialog.tsx
43. ❌ AdvancedFeaturesDialog.tsx
44. ❌ WebSocketDialog.tsx

---

## Automated Conversion Steps

For each dialog file:

1. Read the file
2. Replace imports
3. Replace Dialog components with ClassicDialog components
4. Replace Button with button
5. Replace Label with label + className="form-label"
6. Replace Input with input + className="form-input"
7. Replace Select with select + className="form-input"
8. Update spacing classes to form-group/form-row
9. Save the file

---

## Testing Checklist

After conversion, test each dialog:
- ✅ Opens correctly
- ✅ Form fields work
- ✅ Submit button works
- ✅ Cancel button closes dialog
- ✅ Styling looks professional
- ✅ No console errors

---

**Status**: Conversion guide ready
**Next**: Apply pattern to all 44 dialogs
