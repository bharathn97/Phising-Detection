import streamlit as st
import requests
import json
import os

# File to store history
HISTORY_FILE = "history.json"

# Load history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Save history to file
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

# Main Page
def main_page():
    st.markdown(
        """
        <style>
        .main-page {
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        <div class="main-page">
            <h1 style="color: white;">DEPARTMENT OF INFORMATION TECHNOLOGY</h1>
            <h3 style="color: white;">NATIONAL INSTITUTE OF TECHNOLOGY KARNATAKA, SURATHKAL-575025</h3>
            <h4 style="color: #7f8c8d;">Information Assurance and Security (IT352) Course Project</h4>
            <h4 style="color: #2980b9;">Title: “Phishing URL Detection”</h4>
            <p style="white">Carried out by</p>
            <p><b>Bharath N (221IT017)</b></p>
            <p><b>Dilip Sagar M (221IT024)</b></p>
            <p style="color: #7f8c8d;">During Academic Session January – April 2025</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Go to URL Detection"):
        st.session_state.page = "url_detection"
    if st.button("Go to File Upload"):
        st.session_state.page = "file_upload"

def is_valid_url(url):
    # Check if the input contains spaces
    if " " in url:
        return False
    # Check if the URL starts with http:// or https://
    if url.startswith("http://") or url.startswith("https://"):
        return True
    return False

# URL Detection Page
def url_detection_page():
    st.markdown(
        """
        <style>
        .url-page {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .header {
            color: #2c3e50;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .info-box {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: left;
        }
        </style>
        <div class="url-page">
            <h2 class="header">Phishing URL Detection</h2>
            <div class="info-box">
                <p><b>What is a phishing URL?</b></p>
                <p>A phishing URL is a malicious link designed to steal sensitive information such as usernames, passwords, or credit card details. Always verify the authenticity of a URL before clicking on it.</p>
                <p>Enter a URL below to check if it is a phishing URL.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input for URL
    url = st.text_input("Enter a URL to check if it is a phishing URL:")
    if url:
        if is_valid_url(url):
            st.success("Valid URL!")
            
            # Send POST request to the API
            api_url = "https://b502-34-32-248-237.ngrok-free.app/predict"  # Replace with your ngrok link
            try:
                response = requests.post(api_url, json={"url": url})
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get("prediction", "Unknown")
                    processing_time = result.get("processing_time", "N/A")

                    # Show popup based on prediction
                    if prediction == "phishing":
                        st.error(f"The URL is classified as **Phishing**. (Processed in {processing_time:.2f} seconds)")
                    elif prediction == "legitimate":
                        st.success(f"The URL is classified as **Legitimate**. (Processed in {processing_time:.2f} seconds)")
                    else:
                        st.warning("Unable to classify the URL.")

                    # Store in history
                    history = load_history()
                    history.append({"url": url, "result": prediction, "processing_time": processing_time})
                    save_history(history)
                else:
                    st.error("Error: Unable to process the URL. Please try again later.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Invalid URL! Please enter a valid URL.")
    
    # Display history
    st.subheader("History")
    history = load_history()
    if history:
        for entry in history:
            st.write(f"URL: {entry['url']} - Result: {entry['result']} - Processing Time: {entry['processing_time']} seconds")
    else:
        st.write("No history available.")
    
    if st.button("Back to Main Page"):
        st.session_state.page = "main"

# File Upload Page
def file_upload_page():
    st.markdown(
        """
        <style>
        .file-upload-page {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .header {
            color: #2c3e50;
            font-size: 24px;
            margin-bottom: 20px;
        }
        </style>
        <div class="file-upload-page">
            <h2 class="header">Batch URL Detection</h2>
            <p>Upload a text file containing one URL per line to check if they are phishing URLs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload a file", type=["txt"])
    if uploaded_file is not None:
        # Send POST request to the API
        api_url = "https://b502-34-32-248-237.ngrok-free.app/predict-file"  # Replace with your ngrok link
        try:
            response = requests.post(api_url, files={"file": uploaded_file})
            if response.status_code == 200:
                result = response.json()
                st.subheader("Results")

                # Display results and save to history
                history = load_history()
                for res in result["results"]:
                    st.write(f"URL: {res['url']} - Prediction: {res['prediction']} - Processing Time: {res['processing_time']} seconds")
                    # Save each result to history
                    history.append({
                        "url": res["url"],
                        "result": res["prediction"],
                        "processing_time": res["processing_time"]
                    })
                save_history(history)
            else:
                st.error("Error: Unable to process the file. Please try again later.")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Display history
    st.subheader("History")
    history = load_history()
    if history:
        for entry in history:
            st.write(f"URL: {entry['url']} - Result: {entry['result']} - Processing Time: {entry['processing_time']} seconds")
    else:
        st.write("No history available.")
    
    if st.button("Back to Main Page"):
        st.session_state.page = "main"
    

# Page Navigation
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "url_detection":
    url_detection_page()
elif st.session_state.page == "file_upload":
    file_upload_page()
