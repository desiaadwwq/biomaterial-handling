# 🔩 Week 7 Lab: Viscoelastic Properties — Creep & Stress Relaxation
**– Maxwell Stress Relaxation, Burgers Creep Fitting & Interactive Viscoelastic Simulator –**

> 📂 **Navigation**: [← Week 6: Non-Newtonian Fluids](../week6/Week06_Lab_Non_Newtonian.md) · [Main README](../../README.md) · [📝 Quiz Bank](../../QUIZ_BANK.md)

---

## 0. Lab Data: Apple (Fuji) Stress Relaxation & Creep

### Stress Relaxation Data (constant strain ε₀ = 5%)

| Time $t$ (s) | Stress $\sigma$ (kPa) |
|:---:|:---:|
| 0 | 50.0 |
| 2 | 41.2 |
| 5 | 31.5 |
| 10 | 20.8 |
| 20 | 10.9 |
| 30 | 6.8 |
| 60 | 3.2 |

### Creep Data (constant stress σ₀ = 10 kPa)

| Time $t$ (s) | Strain $\varepsilon$ (%) |
|:---:|:---:|
| 0 | 2.50 |
| 5 | 5.10 |
| 10 | 6.40 |
| 30 | 9.05 |
| 60 | 11.70 |
| 90 | 13.80 |
| 120 | 15.60 |

---

```mermaid
flowchart LR
    A[("Texture Analyzer<br>Time-Series Data")] -->|"Stress Relaxation<br>Simulation"| B(("Step 1<br>Maxwell<br>Stress Relaxation"))
    B -->|"τ_r Parameters"| C{{"Step 2<br>Burgers Creep<br>Curve Fitting"}}
    C -->|"E₁, E₂, η₁, η₂ Inverse"| D(["Step 3<br>Interactive<br>Viscoelastic Simulator"])
    
    style A fill:#f9f0c2,stroke:#d4b106,stroke-width:2px,color:#000
    style B fill:#d0e8f2,stroke:#0f83a0,stroke-width:2px,color:#000
    style C fill:#fce4d6,stroke:#d9703a,stroke-width:2px,color:#000
    style D fill:#d4ecd9,stroke:#3bb143,stroke-width:2px,color:#000
```

---

## 1. Theoretical Background

### 1-1. Viscoelasticity

![Viscoelasticity Concept](../../assets/week7/concept_viscoelasticity.png)

- Combined elastic (instant recovery) + viscous (permanent deformation) response over time
- Applies to most biological materials: apple, pear, cheese, bread dough, gelatin gels

### 1-2. Spring-Dashpot Models

![Creep and Relaxation Concept](../../assets/week7/concept_creep_relaxation.png)

| Model | Structure | Strength | Weakness |
|:---:|:---:|:---|:---|
| Maxwell | Series | Good stress relaxation | Linear creep (unrealistic) |
<br>

![Maxwell Model Behavior](../../assets/week7/model_maxwell.png)
| Kelvin-Voigt | Parallel | Good creep | Cannot model stress relaxation |
<br>

![Kelvin-Voigt Model Behavior](../../assets/week7/model_kelvin_voigt.png)
| Burgers | Maxwell + KV | Complete creep + recovery | 4 parameters (harder fitting) |
<br>

![Burgers Model Strain Decomposition](../../assets/week7/model_burgers.png)

### 1-3. Key Equations
- **Maxwell relaxation**: $\sigma(t) = \sigma_0 \cdot e^{-t/\tau_r}$, $\tau_r = \eta/E$
- **Burgers creep**: $\varepsilon(t) = \sigma_0/E_1 + (\sigma_0/E_2)(1-e^{-t\cdot E_2/\eta_2}) + (\sigma_0/\eta_1)\cdot t$

---

## 2. Python Lab

### 📝 Environment Setup
```bash
pip install numpy matplotlib scipy
python step1_maxwell_relaxation.py
python step2_burgers_creep_fit.py
python step3_viscoelastic_simulator.py
```

### Step 1: Maxwell Stress Relaxation Simulation
- Implements $\sigma(t) = \sigma_0 \cdot e^{-t/\tau_r}$ for 3 viscosity values
- Compares relaxation time sensitivity

### Step 2: Burgers Creep Curve Fitting
- `scipy.optimize.curve_fit` for 4-parameter nonlinear regression
- 3-component decomposition: instant elastic + delayed elastic + viscous flow

### Step 3: Interactive Viscoelastic Simulator
- Radio buttons: Maxwell / Kelvin-Voigt / Burgers model switch
- Sliders: E₁, E₂, η₁, η₂ real-time adjustment
- Dual plotting: Creep (left) + Stress Relaxation (right)

---

