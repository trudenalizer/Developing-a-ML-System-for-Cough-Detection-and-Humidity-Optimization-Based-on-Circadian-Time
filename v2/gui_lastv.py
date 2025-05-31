import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import serial

# ---------- Arduino Ayarları ----------
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# ---------- Model Eğitme Butonu ----------
def modeli_egit():
    log_alani.insert(tk.END, "🔄 Model eğitimi başlatılıyor...\n")
    log_alani.see(tk.END)

    def egitim_islemi():
        try:
            process = subprocess.Popen(["python","new_train_modelv2.py"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       text=True)
            for line in process.stdout:
                log_alani.insert(tk.END, line)
                log_alani.see(tk.END)
            process.wait()
            messagebox.showinfo("Eğitim Tamamlandı", "✅ Model başarıyla eğitildi!")
        except Exception as e:
            log_alani.insert(tk.END, f"🚫 Hata: {e}\n")
            messagebox.showerror("Hata", f"Model eğitilirken bir sorun oluştu:\n{e}")

    threading.Thread(target=egitim_islemi).start()

# ---------- Canlı İzleme Penceresi ----------
def canli_izleme_penceresi():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

        pencere = tk.Toplevel()
        pencere.title("Gerçek Zamanlı İzleme")
        pencere.geometry("800x500")

        temperature_data = []
        humidity_data = []
        time_data = []

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

                        temperature_data[:] = temperature_data[-50:]
                        humidity_data[:] = humidity_data[-50:]
                        time_data[:] = time_data[-50:]

                        line_temp.set_data(range(len(temperature_data)), temperature_data)
                        line_hum.set_data(range(len(humidity_data)), humidity_data)
                        ax.set_xlim(0, len(temperature_data))
                        ax.set_xticks(range(len(time_data)))
                        ax.set_xticklabels(time_data, rotation=45, fontsize=8)
            except Exception as e:
                print(f"Grafik hata: {e}")

        ani = animation.FuncAnimation(fig, veri_guncelle, interval=1000)
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Arduino Hatası", f"Arduino bağlantısı kurulamadı:\n{e}")

# ---------- Ana GUI ----------
ana_pencere = tk.Tk()
ana_pencere.title("Nemlendirici Proje Paneli 🌫️")
ana_pencere.geometry("700x500")

etiket = tk.Label(ana_pencere, text="Model Eğitme ve İzleme Paneli", font=("Arial", 14, "bold"))
etiket.pack(pady=10)

log_alani = scrolledtext.ScrolledText(ana_pencere, width=80, height=20, wrap=tk.WORD)
log_alani.pack(padx=10, pady=10)

buton_egit = tk.Button(ana_pencere, text="Modeli Eğit ✨", command=modeli_egit, bg="#4caf50", fg="white", font=("Arial", 12, "bold"))
buton_egit.pack(pady=5)

buton_izle = tk.Button(ana_pencere, text="Canlı İzle 🔴", command=canli_izleme_penceresi, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
buton_izle.pack(pady=5)

ana_pencere.mainloop()
