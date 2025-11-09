from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import glob 

# Se leen los datos desde el csv
path = "./data/"

files = glob.glob(path + "*.csv")
dataframes = [pd.read_csv(f) for f in files]

# Se juntan los datos en un arreglo
data = pd.concat(dataframes, ignore_index=True)

x = data.drop(columns=["gesture"])
y = data["gesture"]

# Se codifica textos a números
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Se entrena modelo
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=300, max_depth=20, min_samples_split=4, min_samples_leaf=2, random_state=42)
model.fit(x_train, y_train)

# Se prueba modelo
y_pred = model.predict(x_test)
print("Precisión:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

# Exportar modelo
import os
import joblib

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/hand_gesture_model.pkl")
joblib.dump(encoder, "model/gesture_encoder.pkl")