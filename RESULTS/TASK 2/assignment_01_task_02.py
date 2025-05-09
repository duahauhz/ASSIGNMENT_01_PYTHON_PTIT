import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import rcParams
import matplotlib.colors as mcolors

# ====================
# 1. CÀI ĐẶT GIAO DIỆN ĐỒ HỌA
# ====================
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Roboto', 'Arial']
rcParams['axes.linewidth'] = 1.2
rcParams['axes.edgecolor'] = '#333333'
rcParams['grid.color'] = '#D3D3D3'
rcParams['grid.alpha'] = 0.5

available_styles = plt.style.available
if 'seaborn-v0_8-darkgrid' in available_styles:
    plt.style.use('seaborn-v0_8-darkgrid')
elif 'dark_background' in available_styles:
    plt.style.use('dark_background')
else:
    plt.style.use('ggplot')

# Palette màu cho tất cả các đội
TEAM_PALETTE = {
    'Liverpool': '#C8102E',
    'Arsenal': '#EF0107',
    'Manchester City': '#6CABDD',
    'Fulham': '#000000',
    'Newcastle Utd': '#241F20',
    'Brentford': '#E30613',
    'Bournemouth': '#DA291C',
    'Chelsea': '#034694',
    'Tottenham': '#132257',
    'Crystal Palace': '#1B458F',
    'Brighton': '#0057B8',
    "Nott'ham Forest": '#DD0000',
    'Wolves': '#FDB913',
    'Aston Villa': '#95BFE5',
    'West Ham': '#7A263A',
    'Everton': '#003399',
    'Manchester Utd': '#DA291C',
    'Leicester City': '#003087',
    'Southampton': '#D71920',
    'Ipswich Town': '#3A70A3'
}

