# Week 12 Lab: Optical Properties II - Internal Quality Evaluation and Spectroscopy

## 🎯 Lab Objectives

- **Understanding Spectroscopy Principles**: Analysis of correlation between Near-Infrared (NIR) absorbance spectra and target substance concentration (Brix)
- **Acquisition of Spectral Data Preprocessing Techniques**: Application of smoothing and derivative for noise removal and scattering correction
- **Execution of Multivariate Regression Modeling**: Learning Partial Least Squares Regression (PLSR) algorithm using Scikit-Learn and evaluating prediction performance

---

## 📊 1. Overview of Lab Data

- **Dataset Location**: `data/nir_spectra_brix.csv` (Virtually generated data, 100 samples)
- **Independent Variable (X)**: Near-infrared absorbance data across wavelengths from 800nm to 1000nm (201 wavelengths)
- **Dependent Variable (Y)**: Actual reference Brix (sugar content) of fruits (e.g., apples, pears)
- **Characteristics**: Simulation of realistic spectral data including baseline drift and scattering noise

---

## 🛠️ 2. Data Preprocessing Techniques (Savitzky-Golay)

- Raw spectral data includes light scattering due to particle size and mechanical noise
- **Savitzky-Golay Filter** (`scipy.signal.savgol_filter`):
  - Removal of noise while maintaining overall shape (peaks) of data using local polynomial regression
  - Application of 1st Derivative: Removal of baseline shift effects and enhancement of peak characteristics
  - **Parameter Settings**: `window_length=15` (Filter length), `polyorder=2` (Polynomial order), `deriv=1` (1st derivative)

---

## 💻 3. Building PLSR (Partial Least Squares Regression) Model

- **Characteristics of PLSR**:
  - Useful regression technique when the number of variables (wavelengths) exceeds the number of samples, or multicollinearity between variables is high
  - Projection of data into a new Latent Variable space that maximizes the covariance between X and Y
- **Lab Execution Steps**:
  1. Data splitting using `train_test_split` (Training 80%, Validation 20%)
  2. Creation of `PLSRegression(n_components=5)` object and execution of learning via `fit()` function
  3. Prediction of Brix for validation data via `predict()` function

---

## 📈 4. Performance Evaluation and Visualization of Results

- **Performance Evaluation Metrics**:
  - **R² (R-squared)**: The closer to 1, the higher the explanatory power of the model
  - **RMSE (Root Mean Squared Error)**: Average difference (error magnitude) between predicted and actual values
- **Visualization (using Matplotlib)**:
  - Comparison of waveforms between original spectra and spectra after Savitzky-Golay preprocessing (verification of peak sharpness)
  - Analysis of actual Brix vs predicted Brix scatter plot (evaluation of alignment with y=x ideal line)
- **Code Execution Method**:
  - Execution of `python step1_spectroscopy_plsr.py` command in terminal, followed by review of text output for model performance and examination of popup plot window
