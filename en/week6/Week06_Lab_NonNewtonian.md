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

### Topic 5: Pipeline Design Issues for Thixotropic Fluids
- **Background**: Thixotropic fluids like yogurt and apple puree exhibit time-dependent viscosity reduction under constant shear, recovering viscosity upon shear removal.
- **Prompt**: When transporting thixotropic fluids over long-distance pipelines, installing intermediate flow-regulating valves may temporarily allow viscosity recovery, causing additional pump load upon restart. How should this thixotropic history phenomenon be incorporated into pipeline design?

### Topic 6: Application of Generalized Reynolds Number in Non-Newtonian Pipes
- **Background**: The Metzner-Reed generalized Reynolds number ($Re_{MR}$) is used to discriminate laminar/turbulent regimes for Power Law fluids.
- **Prompt**: For a highly shear-thinning fluid ($n \\approx 0.2$), can the $Re_{MR}$-based laminar/turbulent threshold be applied identically to the Newtonian fluid standard ($Re = 2100$)? If differences exist, what compensations are necessary?

---

## 3. 📝 Quiz Questions (8 items)

### Q1. [Theory] Defining Non-Newtonian Fluids
Which of the following most accurately describes the core characteristic of a Non-Newtonian fluid?
- [ ] A. A perfectly linear proportional relationship between shear stress and shear rate passing through the origin.
- [x] B. A non-linear behavior where apparent viscosity fluctuates depending on the shear rate.
- [ ] C. A characteristic where viscosity fluctuates solely dependent on temperature.
- [ ] D. A phenomenon where density proportionally increases with shear rate.

### Q2. [Theory] Identifying Power Law Flow Index ($n$)
In the Power Law model $\\tau = K \\dot{\\gamma}^n$, what is the fluid behavior type if the estimated flow index is $n = 0.35$?
- [x] A. Pseudoplastic / Shear Thinning — Viscosity ↓ as shear rate ↑
- [ ] B. Dilatant / Shear Thickening — Viscosity ↑ as shear rate ↑
- [ ] C. Newtonian — Viscosity remains constant
- [ ] D. Bingham Plastic — Flow initiates after yield stress

### Q3. [Theory] Apparent Viscosity Formula Derivation
Which is the correct formula for apparent viscosity $\\eta$ derived from the Power Law model?
- [ ] A. $\\eta = K \\cdot \\dot{\\gamma}^n$
- [x] B. $\\eta = K \\cdot \\dot{\\gamma}^{n-1}$
- [ ] C. $\\eta = K / \\dot{\\gamma}^n$
- [ ] D. $\\eta = \\tau_y + K \\cdot \\dot{\\gamma}^n$

### Q4. [Theory] Herschel-Bulkley Model Special Case
If the yield stress $\\tau_y = 0$ is set in the Herschel-Bulkley equation $\\tau = \\tau_y + K \\dot{\\gamma}^n$, which model does it reduce to?
- [ ] A. Newtonian Fluid Model
- [x] B. Power Law Model
- [ ] C. Bingham Plastic Model
- [ ] D. Arrhenius Viscosity Model

### Q5. [Theory] Understanding Thixotropic Behavior
Which is the most accurate description of a Thixotropic fluid's core characteristic?
- [ ] A. A non-time-dependent behavior where viscosity instantly decreases as shear rate increases.
- [x] B. Viscosity gradually decreases proportionally over time under constant shear → recovers when shear is removed.
- [ ] C. Rheopectic behavior where viscosity gradually increases under constant shear.
- [ ] D. Bingham plastic behavior requiring yield stress to be exceeded for flow to initiate.

### Q6. [Python] Nonlinear Curve Fitting Module
Which core function in the `scipy` module is used to inversely estimate optimal parameters $K$ and $n$ for the Power Law model $\\tau = K \\dot{\\gamma}^n$?
- [ ] A. `scipy.interpolate.CubicSpline`
- [x] B. `scipy.optimize.curve_fit`
- [ ] C. `scipy.integrate.simpson`
- [ ] D. `scipy.stats.linregress`

### Q7. [Python] Interactive Slider Widget
Which Matplotlib widget module was utilized in Step 2 and Step 3 labs to manipulate $n$ and $\\tau_y$ values in real-time?
- [ ] A. `matplotlib.animation.FuncAnimation`
- [ ] B. `matplotlib.patches.Circle`
- [x] C. `matplotlib.widgets.Slider`
- [ ] D. `matplotlib.colors.Normalize`

### Q8. [Theory] Non-Newtonian Pipeline Design
When transporting tomato paste ($n \\approx 0.3$, $\\tau_y \\approx 20$ Pa) through a 100m pipeline, which pump type is most appropriate?
- [ ] A. Centrifugal Pump — Reduces viscosity via high-speed rotation.
- [x] B. Positive Displacement Pump — Overcomes yield stress and ensures constant flow rate.
- [ ] C. Vacuum Pump — Reduces viscosity via suction pressure.
- [ ] D. Jet Pump — Accelerates fluid via injector mechanism.

---

## 4. Lab Assignments & Github Requirements

- **Submissions**: 
  - One graphical screenshot of the `step1_powerlaw_curve_fit.py` plotted regression curve with calculated console parameters.
  - One adjusted screenshot capturing `step3_herschel_bulkley_yield.py` operating specifically at $n=0.5$ and $\\tau_y=15.0$ margins.
- Ensure strict origin push into the unified repository post-clearance.
