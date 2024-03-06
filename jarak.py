import cv2
import numpy as np
from PIL import Image
import time

# baca gambar
cap = cv2.VideoCapture(0)

# mengubah spesifik ukuran
# lebar
cap.set(3, 640)
# tinggi
cap.set(4, 480)
# kecerahan
# cap.set(10, 100)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 1)

# Variabel untuk menghitung FPS
fps_start_time = time.time()
fps_frame_counter = 0
fps = 0

# # video adalah sekumpulan gambar, sehingga dibutuhkan perulangan
while True:    
    # mengcapture image
    success, img = cap.read()
    
    # menentukan hsv minimum
    r_lower = np.array([136, 87, 111]) # lower red
    o_lower = np.array([8,100,100]) # lower orange
    g_lower = np.array([25, 52, 72]) # lower green

    # menentukan hsv maksimum
    r_upper = np.array([179, 255, 255]) # higher red
    o_upper = np.array([18,255,255]) # higher orange
    g_upper = np.array([102,255,255]) # higher green
    
    # ubah bgr menjadi hsv
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
    # masking
    r_mask = cv2.inRange(imgHSV,r_lower,r_upper) # red
    o_mask = cv2.inRange(imgHSV,o_lower,o_upper) # orange
    g_mask = cv2.inRange(imgHSV,g_lower,g_upper) # green
        
    # Penghalusan gambar dengan operasi morfologi
    kernel = np.ones((5, 5), np.uint8)
    r_mask = cv2.erode(r_mask, kernel, iterations=1) 
    r_mask = cv2.dilate(r_mask, kernel, iterations=1)   
    o_mask = cv2.erode(o_mask, kernel, iterations=1)
    o_mask = cv2.dilate(o_mask, kernel, iterations=1)
    g_mask = cv2.erode(g_mask, kernel, iterations=1)
    g_mask = cv2.dilate(g_mask, kernel, iterations=1)
    
    # Temukan kontur pada gambar hasil masking
    contours_r, _ = cv2.findContours(r_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_o, _ = cv2.findContours(o_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_g, _ = cv2.findContours(g_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # menyatukan dua gambar
    # imgResult = cv2.bitwise_and(img, img, mask=mask)

    # Jika ditemukan setidaknya satu kontur untuk warna merah
    for contour in contours_r:
        # hitung luas contour
        area = cv2.contourArea(contour)
        
         # Gambar persegi panjang berwarna merah jika luas kontur cukup besar
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)

            # Hitung momen spasial untuk mendapatkan centroid
            M = cv2.moments(contour)
            
            # Koordinat x dan y dari centroid
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0  # Atur ke nilai default jika momen spasial bernilai nol
            
            # Gambar titik centroid pada gambar hasil
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1) 

            # tulisan merah pada persegi panjang
            cv2.putText(img, "Merah", (x + w + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            
    # Jika ditemukan setidaknya satu kontur untuk warna orange
    for contour in contours_o:
        # hitung luas contour
        area = cv2.contourArea(contour)
        
         # Gambar persegi panjang berwarna merah jika luas kontur cukup besar
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)

            # Hitung momen spasial untuk mendapatkan centroid
            M = cv2.moments(contour)
            
            # Koordinat x dan y dari centroid
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0  # Atur ke nilai default jika momen spasial bernilai nol
            
            # Gambar titik centroid pada gambar hasil
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1) 

            # tulisan merah pada persegi panjang
            cv2.putText(img, "Orange", (x + w + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 69, 255), 2, cv2.LINE_AA)        
    
    # Jika ditemukan setidaknya satu kontur untuk warna hijau
    for contour in contours_g:
        # hitung luas contour
        area = cv2.contourArea(contour)
        
         # Gambar persegi panjang berwarna merah jika luas kontur cukup besar
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)

            # Hitung momen spasial untuk mendapatkan centroid
            M = cv2.moments(contour)
            
            # Koordinat x dan y dari centroid
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0  # Atur ke nilai default jika momen spasial bernilai nol
            
            # Gambar titik centroid pada gambar hasil
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1) 

            # tulisan merah pada persegi panjang
            cv2.putText(img, "Hijau", (x + w + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 127), 2, cv2.LINE_AA)
        
    # Increment frame counter untuk menghitung FPS
    fps_frame_counter += 1
            
    # Cek waktu setiap detik untuk menghitung FPS
    if time.time() - fps_start_time >= 1:
        fps = fps_frame_counter
        fps_frame_counter = 0
        fps_start_time = time.time()
            
    # Menampilkan FPS di layar
    cv2.putText(img, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    # menampilkan gambar atau video
    # cv2.imshow("window", imgResult)
    
    # menampilkan gambar atau video
    cv2.imshow("img", img)
        
    # pencet q untuk berhenti dari loop
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
cap.release
cv2.destroyAllWindows()