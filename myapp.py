import streamlit as st
import google.generativeai as genai

# Set up Gemini API
genai.configure(api_key= "AIzaSyBJb9F6GeG6_LL9PjWy1nz2T3DW_gjF-0k")  # Replace with your actual API key

# List available models

models = genai.list_models()
for model in models:
    print(model.name)
# Function to get AI response
def chat_with_gemini(user_text):
    gemini_model = genai.GenerativeModel("gemini-1.5-pro")  # Rename model variable
    gemini_response = gemini_model.generate_content(user_text)  # Rename response variable
    return gemini_response.text  # Returning the AI-generated response

# Streamlit UI
st.title("AI Chatbot using Gemini API")
st.write("Ask me anything!")

# Get user input
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = chat_with_gemini(user_input)
        st.text_area("AI:", response, height=150)
