# Structural Engine — Math & Logic Issues (summary)

This file lists the math, units, numerical, and logic issues I found while auditing the principal engine files under `backend/app/engine/`. Each entry includes: file, location / function, short description of the problem, severity, and a concise suggested fix.

---

## High priority (must-fix before production)

### `backend/app/engine/pushover_analysis.py`
- Location: `_update_stiffness` (function contains `pass`).
- Issue: Post-yield stiffness reduction is not implemented. The algorithm calls `_update_stiffness` during pushover steps but it does nothing, so yielded elements won't reduce stiffness and the capacity curve / collapse detection is invalid.
- Severity: Critical
- Suggested fix: Implement reduction of element tangent stiffness for yielded elements (e.g., set DOF-specific reductions to a small fraction of elastic stiffness or assemble element plastic hinge models). Add unit tests that force one element to yield and verify base-shear vs displacement softening.

### `backend/app/engine/pdelta.py`
- Location: `_geometric_stiffness_matrix`, `_update_axial_forces`, assembly logic
- Issue: Geometric stiffness assembly is highly simplified and uses 2-DOF/4x4 local matrices then maps into global using `start_dof = i*2` — but the global model uses 6 DOF per node elsewhere. Indexing and dimensionality mismatch will produce incorrect Kg and may corrupt K_modified = K - Kg in iterations. Also axial force update extracts axial forces from a naive K @ u mapping that is not element-wise.
- Severity: Critical
- Suggested fix: Rework geometric stiffness assembly to match element DOFs (12×12 for 2-node frame elements) and global DOF mapping. Use element axial force computed from element local axial strain/stress (transform global u to local, compute axial force) rather than K@u global shortcut. Add unit tests comparing amplification factor for a simple column to hand-calculated P-Delta amplification.

### `backend/app/engine/analysis.py`
- Location: Units and DOF indexing in `assemble_stiffness_matrix`, `_element_stiffness_3d`, `_get_element_dof_indices`, `assemble_mass_matrix`, `modal_analysis`
- Issues:
  - Unit inconsistencies: E documented as MPa while some element formulations assume Pa (no consistent SI). Section properties use mm^2 and mm^4; length L returned from `Element.length()` appears to be in the same unit (mm). Yet other routines convert mm->m in mass matrix; inconsistent unit bases will produce wrong stiffness/mass and hence wrong dynamics.
  - DOF indexing assumes `node.id` can be used directly as zero-based contiguous node index (`node_id * 6 + i`). If `node.id` values are not contiguous starting at 0 this produces sparse/incorrect assembly and shape mismatches.
  - `assemble_mass_matrix` mixes units by converting some section properties to m^2/m^4 but material density default is `7850` (kg/m^3) while `GeometryEngine.add_material` sets default density as `7850e-9` (kg/mm^3) — inconsistency between files.
  - `modal_analysis` computes `periods = 1 / frequencies` without handling zero or near-zero frequencies; division-by-zero possible.
- Severity: Critical
- Suggested fix:
  - Choose a single unit system (prefer SI: meters, N, Pa). Document it and convert inputs early (e.g., accept mm but convert to m on model ingestion). Ensure E uses Pa (N/m^2) inside numeric routines or consistently use MPa but convert where needed. Add unit tests verifying EA/L for a simple element with known units.
  - Replace node-id arithmetic with a node-index map (node index 0..n-1) so DOF mapping uses contiguous indices.
  - Standardize density units across `GeometryEngine` and `analysis` (document expected units). Add tests that check mass matrix dimensional consistency (M units ~ kg).
  - Guard modal-derived periods against zeros and return None/inf-safe values for rigid-body modes.

### `backend/app/engine/elements.py` (Element library)
- Location: `ShellElement.stiffness_matrix`, `SolidElement.stiffness_matrix`, `CableElement`, `catenary_shape`
- Issues:
  - In `ShellElement` and `SolidElement` some conversions are inconsistent: e.g., in `ShellElement` `t = self.thickness / 1000` and `E = self.E * 1e6` (converting mm to m and MPa to Pa), but the comment says simplified; implementations return zero matrices and state "simplified" — important algorithms are incomplete.
  - `CableElement.stiffness_matrix` computes EA = self.E * self.area without unit conversion; if E is MPa and area mm^2 this is inconsistent. Also weight per length uses `material.get('weight', 0.0)` with unclear units (N/mm?). `catenary_shape` uses sag and cable length formulas with mixed-unit assumptions.
