import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

#Load data
df = pd.read_csv("online_cough_verisi.csv")

#Cleanups
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=['respiratory_condition', 'Ses Seviyesi', 'SNR', 'cough_detected'])

#Convert required columns
df['Ses Seviyesi'] = df['Ses Seviyesi'].astype(float)
df['SNR'] = df['SNR'].replace({'yes': 1, 'no': 0}).astype(float)
df['cough_detected'] = df['cough_detected'].replace({'yes': 1, 'no': 0}).astype(int)
df['respiratory_condition'] = df['respiratory_condition'].replace({'yes': 1, 'no': 0}).astype(int)

#Split specification and target variables
X = df[['Ses Seviyesi', 'SNR', 'cough_detected']]
y = df['respiratory_condition']

#Final cleanup
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y.loc[X.index]

#Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create and train model
model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
model.fit(X_train, y_train)

#Report
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

#Save model
joblib.dump(model, 'classifier_model.pkl')
print("Model başarıyla kaydedildi: classifier_model.pkl")

df = pd.read_csv(r"C:\Users\Atay\Desktop\grad project\cough_dataset\online_cough_verisi.csv")

#Show sick vs. healty
print(df['respiratory_condition'].value_counts())
