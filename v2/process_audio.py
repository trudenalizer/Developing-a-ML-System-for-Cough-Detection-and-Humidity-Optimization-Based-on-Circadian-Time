import os
import pandas as pd
import numpy as np
from pydub import AudioSegment

#Find FFMPEG path
AudioSegment.converter = r"C:\Users\Atay\Desktop\grad project\v2\ffmpeg.exe"

#File paths
DATA_FOLDER = r"C:\Users\Atay\Desktop\grad project\cough_dataset"
CSV_FILE = r"C:\Users\Atay\Desktop\grad project\cough_dataset\metadata_compiled.csv"

#Read .csv file
df = pd.read_csv(os.path.join(DATA_FOLDER, CSV_FILE))
print("Veri başarıyla yüklendi.")

#List existing files
existing_files = set(os.listdir(DATA_FOLDER))

#Function for calculating voice level
def get_loudness(filepath):
    try:
        audio = AudioSegment.from_file(filepath)
        return audio.dBFS
    except Exception as e:
        print(f"{filepath} okunamadı: {e}")
        return -100.0  #Muteness

#Only work with valid sound files
valid_rows = []
volumes = []

for idx, row in df.iterrows():
    uuid = row['uuid']
    filename = uuid + ".ogg"
    file_path = os.path.join(DATA_FOLDER, filename)

    if filename in existing_files:
        loudness = get_loudness(file_path)
        valid_rows.append(row)
        volumes.append(loudness)
    else:
        print(f"Eksik dosya atlandı: {filename}")

#Create a new dataframe
filtered_df = pd.DataFrame(valid_rows)
filtered_df['Ses Seviyesi'] = volumes
filtered_df['Işık Seviyesi'] = 0

#Save
output_path = os.path.join(DATA_FOLDER, "online_cough_verisi.csv")
filtered_df.to_csv(output_path, index=False)
print(f"\nTüm işlem tamamlandı. Yeni dosya: {output_path}")
print(f"İşlenen kayıt sayısı: {len(filtered_df)}")
