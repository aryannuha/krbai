import cv2 as cv
import numpy as np
from PIL import Image

def nothing(x):
  pass

# cap = cv.VideoCapture(r"C:\Users\fredy\Downloads\jarak\jarak2.mp4")

cap = cv.VideoCapture(0)

while True:
  lab = {
    "x": [],
    "color": []
  }

  ret, frame = cap.read()
  if not ret:
    break  # Break the loop if no frame is read

  # Calculate the new height and width (50% of original)
  new_height = int(frame.shape[0] * 0.5)
  new_width = int(frame.shape[1] * 0.5)

  # Resize the frame
  resized_frame = cv.resize(frame, (new_width, new_height))

  hsv = cv.cvtColor(resized_frame, cv.COLOR_BGR2HSV)

  lower_bound = np.array([0, 100, 100])
  # upper_bound = np.array([30, 255, 255])
  upper_bound = np.array([255, 255, 255])

  # Create mask and result
  mask = cv.inRange(hsv, lower_bound, upper_bound)
  res = cv.bitwise_and(resized_frame, resized_frame, mask=mask)

  # Convert mask to LAB space
  mask_lab = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
  mask_lab_pil = Image.fromarray(mask_lab)
  mask_lab_pil = mask_lab_pil.convert("LAB")

  #######################
  tinggi_tengah = resized_frame.shape[0] // 2
  for x in range(resized_frame.shape[1]):
    lab_value = mask_lab_pil.getpixel((x, tinggi_tengah))

    L = lab_value[0]

    # Append the values to the dictionary
    lab["x"].append(x)
    if L == 0:
      lab["color"].append(0)
    else: 
      lab["color"].append(1)

  # Display combined image with trackbars
  combined = np.hstack((resized_frame, mask_lab, res))
  cv.imshow('Tracking', combined)

  key = cv.waitKey(1)
  if key == 27:
    break
  b = []
  for i in range(len(lab["color"])-1):
    if lab["color"][i] != lab["color"][i+1]:
      b.append(i)

  if len(b) == 4:
    # print(b)
    # print(b[2]-b[1])
    jarak = cv.line(res, (b[1], tinggi_tengah), (b[2], tinggi_tengah), (0, 0, 255), 10)
    jarak = cv.circle(jarak, ((b[1]+b[2])//2, tinggi_tengah), 10, (255, 255, 255), thickness=-1)
    if (b[1]+b[2])//2 < jarak.shape[1]//2 and abs((b[1]+b[2])//2 - jarak.shape[1]//2) > 10:
      print("kiri")
    elif (b[1]+b[2])//2 > jarak.shape[1]//2 and abs((b[1]+b[2])//2 - jarak.shape[1]//2) > 10:
      print("kanan")
    else:
      print("maju")
    cv.imshow("jarak", jarak)
  # time.sleep(0.5)

cv.destroyAllWindows()
