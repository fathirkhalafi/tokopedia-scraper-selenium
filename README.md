# Tokopedia Product Scraper (Selenium)

Script Python untuk mengambil data produk dari toko Tokopedia secara otomatis, dengan penanganan tantangan teknis nyata yang umum ditemui saat scraping platform e-commerce besar.

## Fungsi
- Mengambil nama produk dan harga dari halaman toko Tokopedia
- Mendukung multi-halaman (pagination)
- Menangani lazy-loading (produk yang baru muncul setelah di-scroll)
- Mencegah data duplikat dari produk yang menampilkan harga diskon & harga asli
- Menyimpan hasil ke CSV yang siap dibuka di Excel/Google Sheets

## Tech Stack
- Python 3
- `Selenium` — mengambil data dari halaman yang di-render dengan JavaScript
- `csv` — menyimpan hasil dalam format tabel

## Tantangan Teknis yang Diatasi

**1. Class HTML yang di-obfuscate**
Tokopedia menggunakan class CSS yang berubah-ubah (auto-generated), sehingga tidak bisa diandalkan sebagai selector. Solusinya menggunakan XPath berbasis pola teks (misalnya elemen yang diawali "Rp") untuk menemukan data yang konsisten meski struktur class berubah.

**2. Lazy loading**
Produk tidak langsung muncul semua di HTML awal, melainkan dimuat bertahap saat halaman di-scroll. Script ini melakukan scroll otomatis sebelum mengambil data, memastikan seluruh produk sempat termuat.

**3. Data duplikat dari harga diskon**
Produk yang sedang diskon menampilkan dua harga (asli & setelah diskon), yang menyebabkan data terekam dua kali. Ditangani dengan mekanisme deduplikasi berbasis nama produk.

**4. Perilaku scraping yang lebih natural**
Menggunakan jeda waktu acak (bukan tetap) antar request dan scroll, untuk menghindari pola yang terlalu teratur.

## Cara Pakai
1. Install dependency:
   ```bash
   pip install selenium
   ```
2. Sesuaikan URL toko target di dalam script
3. Jalankan script:
   ```bash
   python tokopedia_scraper.py
   ```
4. Hasil akan tersimpan otomatis sebagai `hasil_produk.csv`

## Contoh Output

| halaman | nama                                    | harga    |
|---------|------------------------------------------|----------|
| 1       | ROSE ALL DAY Forever Dew Lip Tint        | Rp99.000 |
| 1       | ESQA Velvet Charm Powder Blush           | Rp125.000|

<img width="1514" height="904" alt="Tangkapan Layar 2026-07-31 pukul 11 10 24" src="https://github.com/user-attachments/assets/adc90e91-6e40-48db-a21f-84ff6612ce4b" />


## Catatan
Script ini dibuat untuk keperluan pembelajaran dan riset harga (contoh: riset harga reseller), serta mengikuti batasan yang tercantum di robots.txt situs target — hanya mengakses halaman toko/produk publik, bukan melalui fitur pencarian internal yang dibatasi.