- Severity: High
- Suggested fix: Standardize units in element attributes and document them. Implement or clearly mark as experimental/incomplete. Provide a minimal working example test for `CableElement` tangent stiffness using consistent SI units.

### `backend/app/engine/nonlinear_analysis.py`
- Location: `NewtonRaphsonSolver.solve`, `MaterialNonlinearity` functions
- Issues:
  - `NewtonRaphsonSolver` uses `relative_residual = residual_norm / force_norm` but `force_norm` computed as `np.linalg.norm(F_ext)` may be close to zero for some load cases; code guards with threshold but tolerances and stopping criteria need clarity. Tolerance default 1e-4 may be too loose for some structural checks.
  - Logging but no escalation on non-convergence aside from returning `converged=False` — higher-level callers may assume success.
  - `MaterialNonlinearity` functions often accept `E` without explicit expected units (MPa vs Pa).
- Severity: High
- Suggested fix: Standardize residual checks (use relative and absolute tolerances), return structured diagnostics (reason for stop). Clearly document expected units for material inputs. Add small convergence tests.

### `backend/app/engine/dynamic_analysis.py`
- Location: `DampingModel.rayleigh_damping`, `TimeHistoryAnalysis.newmark_beta`, `newmark` constants and K_eff assembly
- Issues:
  - Rayleigh coefficients alpha and beta formulas are suspect: implementation uses alpha = zeta * (2 * omega1 * omega2) / (omega1 + omega2) and beta = zeta * 2 / (omega1 + omega2). These formula forms are unconventional — standard solution solves 2*zeta*omega_i = alpha + beta*omega_i^2 for two modes; code appears to be a simplified approximation but could be wrong numerically.
  - Newmark-Gamma constants a0_const etc. are computed, but naming is confusing; ensure algebraic correctness. Also `K_eff = self.K + a0_const * self.M + a1 * self.C` — confirm coefficient definitions match the chosen Newmark form; otherwise time integration will be unstable/incorrect.
  - `TimeHistoryAnalysis` returns arrays as-is (no conversion to JSON-serializable lists) inconsistent with other API outputs.
- Severity: High
- Suggested fix: Replace Rayleigh implementation with the standard linear system solve for alpha and beta. Add a Newmark benchmark test (undamped single-degree oscillator) to validate period and amplitude.

### `backend/app/engine/seismic.py`
- Location: `_spectral_acceleration_is1893`, `response_spectrum_analysis`
- Issues:
  - Spectral acceleration functions use simplified piecewise formula and then clamp `min(Sa_g, 2.5)` — the chosen breakpoints and formulas are ad-hoc; recommended to match the exact code clauses or document intentionally simplified behavior.
  - `response_spectrum_analysis` uses `np.linalg.eig(np.linalg.inv(M) @ K)` which is numerically OK but for large systems prefer `eigh(K, M)` generalized solver or sparse solvers; also `periods = 1 / frequencies` with potential div-by-zero.
- Severity: Medium
- Suggested fix: Use `scipy.linalg.eigh(K, M)` or `scipy.sparse.linalg.eigsh` for large models and guard against zero-frequency modes. Validate spectral formulas against code-specific clauses.

