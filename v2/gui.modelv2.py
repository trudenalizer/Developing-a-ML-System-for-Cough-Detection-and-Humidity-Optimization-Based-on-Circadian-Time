import tkinter as tk
from tkinter import ttk
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import time
import datetime

# Arduino port ve baud rate
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# Veri listeleri
temperature_data = []
humidity_data = []
time_data = []

# Arduino bağlantısı
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Tkinter arayüz
pencere = tk.Tk()
pencere.title("Gerçek Zamanlı Sıcaklık ve Nem İzleyici")
pencere.geometry("800x500")

# Matplotlib figürü
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=pencere)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

line_temp, = ax.plot([], [], label="Sıcaklık (°C)", color='red')
line_hum, = ax.plot([], [], label="Nem (%)", color='blue')
ax.legend()
ax.set_title("Gerçek Zamanlı Sıcaklık ve Nem")
ax.set_xlabel("Zaman")
ax.set_ylabel("Değer")
ax.set_ylim(0, 100)

def veri_guncelle(i):
    try:
        raw = ser.readline().decode().strip()
        if raw:
            parts = raw.split(",")
            if len(parts) >= 2:
                temp = float(parts[0])
                hum = float(parts[1])
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')

                temperature_data.append(temp)
                humidity_data.append(hum)
                time_data.append(timestamp)

                # Maksimum 50 veri göster
                temperature_data[:] = temperature_data[-50:]
                humidity_data[:] = humidity_data[-50:]
                time_data[:] = time_data[-50:]

                line_temp.set_data(range(len(temperature_data)), temperature_data)
                line_hum.set_data(range(len(humidity_data)), humidity_data)
                ax.set_xlim(0, len(temperature_data))
                ax.set_xticks(range(len(time_data)))
                ax.set_xticklabels(time_data, rotation=45, fontsize=8)

    except Exception as e:
        print(f"Hata: {e}")

# Grafik güncelleme döngüsü
ani = animation.FuncAnimation(fig, veri_guncelle, interval=1000)
canvas.draw()

pencere.mainloop()
