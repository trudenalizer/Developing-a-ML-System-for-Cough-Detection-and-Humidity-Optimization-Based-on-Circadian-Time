import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

#File paths
DATA_PATH = "sensor_data.csv"
MODEL_PATH = "trained_model.pkl"

#Read data from .csv file
try:
    df = pd.read_csv(DATA_PATH)
    print("Veri başarıyla yüklendi.")
except FileNotFoundError:
    print(f"Dosya bulunamadı: {DATA_PATH}")
    exit()

#Required data columns
required_cols = ['temperature', 'humidity']
if not all(col in df.columns for col in required_cols):
    print("Gerekli sütun(lar) eksik!")
    print("Beklenen:", required_cols)
    print("Mevcut:", df.columns.tolist())
    exit()

#Create time column
if 'timestamp' in df.columns:
    df['Saat'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.hour.fillna(0).astype(int)
else:
    df['Saat'] = datetime.now().hour  #

#Input (X) and target (y)
X = df[['temperature', 'humidity', 'Saat']]
y = df['humidity']  #

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