## 3. Discussion Topics
1. **Temperature vs viscoelastic parameters** — cold storage effects on τᵣ
2. **Ripening-induced viscoelastic degradation** — pectin hydrolysis
3. **Vibration-accelerated creep** — dynamic fatigue in transport
4. **Burgers model limitations** — fractional calculus models
5. **Maximum stacking height** — creep-based reverse engineering

---

## 4. 📝 Quiz Questions (8 items)

### Q1. [Theory] Definition of Viscoelasticity
Which of the following describes the core characteristic of Viscoelasticity most accurately?
- [ ] A. Newtonian fluid behavior where shear stress is proportional to shear rate.
- [x] B. A complex behavior where elastic (instant recovery) and viscous (permanent deformation) responses manifest simultaneously over time.
- [ ] C. A pure thermodynamic characteristic where viscosity changes entirely dependent on temperature.
- [ ] D. A shear-thinning phenomenon where viscosity decreases as shear rate increases.

### Q2. [Theory] Maxwell Model Strength
Which viscoelastic phenomenon is best described by the Maxwell model (spring + dashpot in series)?
- [x] A. Stress Relaxation — Exponential stress decay under constant strain.
- [ ] B. Creep — Saturated deformation increase under constant stress.
- [ ] C. Dynamic Viscoelasticity — Separation of storage and loss moduli.
- [ ] D. Flow behavior after yield stress.

### Q3. [Theory] 3-Stage Decomposition of Burgers Creep Equation
In the Burgers 4-element creep equation $\\varepsilon(t) = \\sigma_0/E_1 + (\\sigma_0/E_2)(1-e^{-t/\\tau_c}) + (\\sigma_0/\\eta_1) \\cdot t$, what deformation does the third term $(\\sigma_0/\\eta_1) \\cdot t$ represent?
- [ ] A. Instant Elastic Deformation — Spring response at the moment of load application.
- [ ] B. Delayed Elastic Deformation — Time-dependent saturation of the KV unit.
- [x] C. Viscous Flow — Irreversible linear increase caused by the dashpot (permanent deformation).
- [ ] D. Elastic Recovery — Instant recovery upon load removal.

### Q4. [Theory] Physical Meaning of Relaxation Time ($\\tau_r$)
Which is the correct explanation for relaxation time $\\tau_r = \\eta / E$ in the Maxwell model?
- [ ] A. The time required for stress to decrease to 50% of its initial value.
- [x] B. The time required for stress to decrease to $1/e$ (approx. 36.8%) of its initial value.
- [ ] C. The time required for strain to reach its maximum value.
- [ ] D. The time when the creep curve enters the linear phase.

### Q5. [Theory] Kelvin-Voigt Model Limitations
What is the largest limitation of the Kelvin-Voigt model (spring + dashpot in parallel)?
- [ ] A. It cannot describe creep phenomena.
- [ ] B. It cannot predict full recovery after creep.
- [x] C. It cannot represent instant elastic deformation ($\\sigma_0/E$) and cannot describe stress relaxation.
- [ ] D. It requires 4 or more parameters, making data fitting impossible.

### Q6. [Python] Nonlinear Curve Fitting
Which `scipy` function was utilized to inversely estimate the 4 parameters ($E_1, E_2, \\eta_1, \\eta_2$) of the Burgers creep model from experimental data?
- [ ] A. `scipy.integrate.simpson`
- [x] B. `scipy.optimize.curve_fit`
- [ ] C. `scipy.interpolate.CubicSpline`
- [ ] D. `scipy.stats.linregress`

### Q7. [Python] Interactive UI Widgets
Which Matplotlib widgets were utilized in Step 3 lab for real-time drag adjustments of parameters like $E_1$, $\\eta_1$?
- [ ] A. `matplotlib.animation.FuncAnimation`
- [ ] B. `matplotlib.patches.FancyBboxPatch`
- [x] C. `matplotlib.widgets.Slider` and `matplotlib.widgets.RadioButtons`
- [ ] D. `matplotlib.colors.Normalize`

### Q8. [Theory] Permanent Deformation and Viscosity Coefficient
In a Burgers creep-recovery test, which core parameter determines the **permanent deformation** remaining after load removal?
- [ ] A. $E_1$ (Instant elastic modulus)
- [ ] B. $E_2$ (Delayed elastic modulus)
- [x] C. $\\eta_1$ (Maxwell dashpot viscosity coefficient) — determines $(\\sigma_0/\\eta_1) \\cdot t_{load}$
- [ ] D. $\\eta_2$ (KV dashpot viscosity coefficient)

---

## 5. Submission
- Screenshot of `step1_maxwell_relaxation.py` (relaxation curves + τᵣ output)
- Screenshot of `step2_burgers_creep_fit.py` (4-parameter fitting result)
- Push to GitHub `week7` branch