# ====================
# 2. HÀM VẼ BIỂU ĐỒ NÂNG CAO
# ====================
def plot_enhanced_distribution(metric):
    golden_ratio = 1.618
    fig_width = 16
    fig_height = fig_width / golden_ratio
    plt.figure(figsize=(fig_width, fig_height), dpi=300)
    
    team_order = df.groupby('Team')[metric].mean().sort_values(ascending=False).index
    
    gradient_palette = {
        team: mcolors.LinearSegmentedColormap.from_list(
            f"{team}_gradient", ["#FFFFFF", color, color]
        ) for team, color in TEAM_PALETTE.items()
    }
    
    ax = sns.violinplot(data=df, x='Team', y=metric, order=team_order,
                       palette=TEAM_PALETTE, inner=None, linewidth=1.5,
                       saturation=0.8, alpha=0.9)
    
    sns.swarmplot(data=df, x='Team', y=metric, order=team_order,
                 color='black', alpha=0.6, size=3, ax=ax)
    
    for i, team in enumerate(team_order[:3]):
        ax.get_children()[i].set_edgecolor('gold')
        ax.get_children()[i].set_linewidth(2.5)
        ax.get_children()[i].set_alpha(0.95)
    
    for i, team in enumerate(team_order):
        mean_val = df[df['Team'] == team][metric].mean()
        ax.plot([i-0.4, i+0.4], [mean_val, mean_val], 
                color='black', linestyle='--', linewidth=1.5, alpha=0.7)
        ax.text(i, mean_val + 0.02 * (ax.get_ylim()[1] - ax.get_ylim()[0]), 
                f'{mean_val:.2f}', ha='center', fontsize=10, fontweight='bold')
    
    plt.title(f'PHÂN PHỐI {metric.upper()} THEO ĐỘI\nMùa giải 2024-2025',
              fontsize=20, pad=25, fontweight='bold', color='#333333')
    plt.xlabel('', fontsize=12)
    plt.ylabel(metric, fontsize=14, fontweight='medium')
    plt.xticks(rotation=45, ha='right', fontsize=12, fontweight='medium')
    plt.yticks(fontsize=12)
    
    ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    
    plt.annotate('Dữ liệu: Premier League 2024-2025\nThiết kế: Phân tích bóng đá',
                xy=(0.5, -0.25), xycoords='axes fraction',
                ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    safe_name = metric.replace(' ', '_').replace('/', '_')
    plt.savefig(f'team_distribution_plots/ENHANCED_{safe_name}.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# ====================
# 3. HÀM TẠO BẢNG XẾP HẠNG ĐẦY ĐỦ (KHÔNG LƯU CSV)
# ====================
def create_complete_ranking(team_stats):
    key_metrics = [
        'Matches Played', 'Starts', 'Goals', 'Assists',
        'Expected Goals (xG)', 'Expected Assist Goals (xAG)',
        'Progressive Passes (PrgP)', 'Progressive Carries (PrgC)',
        'Tackles (Tkl)', 'Interceptions (Int)', 'Blocks'
    ]
    
    available_metrics = [m for m in key_metrics if m in team_stats.columns.get_level_values(0)]
    
    performance_score = team_stats.xs('mean', axis=1, level=1)[available_metrics].mean(axis=1)
    
    ranking_df = team_stats.xs('mean', axis=1, level=1)[available_metrics]
    ranking_df['Performance Score'] = performance_score
    ranking_df = ranking_df.sort_values('Performance Score', ascending=False)
    
    ranking_df = ranking_df.round(2)
    
    return ranking_df

# ====================
# 4. HÀM TẠO RESULTS2.CSV
# ====================
def generate_results2(df_numeric):
    numeric_metrics = [
        'Age', 'Matches Played', 'Starts', 'Minutes', 'Goals', 'Assists',
        'Yellow Cards', 'Red Cards', 'Expected Goals (xG)', 'Expected Assist Goals (xAG)',
        'Progressive Carries (PrgC)', 'Progressive Passes (PrgP)', 'Progressive Passes Received (PrgR)',
        'Goals per 90', 'Assists per 90', 'xG per 90', 'xAG per 90', 'Goals Against per 90 (GA90)',
        'Save Percentage (Save%)', 'Clean Sheets Percentage (CS%)', 'Penalty Kicks Save Percentage',
        'Shots on Target Percentage (SoT%)', 'Shots on Target per 90 (SoT/90)', 'Goals per Shot (G/Sh)',
        'Average Shot Distance (Dist)', 'Passes Completed (Cmp)', 'Pass Completion Percentage (Cmp%)',
        'Total Passing Distance (TotDist)', 'Short Pass Completion Percentage',
        'Medium Pass Completion Percentage', 'Long Pass Completion Percentage', 'Key Passes (KP)',
        'Passes into Final Third (1/3)', 'Passes into Penalty Area (PPA)', 'Crosses into Penalty Area (CrsPA)',
        'Shot-Creating Actions (SCA)', 'SCA per 90', 'Goal-Creating Actions (GCA)', 'GCA per 90',
        'Tackles (Tkl)', 'Tackles Won (TklW)', 'Challenges (Tkl)', 'Challenges Lost (TklD)', 'Blocks',
        'Blocked Shots (Sh)', 'Blocked Passes (Pass)', 'Interceptions (Int)', 'Touches',
        'Touches in Defensive Penalty Area', 'Touches in Defensive Third', 'Touches in Middle Third',
        'Touches in Attacking Third', 'Touches in Attacking Penalty Area', 'Take-Ons (Att)',
        'Take-On Success Percentage (Succ%)', 'Take-On Tackled Percentage (Tkl%)', 'Carries',
        'Progressive Carrying Distance (TotDist)', 'Carries into Final Third (1/3)',
        'Carries into Penalty Area (CPA)', 'Miscontrols (Mis)', 'Dispossessed (Dis)', 'Passes Received (Rec)',
        'Fouls Committed (Fls)', 'Fouls Drawn (Fld)', 'Offsides (Off)', 'Crosses (Crs)',
        'Ball Recoveries (Recov)', 'Aerials Won (Won)', 'Aerials Lost (Lost)', 'Aerials Won Percentage (Won%)'
    ]
    
    available_metrics = [m for m in numeric_metrics if m in df_numeric.columns]
    
    team_median = df_numeric.groupby('Team')[available_metrics].median().round(2)
    team_median.columns = [f"{col}_Median" for col in team_median.columns]
    
    team_stats = df_numeric.groupby('Team')[available_metrics].agg(['mean', 'std']).round(2)
    team_stats.columns = [f"{col[0]}_{col[1].capitalize()}" for col in team_stats.columns]
    
    overall_stats = df_numeric[available_metrics].agg(['mean', 'std']).T.round(2)
    overall_stats.columns = ['Overall_Mean', 'Overall_Std']
    
    results2_df = team_median.join(team_stats)
    
    overall_row = pd.DataFrame(index=['Overall'], columns=results2_df.columns)
    for metric in available_metrics:
        overall_row[f"{metric}_Median"] = df_numeric[metric].median()
        overall_row[f"{metric}_Mean"] = overall_stats.loc[metric, 'Overall_Mean']
        overall_row[f"{metric}_Std"] = overall_stats.loc[metric, 'Overall_Std']
    overall_row = overall_row.round(2)
    
    results2_df = pd.concat([results2_df, overall_row])
    
    results2_df.to_csv('team_stats_results/results2.csv', encoding='utf-8-sig', float_format='%.2f')
    
    return results2_df, available_metrics

# ====================
# 5. HÀM TẠO TOP_TEAM_PER_METRIC.TXT
# ====================
def generate_top_team_per_metric(df_numeric, available_metrics):
    output = []
    team_means = df_numeric.groupby('Team')[available_metrics].mean()
    
    for metric in available_metrics:
        top_team = team_means[metric].idxmax()
        top_value = team_means[metric].max()
        output.append(f"{metric}: {top_team} ({top_value:.2f})")
    
    with open('team_stats_results/top_team_per_metric.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(output))

# ====================
# 6. HÀM TẠO TOP_3_RANKING.TXT
# ====================
def generate_top_3_ranking(df, available_metrics):
    output = []
    
    for metric in available_metrics:
        top_3 = df[['Name', 'Team', metric]].sort_values(by=metric, ascending=False).head(3)
        output.append(f"\n{metric}:")
        for _, row in top_3.iterrows():
            output.append(f"  {row['Name']} ({row['Team']}): {row[metric]:.2f}")
    
    with open('team_stats_results/top_3_ranking.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(output))

# ====================
# 7. THỰC THI CHÍNH
# ====================
if __name__ == '__main__':
    os.makedirs('team_distribution_plots', exist_ok=True)
    os.makedirs('team_stats_results', exist_ok=True)
    
    try:
        df = pd.read_csv('results.csv')
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file results.csv")
        print("Vui lòng đảm bảo file được đặt đúng thư mục")
        exit()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_numeric = df[['Team'] + list(numeric_cols)]
    
    team_stats = df_numeric.groupby('Team').agg(['mean', 'median', 'std'])
    
    for metric in ['Goals', 'Expected Goals (xG)', 'Assists', 'Progressive Passes (PrgP)']:
        if metric in df_numeric.columns:
            plot_enhanced_distribution(metric)
        else:
            print(f"Cảnh báo: Cột '{metric}' không tồn tại trong dữ liệu.")
    
    ranking = create_complete_ranking(team_stats)
    
    results2, available_metrics = generate_results2(df_numeric)
    
    generate_top_team_per_metric(df_numeric, available_metrics)
    generate_top_3_ranking(df, available_metrics)
    
    print("Hoàn thành phân tích nâng cao!")
    print("\nTop 5 đội mạnh nhất:")
    print(ranking.head(5))
    print("\nĐã tạo file results2.csv với thống kê trung vị, trung bình và độ lệch chuẩn cho tất cả chỉ số số.")
    print("Đã tạo file top_team_per_metric.txt với đội có chỉ số cao nhất cho mỗi metric.")
    print("Đã tạo file top_3_ranking.txt với top 3 cầu thủ cho mỗi metric.")