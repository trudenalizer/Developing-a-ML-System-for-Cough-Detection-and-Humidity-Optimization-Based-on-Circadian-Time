import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

#File paths
REALTIME_DATA_PATH = r"C:\Users\Atay\Desktop\grad project\türkçe kodlar\sensor_data.csv"
MENDELEY_DATA_PATH = r"C:\Users\Atay\Desktop\grad project\türkçe kodlar\v2\merged_mendeley_data.csv"
MODEL_PATH = "trained_model.pkl"

#Read data from .csv file
try:
    df_real = pd.read_csv(REALTIME_DATA_PATH)
    df_mend = pd.read_csv(MENDELEY_DATA_PATH)
    print("Veriler başarıyla yüklendi.")
except FileNotFoundError as e:
    print(f"Dosya bulunamadı: {e.filename}")
    exit()

#Rename required data columns
df_real.rename(columns={'temperature': 'Temperature', 'humidity': 'Humidity', 'timestamp': 'Timestamp'}, inplace=True)
df_mend.rename(columns={'temperature': 'Temperature', 'humidity': 'Humidity'}, inplace=True)

#Create time column
if 'Timestamp' in df_real.columns:
    df_real['Saat'] = pd.to_datetime(df_real['Timestamp'], errors='coerce').dt.hour.fillna(0).astype(int)
else:
    df_real['Saat'] = datetime.now().hour

if 'Timestamp' in df_mend.columns:
    df_mend['Saat'] = pd.to_datetime(df_mend['Timestamp'], errors='coerce').dt.hour.fillna(0).astype(int)
else:
    df_mend['Saat'] = datetime.now().hour

#Check required columns
required_cols = ['Temperature', 'Humidity', 'Saat']
if not all(col in df_real.columns for col in required_cols) or not all(col in df_mend.columns for col in required_cols):
    print("Gerekli sütunlar eksik!")
    print("Gerçek zamanlı sütunlar:", df_real.columns.tolist())
    print("Mendeley sütunlar:", df_mend.columns.tolist())
    exit()

df = pd.concat([df_real[required_cols], df_mend[required_cols]], ignore_index=True)

#Input (X) and target (y)
X = df[['Temperature', 'Humidity', 'Saat']]
y = df['Humidity']

#Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create model and train
model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

#Test prediction and score
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Ortalama Kare Hata (MSE): {mse:.2f}")
print(f"R² Skoru: {r2:.2f}")

#Save model
joblib.dump(model, MODEL_PATH)
print(f"Regresyon modeli '{MODEL_PATH}' olarak kaydedildi.")
