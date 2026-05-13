import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
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

def evaluate_plsr(X, y, title, n_comp=5, print_res=True):
    """Train and evaluate a PLSR model given spectral data"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    pls = PLSRegression(n_components=n_comp)
    pls.fit(X_train, y_train)
    
    y_pred_train = pls.predict(X_train).flatten()
    y_pred_test = pls.predict(X_test).flatten()
    
    r2_train = r2_score(y_train, y_pred_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    
    r2_test = r2_score(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    if print_res:
        print(f"[{title}] (n_components={n_comp})")
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
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    plt.subplots_adjust(bottom=0.15) # Space for slider

    scatter_train = []
    scatter_test = []
    texts = []
    lines = []
    
    n_comp_init = 5

    for idx, (title, X_prep) in enumerate(preprocessors):
        ax_spec = axes[0, idx]
        ax_scatter = axes[1, idx]
        
        # Train and evaluate model
        y_train, y_test, y_pred_train, y_pred_test, metrics = evaluate_plsr(X_prep, y, title, n_comp_init, print_res=False)
        r2_train, rmse_train, r2_test, rmse_test = metrics

        # Top row: Spectra visualization (Plot all samples, adjust transparency)
        for i in range(X_prep.shape[0]):
            ax_spec.plot(wavelengths, X_prep[i, :], alpha=0.3)
        ax_spec.set_title(f'{title} (Spectra)')
        ax_spec.set_xlabel('Wavelength (nm)')
        ax_spec.set_ylabel('Intensity / Absorbance')

        # Bottom row: Scatter plot visualization
        sc_tr = ax_scatter.scatter(y_train, y_pred_train, color='gray', alpha=0.5, label='Train Data')
        sc_te = ax_scatter.scatter(y_test, y_pred_test, color='blue', alpha=0.7, label='Test Data')
        scatter_train.append(sc_tr)
        scatter_test.append(sc_te)
        
        # y=x ideal line
        min_val = min(y_train.min(), y_pred_train.min(), y_test.min(), y_pred_test.min()) - 0.5
        max_val = max(y_train.max(), y_pred_train.max(), y_test.max(), y_pred_test.max()) + 0.5
        l, = ax_scatter.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal (y=x)')
        lines.append(l)
        
        ax_scatter.set_title(f'Brix Prediction ({title})')
        ax_scatter.set_xlabel('Actual Brix')
        ax_scatter.set_ylabel('Predicted Brix')
        
        # Display R² and RMSE values as a text box
        text_str = (f"Train R²: {r2_train:.3f} / RMSE: {rmse_train:.3f}\n"
                    f"Test R² : {r2_test:.3f} / RMSE: {rmse_test:.3f}")
        txt = ax_scatter.text(0.05, 0.95, text_str, transform=ax_scatter.transAxes,
                 fontsize=10, verticalalignment='top',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))
        texts.append(txt)
                 
        ax_scatter.legend(loc='lower right')
        ax_scatter.grid(True, linestyle=':', alpha=0.6)

    # Slider configuration
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    comp_slider = Slider(
        ax=ax_slider,
        label='Num Components (PLSR)',
        valmin=1,
        valmax=20,
        valinit=n_comp_init,
        valstep=1
    )

    def update(val):
        n_comp = int(comp_slider.val)
        for idx, (title, X_prep) in enumerate(preprocessors):
            y_train, y_test, y_pred_train, y_pred_test, metrics = evaluate_plsr(X_prep, y, title, n_comp, print_res=False)
            r2_train, rmse_train, r2_test, rmse_test = metrics
            
            # Update scatter plot data
            scatter_train[idx].set_offsets(np.column_stack((y_train, y_pred_train)))
            scatter_test[idx].set_offsets(np.column_stack((y_test, y_pred_test)))
            
            # Update y=x ideal line
            min_val = min(y_train.min(), y_pred_train.min(), y_test.min(), y_pred_test.min()) - 0.5
            max_val = max(y_train.max(), y_pred_train.max(), y_test.max(), y_pred_test.max()) + 0.5
            lines[idx].set_data([min_val, max_val], [min_val, max_val])
            
            # Update text
            text_str = (f"Train R²: {r2_train:.3f} / RMSE: {rmse_train:.3f}\n"
                        f"Test R² : {r2_test:.3f} / RMSE: {rmse_test:.3f}")
            texts[idx].set_text(text_str)
            
            # Adjust axis limits
            axes[1, idx].set_xlim([min_val, max_val])
            axes[1, idx].set_ylim([min_val, max_val])
            
        fig.canvas.draw_idle()

    comp_slider.on_changed(update)

    plt.tight_layout()
    # Reset bottom margin to protect slider area
    plt.subplots_adjust(bottom=0.15) 
    print("Please check the plot window. You can adjust the number of principal components using the slider at the bottom.")
    plt.show()

if __name__ == "__main__":
    main()
