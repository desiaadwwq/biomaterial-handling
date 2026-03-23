# 🧪 Week 6 Lab: Complex Behavior of Non-Newtonian Fluids
**– Power Law Curve Fitting & Dynamic Apparent Viscosity Simulation –**

> 📂 **Navigation**: [← Week 5: Rheological Properties (Newtonian)](../week5/Week05_Lab_Rheology.md) · [Main README](../../README.md) · [📝 Quiz Bank](../../en/QUIZ_BANK.md)

---

## 0. Target Data: Shear Stress Measurements of Non-Newtonian Fluid

This laboratory employs viscometer reading dataset targeting hypothetical 'Starch Paste' confirming pseudoplastic kinetics.

| Shear Rate ($s^{-1}$) | Shear Stress (Pa) Measurements |
|:---:|:---:|
| 10 | 18.5 |
| 20 | 29.3 |
| 30 | 38.5 |
| 40 | 46.8 |
| 50 | 54.3 |

*(Dataset dynamically mapped from 10~100 scaling inside Python scripts)*

---

## 1. Python Laboratory Algorithms

This curriculum engineers computer vision algorithms to dynamically extract intrinsic Flow Index ($n$) and Consistency Index ($K$) parameters.

### 📝 [Mandatory] Environment Setup & Execution Guide
1. **Verify Packages**: The `scipy` module is structurally mandated.
   ```bash
   pip install numpy matplotlib scipy
   ```
2. **Path**: Execute python scripts confined inside `en/week6/` directory.
3. **Execution Commands**: 
   ```bash
   python step1_powerlaw_curve_fit.py
   python step2_apparent_viscosity.py
   ```

---

### 📊 Python Script Key Highlights (Steps 1 ~ 3)

#### 1-1. [Step 1] Mathematical Power Law Curve Fitting Regression
- Deploys `scipy.optimize.curve_fit` to aggressively reverse-calculate minimize nonlinear errors.
- Synthesizes regression trajectory $\tau = K \cdot \dot{\gamma}^n$ layering atop scatter plots.
- Concludes fluid identity as 'Shear-Thinning' upon validating the $n$ approximation scoring under geometric 1.0.

#### 1-2. 🎛️ [Step 2] Apparent Viscosity Interactive Slider Animation
- Driven by formula $\eta = K \cdot \dot{\gamma}^{n-1}$.
- Operators mandate Slider UI across wide 0.2 ~ 1.8 index spectrum probing fatal pipeline friction limits real-time.

#### 1-3. 💥 [Step 3] Herschel-Bulkley Yield Stress Analyzer
- Features dual-throttle slider injecting the initial $\tau_y$ (Yield Stress) margin.
- Illuminates exactly how much brute-force motor pumping is mandated strictly to shatter interior product matrix networks before flow is even permitted.

---

## 2. 💡 Advanced Discussion Topics

### Topic 1: Shear-Thinning Phenomena & Imbalanced Pipe Velocity Profiles
- **Background**: Pseudoplastic fluids ($n<1$) notoriously suffer viscosity degradation near the high-shear pipe walls while sustaining rigid cores at the low-shear center trajectory.
- **Prompt**: Analyze whether this radical radial 'Viscosity Imbalance' structurally assists or drastically jeopardizes conductive heat transfer efficiencies inside pasteurization heat exchangers compared to homogenous Newtonian liquid mediums.

### Topic 2: Yield Stress and Initial Pump Activation
- **Background**: The Herschel-Bulkley model (Bingham plastic class) requires initial shear force exceeding the yield stress ($\tau_y$) to instigate flow.
- **Prompt**: Following a long holiday, when pumping highly concentrated paste that has solidified inside a dormant pipeline, what are the critical motor design considerations and pipe rupture risks during the initial pump startup sequence?

### Topic 3: Dilatant Fluids and System Relief Valves
- **Background**: Conveying corn starch suspension ($n>1$) is susceptible to sudden viscosity spikes. Minor pipe blockages that temporarily surge impeller speed can instantly petrify the fluid matrix, risking severed motor shafts or catastrophic pipe ruptures.
- **Prompt**: Within pipeline infrastructures handling shear-thickening fluids, how should mechanical Safety Relief Valves be computationally designed and physically positioned to intercept explosive pressure overloads most rapidly?

### Topic 4: Power Law Fitting Errors & $R^2$ Reliability Bounds
- **Background**: Step 1 python script arbitrarily estimates $K$ and $n$. However, embedding scattered outlier-heavy noise data yielding sub-0.8 $R^2$ regressions into facility pump formulas risks fatal design failures.
- **Prompt**: Recognizing major sensor distortions or entrapped air cavities inducing massive data scatter, invent an engineered pythonic solution utilizing data preprocessing algorithms to purge outliers before executing the core regression fitting.

---

## 3. Lab Assignments & Github Requirements

- **Submissions**: 
  - One graphical screenshot of the `step1_powerlaw_curve_fit.py` plotted regression curve with calculated console parameters.
  - One adjusted screenshot capturing `step3_herschel_bulkley_yield.py` operating specifically at $n=0.5$ and $\tau_y=15.0$ margins.
- Ensure strict origin push into the unified repository post-clearance.
