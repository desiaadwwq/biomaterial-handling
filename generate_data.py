import numpy as np
import pandas as pd
import os

def generate_nir_data(num_samples=100):
    # Wavelengths from 800nm to 1000nm (201 points)
    wavelengths = np.linspace(800, 1000, 201)
    
    # Generate random Brix values between 8.0 and 15.0
    brix_values = np.random.uniform(8.0, 15.0, num_samples)
    
    spectra = []
    for brix in brix_values:
        # Base spectrum (scattering baseline, varies per sample)
        baseline = np.random.uniform(0.1, 0.5) + np.random.uniform(-0.001, 0.001) * wavelengths
        
        # Add realistic chemical/physical variations that make prediction harder
        # Simulate that the spectrum reflects "measured" property with some error
        # Std dev of ~0.6 roughly translates to ~0.9 R^2 for a uniform [8, 15] distribution
        effective_brix = brix + np.random.normal(0, 0.6) 
        
        # Main absorption peak for sugar (e.g., around 910nm)
        peak_center = 910 + np.random.normal(0, 0.5) # slight shift in peak
        peak_width = 20 + np.random.normal(0, 0.2)
        peak_intensity = 0.05 * effective_brix
        absorption = peak_intensity * np.exp(-((wavelengths - peak_center) ** 2) / (2 * peak_width ** 2))
        
        # Add some random instrument noise
        noise = np.random.normal(0, 0.005, len(wavelengths))
        
        # Combine to form final spectrum
        spectrum = baseline + absorption + noise
        spectra.append(spectrum)
        
    # Create DataFrame
    columns = [f"{int(w)}nm" for w in wavelengths]
    df = pd.DataFrame(spectra, columns=columns)
    df['Brix'] = brix_values
    
    return df

if __name__ == "__main__":
    np.random.seed(42) # For reproducibility
    df = generate_nir_data(100)
    
    # Save to both ko and en directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ko_path = os.path.join(base_dir, 'ko', 'week12', 'data', 'nir_spectra_brix.csv')
    en_path = os.path.join(base_dir, 'en', 'week12', 'data', 'nir_spectra_brix.csv')
    
    df.to_csv(ko_path, index=False)
    df.to_csv(en_path, index=False)
    
    print(f"Dataset generated with shape {df.shape}")
    print(f"Saved to:\n - {ko_path}\n - {en_path}")
