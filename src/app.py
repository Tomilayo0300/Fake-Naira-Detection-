from pathlib import Path

import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

# -----------------------------
# Load model
# -----------------------------
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent.parent / "models" / "naira_fake_vs_genuine_model.h5"
    return tf.keras.models.load_model(model_path)

model = load_model()

# -----------------------------
# Preprocess
# -----------------------------
def preprocess(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (224, 224))
    frame = frame / 255.0
    return np.expand_dims(frame, axis=0)

# -----------------------------
# Predict
# -----------------------------
def predict(frame):
    processed = preprocess(frame)
    prob = model.predict(processed)[0][0]

    label = "🟢 Genuine" if prob > 0.5 else "🔴 Fake"
    confidence = prob if prob > 0.5 else 1 - prob

    return label, confidence

# -----------------------------
# UI
# -----------------------------
st.title("💵 Naira Currency Detector")

st.sidebar.header("Settings")

camera_url = st.sidebar.text_input(
    "Camera URL",
    "http://192.168.1.5:8080/video"
)

run = st.sidebar.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

# -----------------------------
# Live camera
# -----------------------------
if run:
    cap = cv2.VideoCapture(camera_url)

    while True:
        ret, frame = cap.read()

        if not ret:
            st.error("Camera not accessible")
            break

        label, confidence = predict(frame)

        text = f"{label} ({confidence:.2f})"

        cv2.putText(frame, text, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        FRAME_WINDOW.image(frame)

    cap.release()

# -----------------------------
# Upload option
# -----------------------------
st.subheader("Upload Image")

file = st.file_uploader("Upload banknote")

if file:
    img = Image.open(file)
    st.image(img)

    frame = np.array(img)
    label, confidence = predict(frame)

    st.success(f"{label} ({confidence:.2f})")


