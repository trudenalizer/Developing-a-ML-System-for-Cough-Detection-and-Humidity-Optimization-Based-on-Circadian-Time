Developing a ML System for Cough Detection and Humidity Optimization Based on Circadian Time

This project implements a real-time, Arduino-based system for nocturnal cough monitoring and humidity regulation. It uses machine learning to analyze environmental conditions and coughing events, with the aim of improving sleep quality by activating a humidifier only when needed.


Project Structure

    v2/
     ├──classifier_model.pkl       # Trained classifier for cough type
     ├── trained_model.pkl          # Regressor model for humidity estimation
     ├── sensor_data.csv            # Logged real-time sensor data
     ├── merged_mendeley_data.csv   # Historical dataset for training
     ├── gui_lastv2.py              # GUI interface for real-time predictions
     ├── serial_relay_main.py       # Arduino communication and actuator control
     ├── train_new_model.py         # Model training for humidity prediction
     ├── accuracy.py                # Evaluation of model performance



System Overview
 Hardware Components:

   Arduino Uno

   SL2591 or AS7341 (light sensor – used to detect night conditions)

   MAX4466 (microphone – used for cough detection)

   DHT22 (temperature & humidity sensor)

   5V Relay (controls humidifier)

 Machine Learning:

  A Random Forest Regressor predicts humidity needs based on temperature, time, and past humidity.

  A Classifier detects if the cough is likely related to dryness or illness.

  The system avoids false positives by checking ambient light before activation (only operates in dark).


  
How It Works

The system waits for ambient darkness.

It listens for cough-like sounds using the microphone.

  If a cough is detected, it queries ML models to:

   Estimate if humidity is suboptimal,

   Predict whether the cough is dryness-related or illness-related.

   If the cough is dryness-related and humidity is low, the humidifier is activated via relay.
Model Evaluation

   Performance is measured using R² Score and Mean Squared Error for the regressor.

   Rolling Predictive Error is also plotted to assess model stability over time.


Getting Started
 Prerequisites

   Python 3.9+

   Arduino IDE

   Required Python packages:
   
    pip install pandas matplotlib scikit-learn joblib


Running the Project

   Upload the Arduino sketch (not included here) that communicates over serial.

   Run serial_relay_main.py to start real-time monitoring.

   Use gui_lastv2.py for a basic GUI.

   To retrain the ML model: run train_new_model.py.


Authors

  Atay Yurt – real-time system design, data logging, integration

  Rabia Nur Bilgin – ML model development and training pipeline


License

This project is licensed under the MIT License.


Acknowledgements

Inspired by research on circadian rhythm impact on respiratory health and environmental control for nocturnal cough mitigation.
