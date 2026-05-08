import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def apply_snv(spectra):
    """Standard Normal Variate (SNV) Preprocessing"""
    mean = np.mean(spectra, axis=1, keepdims=True)
    std = np.std(spectra, axis=1, keepdims=True)
    return (spectra - mean) / std

def evaluate_plsr(X, y, title):
    """Train and evaluate a PLSR model given spectral data"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    pls = PLSRegression(n_components=5)
    pls.fit(X_train, y_train)
    
    y_pred_train = pls.predict(X_train).flatten()
    y_pred_test = pls.predict(X_test).flatten()
    
    r2_train = r2_score(y_train, y_pred_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    
    r2_test = r2_score(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    print(f"[{title}]")
    print(f" - Train: R² = {r2_train:.3f}, RMSE = {rmse_train:.3f}")
    print(f" - Test : R² = {r2_test:.3f}, RMSE = {rmse_test:.3f}\n")
    
    return y_train, y_test, y_pred_train, y_pred_test, (r2_train, rmse_train, r2_test, rmse_test)

def main():
    # 1. Load Data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'nir_spectra_brix.csv')
    
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Could not find the data. Please check the path: {data_path}")
        return

    print(f"Data loaded successfully: {df.shape[0]} samples, {df.shape[1]} columns\n")
    
    X = df.drop(columns=['Brix']).values
    y = df['Brix'].values
    wavelengths = np.array([float(col.replace('nm', '')) for col in df.columns[:-1]])

    # 2. Apply various preprocessing techniques (Raw, SNV, Savitzky-Golay)
    X_raw = X
    X_snv = apply_snv(X)
    X_savgol = savgol_filter(X, window_length=15, polyorder=2, deriv=1, axis=1)

    preprocessors = [
        ('Raw Spectra', X_raw),
        ('SNV', X_snv),
        ('SavGol 1st Deriv', X_savgol)
    ]

    # 3. Evaluate Models and Visualize
    plt.figure(figsize=(18, 10))

    for idx, (title, X_prep) in enumerate(preprocessors):
        # Train and evaluate model
        y_train, y_test, y_pred_train, y_pred_test, metrics = evaluate_plsr(X_prep, y, title)
        r2_train, rmse_train, r2_test, rmse_test = metrics

        # Top row: Spectra visualization (plot 5 samples only)
        plt.subplot(2, 3, idx + 1)
        for i in range(5):
            plt.plot(wavelengths, X_prep[i, :])
        plt.title(f'{title} (Spectra)')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity / Absorbance')

        # Bottom row: Scatter plot visualization
        plt.subplot(2, 3, idx + 4)
        plt.scatter(y_train, y_pred_train, color='gray', alpha=0.5, label='Train Data')
        plt.scatter(y_test, y_pred_test, color='blue', alpha=0.7, label='Test Data')
        
        # y=x ideal line
        min_val = min(y_train.min(), y_pred_train.min(), y_test.min(), y_pred_test.min()) - 0.5
        max_val = max(y_train.max(), y_pred_train.max(), y_test.max(), y_pred_test.max()) + 0.5
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal (y=x)')
        
        plt.title(f'Brix Prediction ({title})')
        plt.xlabel('Actual Brix')
        plt.ylabel('Predicted Brix')
        
        # Display R² and RMSE values as a text box
        text_str = (f"Train R²: {r2_train:.3f} / RMSE: {rmse_train:.3f}\n"
                    f"Test R² : {r2_test:.3f} / RMSE: {rmse_test:.3f}")
        plt.text(0.05, 0.95, text_str, transform=plt.gca().transAxes,
                 fontsize=10, verticalalignment='top',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))
                 
        plt.legend(loc='lower right')
        plt.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, 'data', 'plsr_result_comparison.png'), dpi=150)
    print("Please check the plot window. Close the window to exit the program.")
    plt.show()

if __name__ == "__main__":
    main()
