import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler


s = pd.read_csv("social_media_usage.csv")

def clean_sm(x):
    if x == 1:
        return 1
    else:
        return 0

ss = s[['income', 'educ2', 'par', 'marital', 'gender', 'age']].copy()
ss['sm_li'] = s['web1h'].apply(clean_sm)
ss = ss[(ss['income'] <= 9) & (ss['educ2'] <= 8) & (ss['par'] <= 2) & ((ss['marital'] == 1) | (ss['marital'] == 6)) & (ss['age'] <= 98)].dropna()

y = ss['sm_li']
X = ss.drop('sm_li', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

def load_model():
    # Load your trained model here
    # For example: model = joblib.load('your_model_file.pkl')
    return model
 
def load_scaler():
    # Load your fitted scaler here
    # For example: scaler = joblib.load('your_scaler_file.pkl')
    return scaler
 
def predict_probability(features, scaler, model):
    # Standardize features
    features_scaled = scaler.transform(features)
    # Make prediction
    probability = model.predict_proba(features_scaled)[:, 1]
    return probability
 
def main():
    st.title("LinkedIn User Prediction App")
 
    st.markdown("""
            This app predicts the probability that a user is a LinkedIn member based on their 
            demographics and social attributes. It is trained using logistic regression to 
            estimate membership likelihood from parameters like income, education, age etc.
            """)
 
    # Sidebar with user input
    st.sidebar.header("User Input Features")
    income = st.sidebar.slider("Income", 1, 9, 5)
    education = st.sidebar.slider("Education", 1, 8, 4)
    parent = st.sidebar.radio("Parent", ["No", "Yes"])
    marital_status = st.sidebar.radio("Marital Status", ["Single", "Married"])
    gender = st.sidebar.radio("Gender", ["Male", "Female"])
    age = st.sidebar.slider("Age", 18, 98, 30)
 
    # Load the fitted scaler
    scaler = load_scaler()
 
    # Display the user input features
    st.write("## User Input Features")
    user_input = pd.DataFrame({'income': [income], 'educ2': [education], 'par': [1 if parent == "Yes" else 0],
                               'marital': [1 if marital_status == "Married" else 0],
                               'gender': [1 if gender == "Female" else 0], 'age': [age]})
    st.table(user_input)
 
    # Load the model and make predictions
    model1 = load_model()
    probability = predict_probability(user_input, scaler, model1)
 
    # Display prediction results
    st.write("## Prediction")
    st.write(f"Probability of being a LinkedIn user: {probability[0]:.2f}")
 
    prediction = "LinkedIn User" if probability >= 0.5 else "Non-LinkedIn User"
    st.write(f"Prediction: {prediction}")
 
if __name__ == '__main__':
    main()