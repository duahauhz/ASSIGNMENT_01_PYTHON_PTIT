import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import umap
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import NearestNeighbors
import hdbscan
import seaborn as sns
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.spatial import ConvexHull


# Read CSV file ------------------------------------------------------------------------------------------------------------------------------------------
# Đọc file CSV ------------------------------------------------------------------------------------------------------------------------------------------
data = pd.read_csv('results.csv')

# Select required columns for each group (e.g., 'Standard Stats' group)
# Chọn các cột cần thiết theo từng nhóm (ví dụ nhóm 'Standard Stats')
required_cols = [
    'Progressive Carries (PrgC)',
    'Goals per 90', 'Assists per 90', 'xG per 90', 'xAG per 90',
    'Goals Against per 90 (GA90)', 'Save Percentage (Save%)', 'Clean Sheets Percentage (CS%)', 'Penalty Kicks Save Percentage',
    'Shots on Target Percentage (SoT%)', 'Shots on Target per 90 (SoT/90)', 'Goals per Shot (G/Sh)', 'Average Shot Distance (Dist)',
    'Pass Completion Percentage (Cmp%)',
    'Key Passes (KP)', 'Passes into Final Third (1/3)', 'Passes into Penalty Area (PPA)', 'Shot-Creating Actions (SCA)', 'SCA per 90', 'Goal-Creating Actions (GCA)', 'GCA per 90',
    'Tackles Won (TklW)', 'Challenges (Tkl)', 'Challenges Lost (TklD)', 'Blocked Shots (Sh)', 'Interceptions (Int)',
    'Touches in Attacking Third',
    'Take-On Success Percentage (Succ%)', 'Take-On Tackled Percentage (Tkl%)',
    'Carries', 'Progressive Carrying Distance (TotDist)', 'Carries into Final Third (1/3)', 'Carries into Penalty Area (CPA)',
    'Passes Received (Rec)', 'Progressive Passes Received (PrgR)',
    'Offsides (Off)', 'Crosses (Crs)', 'Ball Recoveries (Recov)',
    'Aerials Won Percentage (Won%)'
]

# Filter data to keep only required columns
# Lọc dữ liệu chỉ giữ lại các cột cần thiết
filtered_data = data[required_cols]

# Handle Missing Values------------------------------------------------------------------------------------------------------------------------------------
# Xử lý Missing Values------------------------------------------------------------------------------------------------------------------------------------
# Replace 'N/a' with NaN and convert to numeric
# Thay thế 'N/a' thành NaN và chuyển sang kiểu số
filtered_data = filtered_data.replace('N/a', pd.NA)
filtered_data = filtered_data.apply(pd.to_numeric, errors='coerce')

# Fill with median values
# Điền giá trị trung vị
for col in filtered_data.columns:
    median_value = filtered_data[col].median()
    filtered_data[col] = filtered_data[col].fillna(median_value)

# Check remaining missing values
# Kiểm tra số lượng missing values còn lại
print(filtered_data.isnull().sum())

# Exported CSV to verify 100% no Missing Values remaining
# Đã xuất ra csv kiểm tra 100% không còn Missing Values

# Dimensionality Reduction using UMAP------------------------------------------------------------------------------------------------------------
# Giảm chiều dữ liệu phương pháp lựa chọn UMAP------------------------------------------------------------------------------------------------------------
# Data Standardization-----------------------------------------------------------------
# Chuẩn hóa dữ liệu-----------------------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(filtered_data)
#print("\nDữ liệu sau chuẩn hóa (5 hàng đầu):")
#print(X_scaled[:5])

# Initialize UMAP with default parameters------------------------------------------------
# Khởi tạo UMAP với tham số mặc định------------------------------------------------
reducer = umap.UMAP(
    n_components=2,          # Reduce to 2 dimensions for visualization
    n_neighbors=15,          # Number of neighboring points to consider
    min_dist=0.1,            # Minimum distance between points
    metric='euclidean',      # Distance metric
    n_jobs=-1,               # Use all CPUs
    random_state=None        # Remove random_state to allow parallelization
)

# Perform dimensionality reduction---------------------------------------------------------------
# Thực hiện giảm chiều---------------------------------------------------------------
X_umap = reducer.fit_transform(X_scaled)
#print("\nKết quả giảm chiều (5 hàng đầu):")
#print(X_umap[:5])
# Export to CSV file
# xuất ra file csv
output = pd.DataFrame({
   'Player': data['Name'], 
   'UMAP1': X_umap[:, 0],
   'UMAP2': X_umap[:, 1]
})
output.to_csv('umap_results_clean.csv', index=False)

