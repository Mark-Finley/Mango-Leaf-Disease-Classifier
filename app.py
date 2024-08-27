import os
import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("mango_leaf_disease_model.h5")

# Define class labels
class_labels = {
    0: "Anthracnose",
    1: "Bacterial Canker",
    2: "Cutting Weevil",
    3: "Die Back",
    4: "Gall Midge",
    5: "Healthy",
    6: "Powdery Mildew",
    7: "Sooty Mould"
}

# Define recommendations for each disease
disease_recommendations = {
    "Anthracnose": "Apply fungicides containing copper hydroxide or mancozeb. Prune affected areas and remove infected leaves and fruits.",
    "Bacterial Canker": "Prune affected areas using sterilized equipment. Apply copper-based fungicides. Avoid overhead irrigation.",
    "Cutting Weevil": "Prune and remove infested twigs. Apply insecticides containing imidacloprid or thiamethoxam.",
    "Die Back": "Prune affected areas. Ensure proper drainage and avoid over-watering. Apply fungicides if necessary.",
    "Gall Midge": "Remove and destroy infested leaves and shoots. Apply neem oil or insecticidal soap. Avoid overhead irrigation.",
    "Healthy": "No action needed. Continue regular monitoring of the orchard.",
    "Powdery Mildew": "Apply fungicides containing sulfur or potassium bicarbonate. Prune affected areas and improve air circulation.",
    "Sooty Mould": "Remove and destroy affected leaves. Control the insect pests responsible for honeydew secretion."
}

# Function to preprocess and classify an image
def classify_image(img):
    try:
        # Resize and preprocess the image
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # Make predictions
        predictions = model.predict(img)

        # Get the predicted class and corresponding label
        predicted_class_idx = np.argmax(predictions)
        predicted_class = class_labels[predicted_class_idx]

        return predicted_class, predictions[0]
    except Exception as e:
        return None, None

def main():
    st.title('Mango Leaf Disease Classifier')
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Classify the uploaded image
        predicted_class, prediction_probabilities = classify_image(image)
        
        # Display the result
        if predicted_class is not None:
            st.write('Diseased Mango Leaf with Class:', predicted_class)
            
            # Provide recommendations
            if predicted_class != 'Healthy':
                st.subheader("Recommendations:")
                # Split recommendations into a list
                recommendations_list = disease_recommendations[predicted_class].split('. ')
                # Display recommendations as a numbered list
                for i, recommendation in enumerate(recommendations_list):
                    st.write(f"{i+1}. {recommendation}")
        else:
            st.write("Cannot classify the image. Please make sure the uploaded image is a valid image of a mango leaf.")

if __name__ == '__main__':
    main()
