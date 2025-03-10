import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import time
import gdown
import os

file_id= "1VG0LJEeiJt1OR9H6mEhfwXjyLZ47JBnn"
url = 'https://drive.google.com/file/d/1VG0LJEeiJt1OR9H6mEhfwXjyLZ47JBnn/view?usp=drive_link'
model_path="trained_plant_disease_model.keras"   

if not os.path.exists(model_path):
    st.warning("Downloading model from Google Drive...")
    gdown.download(url, model_path,quiet=False)
    

# Load the trained model
@st.cache_resource()
def load_model(): 
    return tf.keras.models.load_model(model_path)

model = load_model()

# Class labels based on training
CLASS_NAMES = ['Healthy', 'Early Blight', 'Late Blight']

# Define Prediction Function
def predict(image):
    try:
        # Convert image to RGB (handle cases where it has an alpha channel)
        image = image.convert("RGB")

        # Convert image to NumPy array
        img_array = np.array(image)

        # Resize image to model input size (128x128)
        img_resized = cv2.resize(img_array, (128, 128))

        # Expand dimensions to match model input shape
        img_expanded = np.expand_dims(img_resized, axis=0)

        # Debugging: Show image shape before prediction
        st.write(f"🖼 Image shape before prediction: {img_expanded.shape}")

        # Predict using model
        predictions = model.predict(img_expanded)

        # Get the highest probability class
        predicted_class_index = np.argmax(predictions)
        predicted_class = CLASS_NAMES[predicted_class_index]
        confidence = predictions[0][predicted_class_index] * 100

        # Debugging Outputs
        st.write("🔍 Model Raw Output (Softmax Probabilities):", predictions)
        st.write(f"📌 Predicted Class: {predicted_class}")
        st.write(f"🎯 Confidence Score: {confidence:.2f}%")

        return f"{predicted_class} ({confidence:.2f}% Confidence)", confidence

    except Exception as e:
        st.error(f"Error in prediction: {e}")
        return "Error", 0

# Upload Image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "png", "jpeg"])

# Camera Option
st.write("📸 Or capture a live image:")
camera_img = st.camera_input("Take a Photo")

# Select image source
image_source = None
if uploaded_file is not None:
    image_source = Image.open(uploaded_file)
elif camera_img is not None:
    image_source = Image.open(camera_img)

# Display Image & Predict
if image_source is not None:
    st.image(image_source, caption="📌 Uploaded Image", use_column_width=True)

    if st.button("🔍 Predict Disease 🩺"):
        with st.spinner("Analyzing the image... ⏳"):
            time.sleep(2)  # Simulate processing time
            result, confidence = predict(image_source)

            # Display Prediction
            st.success(f"✅ Prediction: {result}")