# Visualize the results--------------------------------------------------------------
# Trực quan hóa kết quả--------------------------------------------------------------
plt.figure(figsize=(12, 8))
plt.scatter(
    X_umap[:, 0],           # x-axis - UMAP dimension 1
    X_umap[:, 1],           # y-axis - UMAP dimension 2
    c=X_umap[:, 0],         # Color by dimension 1
    s=10,                   # Point size
    alpha=0.7,              # Transparency
    cmap='Spectral'         # Color map
)

plt.title('Player Distribution by Technical Characteristics (UMAP)', fontsize=16)
plt.xlabel('UMAP Dimension 1', fontsize=12)
plt.ylabel('UMAP Dimension 2', fontsize=12)
plt.grid(alpha=0.3)
plt.colorbar(label='Density')

# Save the plot
# Lưu đồ thị
plt.savefig('umap_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

# Evaluate dimensionality reduction quality----------------------------------------------------
# Đánh giá chất lượng giảm chiều----------------------------------------------------
# print("\nĐÁNH GIÁ CHẤT LƯỢNG GIẢM CHIỀU:")

# Method 1: Dummy labels (for reference only)
# Cách 1: Dummy labels (chỉ để tham khảo)
# dummy_labels = np.random.randint(0, 4, size=len(X_umap))
# print(f"- Silhouette Score (dummy): {silhouette_score(X_umap, dummy_labels):.3f}")

# Method 2: Distance measurement (recommended)
# Cách 2: Đo khoảng cách (khuyến nghị)
# nbrs = NearestNeighbors(n_neighbors=5).fit(X_umap)
# distances = np.mean(nbrs.kneighbors(X_umap)[0][:, 1:])
# print(f"- Avg 5-NN distance: {np.mean(distances):.3f} (càng lớn càng tốt)")   #đã đánh giá khoảng 0.183(chấp nhận được)
# print(f"- Kích thước embedding: {X_umap.shape}")

# Determine optimal number of clusters using Elbow method------------------------------------------------------------------------------------------------------------
# Xác định số cụm tối ưu bằng phương pháp Elbow------------------------------------------------------------------------------------------------------------
range_n_clusters = range(2, 11)
silhouette_scores = []
davies_bouldin_scores = []

for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_umap)
    
    silhouette_avg = silhouette_score(X_umap, cluster_labels)
    silhouette_scores.append(silhouette_avg)
    
    db_score = davies_bouldin_score(X_umap, cluster_labels)
    davies_bouldin_scores.append(db_score)
    
    print(f"With n_clusters = {n_clusters}:")
    print(f"  - Silhouette Score: {silhouette_avg:.3f}")
    print(f"  - Davies-Bouldin Score: {db_score:.3f}")
    
# Plot Elbow chart--------------------------------------------------------------------
# Vẽ biểu đồ Elbow--------------------------------------------------------------------
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(range_n_clusters, silhouette_scores, 'bo-')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score')

plt.subplot(1, 2, 2)
plt.plot(range_n_clusters, davies_bouldin_scores, 'ro-')
plt.xlabel('Number of clusters')
plt.ylabel('Davies-Bouldin Score')
plt.title('Davies-Bouldin Score (lower is better)')

plt.tight_layout()
plt.show()

# Export Silhouette Score plot separately
plt.figure(figsize=(8, 6))
plt.plot(range_n_clusters, silhouette_scores, 'bo-')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score for Optimal Cluster Selection')
plt.grid(True)
plt.savefig('silhouette_score.png', dpi=300, bbox_inches='tight')
plt.close()

# Export Davies-Bouldin Score plot separately
plt.figure(figsize=(8, 6))
plt.plot(range_n_clusters, davies_bouldin_scores, 'ro-')
plt.xlabel('Number of clusters')
plt.ylabel('Davies-Bouldin Score')
plt.title('Davies-Bouldin Score for Optimal Cluster Selection\n(lower is better)')
plt.grid(True)
plt.savefig('davies_bouldin_score.png', dpi=300, bbox_inches='tight')
plt.close()

# Select optimal number of clusters based on Silhouette Score---------------------------------------
# Chọn số cụm tốt nhất dựa trên Silhouette Score---------------------------------------
optimal_clusters = range_n_clusters[np.argmax(silhouette_scores)]
print(f"\nOptimal number of clusters selected: {optimal_clusters}")

