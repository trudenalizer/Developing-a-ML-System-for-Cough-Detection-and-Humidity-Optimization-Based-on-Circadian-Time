# Model Eğitimi ve Kaydetme

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Veriyi yükle
try:
    df = pd.read_csv(r"C:\Users\Atay\Desktop\grad project\türkçe kodlar\v2\sentetik_nem_verisi.csv")
    print("Veri başarıyla yüklendi.")
except FileNotFoundError:
    print("Veri dosyası bulunamadı. Lütfen doğru yolu kontrol edin.")
    exit()

# Beklenen sütunları kontrol et
expected_columns = [
    'Sıcaklık (°C)', 'Başlangıç Nem (%)', 'Saat', 
    'Dış Nem (%)', 'Ses Seviyesi', 'Işık Seviyesi', 'Hedef Nem (%)'
]

if not all(col in df.columns for col in expected_columns):
    print("🚫 Veri kümesinde eksik sütun(lar) var!")
    print("Beklenen sütunlar:", expected_columns)
    print("Mevcut sütunlar:", df.columns.tolist())
    exit()

# Özellikleri ve hedef değişkeni belirle
X = df[['Sıcaklık (°C)', 'Başlangıç Nem (%)', 'Saat', 'Dış Nem (%)', 'Ses Seviyesi', 'Işık Seviyesi']]
y = df['Hedef Nem (%)']

# Eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur ve eğit
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Modelin performansını kontrol et
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("✅ Model eğitildi!")
print(f"📉 Mean Squared Error (MSE): {mse:.2f}")
print(f"📈 R^2 Score: {r2:.2f}")

# Modeli kaydet
joblib.dump(model, 'trained_model.pkl')
print("📦 Model 'trained_model.pkl' olarak kaydedildi.")
