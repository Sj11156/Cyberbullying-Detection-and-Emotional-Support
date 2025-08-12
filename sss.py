import streamlit as st
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Define the emotions and their corresponding emojis
emotions_emoji_dict = {
    "anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗",
    "joy": "😂", "neutral": "😐", "sad": "😔", "sadness": "😔",
    "shame": "😳", "surprise": "😮"
}

# Load the model pipeline
def load_model():
    model_pipeline = joblib.load(open('./models/emotion_classifier_pipe_lr.pkl', 'rb'))
    return model_pipeline

# Predict emotion using the loaded model
def predict_emotion(text, model_pipeline):
    prediction = model_pipeline.predict([text])[0]
    probability = model_pipeline.predict_proba([text])
    return prediction, probability

# Load test data for accuracy evaluation
def load_test_data():
    test_df = pd.read_csv('./test_data.csv')  # Make sure this path is correct
    return test_df

# Calculate accuracy of the model
def calculate_accuracy(test_df, model_pipeline):
    test_texts = test_df['text']
    true_labels = test_df['label']

    # Predict emotions for the test set
    predictions = model_pipeline.predict(test_texts)

    # Calculate accuracy
    accuracy = accuracy_score(true_labels, predictions)
    return accuracy, true_labels, predictions

# Main Application
def main():
    st.title("Emotion Classifier App")
    menu = ["Home", "Monitor", "Accuracy", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Load the model
    model_pipeline = load_model()

    if choice == "Home":
        st.subheader("Emotion Detection in Text")
        with st.form(key='emotion_clf_form'):
            raw_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label='Submit')

        if submit_text:
            prediction, probability = predict_emotion(raw_text, model_pipeline)
            st.success("Original Text")
            st.write(raw_text)

            st.success("Prediction")
            emoji_icon = emotions_emoji_dict.get(prediction, "❓")  # Use a default emoji if not found
            st.write(f"{prediction}: {emoji_icon}")
            st.write(f"Confidence: {np.max(probability):.2f}")

    elif choice == "Accuracy":
        st.subheader("Model Accuracy")
        
        # Load test data and calculate accuracy
        test_df = load_test_data()
        accuracy, true_labels, predictions = calculate_accuracy(test_df, model_pipeline)

        # Display the accuracy
        st.write(f"Model Accuracy: {accuracy * 100:.2f}%")
        
        # Display confusion matrix
        cm = confusion_matrix(true_labels, predictions)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model_pipeline.classes_)
        
        fig, ax = plt.subplots()
        disp.plot(ax=ax)
        st.pyplot(fig)

    elif choice == "About":
        st.write("This app uses NLP to detect emotions in text.")
        st.write("You can input text, and the model will predict the emotion associated with it.")
        
if __name__ == '__main__':
    main()