# Cluster using KMeans with optimal number of clusters------------------------------------------------
# Phân cụm bằng KMeans với số cụm tối ưu------------------------------------------------
kmeans = KMeans(
    n_clusters=optimal_clusters,
    random_state=42,
    n_init=10
)
labels = kmeans.fit_predict(X_umap)
centroids = kmeans.cluster_centers_

# Visualize clustering results-------------------------------------------------------------------
# Trực quan hóa kết quả-------------------------------------------------------------------
plt.figure(figsize=(12, 8))
cmap = plt.cm.get_cmap('tab20', optimal_clusters)

# Draw convex hull for each cluster---------------------------------------------------------------
# Vẽ convex hull cho mỗi cụm---------------------------------------------------------------
for cluster in np.unique(labels):
    cluster_points = X_umap[labels == cluster]
    if len(cluster_points) > 2:  # ConvexHull needs at least 3 points
        hull = ConvexHull(cluster_points)
        plt.fill(cluster_points[hull.vertices, 0],
                cluster_points[hull.vertices, 1],
                alpha=0.1, color=cmap(cluster))

# Plot points---------------------------------------------------------------------------
# Vẽ các điểm---------------------------------------------------------------------------
scatter = plt.scatter(
    X_umap[:, 0], X_umap[:, 1],
    c=labels, cmap=cmap,
    s=30, alpha=0.8,
    edgecolor='white', linewidth=0.5
)

# Plot centroids----------------------------------------------------------------------------
# Vẽ centroid----------------------------------------------------------------------------
plt.scatter(
    centroids[:, 0], centroids[:, 1],
    marker='*', s=400,
    c='red', edgecolor='black',
    linewidth=1.5, label='Centroids'
)

# Add cluster labels-------------------------------------------------------------------
# Thêm nhãn cho các cụm-------------------------------------------------------------------
for i, (x, y) in enumerate(centroids):
    plt.annotate(
        f"C{i}\n({sum(labels==i)})",
        (x, y), xytext=(0, 10),
        textcoords="offset points",
        ha='center', fontsize=9,
        weight='bold', color='black'
    )

# Calculate evaluation metrics-----------------------------------------------------------
# Tính toán các chỉ số đánh giá-----------------------------------------------------------
metrics = {
    "Silhouette": silhouette_score(X_umap, labels),
    "Davies-Bouldin": davies_bouldin_score(X_umap, labels),
    "Calinski-Harabasz": calinski_harabasz_score(X_umap, labels)
}

# Display parameters------------------------------------------------------------------------
# Hiển thị thông số------------------------------------------------------------------------
plt.title(f'Player Clustering with KMeans (Silhouette: {metrics["Silhouette"]:.2f})', fontsize=16)
plt.colorbar(scatter, label='Cluster ID')
plt.grid(alpha=0.1)
plt.tight_layout()
plt.savefig('kmeans_clusters.png', dpi=300)
plt.show()

# Analyze cluster characteristics-------------------------------------------------------------------
# Phân tích đặc trưng cụm-------------------------------------------------------------------
data['Cluster'] = labels
for cluster in np.unique(labels):
    cluster_data = filtered_data[labels == cluster]
    print(f"\nCluster {cluster} ({len(cluster_data)} players):")
    
    # Top 5 distinctive features
    # Top 5 đặc trưng nổi bật
    top_features = cluster_data.mean().sort_values(ascending=False).head(5)
    for feat, val in top_features.items():
        print(f"- {feat}: {val:.2f} ({val/filtered_data[feat].mean():.1f}x average)")
    
    # Top 3 representative players (closest to centroid)
    # Top 3 cầu thủ tiêu biểu (gần centroid nhất)
    distances = np.linalg.norm(X_umap[labels == cluster] - centroids[cluster], axis=1)
    print("Representatives:", ', '.join(data[labels == cluster].iloc[np.argsort(distances)[:3]]['Name'].values))

# Save results---------------------------------------------------------------------------------
# Lưu kết quả---------------------------------------------------------------------------------
output = pd.concat([
    data[['Name', 'Cluster']],
    pd.DataFrame(X_umap, columns=['UMAP1', 'UMAP2']),
    filtered_data
], axis=1)
output.to_csv('kmeans_cluster_results.csv', index=False)