import os
import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from training import read_data, preprocess_data, train_model, evaluate_model
import base64

working_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(working_dir)

st.set_page_config(
    page_title="Automate ML",
    page_icon="🧠",
    layout="centered")

st.title("🤖 No Code ML Model Training")

dataset_option = st.selectbox("Choose dataset option", ["Upload a Dataset", "Already existing dataset"],index=None)

if dataset_option == "Upload a Dataset":
    uploaded_dataset_name = st.text_input("Enter a name for the uploaded dataset (if applicable)")
    uploaded_file = st.file_uploader("Upload a dataset (CSV or XLSX)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        st.write("Uploaded dataset:")
        dataset = uploaded_dataset_name if uploaded_dataset_name else "uploaded_dataset"
        st.dataframe(df.head())
    else:
        df = None

elif dataset_option == "Already existing dataset":
    # List datasets from the directory
    # dataset_list = os.listdir(f"{parent_dir}/data")
    # dataset = st.selectbox("Select a dataset from the dropdown", dataset_list)
    # df = read_data(f"{parent_dir}/data/{dataset}")
    # st.dataframe(df.head())
    dataset_list = os.listdir(f"{parent_dir}/data")
    dataset = st.selectbox("Select a dataset from the dropdown",dataset_list,index=None)
    df = read_data(dataset)

    if df is not None:
        st.dataframe(df.head())

else:
    df = None

if df is not None:

    col1, col2, col3, col4 = st.columns(4)

    scaler_type_list = ["standard", "minmax"]

    model_dictionary = {
        "Logistic Regression": LogisticRegression(),
        "Support Vector Classifier": SVC(),
        "Random Forest Classifier": RandomForestClassifier(),
        "XGBoost Classifier": XGBClassifier()
    }

    with col1:
        target_column = st.selectbox("Select the Target Column", list(df.columns))
    with col2:
        scaler_type = st.selectbox("Select a scaler", scaler_type_list)
    with col3:
        selected_model = st.selectbox("Select a Model", list(model_dictionary.keys()))
    with col4:
        model_name = st.text_input("Model name")

    if st.button("Train the Model"):
        X_train, X_test, y_train, y_test = preprocess_data(df, target_column, scaler_type)

        model_to_be_trained = model_dictionary[selected_model]

        model = train_model(X_train, y_train, model_to_be_trained, model_name)

        accuracy = evaluate_model(model, X_test, y_test)

        st.success("Test Accuracy: " + str(accuracy))

        # if model_name:
        #     st.markdown(get_download_link(model_name), unsafe_allow_html=True)
        model_path = f"{parent_dir}/trained_models/{model_name}.pkl"

        # Provide a download button for the pickle file
        with open(model_path, 'rb') as file:
            st.download_button(
                label="Download Model",
                data=file,
                file_name=f"{model_name}.pkl",
                mime="application/octet-stream"
            )

