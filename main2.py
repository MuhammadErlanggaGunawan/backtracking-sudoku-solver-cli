'''
╔════════════════════════════════════════════════════════════════════╗
║               Sudoku Solver CLI Interaktif 🇮🇩 - Kelompok 5         ║
╚════════════════════════════════════════════════════════════════════╝

Anggota Kelompok 5 (Algoritma Backtracking):
1. REVA YULIAN SATRIA        - I.2210497
2. MUHAMAD ELGAR             - I.2210197
3. MUHAMMAD ERLANGGA GUNAWAN - I.2210161
4. AGUNG RESTU RAMADHAN      - I.2210546
5. ARDIANSYAH PUTRA PRATAMAA - I.2210463
6. ELITA NUR ILAHI           - I.2210060

📌 Deskripsi Program:
Program ini adalah aplikasi command-line interaktif untuk menyelesaikan puzzle Sudoku menggunakan algoritma backtracking,
dengan dukungan heuristik Minimum Remaining Value (MRV) dan animasi proses solving secara visual di terminal.

🎯 Fitur Utama:
- Pemilihan level kesulitan puzzle (Mudah, Menengah, Sulit)
- Opsi seed acak atau manual untuk reproducibility
- Mode solving: Backtracking Biasa atau Backtracking + MRV
- Tampilan animasi solving langsung di terminal
- Logging otomatis ke file CSV (timestamp, level, langkah, durasi, seed, mode, dll.)
- Validasi bahwa puzzle hanya memiliki satu solusi sebelum diselesaikan

🎓 Tujuan:
Program ini ditujukan sebagai implementasi dan visualisasi praktis dari algoritma backtracking
pada masalah Constraint Satisfaction Problem (CSP), khususnya penyelesaian Sudoku.

'''

# ===============================================================================

import time     # Untuk jeda animasi antar langkah solver
import os       # Membersihkan layar terminal
import sys      # Akses dan kontrol argumen terminal & keluar program
import copy     # Duplikasi objek puzzle tanpa ngubah yang asli (deep copy)
import csv      # Ekspor hasil solving ke file CSV
import random   # Digunakan untuk acak angka (generate puzzle)
from colorama import init, Fore, Style  # Untuk mewarnai teks di terminal / CLI
from sudoku import Sudoku  # Library untuk generate puzzle sudoku
from datetime import datetime  # Format tanggal, waktu sekarang, atau menghitung durasi

def apakah_support_warna(): 
    '''
    Fungsi ini digunakan untuk mengecek apakah terminal mendukung output berwarna.
    Caranya dengan memeriksa apakah stdout memiliki atribut isatty,
    dan apakah terminal yang digunakan adalah terminal interaktif (bukan file atau pipe).
    Jika keduanya True, maka warna bisa ditampilkan dengan aman.
    '''

    # Mengecek apakah sys.stdout memiliki atribut/fungsi isatty
    # Ini penting karena jika output di-redirect ke file atau objek lain, bisa saja nggak ada isatty
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    # sys.stdout.isatty() akan True jika output mengarah ke terminal asli
    # Jika False, berarti output ke file/pipe dan sebaiknya hindari print dengan warna