### `backend/app/engine/wind.py`
- Location: `_terrain_height_factor_is875`, `_external_pressure_coefficient_is875`, `calculate_wind_forces`
- Issues:
  - Some empirical exponents and coefficients (e.g., k2 formulas, external pressure coefficients) are heuristics; must be validated with the standard tables. No units stated for basic wind speed vs conversion, `qz` uses 0.613 factor — check units (0.613 for Pa when V in m/s — that's correct if density 1.225 kg/m^3), but `basic_wind_speed` default 44.0 has no provenance.
  - `calculate_wind_forces` divides p*A by 1000 to get kN, but earlier many functions use inconsistent units (N/m^2 vs kN). Potential scaling errors.
- Severity: Medium
- Suggested fix: Document expected units and check factor 0.613 usage and conversions. Add small tests for a canonical building case.

---

## Medium priority

### `backend/app/engine/load_combinations.py`
- Location: generation functions for IS456 / ACI / Eurocode
- Issues: Several combination factors use simplified or non-standard factors (e.g., some factors are identical 1.5 for dead/live). For IS456, the typical factor set differs; verify clauses (the code mixes ULS multipliers and occasionally uses 1.5 for live which may be incorrect). Also `LoadType` checks use `LoadType.DEAD in load_types` where `load_types` might be a List[str] not enum values.
- Severity: Medium
- Suggested fix: Ensure `load_types` is a list of `LoadType` enums or accept strings and normalize. Cross-check combination factors against authoritative clauses and add unit tests that compare a small set of known combinations.

### `backend/app/engine/results_processor.py`
- Location: `generate_deflection_curve` uses span in meters multiplied by 1000 then compares deflection (which may be in mm) — mixing units.
- Severity: Medium
- Suggested fix: Standardize deflection units (store numeric deflections consistently in mm or m) and document limits comparison.

### `backend/app/engine/design_codes.py` and `design_codes_extended.py`
- Location: Flexure and shear checks
- Issues: Several magic constants and formula implementations are used without unit annotations (e.g., Mu expressed in kNm vs Nmm), conversions sometimes multiply/divide by 1e6 arbitrarily. Some simplified checks may under/over-predict required reinforcement (e.g., `IS456.check_flexure` computes `Ast = M / (0.87 * fy * 0.9 * d)` which assumes unit consistency but lacks explicit unit conversions).
- Severity: Medium
- Suggested fix: Add unit tests validating design outputs for benchmark problems (compare with hand calculations or reference examples). Add unit annotations in docstrings and ensure M units are consistent across functions (kNm or Nmm consistently).

---

## Low priority / code quality / robustness

- Transformation matrix in `analysis._transformation_matrix_3d` chooses reference vector `v` and divides `y_local = np.cross(x_local, v)` by its norm without checking for near-zero length; this can produce NaNs when x_local nearly parallel to v. Suggest guard and fallback (if cross norm < 1e-8, pick a different reference vector).
- `geometry.Element.length()` returns 0 for elements with >2 nodes; better raise clear exception for unsupported element types or implement appropriate length for 1D elements.
- Several functions print directly (e.g., pushover prints convergence failure) — replace prints with logger calls and structured exceptions.
- Bare `except` forms and suppressed exceptions (found during wider scan) were seen elsewhere; recommend replacing with explicit exception handling + logging.

---

## Recommended immediate actions (short)
1. Fix the `pushover_analysis._update_stiffness` implementation to reduce stiffness for yielded elements and add a unit test exercising yielding and capacity curve behaviour. (Critical)
2. Pick and document a single unit system (recommend SI: meters, N, Pa). Add a small conversion utility and convert element/section/material inputs on model ingestion. (Critical)
3. Replace node-based DOF mapping arithmetic with an explicit zero-based node index map used across assembly routines. (Critical)
4. Rework geometric stiffness and P-Delta assembly to use element-local approaches and proper DOF mapping. (Critical)
5. Add unit tests for modal extraction (single-degree oscillator), mass matrix dimensional check, and Newmark integration on a 1-DOF system. (High)

---

## Next steps I can take (if you want)
- Implement minimal code fixes for the critical items above and add fast pytest tests (I can open a PR).  
- Provide line-numbered diffs for each suggested change.  

If you want me to proceed and apply fixes + tests, say "Proceed to fix" and I will implement the top critical fixes and run the test suite.

---

Generated: October 16, 2025
Audit scope: Files inspected for this summary include (non-exhaustive):
`analysis.py`, `geometry.py`, `elements.py`, `pdelta.py`, `nonlinear_analysis.py`, `dynamic_analysis.py`, `pushover_analysis.py`, `results_processor.py`, `load_combinations.py`, `seismic.py`, `wind.py`, `design_codes_extended.py`, `design_codes.py`.

If you want the report split per-file into separate markdowns or more detailed line-level annotations, tell me which files to prioritize.
