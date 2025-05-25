import serial
import time
import sqlite3
import joblib
import pandas as pd
from datetime import datetime

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

#Database and model path
DB_PATH = 'humidity_data.db'
MODEL_PATH = 'trained_model.pkl'
CLASSIFIER_MODEL_PATH = 'classifier_model.pkl'

#Ideal humidity sections
IDEAL_HUMIDITY_MIN = 40.0
IDEAL_HUMIDITY_MAX = 60.0

#Create database
def create_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                temperature REAL,
                humidity REAL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database is created or already avaible.")
    except sqlite3.Error as e:
        print(f"Database creation error: {e}")

#Save data to database
def insert_data(Temperature, Humidity):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO sensor_data (timestamp, Temperature, Humidity)
            VALUES (?, ?, ?)
        ''', (timestamp, Temperature, Humidity))
        conn.commit()
        conn.close()
        print(f"Recorded data: {timestamp}, Temperature: {Temperature} °C, Humidity: {Humidity} %")
    except sqlite3.Error as e:
        print(f"Data record error: {e}")

#Load model
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Model load error: {e}")
        return None

#Load classifier model
def load_classifier():
    try:
        return joblib.load(CLASSIFIER_MODEL_PATH)
    except Exception as e:
        print(f"Classifier model load error: {e}")
        return None

#Send data to Arduino
def send_to_arduino(action):
    try:
        ser.write(action.encode())
        print(f"Data sent to Arduino: {action}")
    except serial.SerialException as e:
        print(f"Arduino data delivery error: {e}")


create_database()

#Arduino connection and dataflow
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Arduino is connected. Waiting for data")

    model = load_model()
    classifier = load_classifier()

    if model is None or classifier is None:
        raise Exception("Unable to load models.")

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip().replace('\x00', '')
        if not line:
            continue  
        parts = line.split(',')

        if len(parts) != 5:
            print(f"Unexpected data format: {line}")
            continue

        try:
            Temperature, Humidity, snr, ses, cough = map(float, parts)
            print(f"Data recieved -> Tempature: {Temperature}, Humidity: {Humidity}, SNR: {snr}, Sound: {ses}, Detected cough: {cough}")
        except ValueError as ve:
            print(f"Data transform error at: {parts}, error: {ve}")
            continue

        insert_data(Temperature, Humidity)

        #Humidity guess
        X_new = pd.DataFrame([[Temperature, Humidity, datetime.now().hour]],
                             columns=['Temperature', 'Humidity', 'Saat'])
        predicted_Humidity = model.predict(X_new)[0]
        print(f"Predicted humidity: {predicted_Humidity:.2f}%")

        #Sickness guess
        X_class = pd.DataFrame([[ses, snr, int(cough)]],
                               columns=['Ses Seviyesi', 'SNR', 'cough_detected'])
        disease_prediction = classifier.predict(X_class)[0]
        print(f"Sickness prediction: {'Sick' if disease_prediction == 1 else 'Healthy'}")

        #Determination system
        if int(cough) == 1:
            print("Cough detected.")
            if disease_prediction == 1:
                print("Sickness releated cough detected, humidifier inactive.")
                send_to_arduino("0")
            else:
                print("Dry cough detected. Checking humidity...")
                if predicted_Humidity < IDEAL_HUMIDITY_MIN:
                    print("Low humidity. Humidifier activated.")
                    send_to_arduino("1")
                elif predicted_Humidity > IDEAL_HUMIDITY_MAX:
                    print("High humidity Humidifier deactivated.")
                    send_to_arduino("0")
                else:
                    print("Ideal humidity detected. Humidifier remains inactive.")
                    send_to_arduino("0")
        else:
            print("No coughs detected. Checking humidity...")
            if predicted_Humidity < IDEAL_HUMIDITY_MIN:
                print("Low humidity. Humidifier activated.")
                send_to_arduino("1")
            elif predicted_Humidity > IDEAL_HUMIDITY_MAX:
                print("High humidity. Humidifier deactivated.")
                send_to_arduino("0")
            else:
                print("Ideal humidity detected. Humidifier remains inactive.")
                send_to_arduino("0")

except serial.SerialException as e:
    print(f"Serial port error: {e}")
except KeyboardInterrupt:
    print("Program is shutting down.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
