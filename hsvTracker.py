import cv2
import numpy as np

# Fungsi untuk tidak melakukan apa-apa
def nothing(x):
    pass

# Inisialisasi video capture
cap = cv2.VideoCapture(1)

# Membuat window untuk menampilkan video
cv2.namedWindow('Tracking')

# Membuat trackbar untuk mengatur nilai H, S, dan V
cv2.createTrackbar('LH', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('LS', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('LV', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('UH', 'Tracking', 255, 255, nothing)
cv2.createTrackbar('US', 'Tracking', 255, 255, nothing)
cv2.createTrackbar('UV', 'Tracking', 255, 255, nothing)

while True:
    # Membaca frame demi frame
    ret, frame = cap.read()

    if not ret:
        break

    # Mengubah warna BGR ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mendapatkan nilai trackbar
    l_h = cv2.getTrackbarPos('LH', 'Tracking')
    l_s = cv2.getTrackbarPos('LS', 'Tracking')
    l_v = cv2.getTrackbarPos('LV', 'Tracking')
    u_h = cv2.getTrackbarPos('UH', 'Tracking')
    u_s = cv2.getTrackbarPos('US', 'Tracking')
    u_v = cv2.getTrackbarPos('UV', 'Tracking')

    # Menentukan batas-batas warna HSV berdasarkan nilai trackbar
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    # Membuat mask berdasarkan batas-batas warna HSV
    mask = cv2.inRange(hsv, lower, upper)

    # Mengaplikasikan mask pada frame asli
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Menampilkan hasil pelacakan
    cv2.imshow('Tracking', res)

    # Menghentikan proses dengan menekan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Menutup video capture dan window OpenCV
cap.release()
cv2.destroyAllWindows()
