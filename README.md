# 🧠 Backtracking Sudoku Solver CLI
> Visualisasi solving Sudoku dengan algoritma Backtracking & Heuristik MRV (Terminal Version)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-CLI-informational?logo=windows-terminal&logoColor=white)
![Made with](https://img.shields.io/badge/Made%20with-❤️%20and%20Backtracking-blue)


Sudoku Solver berbasis terminal menggunakan algoritma **Backtracking** dan heuristik **MRV (Minimum Remaining Value)**.  
Dilengkapi dengan animasi solving, logging hasil ke CSV, serta pemilihan tingkat kesulitan dan seed untuk reproducibility.

---

## 🎓 Tentang Proyek

Proyek ini dibuat sebagai bagian dari tugas akhir  
**Mata Kuliah Desain dan Analisis Algoritma – Semester 6**  
Program Studi Ilmu Komputer, Universitas Djuanda.

Tujuan proyek ini adalah mengimplementasikan dan memvisualisasikan algoritma **Backtracking**  
dalam menyelesaikan masalah **Constraint Satisfaction Problem (CSP)**, yaitu Sudoku.

---

## 👥 Anggota Kelompok 5

| Peran               | Nama Lengkap                 | NIM         |
|---------------------|------------------------------|-------------|
| 💻 Program           | Muhammad Erlangga Gunawan    | I.2210161   |
|                     | Reva Yulian Satria           | I.2210497   |
| 🗣️ Presentasi        | Muhamad Elgar                | I.2210197   |
| 📄 Artikel/Jurnal    | Agung Restu Ramadhan         | I.2210546   |
|                     | Ardiansyah Putra Pratamaa    | I.2210463   |
|                     | Elita Nur Ilahi              | I.2210060   |

---

## 🕹️ Cara Menjalankan

Pastikan sudah install **Python 3.8+**, lalu jalankan dari terminal:

```bash
python main2.py
```

💡 Untuk panduan lengkap, baca file [`cara-run.txt`](cara-run.txt)

---

## 🎮 Fitur Utama

* ✅ Pilih tingkat kesulitan: Mudah 🟢 / Menengah 🟠 / Sulit 🔴  
* 🎲 Gunakan seed acak atau input manual  
* 🔁 Mode solving:
  * Backtracking biasa
  * Backtracking + MRV heuristic
* 🎥 Animasi proses solving langsung di terminal
* 🧠 Validasi puzzle hanya dengan 1 solusi
* 📦 Logging hasil solving ke file `log_sudoku.csv`

---

## 🧪 Contoh Output CLI

```
🔁 + 🧠 Mode: BT + MRV
------------------------------
5 7 3 | 8 6 9 | 1 2 4
2 1 8 | 5 4 7 | 3 6 9
4 6 9 | 1 2 3 | 5 8 7
---------------------
1 9 5 | 2 8 4 | 6 7 3
7 2 6 | 3 1 5 | 4 9 8
3 8 4 | 7 9 6 | 2 1 5
---------------------
8 3 1 | 4 7 2 | 9 5 6
6 4 7 | 9 5 1 | 8 3 2
9 5 2 | 6 3 8 | 7 4 1

🧬 Seed yang digunakan: (28093) dan memiliki 1 solusi.

✅ Sudoku berhasil dipecahkan!
🔴 Kesulitan Sudoku: Sulit
🧩 Total langkah: 71
⏱️ Waktu: 5.29 detik
🎞️ Animasi aktif: Ya
```

---

## 📁 Struktur Proyek (Singkat)

* `main2.py` – Program utama (semua logic ada di sini)  
* `log_sudoku.csv` – Hasil pencatatan solving
* `cara-run.txt` – Panduan teknis

---

## 📌 Catatan Tambahan

* Minimum Python: `3.8+`  
* Modul yang digunakan: `colorama`, `csv`, `datetime`, `time`, `random`, dll.  
* Tidak butuh koneksi internet atau GUI — full CLI experience!

---

## 🙌 Kontribusi & Forking

Repo ini open-source dan bisa kamu forking/modifikasi untuk tugas, eksperimen, atau eksplorasi algoritma lainnya.  
Silakan bintang ⭐ repo ini kalau merasa bermanfaat!

---

> 🚀 Powered by Kelompok 5 | DAA Project 2025 – Universitas Djuanda

---

## 🌍 English Version

This is a terminal-based Sudoku Solver using the **Backtracking algorithm**, enhanced with **MRV heuristic** for optimization.  
Features include difficulty selection, animation of the solving process, and automatic logging to a CSV file.

---

### 🎓 About This Project

This project was developed as a final assignment  
for the course **Design and Analysis of Algorithms – Semester 6**  
at Computer Science, Universitas Djuanda.

Its main purpose is to implement and visualize the **Backtracking algorithm**  
for solving a **Constraint Satisfaction Problem (CSP)**: Sudoku.

---

### 🧩 Features

- Difficulty selection: Easy / Medium / Hard
- Random seed or manual seed input
- Solving Modes:
  - Naive Backtracking
  - Backtracking + MRV heuristic
- Terminal animation (optional)
- Uniqueness check before solving
- CSV logging (timestamp, level, mode, steps, duration, etc.)

---

### ▶️ How to Run

Make sure Python 3.8+ is installed, then run:

```bash
python main2.py
```

For detailed steps, refer to the [`cara-run.txt`](cara-run.txt) file (Bahasa Indonesia).

---

> 🌟 Built with logic, caffeine, ChatGPT, and a bit of suffering.
