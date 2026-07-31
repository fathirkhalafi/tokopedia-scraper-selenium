from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import csv

options = Options()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(options=options)

data_produk = []

for nomor_halaman in range(1, 3):
    url = f"https://www.tokopedia.com/beautyhaulindo/page/{nomor_halaman}?perpage=40"
    
    print(f"Sedang scraping halaman {nomor_halaman}...")
    driver.get(url)
    time.sleep(random.uniform(2, 4))  # jeda acak setelah buka halaman
    
    # Scroll dengan jeda acak tiap kali
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(random.uniform(0.8, 1.8))  # jeda acak antar scroll
    
    harga_elements = driver.find_elements(By.XPATH, "//span[starts-with(text(), 'Rp')]")
    print(f"  Ketemu {len(harga_elements)} elemen harga di halaman ini")
    
    nama_sudah_diambil = set()
    
    for h in harga_elements:
        try:
            harga = h.text
            parent = h.find_element(By.XPATH, "./ancestor::div[3]")
            nama = parent.text.split("\n")[0]
            
            if nama in nama_sudah_diambil:
                continue
            
            nama_sudah_diambil.add(nama)
            data_produk.append({"halaman": nomor_halaman, "nama": nama, "harga": harga})
        except Exception:
            continue
    
    time.sleep(random.uniform(3, 6))  # jeda acak lebih lama sebelum pindah halaman

driver.quit()

print(f"Total data terkumpul: {len(data_produk)}")

with open("hasil_produk.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=["halaman", "nama", "harga"], delimiter=";")
    writer.writeheader()
    for row in data_produk:
        writer.writerow(row)

print("Selesai! Data disimpan ke beautyhaulindo_produk.csv")
