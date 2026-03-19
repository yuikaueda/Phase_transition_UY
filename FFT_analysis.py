#%%
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from statannotations.Annotator import Annotator

# ==========================================
# 1. Settings and preparation
# ==========================================

base_path = os.path.dirname(os.path.abspath(__file__))
conditions = ['7kPa', '20kPa', '41kPa', 'Glass']
save_dir_fits = os.path.join(base_path, "Fitting_Results")
os.makedirs(save_dir_fits, exist_ok=True)

def exponential_decay(r, A, xi, B):
    return A * np.exp(-r / xi) + B

data_list = []
all_curves = {c: [] for c in conditions}
max_radius_limit = 150 # Radius range to display in the final plot

print(f"Starting analysis: {base_path}")
print("-" * 50)

# ==========================================
# 2. Data loading and fitting
# ==========================================

for condition in conditions:
    csv_folder = os.path.join(base_path, condition, 'FFT')
    csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))
    
    if not csv_files:
        print(f"[×] No data found for: {condition}")
        continue

    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            df = df.apply(pd.to_numeric, errors='coerce').dropna()
            
            r_data = df.iloc[:, 0].values
            g_data = df.iloc[:, 1].values
            
            g_norm = g_data / g_data[0]
            
            p0 = [0.9, 20, 0.1]
            popt, _ = curve_fit(exponential_decay, r_data, g_norm, p0=p0, maxfev=5000)
            A, xi, B = popt
            
            data_list.append({
                'Condition': condition, 
                'Correlation_Length': xi, 
                'File': os.path.basename(file_path)
            })
            
            all_curves[condition].append((r_data, g_norm))

            plt.figure(figsize=(5, 4))
            plt.scatter(r_data, g_norm, s=5, color='gray', alpha=0.5, label='Raw Data')
            plt.plot(r_data, exponential_decay(r_data, *popt), 'r-', label=f'Fit (xi={xi:.2f})')
            plt.title(f"{condition}: {os.path.basename(file_path)}")
            plt.xlabel("Distance (pixels)")
            plt.ylabel("Normalized correlation")
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(save_dir_fits, f"Fit_{condition}_{os.path.basename(file_path)}.png"))
            plt.close()

        except Exception as e:
            print(f"[!] Error processing {file_path}: {e}")

    print(f"[○] {condition}: Processed {len(csv_files)} files")

# ==========================================
# 3. Statistics and visualization
# ==========================================

if not data_list:
    print("Error: No data available for plotting.")
