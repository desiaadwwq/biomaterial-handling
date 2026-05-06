# 📚 Weekly Discussion Topics & Quiz Bank
> A consolidated reference of advanced discussion topics and quiz questions from the **Biomaterial Handling & Processing** lab course.  
> 📌 **[한국어 버전](../ko/QUIZ_BANK.md)**

---

## 📖 Table of Contents
- [Week 02: Circularity & Sphericity](#week-02-circularity--sphericity)
- [Week 03: Volume & Surface Area Estimation](#week-03-volume--surface-area-estimation)
- [Week 04: Density & Porosity Measurement and Visualization](#week-04-density--porosity-measurement-and-visualization)
- [Week 05: Rheological Properties (Newtonian Fluids)](#week-05-rheological-properties-newtonian-fluids)
- [Week 06: Complex Behavior of Non-Newtonian Fluids](#week-06-complex-behavior-of-non-newtonian-fluids)
- [Week 07: Viscoelastic Properties — Creep & Stress Relaxation](#week-07-viscoelastic-properties--creep--stress-relaxation)
- [Week 09: Contact Stress & Hertz Theory](#week-09-contact-stress--hertz-theory)
- [Week 10: Impact Characteristics & Damage Prediction Modeling](#week-10-impact-characteristics--damage-prediction-modeling)

---

# Week 02: Circularity & Sphericity
> 🔗 [View Detailed Lab Tutorial](week2/week02_lab_circularity_sphericity.md)

## 💡 Discussion Topics

### Discussion 1: Impact of Digital Aliasing on Shape Analysis

**Background**: When measuring circularity of a nearly spherical apple via OpenCV, the result is ~`0.85–0.9` instead of the theoretical `1.0`, due to aliasing — the pixel grid represents curved boundaries as stair-steps, causing perimeter over-measurement.

> **Prompt**: What software-based approaches could correct aliasing-induced perimeter over-estimation? (e.g., subpixel contour detection, Gaussian blur intensity adjustment, resolution-dependent circularity convergence experiments)

### Discussion 2: Industrial Applications — Automated Agricultural Produce Sorting

**Background**: Automated sorting lines must distinguish defective shapes in real-time using only 2D images. Circularity is a 2D metric while sphericity is 3D — but single cameras cannot directly capture 3D information.

> **Prompt**: To estimate 3D sphericity from only 2D images (front + side views) of an apple on a conveyor belt, what assumptions and algorithms are needed, and what are their limitations?

### Discussion 3: Impact of Thresholding Method on Shape Indices

**Background**: Otsu's auto-thresholding is used, but non-uniform lighting or similar background colors can distort contours and introduce errors in circularity/sphericity.

> **Prompt**: What are the pros and cons of Adaptive Thresholding, HSV color space segmentation, and other alternatives for agricultural image analysis?

---

## 📝 Quiz Questions

### Q1. [Theory] Definition of Circularity
Which formula correctly represents **Circularity** in OpenCV-based image analysis?

| Option | Formula |
| --- | --- |
| A | `Perimeter / Area` |
| B | `Area / Perimeter²` |
| **C** | **`(4 × π × Area) / Perimeter²`** |
| D | `(Circumscribed circle area) / (Actual area)` |

<details>
<summary>View Answer</summary>

**Answer: C** — Perfect circle yields 1.0; complex shapes approach 0. Sensitive to contour noise due to P² in denominator.
</details>

### Q2. [Lab] Role of Otsu's Thresholding
Why is `cv2.THRESH_OTSU` used in `cv2.threshold()`?

| Option | Content |
| --- | --- |
| A | Auto-adjust image resolution |
| **B** | **Auto-determine optimal threshold via histogram analysis** |
| C | Convert color to grayscale |
| D | Calculate contour area |

<details>
<summary>View Answer</summary>

**Answer: B** — Maximizes between-class variance to automatically separate foreground/background.
</details>

### Q3. [Lab] Meaning of Geometric Mean Diameter (GMD)
Sphericity uses `GMD = (L × W × T)^(1/3)`. What does GMD represent?

<details>
<summary>View Answer</summary>

**Answer**: Geometric mean of 3D dimensions (L, W, T) — the diameter of an equivalent sphere. GMD/L ratio = sphericity; closer to 100% = more spherical. Apples ~90%, grains 50–60%.
</details>

### Q4. [Theory] Purpose of Gaussian Blur
Why is Gaussian Blur applied immediately after grayscale conversion?

| Option | Content |
| --- | --- |
| A | Reduce color channels |
| B | Enhance contrast |
| **C** | **Smooth noise to prevent perimeter over-estimation (circularity distortion)** |
| D | Accurately measure area |

<details>
<summary>View Answer</summary>

**Answer: C** — Surface noise inflates perimeter, and since P² is in the circularity denominator, this distorts the value downward. Blur removes high-frequency noise.
</details>

---

# Week 03: Volume & Surface Area Estimation
> 🔗 [View Detailed Lab Tutorial](week3/week03_lab_volume_surface_area.md)

## 💡 Discussion Topics

### Discussion 1: Limitations of Geometric Simplification

**Background**: Manual 5-segment calculation yields ~8.03% surface area and ~4.33% volume errors. Python applies 100+ segment numerical integration.

> **Prompt**: Beyond increasing subdivisions (n), what are the fundamental **'asymmetry limitations'** of single-view 2D profile rotation integration, and how can 3D digital metrology address these?

### Discussion 2: Specific Surface Area & Processing Operations

**Background**: Wheat (1,316 m²/m³) dries significantly faster than soybeans (558 m²/m³) under identical conditions.

> **Prompt**: What engineering strategies should be adopted when designing cooling/ventilation systems for large-scale long-term storage silos, applying the physical properties of specific surface area?

### Discussion 3: Liquid Displacement vs. Air Pycnometer

**Background**: Low-moisture materials → water displacement (Archimedes); moisture-absorbing grains → air pycnometer (Boyle's Law).

> **Prompt**: What impact could **temperature changes** within the pycnometer chamber have on precision, and what cross-validation methods can improve reliability?

---

## 📝 Quiz Questions

### Q1. [Theory] Primary Error Source in Segmental Modeling
What is the **most significant cause** of error when applying segmental modeling?

| Option | Content |
| --- | --- |
| A | Internal moisture content differences |
| B | Numerical integration formula errors |
| **C** | **Geometric assumptions simplifying natural curvature into mathematical shapes** |
| D | Caliper quantization errors |

<details>
<summary>View Answer</summary>

**Answer: C** — Linearizing continuous curvature into truncated cones causes ~8.03% surface area and ~4.33% volume error.
</details>

### Q2. [Lab] Preprocessing Interpolation Technique
What technique converts discrete measurement points into a smooth function curve?

<details>
<summary>View Answer</summary>

**Answer: Cubic Spline Interpolation** — `scipy.interpolate.CubicSpline` converts discrete data into 100+ continuous curve points.
</details>

### Q3. [Lab] Numerical Integration Comparison
Which function provides higher precision than `trapezoid` by using **2nd-order parabolic approximation**?

<details>
<summary>View Answer</summary>

**Answer: Simpson's Rule (`scipy.integrate.simpson`)** — O(h⁴) accuracy via parabolic approximation, advantageous for curved surfaces.
</details>

### Q4. [Theory] Air Pycnometer Physical Law
What **fundamental physical law** does the air pycnometer apply?

<details>
<summary>View Answer</summary>

**Answer: Boyle's Law** — At constant temperature, pressure and volume are inversely proportional, enabling precise absolute volume calculation.
</details>

---

# Week 04: Density & Porosity Measurement and Visualization
> 🔗 [View Detailed Lab Tutorial](week4/Week04_Lab_Density_Porosity.md)

## 💡 Discussion Topics

### Discussion 1: Correlation Between Particle Radius and Void Structure
**Background**: In the lab, packing avocados into a 40x30x15 cm box demonstrates how single object volume and shape dictate the arrangement of the void space.
> **Prompt**: If we replaced the avocados (~205cm³) with smaller, perfectly spherical agricultural products of equivalent total mass in the same box, how would the theoretical porosity and actual fluid flow characteristics (e.g., aeration resistance) change?

### Discussion 2: Impact of Moisture Penetration on Particle Density Measurement
**Background**: When measuring particle density using liquid displacement, liquid can penetrate the target product due to skin properties or micro-pores.
> **Prompt**: What are the primary error sources when measuring the true density of porous biological resources (e.g., rice, wheat) via liquid displacement, and what are the pros/cons of using experimental coatings or alternative mediums (like toluene or sand) to mitigate this?

### Discussion 3: Bulk Density and Transportation Logistics Optimization
**Background**: Bulk density is lower than particle density and is directly determined by the porosity (void ratio) within the packing container.
### Discussion 4: Operational Impact of True vs. Apparent Density Discrimination
**Background**: Biological resources possessing porous, sponge-like tissue or fibrous husks exhibit a distinct divergence between their "Apparent Density" (encompassing internal micro-pores) and their intrinsic "True Density".
> **Prompt**: Cite specific examples to debate how the gap between true and apparent density (i.e., intra-particle porosity) directly governs physical processing traits such as convective drying kinetics or the textural qualities of processed foods.

### Discussion 5: Computational Complexity in Visualizing 3D Virtual Packing Models
**Background**: In our Week 4 Python lab, we arranged the avocados linearly into uniform spatial cells using an orthogonal coordinate grid (`np.meshgrid`)—an approach defined as 'Ordered Packing'.
> **Prompt**: Consider the scenario of 'Random Packing' where fruits are haphazardly dumped into a container. Discuss the computational complexities involved in running random number generators paired with Collision Detection algorithms to simulate this irregular void distribution, and propose optimization methodologies.

### Discussion 6: Dynamic Perturbations of Bulk Density Due to Moisture Content Shifts
**Background**: Post-harvest agricultural products continuously lose internal moisture to evaporation during storage and drying operations, prompting simultaneous mass reduction and volumetric shrinkage.
> **Prompt**: If grains stored long-term in a silo drop their moisture content from 20% to 12%, analyze the disparity between the rates of mass reduction versus volume shrinkage—how would these diverging rates dynamically alter the overarching 'Bulk Density' and 'Porosity' within the container?

---

## 📝 Quiz Questions

### Q1. [Theory] Porosity Calculation Formula
Given Particle Density and Bulk Density, which formula correctly calculates Porosity?

| Option | Formula |
| --- | --- |
| A | `(Particle Density / Bulk Density) × 100` |
| B | `(Bulk Density / Particle Density) × 100` |
| **C** | **`(1 - (Bulk Density / Particle Density)) × 100`** |
| D | `(Particle Density - Bulk Density) / Bulk Density × 100` |

<details>
<summary>View Answer</summary>

**Answer: C** — Porosity represents the void fraction, so it is 1 minus the ratio of actual occupied volume (Bulk Density vs Particle Density).
</details>

### Q2. [Lab] Purpose of 3D Scatter Visualization
In the `matplotlib` 3D Scatter, avocados are green while the void spaces are visualized as red/cyan semi-transparent dots. What is the primary educational purpose of this technique?

| Option | Content |
| --- | --- |
| A | Accurately measure the sphericity of avocados |
| B | Optimize resolution through high color contrast |
| **C** | **Intuitively verify the spatial distribution and volume ratio of the voids** |
| D | Predict the structural strength of the packing box |

<details>
<summary>View Answer</summary>

**Answer: C** — Since porosity is an abstract numerical value, filling the empty space visually acts like a fluid representation, helping to intuitively grasp the concepts of bulk density and porosity.
</details>

### Q3. [Theory] Variables Affecting Bulk Density
Which of the following does **not** cause a change in bulk density when packing the same agricultural product into the same container?

<details>
<summary>View Answer</summary>

**Answer: Changes in the particle density of the individual object itself** — Particle density is an intrinsic material property. Factors that *do* change bulk density include the packing pattern (arrangement), vibration settling, and size variations allowing smaller items to fill gaps.
</details>

### Q4. [Lab] Criterion for Settling (Sinking)
According to the Step 1 calculation, the particle density of the avocado is 1.047 g/cm³. How will this avocado react during a water flume washing process?

<details>
<summary>View Answer</summary>

**Answer: It will sink to the bottom** — Because its density is higher than water (1.0 g/cm³), negative buoyancy occurs. This is a critical factor when designing hydro-sorting or washing tanks.
</details>

### Q5. [Theory] Exceptions to True vs. Apparent Density Merging
In contrast to solid fruits, which of the following biological resources makes it **most difficult** to equate True Density with Apparent Density (due to abundant internal voids)?

| Option | Content |
| --- | --- |
| A | A freshly harvested, dense apple |
| B | A smooth-skinned potato |
| **C** | **Puffed grains (e.g., puffed rice) or thick sponge-like peels** |
| D | A grape densely filled with internal juice |

<details>
<summary>View Answer</summary>

**Answer: C** — Puffed tissues or sponge-like peels are saturated with numerous closed pores filled with air, causing a massive divergence between the true density of the solid carbohydrate matrix and the apparent density of the entire swollen particle.
</details>

### Q6. [Python Integration] Distance Calculation and Proximity Matrix
Within the `step1_density_porosity.py` script, which function from the `scipy` module was deployed to compute the pairwise distances between an immense grid of 3D point clouds and avocado centroids, thereby determining which spatial coordinates constitute the empty 'Void' beyond a certain radius?

| Option | Content |
| --- | --- |
| **A** | **`scipy.spatial.distance.cdist`** |
| B | `scipy.integrate.simpson` |
| C | `scipy.interpolate.CubicSpline` |
| D | `scipy.stats.linregress` |

<details>
<summary>View Answer</summary>

**Answer: A** — `cdist` is a highly optimized, vectorized distance function that calculates the distance between every coordinate pair in two distinct n-dimensional arrays simultaneously.
</details>

### Q7. [Lab] Analytical Consequences of Particle Density
In the [Advanced] Lab segment computing the apple's metric properties, a particle density of 0.889 g/cm³ was derived. Describe the profound kinetic trait this apple will exhibit when subjected to a water flume hydro-washing operation.

<details>
<summary>View Answer</summary>

**Answer: It will float atop the water surface (Flotation Flume Behavior)** — Because its particle density (0.889) is lower than the density of water (1.0 g/cm³), it generates a positive buoyancy vector pushing it toward the surface.
</details>

### Q8. [Theory] Respiration Heat vs. Aeration Voids
Assuming density and porosity are paramount to harvest storage stability, what is the most critical impending failure mechanism for freshly picked, high-respiration produce (like apples or pears) if the localized **'porosity is excessively low'** (i.e., tightly crammed to the brim)?

<details>
<summary>View Answer</summary>

**Answer: Accelerated Spoilage resulting from Respiration Heat Accumulation due to Insufficient Aeration** — When void spaces (porosity) are drastically minimized, cooling airflow cannot penetrate. Heat and metabolic moisture exuded by the living produce accumulate exponentially, sharply escalating internal temperatures and catalyzing rapid microbial rotting.
</details>

---

# Week 05: Rheological Properties (Newtonian Fluids)
> 🔗 [View Detailed Lab Tutorial](week5/Week05_Lab_Rheology.md)

## 💡 Discussion Topics

### Discussion 1: Analyzing the Trade-off Between Viscosity and Economics
**Background**: The Week 5 simulation confirms an intersecting tradeoff chart where escalating temperatures steadily curtail motor pumping expenses while triggering an alarming proportional spike in boiler heating fees.
> **Prompt**: Beyond merely tallying operational financial constraints, how must process engineers fuse these energy cost models with biological restrictions like 'Nutritional Integrity Loss' or 'Thermal Degradation' dynamics when forcibly preheating agricultural fluids?

### Discussion 2: Optimizing Pipe Diameter Design using the Hagen-Poiseuille Equation
**Background**: Within the Hagen-Poiseuille mandate determining pipe pressure drop (ΔP), the pipe diameter (D) engages in an inverse square proportionality mapping against pressure attrition.
> **Prompt**: Technically, laying mammoth super-caliber pipes across a factory would drastically eradicate sheer friction losses and save vast pumping costs. Logically speaking, why do real-world system engineers stubbornly cap pipeline expansion and instead resort to installing intermediate booster pumps?

### Discussion 3: The Impact of Reynolds Number on Heat Exchange Efficiency
**Background**: Viscous fluids naturally default to Laminar flow orientations inside heat exchanger (e.g., sterilization) pipelines. Propelling extreme velocities or debilitating viscosity thresholds triggers a shift towards turbulent kinetic chaos.
> **Prompt**: When injecting milk or fruit juice through a High-Temperature Short-Time (HTST) pasteurizer, laminar states offer unequivocally cheaper electrical bills due to fewer friction taxes. Yet developmentally, why does facility architecture intentionally sabotage this energy margin to aggressively enforce 'Turbulent' fluid motion?

### Discussion 4: Extension to Non-Newtonian Fluid Pipeline Design
**Background**: This lab calculates friction loss (Hagen-Poiseuille) based on a 'Clear Apple Juice (Newtonian fluid)' model, where viscosity remains constant and is strictly influenced by temperature. However, real-world processing plants frequently transport fluids like high-concentration tomato paste or starch slurry, whose viscosity fluctuates massively under pump shear stress or agitation time.
> **Prompt**: If we scale this targeting pipeline to handle Bingham Plastic fluids (which refuse to flow until a critical Yield Stress is breached) or Pseudoplastic fluids (which undergo severe shear-thinning as velocity increases), how should we technically recalibrate the current Python viscosity mathematical equations and pump power estimation models?

---

## 📝 Quiz Questions

### Q1. [Theory] Comprehending Newtonian Fluid Viscosity Characteristics
A facility operator turns up the shear rate (pump impeller RPM) to accelerate milk propulsion through a process line. According to Newtonian mechanics, how does the absolute viscosity of the milk react to this artificially surged pipe thrust rate?

| Option | Content |
| --- | --- |
| A | Viscosity rises linearly commensurate with the velocity. |
| B | Viscosity thins out in an inverse proportion to the speed. |
| **C** | **Viscosity remains obstinately constant regardless of velocity or shear rate fluctuations.** |
| D | Viscosity forms an irregular oscillatory wave function. |

<details>
<summary>View Answer</summary>

**Answer: C** — For Newtonian fluids, viscosity is constant and independent of shear rate or velocity. The shear stress simply increases proportionally.
</details>

### Q2. [Theory] Unit Proportionality of Shear Stress and Shear Rate
In Newton's Law of Viscosity formula ($\tau = \mu \dot{\gamma}$), where the absolute viscosity coefficient ($\mu$) resolves as the linear trajectory slope, what is the globally recognized metric unit representing the Shear Rate ($\dot{\gamma}$)?

| Option | Content |
| --- | --- |
| A | $m/s$ |
| **B** | **$s^{-1}$ (Reciprocal seconds)** |
| C | $Pa$ (Pascals) |
| D | $Stokes$ |

<details>
<summary>View Answer</summary>

**Answer: B** — Shear rate measures velocity gradient across fluid layers (velocity over distance squared), thus cancelling distance dimensions and resolving purely to reciprocal seconds.
</details>

### Q3. [Python Function] Arrhenius Model Viscosity Exponential Transformation
To universally implement the Arrhenius equation matrix $\mu = \mu_0 \cdot e^{(E_a / RT)}$ rapidly across a Python array dataset, what is the universally deployed Numpy library engine module?

| Option | Content |
| --- | --- |
| **A** | **`np.exp()`** |
| B | `np.linalg.inv()` |
| C | `np.log10()` |
| D | `np.gradient()` |

<details>
<summary>View Answer</summary>

**Answer: A** — `np.exp()` inherently calculates the exponential power `e^x` via rapid vectorized broadcasting across the entire mathematical array directly.
</details>

### Q4. [Theory] Reynolds Number Decoding and Kinematic Flow Comprehension
A mechanical audit of a circular pipe perimeter revealed a calculated Reynolds Number (Re) output of $1,500$. Based on fluid dynamics protocols, how can you define the ruling behavioral mechanism occurring inside the conduit?

| Option | Content |
| --- | --- |
| **A** | **The Laminar zone where dominant viscous forces actively suppress erratic inertial motions.** |
| B | The chaotic Transition zone denoting a violent clash between laminar and turbulent states. |
| C | The Turbulent zone where supreme inertial vectors generate overwhelming velocity vortices. |
| D | Undetectable zero-gravity state. |

<details>
<summary>View Answer</summary>

**Answer: A** — For internal flow within circular pipes, a Reynolds number (Re) falling below the threshold of ~2100 conventionally designates a stable, laminar flow profile dictating friction loss estimation.
</details>

### Q5. [Python Function] Extracting the Lowest Cost Data Index Array
Having processed total operational bills from 10 to 80 degrees within the `cost_total_array` variable, which dedicated Numpy operative specifically targets and retrieves only the exact coordinate index corresponding to the lowest recorded (most economical) numeric plateau?

| Option | Content |
| --- | --- |
| A | `np.minimum()` |
| **B** | **`np.argmin()`** |
| C | `np.sort()` |
| D | `np.where()` |

<details>
<summary>View Answer</summary>

**Answer: B** — `np.argmin()` specifically returns the localized positional index corresponding strictly to the smallest value array element. This isolates the mapping matrix back to the absolute 'Optimal Temperature'.
</details>

---

# Week 06: Complex Behavior of Non-Newtonian Fluids
> 🔗 [View Detailed Lab Tutorial](week6/Week06_Lab_NonNewtonian.md)

## 💡 Discussion Topics

### Discussion 1: Shear-Thinning Phenomena & Imbalanced Pipe Velocity Profiles
**Background**: Pseudoplastic fluids ($n<1$) notoriously suffer viscosity degradation near the high-shear pipe walls while sustaining rigid cores at the low-shear center trajectory.
> **Prompt**: Analyze whether this radical radial 'Viscosity Imbalance' structurally assists or drastically jeopardizes conductive heat transfer efficiencies inside pasteurization heat exchangers compared to homogenous Newtonian liquid mediums.

### Discussion 2: Yield Stress and Initial Pump Activation
**Background**: The Herschel-Bulkley model (Bingham plastic class) requires initial shear force exceeding the yield stress ($\tau_y$) to instigate flow.
> **Prompt**: Following a long holiday, when pumping highly concentrated paste that has solidified inside a dormant pipeline, what are the critical motor design considerations and pipe rupture risks during the initial pump startup sequence?

### Discussion 3: Dilatant Fluids and System Relief Valves
**Background**: Conveying corn starch suspension ($n>1$) is susceptible to sudden viscosity spikes. Minor pipe blockages that temporarily surge impeller speed can instantly petrify the fluid matrix, risking severed motor shafts or catastrophic pipe ruptures.
> **Prompt**: Within pipeline infrastructures handling shear-thickening fluids, how should mechanical Safety Relief Valves be computationally designed and physically positioned to intercept explosive pressure overloads most rapidly?

### Discussion 4: Power Law Fitting Errors & $R^2$ Reliability Bounds
**Background**: Step 1 python script arbitrarily estimates $K$ and $n$. However, embedding scattered outlier-heavy noise data yielding sub-0.8 $R^2$ regressions into facility pump formulas risks fatal design failures.
> **Prompt**: Recognizing major sensor distortions or entrapped air cavities inducing massive data scatter, invent an engineered pythonic solution utilizing data preprocessing algorithms to purge outliers before executing the core regression fitting.

## 📝 Quiz Questions

### Q1. [Theory] Characteristics of Shear-Thinning Fluids
Which of the following correctly describes a shear-thinning (pseudoplastic) fluid like ketchup?
| Option | Content |
| --- | --- |
| A | Viscosity continuously rises as more force is applied. |
| **B** | **Apparent viscosity decreases as the shear rate escalates.** |
| C | Exhibits identical viscosity to Newtonian fluids across all shear zones. |
| D | It will absolutely never flow without a yield stress block. |

<details>
<summary>View Answer</summary>

**Answer: B** — By definition, its flow index ($n$) is less than 1, causing the fluid structure to break down and thin out under high shear forces.
</details>

### Q2. [Theory] Significance of the Flow Index (n)
In the Power Law equation ($\tau = K \dot{\gamma}^n$), which academic term designates fluids where the flow index $n > 1$?
| Option | Content |
| --- | --- |
| A | Bingham Plastic |
| **B** | **Dilatant (Shear Thickening)** |
| C | Pseudoplastic (Shear Thinning) |
| D | Newtonian |

<details>
<summary>View Answer</summary>

**Answer: B** — When $n > 1$, applying rapid force structurally hardens the liquid, a trait distinctly known as Dilatant behavior.
</details>

### Q3. [Theory] Universal Breadth of the Herschel-Bulkley Equation
Identify the structural formula for the Herschel-Bulkley model, acclaimed dynamically for universally encapsulating Bingham Plastics, Pure Power Law, and raw Newtonian mechanics within a single master equation:
| Option | Content |
| --- | --- |
| A | $\tau = \mu \dot{\gamma}$ |
| B | $\tau = K \dot{\gamma}^n$ |
| **C** | **$\tau = \tau_y + K \dot{\gamma}^n$** |
| D | $\eta = K \dot{\gamma}^{n-1}$ |

<details>
<summary>View Answer</summary>

**Answer: C** — By merging the Yield Stress ($\tau_y$) coordinate with the standard exponential Power Law architecture, scientists created a universal skeleton that elegantly downgrades into Newtonian formulas simply by assigning $\tau_y=0$ and $n=1$.
</details>

### Q4. [Application] Tracking Apparent Viscosity Dynamics
For a shear-thinning fluid defined by $n=0.6$, what happens to its Apparent Viscosity and required pump motor torque dynamics when aggressively agitated at extreme high shear rates within the pipe lumen?
| Option | Content |
| --- | --- |
| A | Apparent viscosity skyrockets, plummeting total energy efficiency. |
| B | Viscosity stubbornly mirrors Newtonian consistency, plateauing the energy curve. |
| **C** | **Apparent Viscosity steeply collapses, temporarily thinning the fluid into a watery state which exponentially eases pumping.** |
| D | Spontaneous catastrophic Yield Stress initiates, immediately stalling impeller motors. |

<details>
<summary>View Answer</summary>

**Answer: C** — Possessing flow matrices under $n<1$, extreme kinetic shear fractures temporary molecular networks, rendering swift liquidity that vastly streamlines mass delivery capabilities.
</details>

### Q5. [Python Code] Extracting `curve_fit` Internal Arrays
During our Python implementation scaling the `scipy.optimize.curve_fit` regression loop, what exact mathematical data is exclusively encapsulated within the primary output array `popt`?
| Option | Content |
| --- | --- |
| A | Mathematical average arrays of the baseline simulated X-coordinates. |
| **B** | **The ultimate optimized fitting parameters mathematically solved (i.e. finalized $K$ and $n$ variables).** |
| C | Raw residual covariance logic grids derived exclusively from first-derivative errors. |
| D | Comprehensive $R^2$ confidence interval percentile ratios. |

<details>
<summary>View Answer</summary>

**Answer: B** — SciPy logically partitions output; `popt` contains the exact targeted array of Optimal Evaluated Parameters solving the target equation, whereas secondary limits yield covariance error matrices (`pcov`).
</details>

---

# Week 07: Viscoelastic Properties — Creep & Stress Relaxation
> 🔗 [View Detailed Lab Tutorial](week7/Week07_Lab_Viscoelastic_Properties.md)

## 💡 Discussion Topics

### Discussion 1: Temperature vs. Viscoelastic Parameters
**Background**: Refrigerated (4°C) vs room temperature (25°C) storage alters apple E and η values.
> **Prompt**: Analyze the molecular-level causes of relaxation time (τᵣ) reduction as temperature rises, and quantify the effect of cold-chain transport on load-induced deformation mitigation.

### Discussion 2: Ripening-Induced Viscoelastic Degradation
**Background**: Pectin hydrolysis → cell wall network weakening → sharp E decline and η reduction.
> **Prompt**: Discuss the feasibility of non-destructive ripeness assessment through viscoelastic monitoring and its integration into real-time sorting systems.

### Discussion 3: Vibration-Accelerated Creep
**Background**: Repeated vibration loads during truck transport may accelerate deformation beyond static creep predictions.
> **Prompt**: Discuss the concept of dynamic fatigue and its integration with cushion material design. Propose methods for estimating creep acceleration factors at different vibration frequencies.

### Discussion 4: Limitations of Burgers Model & Fractional Viscoelastic Models
**Background**: Even the 4-parameter Burgers model cannot perfectly capture the full relaxation time spectrum of real biological materials.
> **Prompt**: Discuss the physical meaning of fractional calculus-based Scott-Blair models and their potential for improving fitting precision beyond Burgers.

### Discussion 5: Maximum Stacking Height from Creep Data
**Background**: Predicting 24-hour cumulative creep deformation of the bottom fruit in an n-tier stack of 20 kg apple boxes.
> **Prompt**: Develop an algorithm to determine whether allowable strain (εₐₗₗₒᵥ ≈ 3%) is exceeded using Burgers parameters, and quantify the stacking tier increase potential with refrigerated transport.

---

## 📝 Quiz Questions

### Q1. [Theory] Definition of Viscoelasticity
Which statement best describes viscoelasticity?
| Option | Content |
| --- | --- |
| A | Newtonian fluid behavior where shear stress and shear rate are proportional |
| **B** | **Combined elastic (instant recovery) and viscous (permanent deformation) response occurring simultaneously over time** |
| C | Pure thermodynamic property dependent only on temperature |
| D | Shear-thinning behavior where viscosity decreases with shear rate |

<details>
<summary>View Answer</summary>

**Answer: B** — Viscoelasticity is the intermediate behavior where partial recovery and permanent deformation coexist depending on the time scale.
</details>

### Q2. [Theory] Maxwell Model Strength
What viscoelastic phenomenon does the Maxwell model (spring + dashpot in series) describe best?
| Option | Content |
| --- | --- |
| **A** | **Stress Relaxation — exponential stress decay under constant strain** |
| B | Creep — saturating strain increase under constant stress |
| C | Dynamic viscoelasticity — storage and loss moduli separation |
| D | Flow behavior beyond yield stress |

<details>
<summary>View Answer</summary>

**Answer: A** — The series dashpot precisely implements exponential decay: σ(t) = σ₀·exp(-t/τᵣ).
</details>

### Q3. [Theory] Burgers Creep 3-Component Decomposition
In the Burgers creep equation, what does the third term (σ₀/η₁)·t represent?
| Option | Content |
| --- | --- |
| A | Instantaneous elastic deformation — spring response at load application |
| B | Delayed elastic deformation — time-dependent saturation of KV unit |
| **C** | **Viscous flow — irreversible linear increase from dashpot (permanent deformation)** |
| D | Elastic recovery — immediate recovery upon load removal |

<details>
<summary>View Answer</summary>

**Answer: C** — The Maxwell dashpot (η₁) pure viscous flow component, linearly proportional to time and permanently retained after load removal.
</details>

### Q4. [Theory] Physical Meaning of Relaxation Time (τᵣ)
Which statement correctly describes relaxation time τᵣ = η/E in the Maxwell model?
| Option | Content |
| --- | --- |
| A | Time for stress to decrease to 50% of initial value |
| **B** | **Time for stress to decrease to 1/e (~36.8%) of initial value** |
| C | Time for strain to reach maximum |
| D | Time for creep curve to enter the linear region |

<details>
<summary>View Answer</summary>

**Answer: B** — Exponential decay e⁻¹ ≈ 0.368, so relaxation time marks ~36.8% of initial stress.
</details>

### Q5. [Theory] Kelvin-Voigt Model Limitation
What is the most significant limitation of the Kelvin-Voigt model (spring + dashpot in parallel)?
| Option | Content |
| --- | --- |
| A | Cannot describe creep |
| B | Cannot predict complete recovery after creep |
| **C** | **Cannot express instantaneous elastic deformation (σ₀/E), and cannot describe stress relaxation** |
| D | Requires 4+ parameters making fitting impossible |

<details>
<summary>View Answer</summary>

**Answer: C** — Parallel structure starts at strain 0 at t=0 (no instant elasticity), and stress relaxation reaches equilibrium instantly (no decay).
</details>

### Q6. [Python] Burgers Fitting Function
Which `scipy` function is used to estimate Burgers 4-parameter values via inverse regression?
| Option | Content |
| --- | --- |
| A | `scipy.integrate.simpson` |
| **B** | **`scipy.optimize.curve_fit`** |
| C | `scipy.interpolate.CubicSpline` |
| D | `scipy.stats.linregress` |

<details>
<summary>View Answer</summary>

**Answer: B** — Nonlinear least squares method to inversely estimate optimal parameters of a user-defined function.
</details>

### Q7. [Python] UI Widgets
Which Matplotlib widgets are used for model switching and parameter adjustment in Step 3?
| Option | Content |
| --- | --- |
| A | `matplotlib.animation.FuncAnimation` |
| B | `matplotlib.patches.FancyBboxPatch` |
| **C** | **`matplotlib.widgets.Slider` and `matplotlib.widgets.RadioButtons`** |
| D | `matplotlib.colors.Normalize` |

<details>
<summary>View Answer</summary>

**Answer: C** — Sliders for continuous parameter adjustment, radio buttons for discrete model switching.
</details>

### Q8. [Theory] Permanent Deformation Parameter
In a Burgers creep-recovery test, which parameter determines the permanent deformation remaining after load removal?
| Option | Content |
| --- | --- |
| A | E₁ (instantaneous elastic modulus) |
| B | E₂ (delayed elastic modulus) |
| **C** | **η₁ (Maxwell dashpot viscosity) — (σ₀/η₁)·t_load** |
| D | η₂ (KV dashpot viscosity) |

<details>
<summary>View Answer</summary>

**Answer: C** — Only the Maxwell dashpot's viscous flow component is irreversible; smaller η₁ means greater permanent deformation.
</details>

---

# Week 09: Contact Stress & Hertz Theory
> 🔗 [View Detailed Lab Tutorial](week9/Week09_Lab_Contact_Stress_Hertz.md)

## 💡 Discussion Topics

### Discussion 1: Temperature & Mechanical Properties
**Background**: Cell turgor pressure decreases at high temperature → E reduction → contact area expansion under same load.
> **Prompt**: Compare Hertz contact stress at refrigerated (4°C) vs room temperature (25°C) and discuss how cold-chain maintenance affects bruise prevention.

### Discussion 2: Selecting Roller Materials for Sorting Lines
**Background**: Steel rollers (E~200 GPa) vs silicone rubber (E~5 MPa) produce vastly different contact stresses at sorting line throughputs.
> **Prompt**: Analyze the trade-off between roller material stiffness and fruit damage rate, and propose optimal E* ranges for different fruit categories.

### Discussion 3: Multi-Contact Loading
**Background**: Fruits in bulk storage experience simultaneous contact from multiple adjacent fruits, not single-point Hertz contact.
> **Prompt**: Discuss superposition approaches and limitations when extending single-contact Hertz theory to multi-contact bulk storage scenarios.

### Discussion 4: Dynamic Impact vs Static Hertz
**Background**: Drop impact generates transient stress exceeding static Hertz predictions due to inertial effects.
> **Prompt**: Compare static Hertz contact stress with dynamic impact analysis, and discuss why allowable drop height calculations require correction factors.

### Discussion 5: Robotic Gripper Force Optimization
**Background**: Harvesting robots must apply sufficient grip force without bruising fruit.
> **Prompt**: Using Hertz theory, derive the maximum safe gripping force for a spherical fruit-gripper system and discuss sensor-based real-time force control strategies.

---

## 📝 Quiz Questions

### Q1. [Theory] Hertz Contact Radius Formula
In sphere-plate contact, what is the contact radius given by?
| Option | Content |
| --- | --- |
| A | a = F / (π·E*) |
| **B** | **a = (3FR / 4E*)^(1/3)** |
| C | a = (F·R) / E* |
| D | a = √(F / E*) |

<details>
<summary>View Answer</summary>

**Answer: B** — Hertz theory derives a = (3FR/4E*)^(1/3), where R is the effective radius and E* is the combined modulus.
</details>

### Q2. [Theory] Maximum Contact Stress Location
Where does the maximum compressive stress occur in Hertz contact?
| Option | Content |
| --- | --- |
| **A** | **At the center of the contact area (r=0, z=0)** |
| B | At the edge of the contact circle |
| C | At depth z = 0.48a below the surface |
| D | Uniformly distributed across the contact area |

<details>
<summary>View Answer</summary>

**Answer: A** — p_max = (3F)/(2πa²) occurs at the contact center. The subsurface maximum shear stress at z≈0.48a is a separate phenomenon.
</details>

### Q3. [Theory] Subsurface Shear Stress & Bruising
At what approximate depth below the contact surface does the maximum shear stress occur (the primary bruise initiation site)?
| Option | Content |
| --- | --- |
| A | At the surface (z = 0) |
| B | z ≈ 0.1a |
| **C** | **z ≈ 0.48a** |
| D | z ≈ 2a |

<details>
<summary>View Answer</summary>

**Answer: C** — τ_max ≈ 0.31·p_max occurs at z ≈ 0.48a below the surface, explaining why bruises initiate internally.
</details>

### Q4. [Theory] Combined Elastic Modulus E*
The combined elastic modulus E* accounts for:
| Option | Content |
| --- | --- |
| A | Only the fruit's elastic modulus |
| **B** | **Both contacting bodies' elastic moduli and Poisson's ratios** |
| C | Only the contact surface's hardness |
| D | Temperature-dependent viscosity |

<details>
<summary>View Answer</summary>

**Answer: B** — 1/E* = (1-ν₁²)/E₁ + (1-ν₂²)/E₂, combining properties of both contacting materials.
</details>

### Q5. [Theory] Pressure Distribution Shape
What is the shape of the Hertz contact pressure distribution?
| Option | Content |
| --- | --- |
| A | Uniform rectangular |
| B | Linear triangular |
| **C** | **Semi-elliptical (hemispheroid)** |
| D | Gaussian bell curve |

<details>
<summary>View Answer</summary>

**Answer: C** — p(r) = p_max·√(1 - r²/a²), a semi-elliptical profile with maximum at center and zero at contact edge.
</details>

### Q6. [Python] 3D Pressure Visualization
Which matplotlib function creates the 3D surface plot of the pressure distribution?
| Option | Content |
| --- | --- |
| A | `plt.contourf()` |
| **B** | **`ax.plot_surface()`** |
| C | `plt.scatter()` |
| D | `plt.bar3d()` |

<details>
<summary>View Answer</summary>

**Answer: B** — `Axes3D.plot_surface()` renders the semi-elliptical pressure as a continuous 3D surface with color mapping.
</details>

### Q7. [Theory] Effect of Roller Material on Contact Stress
Replacing a steel roller (E=200 GPa) with silicone rubber (E=5 MPa) on a sorting line results in:
| Option | Content |
| --- | --- |
| A | Smaller contact area and higher maximum stress |
| **B** | **Much larger contact area and drastically lower maximum stress** |
| C | No change in contact stress |
| D | Higher contact stress due to increased friction |

<details>
<summary>View Answer</summary>

**Answer: B** — Softer contact surface → lower E* → larger contact radius a → stress distributed over wider area → significantly reduced p_max.
</details>

### Q8. [Python] Interactive Simulator Widgets
In Step 3's interactive Hertz simulator, which widgets enable real-time parameter exploration?
| Option | Content |
| --- | --- |
| A | `matplotlib.animation.FuncAnimation` |
| **B** | **`matplotlib.widgets.Slider` and `matplotlib.widgets.RadioButtons`** |
| C | `matplotlib.patches.Circle` |
| D | `matplotlib.colorbar.Colorbar` |

<details>
<summary>View Answer</summary>

**Answer: B** — Sliders adjust force, radius, and elastic modulus; radio buttons switch between contact surface materials.
</details>

---

# Week 10: Impact Characteristics & Damage Prediction Modeling
> 🔗 [View Detailed Lab Tutorial](week10/Week10_Lab_Impact_Damage_Prediction.md)

## 💡 Discussion Topics

### Discussion 1: Coefficient of Restitution and Energy Conservation in Free-Fall Impact
**Background**: The coefficient of restitution is defined as the ratio of post-impact velocity to pre-impact velocity.
> **Prompt**: Between a perfectly elastic collision (e=1) and a perfectly inelastic collision (e=0), what characteristics do biological resources exhibit? Discuss into what physical or biological forms the "lost" kinetic energy is converted within the biomaterial.

### Discussion 2: Mechanical Properties of Cushioning Materials and Minimizing Peak Impact Force
**Background**: Applying cushioning material extends the collision duration ($\Delta t$), thereby reducing the maximum impact force.
> **Prompt**: When comparing the load-deformation curves of various packaging materials such as corrugated cardboard, expanded polystyrene (EPS), and bubble wrap, how should the yield strength and viscoelastic design criteria be established to achieve optimal cushioning?

## 📝 Quiz Questions

### Q1. [Theory] Coefficient of Restitution
Which of the following correctly describes the formula for the coefficient of restitution $e$ using pre- and post-collision velocities?
| Option | Content |
| --- | --- |
| A | $e = |v_1 - v_2|$ |
| **B** | **$e = |v_2 / v_1|$** |
| C | $e = v_1 \times v_2$ |
| D | $e = v_1 / v_2$ |

<details>
<summary>View Answer</summary>

**Answer: B** — The coefficient of restitution is the absolute ratio of the relative velocity after collision to the relative velocity before collision.
</details>

### Q2. [Theory] Collision Duration and Impact Force
When a free-falling apple hits the ground at the exact same velocity, what is the physical reason it suffers less damage if the floor is covered with a soft sponge compared to a hard concrete floor?
| Option | Content |
| --- | --- |
| A | The sponge reduces the mass of the apple |
| B | The sponge slows the pre-impact velocity |
| **C** | **The collision duration is prolonged, reducing the maximum impact force** |
| D | Gravity acts weaker on the sponge surface |

<details>
<summary>View Answer</summary>

**Answer: C** — For a given impulse ($I = F \Delta t$), extending the collision time $\Delta t$ significantly decreases the average impact force $F$, preventing it from exceeding the tissue rupture threshold.
</details>

---

*This document is updated as new weeks are added.*
