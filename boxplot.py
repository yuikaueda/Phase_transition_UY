#%%
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator

# ==========================================
# 1. データ読み込み
# ==========================================

#base_path = r"C:\Users\yuika\Dropbox\研究_共有\研究\相転移\Experiment for Ueda"
base_path = os.path.dirname(os.path.abspath(__file__))
conditions = ['7kPa', '20kPa', '41kPa', 'Glass']
data_list = []

print(f"解析開始: {base_path}")
print("-" * 50)

for condition in conditions:
    folder_path = os.path.join(base_path, condition)
    file_path = os.path.join(folder_path, 'Log.txt')
    
    if not os.path.exists(file_path):
        print(f"[×] ファイルなし: {condition}")
        continue

    vals = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) > 6:
                    try:
                        val = float(parts[6])
                        vals.append(val)
                    except ValueError:
                        pass
        
        if len(vals) > 0:
            df_subset = pd.DataFrame({
                'Condition': condition,
                'Anisotropy': vals
            })
            data_list.append(df_subset)
            print(f"[○] {condition}: {len(vals)} 個のデータを読み込み成功")
        else:
            print(f"[!] {condition}: データなし")

    except Exception as e:
        print(f"[×] {condition} エラー: {e}")

print("-" * 50)

if not data_list:
    print("エラー: データがありません。")
else:
    df_all = pd.concat(data_list, ignore_index=True)
    
    # --- 共通設定 ---
    plt.rcParams['font.family'] = 'Times New Roman'
    sns.set(style="ticks", font_scale=1.2, rc={'font.family': 'Times New Roman'})
    plt.rcParams['mathtext.fontset'] = 'stix' # 数式フォントをTimes調(stix)にする
    plt.rcParams['font.family'] = 'Times New Roman' # 全体フォント
    palette = sns.color_palette("Blues", n_colors=len(conditions))
    
    # 統計検定用のペア設定
    loaded_conditions = df_all['Condition'].unique()
    box_pairs = [
        ("7kPa", "20kPa"),
        ("20kPa", "41kPa"),
        ("41kPa", "Glass"),
        ("7kPa", "Glass")
    ]
    valid_pairs = [pair for pair in box_pairs if pair[0] in loaded_conditions and pair[1] in loaded_conditions]


    # ==========================================
    # パターンA: 検定ありのグラフ
    # ==========================================
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    
    # プロット
    sns.boxplot(x='Condition', y='Anisotropy', data=df_all, order=conditions,
                hue='Condition', palette=palette, legend=False,
                width=0.5, linewidth=1.5, showfliers=False, ax=ax1)
    sns.swarmplot(x='Condition', y='Anisotropy', data=df_all, order=conditions,
                  color=".25", size=4, alpha=0.6, ax=ax1)
    
    # 統計解析（有意差のみ表示）
    if valid_pairs:
        try:
            annotator = Annotator(ax1, valid_pairs, data=df_all, x='Condition', y='Anisotropy', order=conditions)
            annotator.configure(test='Mann-Whitney', text_format='star', loc='inside', 
                                hide_non_significant=True, verbose=0)
            annotator.apply_and_annotate()
        except Exception as e:
            print(f"統計解析エラー: {e}")

    ax1.set_xlabel("Substrate stiffness", fontweight='bold', fontsize=20)
    ax1.set_ylabel("Anisotropy", fontweight='bold', fontsize=20)
    ax1.set_ylim(0, 0.7)
    sns.despine()
    plt.tight_layout()
    
    save_path1 = os.path.join(base_path, "Anisotropy_With_Stats.png")
    plt.savefig(save_path1, dpi=300)
    print(f"保存完了(検定あり): {save_path1}")
    plt.show()
    plt.close(fig1) # メモリ解放


    # ==========================================
    # パターンB: 検定なしのグラフ
    # ==========================================
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    # プロット（同じ設定）
    sns.boxplot(x='Condition', y='Anisotropy', data=df_all, order=conditions,
                hue='Condition', palette=palette, legend=False,
                width=0.5, linewidth=1.5, showfliers=False, ax=ax2)
    sns.swarmplot(x='Condition', y='Anisotropy', data=df_all, order=conditions,
                  color=".25", size=4, alpha=0.6, ax=ax2)
    
    # 統計解析の部分をスキップするだけ

    ax2.set_xlabel("Substrate stiffness", fontweight='bold', fontsize=20)
    ax2.set_ylabel("Anisotropy", fontweight='bold', fontsize=20)
    ax2.set_ylim(0, 0.6) # スケールを合わせるため同じ設定にする
    sns.despine()
    plt.tight_layout()
    
    save_path2 = os.path.join(base_path, "Anisotropy_No_Stats.png")
    plt.savefig(save_path2, dpi=300)
    print(f"保存完了(検定なし): {save_path2}")
    plt.show()
    plt.close(fig2)

    print("\nすべての処理が完了しました。")