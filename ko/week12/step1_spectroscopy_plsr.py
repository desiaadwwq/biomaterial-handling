import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def apply_snv(spectra):
    """Standard Normal Variate (SNV) 전처리"""
    mean = np.mean(spectra, axis=1, keepdims=True)
    std = np.std(spectra, axis=1, keepdims=True)
    return (spectra - mean) / std

def evaluate_plsr(X, y, title):
    """주어진 스펙트럼 데이터로 PLSR 모델을 학습하고 평가하는 함수"""
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
    # 1. 데이터 로드
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'nir_spectra_brix.csv')
    
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"오류: 데이터를 찾을 수 없습니다. 경로를 확인하세요: {data_path}")
        return

    print(f"데이터 로드 완료: {df.shape[0]} 샘플, {df.shape[1]} 컬럼\n")
    
    X = df.drop(columns=['Brix']).values
    y = df['Brix'].values
    wavelengths = np.array([float(col.replace('nm', '')) for col in df.columns[:-1]])

    # 2. 다양한 전처리 기법 적용 (Raw, SNV, Savitzky-Golay)
    X_raw = X
    X_snv = apply_snv(X)
    X_savgol = savgol_filter(X, window_length=15, polyorder=2, deriv=1, axis=1)

    preprocessors = [
        ('Raw Spectra', X_raw),
        ('SNV', X_snv),
        ('SavGol 1st Deriv', X_savgol)
    ]

    # 3. 모델 평가 및 시각화
    plt.figure(figsize=(18, 10))

    for idx, (title, X_prep) in enumerate(preprocessors):
        # 모델 학습 및 평가
        y_train, y_test, y_pred_train, y_pred_test, metrics = evaluate_plsr(X_prep, y, title)
        r2_train, rmse_train, r2_test, rmse_test = metrics

        # 위쪽 행: 스펙트럼 시각화 (샘플 5개만)
        plt.subplot(2, 3, idx + 1)
        for i in range(5):
            plt.plot(wavelengths, X_prep[i, :])
        plt.title(f'{title} (Spectra)')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity / Absorbance')

        # 아래쪽 행: 산점도 시각화
        plt.subplot(2, 3, idx + 4)
        plt.scatter(y_train, y_pred_train, color='gray', alpha=0.5, label='Train Data')
        plt.scatter(y_test, y_pred_test, color='blue', alpha=0.7, label='Test Data')
        
        # y=x 기준선
        min_val = min(y_train.min(), y_pred_train.min(), y_test.min(), y_pred_test.min()) - 0.5
        max_val = max(y_train.max(), y_pred_train.max(), y_test.max(), y_pred_test.max()) + 0.5
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal (y=x)')
        
        plt.title(f'Brix Prediction ({title})')
        plt.xlabel('Actual Brix')
        plt.ylabel('Predicted Brix')
        
        # R² 및 RMSE 텍스트 박스
        text_str = (f"Train R²: {r2_train:.3f} / RMSE: {rmse_train:.3f}\n"
                    f"Test R² : {r2_test:.3f} / RMSE: {rmse_test:.3f}")
        plt.text(0.05, 0.95, text_str, transform=plt.gca().transAxes,
                 fontsize=10, verticalalignment='top',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))
                 
        plt.legend(loc='lower right')
        plt.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, 'data', 'plsr_result_comparison.png'), dpi=150)
    print("플롯 창을 확인하세요. 창을 닫으면 프로그램이 종료됩니다.")
    plt.show()

if __name__ == "__main__":
    main()