else:
    df_results = pd.DataFrame(data_list)
    plt.rcParams['font.family'] = 'Times New Roman'
    sns.set(style="ticks", font_scale=1.2, rc={'font.family': 'Times New Roman'})
    plt.rcParams['mathtext.fontset'] = 'stix' # 数式フォントをTimes調(stix)にする
    plt.rcParams['font.family'] = 'Times New Roman' # 全体フォント
    
    orange_palette = sns.color_palette("YlOrBr", n_colors=len(conditions))

    # --- Graph 1: Box Plot ---
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='Condition', y='Correlation_Length', data=df_results, order=conditions,
                hue='Condition', palette=orange_palette, legend=False, 
                width=0.5, linewidth=1.5, showfliers=False, ax=ax1)
    sns.swarmplot(x='Condition', y='Correlation_Length', data=df_results, order=conditions,
                  color=".25", size=5, alpha=0.6, ax=ax1)

    box_pairs = [("7kPa", "20kPa"), ("20kPa", "41kPa"), ("41kPa", "Glass"), ("7kPa", "Glass")]
    valid_pairs = [p for p in box_pairs if p[0] in df_results['Condition'].unique() and p[1] in df_results['Condition'].unique()]

    if valid_pairs:
        annotator = Annotator(ax1, valid_pairs, data=df_results, x='Condition', y='Correlation_Length', order=conditions)
        annotator.configure(test='Mann-Whitney', text_format='star', loc='inside', hide_non_significant=True)
        annotator.apply_and_annotate()

    ax1.set_xlabel("Substrate stiffness", fontweight='bold', fontsize=20)
    ax1.set_ylabel(r"Correlation length $\xi$ (pixels)", fontweight='bold', fontsize=20)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(base_path, "PT1_Correlation_Boxplot.png"), dpi=300)
    plt.show()

    # --- Graph 2: Overlaid Mean Correlation Curves ---
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    # --- Graph 3: Semi-log Overlaid Mean Correlation Curves (Added) ---
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    
    common_r = np.linspace(0, max_radius_limit, 200)

    for i, condition in enumerate(conditions):
        if not all_curves[condition]: continue
        
        interp_gs = []
        for r_raw, g_raw in all_curves[condition]:
            f = interp1d(r_raw, g_raw, bounds_error=False, fill_value="extrapolate")
            interp_gs.append(f(common_r))
        
        gs_matrix = np.array(interp_gs)
        mean_g = np.nanmean(gs_matrix, axis=0)
        std_g = np.nanstd(gs_matrix, axis=0)
        
        # Plot for Graph 2 (Linear)
        ax2.plot(common_r, mean_g, label=condition, color=orange_palette[i], lw=2.5)
        ax2.fill_between(common_r, mean_g - std_g, mean_g + std_g, 
                         color=orange_palette[i], alpha=0.2)
        
        # Plot for Graph 3 (Semi-log)
        ax3.plot(common_r, mean_g, label=condition, color=orange_palette[i], lw=2.5)
        # Standard deviation shading can be tricky on log scales if values go near or below zero
        lower_bound = np.maximum(mean_g - std_g, 1e-4) # Clip to a small positive value
        ax3.fill_between(common_r, lower_bound, mean_g + std_g, 
                         color=orange_palette[i], alpha=0.1)

    # Finalize Graph 2
    ax2.set_xlim(0, max_radius_limit)
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel(r"Distance $r$ (pixels)", fontweight='bold', fontsize=20)
    ax2.set_ylabel(r"Normalized correlation $g(r)$", fontweight='bold', fontsize=20)
    ax2.legend(frameon=False, fontsize=15)
    sns.despine(fig=fig2)
    fig2.tight_layout()
    fig2.savefig(os.path.join(base_path, "PT1_Overlay_Correlation_Curves.png"), dpi=300)

    # Finalize Graph 3 (Semi-log)
    ax3.set_yscale('log')
    ax3.set_xlim(0, max_radius_limit)
    ax3.set_ylim(1e-2, 1.2) # Adjusted limits for log scale
    ax3.set_xlabel("Distance r (pixels)", fontweight='bold')
    ax3.set_ylabel("Normalized autocorrelation g(r) [Log]", fontweight='bold')
    ax3.legend(frameon=False)
    sns.despine(fig=fig3)
    fig3.tight_layout()
    fig3.savefig(os.path.join(base_path, "PT1_SemiLog_Correlation_Curves.png"), dpi=300)

    plt.show()
    print("\nAnalysis completed. Files saved to the current directory.")


    # --- Graph 4: Zoomed Mean Correlation Curves (Focused on PT1 Transition) ---
    fig4, ax4 = plt.subplots(figsize=(8, 6))

    # 表示範囲の設定（5~20付近に注目するため、0~40程度までを表示）
    zoom_limit = 20 
    common_r_zoom = np.linspace(0, zoom_limit, 100)

    for i, condition in enumerate(conditions):
        if not all_curves[condition]: continue
    
        interp_gs = []
        for r_raw, g_raw in all_curves[condition]:
            f = interp1d(r_raw, g_raw, bounds_error=False, fill_value="extrapolate")
            interp_gs.append(f(common_r_zoom))
    
        gs_matrix = np.array(interp_gs)
        mean_g = np.nanmean(gs_matrix, axis=0)
        std_g = np.nanstd(gs_matrix, axis=0)
    
        ax4.plot(common_r_zoom, mean_g, label=condition, color=orange_palette[i], lw=3)
        ax4.fill_between(common_r_zoom, mean_g - std_g, mean_g + std_g, 
                        color=orange_palette[i], alpha=0.15)

    # 相関距離 xi の基準となる 1/e (約0.37) に水平線を引く
    ax4.axhline(y=1/np.e, color='gray', linestyle='--', lw=1, label='1/e (Threshold for ξ)')

    ax4.set_xlim(0, zoom_limit)
    ax4.set_ylim(0, 1.05)
    ax4.set_xlabel("Distance r (pixels)", fontweight='bold', fontsize=16)
    ax4.set_ylabel("Normalized Autocorrelation g(r)", fontweight='bold', fontsize=16)
    ax4.set_title("Zoomed View: Initial Decay of Structural Correlation", fontsize=14)
    ax4.legend(frameon=False, loc='upper right')
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(base_path, "PT1_Zoomed_Correlation_Curves.png"), dpi=300)
    plt.show()