def apakah_valid(papan, tebakan, baris, kolom):
    '''
    Fungsi ini digunakan untuk mengecek apakah angka 'tebakan' valid 
    jika dimasukkan ke posisi (baris, kolom) di papan Sudoku.
    Valid artinya tidak melanggar tiga aturan utama Sudoku:
    - Tidak boleh ada angka yang sama di baris
    - Tidak boleh ada angka yang sama di kolom
    - Tidak boleh ada angka yang sama di dalam kotak 3x3 tempat sel itu berada

    jika lolos semua pengecekan, fungsi ini return True, artinya tebakan sah.
    jika ada yang dilanggar, langsung return False.
    '''
    
    # Cek apakah tebakan sudah ada di baris yang sama
    if tebakan in papan[baris]:  # Cek duplikat di baris
        return False
    
    # Cek apakah tebakan sudah ada di kolom yang sama
    if any(papan[i][kolom] == tebakan for i in range(9)):  # Cek duplikat di kolom
        return False
    
    # Cari posisi kiri-atas dari kotak 3x3 tempat sel (baris, kolom) berada
    box_baris, box_kolom = (baris // 3) * 3, (kolom // 3) * 3  # Menghitung indeks awal kotak 3x3
    
    # Loop untuk mengecek seluruh isi kotak 3x3
    for i in range(3):
        for j in range(3):
            # Cek apakah tebakan sudah ada di kotak 3x3
            if papan[box_baris + i][box_kolom + j] == tebakan:
                return False
    
    # Jika lolos semua pengecekan, berarti tebakan valid
    return True


def cari_sel_kosong_biasa(papan):
    '''
    Fungsi ini digunakan untuk mencari posisi sel kosong (yang bernilai 0) 
    di papan Sudoku secara urut dari kiri ke kanan, atas ke bawah (Naive/Basic).
    Jika ditemukan, fungsi langsung mengembalikan indeks (baris, kolom) dari sel kosong pertama.
    jika tidak ada sel kosong lagi, berarti papan sudah penuh, dan fungsi return (None, None).
    '''
    
    # Looping baris dari 0 sampai 8
    for baris in range(9):
        # Looping kolom dari 0 sampai 8
        for kolom in range(9):
            # Cek apakah sel ini kosong (bernilai 0)
            if papan[baris][kolom] == 0:
                return (baris, kolom)  # Return posisi sel kosong pertama

    # jika tidak ada sel kosong, return (None, None) sebagai penanda papan sudah penuh
    return (None, None)


def cari_sel_kosong_mrv(papan):
    '''
    Fungsi ini menerapkan heuristik Minimum Remaining Value (MRV),
    yaitu mencari sel kosong yang memiliki kemungkinan tebakan paling sedikit.
    Tujuannya adalah meminimalkan kemungkinan salah, karena semakin sedikit opsi,
    semakin besar kemungkinan kita memilih angka yang benar di awal.
    
    Fungsi akan mengembalikan posisi (baris, kolom) dari sel kosong
    dengan jumlah opsi terkecil. Jika ada sel dengan hanya 1 kemungkinan valid,
    langsung dikembalikan karena itu paling prioritas.
    jika tidak ada sel kosong, fungsi akan return (None, None).
    '''

    min_opsi = 10  # Jumlah kemungkinan minimum, inisialisasi dengan nilai maksimal
    kandidat = None  # Menyimpan posisi kandidat terbaik (sel dengan opsi paling sedikit)

    # Looping semua baris dan kolom
    for baris in range(9):
        for kolom in range(9):
            # Cek hanya sel yang kosong (bernilai 0)
            if papan[baris][kolom] == 0:
                # Hitung jumlah kemungkinan angka valid untuk sel ini
                opsi = [tebakan for tebakan in range(1, 10) if apakah_valid(papan, tebakan, baris, kolom)]

                # Update jika jumlah opsi lebih sedikit dari sebelumnya
                if len(opsi) < min_opsi:
                    min_opsi = len(opsi)
                    kandidat = (baris, kolom)

                    # Jika cuma punya 1 opsi, langsung balikin (paling optimal)
                    if min_opsi == 1:
                        return kandidat
                    
    # Return kandidat terbaik, atau (None, None) jika tidak ada sel kosong
    return kandidat if kandidat else (None, None)


def pecahkan_sudoku_anim(papan, delay=0.03, papan_awal=None, deskripsi_mode=None, mode='1'):
    '''
    Fungsi utama untuk menyelesaikan Sudoku dengan metode backtracking, 
    sekaligus menampilkan animasi proses solving-nya di terminal (jika delay > 0).
    
    Parameter:
    - papan: papan sudoku 9x9 yang ingin dipecahkan.
    - delay: waktu tunda antar langkah animasi (0.03 detik default).
    - papan_awal: untuk referensi posisi awal yang sudah diisi.
    - deskripsi_mode: label yang menunjukkan mode solving (Naive / MRV).
    - mode: '1' untuk naive (kiri atas), selain itu pakai MRV heuristik.

    Fungsi mengembalikan:
    - sukses: apakah puzzle berhasil diselesaikan
    - langkah: jumlah langkah percobaan yang dilakukan
    - durasi: waktu total yang dibutuhkan untuk menyelesaikan
    '''

    langkah = 0  # Hitung jumlah langkah percobaan
    start = time.time()  # Waktu mulai

    def backtrack():
        nonlocal langkah  # Biar langkah bisa diupdate dari fungsi dalam
        if delay > 0:
            animasi_cli(papan, None, 0, papan_awal, deskripsi_mode)  # Tampilkan papan pertama

        # Pilih metode pencarian sel kosong: naive atau MRV
        baris, kolom = cari_sel_kosong_biasa(papan) if mode == '1' else cari_sel_kosong_mrv(papan)

        # jika tidak ada sel kosong, artinya sudah selesai
        if baris is None or kolom is None:
            os.system('cls' if os.name == 'nt' else 'clear')  # Bersihin terminal
            print(
                deskripsi_mode + "\n" +
                (Fore.WHITE + "-"*30 + Style.RESET_ALL if apakah_support_warna() else "-"*30 + "\n")
            )
            tampilkan_papan(papan, None, papan_awal)  # Tampilkan hasil akhir
            return True

        # Coba angka 1–9 di posisi kosong yang dipilih
        for tebakan in range(1, 10):
            if apakah_valid(papan, tebakan, baris, kolom):  # Cek valid atau nggak
                papan[baris][kolom] = tebakan  # Masukkan angka
                langkah += 1  # Tambah langkah

                if delay > 0:
                    print(f"Langkah {langkah}: Coba {tebakan} di ({baris}, {kolom})")
                    animasi_cli(papan, (baris, kolom), delay, papan_awal, deskripsi_mode)

                if backtrack():  # Rekursi: lanjut ke sel berikutnya
                    return True

                # Backtrack jika gagal
                papan[baris][kolom] = 0  # Reset sel
                if delay > 0:
                    print(f"Langkah {langkah}: Backtrack dari ({baris}, {kolom})")
                    animasi_cli(papan, (baris, kolom), delay, papan_awal, deskripsi_mode)

        return False  # jika semua angka gagal, berarti perlu backtrack ke level sebelumnya

    sukses = backtrack()  # Mulai solving
    durasi = time.time() - start  # Hitung durasi total
    return sukses, langkah, durasi  # Return hasil solving


def apakah_satu_solusi(papan):
    '''
    Fungsi ini digunakan untuk mengecek apakah sebuah puzzle Sudoku 
    masih memungkinkan punya satu solusi yang unik.
    
    Ide utamanya: jika jumlah sel kosong terlalu banyak (di atas 58), 
    besar kemungkinan puzzle itu terlalu ambigu, dan solver bisa 
    menghasilkan banyak solusi berbeda. Jadi kita tolak aja sejak awal.
    
    Angka 58 ini threshold konservatif—berdasarkan eksperimen,
    puzzle dengan lebih dari 58 sel kosong cenderung tidak unik solusinya.
    '''

    sel_kosong = sum(1 for row in papan for num in row if num == 0)  # Hitung jumlah sel kosong

    if sel_kosong > 58:  # Threshold kasar: lebih dari 58 sel kosong, kemungkinan lebih dari 1 solusi
        return False
    return True  # Masih mungkin punya solusi unik


def hitung_solusi(papan):
    '''
    Fungsi ini digunakan untuk menghitung jumlah solusi dari sebuah papan Sudoku.
    
    Tujuannya adalah untuk memastikan bahwa puzzle yang kita proses hanya punya 
    satu solusi (unik). Kita gunakan teknik backtracking, tapi dengan early stop
    ketika sudah ketemu lebih dari 1 solusi, jadi hemat waktu juga.
    '''

    count = 0  # Inisialisasi jumlah solusi
    papan_copy = copy.deepcopy(papan)  # Salin papan supaya tidak mengubah papan asli

    def solve(papan_copy):
        nonlocal count  # Supaya bisa update variabel count dari dalam fungsi lokal

        if count > 1:  # jika udah dapet 2 solusi, kita stop aja langsung (early exit)
            return

        baris, kolom = cari_sel_kosong_mrv(papan_copy)  # Cari sel kosong pakai MRV untuk efisiensi

        if baris is None:  # jika tidak ada sel kosong lagi, berarti solusi ditemukan
            count += 1
            return

        for tebakan in random.sample(range(1, 10), 9):  # Coba angka 1–9 secara acak
            if apakah_valid(papan_copy, tebakan, baris, kolom):  # Cek apakah tebakan valid
                papan_copy[baris][kolom] = tebakan  # Isi sel dengan tebakan
                solve(papan_copy)  # Rekursi untuk lanjut ke langkah berikutnya
                papan_copy[baris][kolom] = 0  # Backtrack: kosongkan lagi
                if count > 1:  # Early exit kedua, buat jaga-jaga
                    return

    solve(papan_copy)  # Mulai solve
    return count  # Kembalikan jumlah solusi yang ditemukan


def generate_valid_puzzle(tingkat, seed_input=None, max_attempts=100):
    '''
    Fungsi ini bertugas untuk menghasilkan puzzle Sudoku yang valid dan hanya memiliki satu solusi.
    
    Prosesnya dilakukan dengan mencoba generate puzzle secara acak berdasarkan seed.
    Puzzle yang dihasilkan akan dicek:
    1. Apakah jumlah sel kosongnya masih memungkinkan punya 1 solusi?
    2. Apakah hasilnya benar-benar hanya punya 1 solusi?

    jika gagal nemu puzzle valid setelah sejumlah percobaan, fungsi akan mengembalikan None.
    '''

    for _ in range(max_attempts):  # Batas maksimal percobaan
        try:
            seed = seed_input if seed_input is not None else random.randint(0, 99999)  # Tentukan seed random
            puzzle = Sudoku(3, seed=seed).difficulty(tingkat)  # Generate puzzle pakai library sudoku
            
            if contoh_papan is None: # Handle case ketika gagal generate puzzle
                print(f"❌ Gagal generate puzzle setelah {max_attempts} percobaan. Seed: {seed}")
                continue

            contoh_papan = [[num if num else 0 for num in row] for row in puzzle.board]  # Ubah jadi list biasa dengan 0 untuk sel kosong

            # Validasi puzzle: hanya diterima jika masih mungkin unik dan jumlah solusi tepat 1
            if not apakah_satu_solusi(contoh_papan):
                continue

            if hitung_solusi(contoh_papan) == 1:
                return contoh_papan, seed  # Puzzle valid dikembalikan

        except Exception as e:
            print(f"Error saat generate puzzle: {str(e)}")

        if seed_input is not None:
            break  # jika seed input manual, kita gak mau ulang-ulang (hanya 1 percobaan)

    print(f"❌ Gagal menemukan puzzle valid setelah {max_attempts} percobaan")
    return None, None  # Gagal menghasilkan puzzle valid


def tampilkan_papan(papan, pos_terakhir=None, papan_awal=None):
    '''
    Fungsi ini bertugas untuk menampilkan papan Sudoku ke terminal dengan format rapi.
    Jika terminal mendukung warna, akan ditampilkan dengan:
    - Warna merah untuk posisi sel yang terakhir diisi
    - Warna hijau untuk angka hasil isian solver
    - Warna putih untuk angka asli dari puzzle awal

    Fungsi ini juga menambahkan garis pemisah antar kotak 3x3 agar lebih mudah dibaca.
    '''

    for i, baris in enumerate(papan):  # Loop baris
        # Setiap 3 baris, tampilkan garis horizontal pembatas antar kotak
        if i % 3 == 0 and i != 0:
            print(Fore.WHITE + "-" * 21 + Style.RESET_ALL if apakah_support_warna() else "-" * 21)
        
        for j, angka in enumerate(baris):  # Loop kolom
            # Setiap 3 kolom, tampilkan garis vertikal pembatas antar kotak
            if j % 3 == 0 and j != 0:
                print(Fore.WHITE + "|" + Style.RESET_ALL if apakah_support_warna() else "|", end=" ")

            if not apakah_support_warna():
                # jika warna tidak disupport terminal, tampilkan angka biasa atau titik untuk kosong
                print(str(angka) if angka != 0 else '.', end=" ")
            else:
                # Tentukan warna berdasarkan kondisi posisi dan sumber angka
                if pos_terakhir and (i, j) == pos_terakhir:
                    color = Fore.RED  # Posisi terakhir yang dicoba solver
                elif papan_awal and papan_awal[i][j] == 0 and papan[i][j] != 0:
                    color = Fore.GREEN  # Angka hasil solver (bukan angka awal)
                else:
                    color = Fore.WHITE  # Angka asli dari puzzle
                print(color + (str(angka) if angka != 0 else '.') + Style.RESET_ALL, end=" ")
            
        print()  # Ganti baris setelah satu baris selesai ditampilkan

    
def animasi_cli(papan, pos_terakhir=None, delay=0.03, papan_awal=None, deskripsi_mode=None):
    '''
    Fungsi ini menampilkan animasi step-by-step di terminal saat solver berjalan.
    - Membersihkan layar setiap langkah
    - Menampilkan deskripsi mode solver (misal: Naive, MRV)
    - Menampilkan papan saat ini (dengan warna jika didukung)
    - Delay kecil antar langkah agar terlihat seperti animasi
    '''

    os.system('cls' if os.name == 'nt' else 'clear')  # Bersihkan layar (Windows: cls, Linux/macOS: clear)

    if deskripsi_mode:
        # Tampilkan deskripsi mode + garis pemisah
        print(
            deskripsi_mode + "\n" + 
            (Fore.WHITE + "-"*30 + Style.RESET_ALL + "\n" if apakah_support_warna() else "-"*30 + "\n")
        )

    tampilkan_papan(papan, pos_terakhir, papan_awal)  # Tampilkan state terkini papan
    time.sleep(delay)  # Kasih jeda animasi biar keliatan step-by-step


def landing_page():
    os.system('cls' if os.name == 'nt' else 'clear')  # clear terminal screen
    print("╔══════════════════════════════════════════════╗")
    print("║                                              ║")
    print("║     🧠 Sudoku Solver CLI with Animation      ║")
    print("║                                              ║") 
    print("║   📌 Dibuat oleh Kelompok 6 - DAA 2025       ║")
    print("║   🔍 Pilih level dan lihat cara solve-nya!   ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    print()
    time.sleep(0.2)  # biar ga langsung lompat ke menu


def main():
    '''
    Fungsi utama program CLI Sudoku Solver.
    Menampilkan landing page, meminta input level kesulitan, seed puzzle, serta mode algoritma yang diinginkan.
    Melakukan solving dengan animasi opsional, dan mencatat hasil solving ke file log.
    '''
    try:
        init(autoreset=True, strip=False) # Inisialisasi ANSI color di terminal
        if sys.platform == 'win32': os.system('color') # Fix warna di CMD Windows

        while True:
            landing_page() # Tampilkan fungsi landing_page()
        
            # Pilih tingkat kesulitan
            print("\n- Pilih level kesulitan Sudoku:")
            print("1. 🟢 Mudah")
            print("2. 🟠 Menengah")
            print("3. 🔴 Sulit")
            print("4. Kembali / Keluar")
            level_input = input("Masukan pilihan (1-4): ").strip() # input user

            if  level_input == '4':
                print("Keluar Program!.")
                sys.exit(0) # Keluar program jika user pilih opsi ke-4

            # Mapping level input ke tingkat kesulitan dan persentase angka kosong
            tingkat_kesulitan = {
                '1': ('mudah', 0.3),      # Mudah → 30% sel kosong
                '2': ('menengah', 0.4),   # Menengah → 40% sel kosong
                '3': ('sulit', 0.60)      # Sulit → 60% sel kosong
            }

            # Cek apakah input level valid (ada di dictionary tingkat_kesulitan)
            if level_input not in tingkat_kesulitan:
                print("❌ Level tidak dikenali. Coba lagi!.")
                continue  # Balik ke atas loop untuk minta input ulang

            # Ambil label level dan persentase angka kosong berdasarkan input user
            level, tingkat = tingkat_kesulitan[level_input]

            print("\n- Pilih Seed?")
            print("1. 🎲 Acak (Random)")
            print("2. ✍️ Input manual")
            pilih_seed = input("Pilihan (1/2): ").strip()  # Input seed

            # Input seed manual atau otomatis
            seed_user = None  # Default: None (berarti nanti pakai seed acak)

            # jika user pilih '2', berarti dia mau input seed manual
            if pilih_seed == '2':
                while True:
                    try:
                        # Ambil input seed dari user, hapus spasi di kiri-kanan, lalu ubah ke int
                        seed_user = int(input("- Masukkan seed (angka 0 - 99999): ").strip())
                        
                        # Validasi rentang seed
                        if 0 <= seed_user <= 99999:
                            break  # jika valid, keluar dari loop
                        else:
                            print("❌ Seed harus dalam rentang 0 - 99999.")
                    
                    except ValueError:
                        # jika input bukan angka, munculkan error
                        print("❌ Input harus berupa angka.")
                        
            # Generate puzzle valid dengan satu solusi
            while True:
                '''
                Bagian ini menghasilkan puzzle Sudoku yang valid dan hanya punya satu solusi.
                Jika gagal menemukan puzzle setelah 100 kali percobaan, user akan disuruh ulangi.
                Puzzle yang valid lalu ditampilkan ke layar sebagai papan awal.
                '''
                # Generate puzzle valid dengan tingkat kesulitan yang dipilih user, dan seed (acak atau manual)
                contoh_papan, seed = generate_valid_puzzle(tingkat, seed_user)

                # jika gagal generate puzzle (hasil None), ulangi proses
                if contoh_papan is None:
                    print("❌ Gagal menemukan puzzle dengan 1 solusi setelah 100 percobaan.")
                    continue

                # Hitung jumlah solusi dari puzzle yang berhasil dibuat (seharusnya selalu 1)
                solusi = hitung_solusi(contoh_papan)

                # Tampilkan info seed dan jumlah solusi
                print(f"\n🧬 Seed yang digunakan: ({seed}) dan memiliki {solusi} solusi.")

                # Salin papan awal untuk referensi saat animasi/visualisasi
                papan_awal = copy.deepcopy(contoh_papan)

                # Tampilkan puzzle Sudoku ke user di terminal
                print("\nPuzzle Sudoku:")
                tampilkan_papan(contoh_papan, papan_awal=papan_awal)

                # Pilih mode solving
                print("\n- Pilih mode algoritma:")
                print("1. 🔁 (Backtracking Naive)")
                print("2. 🔁 + 🧠 (Backtracking + MRV)")
                print("q. 🔙 Kembali ke pilihan level")
                mode = input("Masukkan mode (1/2/q): ").strip() # Input mode

                '''
                Bagian ini menangani input user untuk memilih mode algoritma yang akan digunakan:
                1. Backtracking biasa
                2. Backtracking dengan MRV heuristic

                jika input tidak valid, user diminta ulang. jika input 'q', kembali ke pemilihan level.
                '''
                # Jika user memilih keluar dari menu mode
                if mode == 'q':
                    break  # kembali ke pemilihan level/kesulitan

                # Validasi input mode (hanya boleh 1 atau 2)
                if mode not in ['1', '2']:
                    print("❌ Mode tidak valid. Coba lagi!.")
                    continue  # ulangi input mode

                # Deskripsi mode yang akan ditampilkan di CLI (pakai warna biar menarik)
                deskripsi_mode = {
                    '1': Fore.YELLOW + "\n🔁 Mode: Backtracking Biasa" + Style.RESET_ALL,
                    '2': Fore.CYAN + "\n🔁 + 🧠 Mode: BT + MRV" + Style.RESET_ALL
                }.get(mode, "")  # jika mode tidak dikenali, default ke string kosong


                '''
                Bagian ini mengatur apakah user ingin menampilkan animasi visual step-by-step saat solving.
                Setelah itu, solver dijalankan dan hasilnya (jumlah langkah, durasi, mode, seed) dicatat,
                baik ditampilkan ke layar maupun disimpan ke file log CSV jika sukses.
                '''

                # Tanya user apakah ingin mengaktifkan animasi saat solving
                jawab = input("Aktifkan animasi? (y/n): ").strip().lower()
                animasi = jawab == 'y'  # True kalau jawab 'y', False kalau tidak

                langkah = 0  # Inisialisasi penghitung langkah
                start = time.time()  # Catat waktu mulai

                # Jalankan solver animasi berdasarkan mode yang dipilih
                sukses, langkah, durasi = pecahkan_sudoku_anim(
                    contoh_papan,
                    delay=0.03 if animasi else 0,  # Delay animasi jika aktif
                    papan_awal=papan_awal,
                    deskripsi_mode=deskripsi_mode,
                    mode=mode
                )

                # Cek apakah solving berhasil
                if sukses:
                    durasi = time.time() - start  # Hitung durasi waktu solving
                    print(f"\n🧬 Seed yang digunakan: ({seed}) dan memiliki {solusi} solusi.")
                    
                    # Tampilkan emoji level kesulitan sesuai level
                    emoji_level = {'mudah': '🟢', 'menengah': '🟠', 'sulit': '🔴'}
                    
                    # Informasi keberhasilan solving
                    print("\n✅ Sudoku berhasil dipecahkan!")
                    print(f"{emoji_level.get(level, '')} Kesulitan Sudoku: {level.capitalize()}")
                    print(f"🧩 Total langkah: {langkah}") # Info Langkah
                    print(f"⏱️ Waktu: {durasi:.2f} detik") # Info Durasi
                    print(f"🎞️ Animasi aktif: {'Ya' if animasi else 'Tidak'}")  # Info animasi

                    # Logging hasil solving ke file CSV
                    log_file = "log_sudoku.csv"
                    file_exists = os.path.isfile(log_file)  # Cek apakah file log sudah ada

                    # Mapping nama mode dari input ke string yang lebih readable
                    mode_nama = {
                        '1': "Naive",
                        '2': "BT + MRV"
                    }.get(mode, "Unknown")  # fallback default kalau mode gak dikenal

                    # Tulis data log ke file
                    with open(log_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        if not file_exists:
                            # Tulis header jika file belum ada
                            writer.writerow(["Timestamp", "Level", "Mode", "Langkah", "Durasi", "Seed", "Animasi"])
                        writer.writerow([
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            level,
                            mode_nama,
                            langkah,
                            f"{durasi:.2f}",
                            seed,
                            "Ya" if animasi else "Tidak"
                        ])
                else:
                    # Kalau solving gagal
                    print("\n❌ Sudoku tidak bisa diselesaikan.")


                # Main lagi atau keluar
                lanjut = input("\nMain lagi? (y/n): ").strip().lower()  # Bersihkan input dan ubah ke lowercase
                if lanjut != 'y':
                    print("Terima Kasih sudah bermain!")  # Pesan penutup
                    sys.exit(0)  # Keluar dari program dengan kode normal

    # Tangkap error tak terduga selama eksekusi main loop
    except Exception as e:
        print(f"Terjadi error: {str(e)}")  # Tampilkan pesan error
        sys.exit(1)  # Keluar dengan kode error

# Entry point program: kalau file ini dijalankan langsung, panggil main()
if __name__ == '__main__':
    main()