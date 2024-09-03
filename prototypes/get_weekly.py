import pyautogui as pg
import time
import keyboard
import utils.helper as hp

def get_posisi_awal():
  # dapatkan posisi awal
  print("Tentukan posisi awal, jika sudah tekan 'g'")
  keyboard.wait('g')
  x, y = pg.position()
  patokan = (x, y)
  print(f"patokan: {patokan}")
  return patokan

def get_region_harga():
  # menentukan region untuk mengambil data harga
  print("Taruh kursor ke sudut kiri atas area harga, jika sudah tekan 's'")
  keyboard.wait('s')
  left_top = pg.position()
  print(f"left_top: {left_top}")
  time.sleep(0.5)

  print("Taruh kursor ke sudut kanan bawah area harga, jika sudah tekan 's'")
  keyboard.wait('s')
  right_bottom = pg.position()
  print(f"right_bottom: {right_bottom}")
  time.sleep(0.5)

  width = right_bottom[0] - left_top[0]
  height = right_bottom[1] - left_top[1]

  price_region = (left_top[0], left_top[1], width, height)
  print(f"price_region: {price_region}")
  return price_region

def get_region_weekly():
  # menentukan region untuk mengambil data tanggal
  print("Taruh kursor ke sudut kiri atas area weekly, jika sudah tekan 's'")
  keyboard.wait('s')
  left_top = pg.position()
  print(f"left_top: {left_top}")
  time.sleep(0.5)

  print("Taruh kursor ke sudut kanan bawah area weekly, jika sudah tekan 's'")
  keyboard.wait('s')
  right_bottom = pg.position()
  print(f"right_bottom: {right_bottom}")
  time.sleep(0.5)

  width = right_bottom[0] - left_top[0]
  height = right_bottom[1] - left_top[1]

  weekly_region = (left_top[0], left_top[1], width, height)
  print(f"weekly_region: {weekly_region}")

if __name__ == "__main__":
  get_posisi_awal()
  get_region_harga()
  get_region_weekly()