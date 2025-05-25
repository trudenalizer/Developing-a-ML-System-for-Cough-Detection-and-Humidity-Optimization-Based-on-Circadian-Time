import joblib

model = joblib.load("trained_model.pkl")
classifier = joblib.load("classifier_model.pkl")

print("trained_model.pkl feature names:", model.feature_names_in_)
print("classifier_model.pkl feature names:", classifier.feature_names_in_)
