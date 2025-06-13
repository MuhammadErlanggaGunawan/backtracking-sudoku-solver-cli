import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv('log_sudoku.csv')

# Pastikan tipe data
df["Durasi"] = df["Durasi"].astype(float)
df["Langkah"] = df["Langkah"].astype(int)

# Set style
sns.set(style="whitegrid", palette="muted", font_scale=1.1)

# ===== 1. Boxplot Jumlah Langkah dengan Zoom + Outlier Highlight =====
plt.figure(figsize=(8, 6))
sns.boxplot(x="Mode", y="Langkah", data=df)
sns.stripplot(x="Mode", y="Langkah", data=df, color="red", jitter=True, alpha=0.5)
plt.ylim(0, 1000)  # Zoom biar distribusi lebih jelas
plt.title("Perbandingan Jumlah Langkah: Naive vs BT + MRV (Zoom <1000)")
plt.ylabel("Jumlah Langkah")
plt.xlabel("Metode")
plt.tight_layout()
plt.show()

# ===== 2. Bar Chart Rata-Rata Langkah & Durasi =====
mean_df = df.groupby("Mode")[["Langkah", "Durasi"]].mean().reset_index()

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.barplot(x="Mode", y="Langkah", data=mean_df, ax=ax[0])
ax[0].set_title("Rata-rata Langkah")
ax[0].set_ylabel("Langkah")

sns.barplot(x="Mode", y="Durasi", data=mean_df, ax=ax[1])
ax[1].set_title("Rata-rata Durasi")
ax[1].set_ylabel("Durasi (detik)")
ax[1].set_xlabel("Metode")

plt.tight_layout()
plt.show()

# ===== 3. Lineplot per Seed (Performa Tiap Puzzle) =====
df_sorted = df.sort_values(by="Seed")

plt.figure(figsize=(10, 6))
sns.lineplot(x="Seed", y="Langkah", hue="Mode", data=df_sorted, marker='o')
plt.title("Jumlah Langkah per Seed")
plt.xlabel("Seed")
plt.ylabel("Jumlah Langkah")
plt.tight_layout()
plt.show()

# ===== 4. Print Outlier Info (Optional tapi penting!) =====
threshold = 1000
outliers = df[df["Langkah"] > threshold]
if not outliers.empty:
    print("⚠️ Outlier Terdeteksi (Langkah > 1000):")
    print(outliers[["Mode", "Langkah", "Seed"]])
