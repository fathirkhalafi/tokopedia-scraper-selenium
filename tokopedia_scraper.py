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
    time.sleep(random.uniform(2, 4))
    
    # SCROLL ADAPTIF: terus scroll sampai halaman gak nambah tinggi lagi
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0
    max_scroll = 20  # batas aman biar gak infinite loop kalau ada kasus aneh
    
    while scroll_count < max_scroll:
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(random.uniform(1, 2))
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # udah gak ada tambahan konten baru, coba 1x lagi buat mastiin (jaga-jaga loading lambat)
            time.sleep(random.uniform(1.5, 2.5))
            new_height_recheck = driver.execute_script("return document.body.scrollHeight")
            if new_height_recheck == last_height:
                break  # beneran udah mentok, berhenti scroll
        
        last_height = new_height
        scroll_count += 1
    
    print(f"  Selesai scroll setelah {scroll_count} kali")
    
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
    
    time.sleep(random.uniform(3, 6))

driver.quit()

print(f"Total data terkumpul: {len(data_produk)}")

with open("hasil_produk.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=["halaman", "nama", "harga"], delimiter=";")
    writer.writeheader()
    for row in data_produk:
        writer.writerow(row)

print("Selesai! Data disimpan ke hasil_produk.csv")
