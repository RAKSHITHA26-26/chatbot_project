import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# 🔐 Configure API key
genai.configure(api_key="AIzaSyBJb9F6GeG6_LL9PjWy1nz2T3DW_gjF-0k")  # Replace with your API key

# Initialize models
text_model = genai.GenerativeModel('gemini-1.5-pro-latest')
vision_model = genai.GenerativeModel('gemini-1.5-flash')

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(
        temperature=0.7,
        max_output_tokens=1024,
    ),
    safety_settings={
        "HARASSMENT": "BLOCK_NONE",
        "HATE": "BLOCK_NONE",
        "SEXUAL": "BLOCK_NONE",
        "DANGEROUS": "BLOCK_NONE",
    }
)

# Title
st.title("Gem-Y AI Chatbot 🤖✨")

st.session_state.username = st.text_input("What's your name? 😊")
f"Hey {st.session_state.username}! You’re awesome 😍, let’s dive into this!"

# Layout: Upload Icon + Text Input in one line
col1, col2 = st.columns([1, 5])

with col1:
    uploaded_file = st.file_uploader(" ", type=["jpg", "jpeg", "png", "pdf"], label_visibility="collapsed")

with col2:
    user_input = st.text_input("Type your message here...")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Handle Uploaded File
if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        with st.spinner("Analyzing image... 🧠🖼️"):
            image = PIL.Image.open(uploaded_file)
            vision_response = vision_model.generate_content([image, "Describe this image or provide insights."])
            st.success("Gemini's response:")
            st.write(vision_response.text)

    elif uploaded_file.type == "application/pdf":
        st.write("📄 Uploaded Document:")
        with st.spinner("Analyzing document... 📄🧠"):
            pdf_bytes = uploaded_file.read()
            vision_response = vision_model.generate_content([pdf_bytes, "Analyze this document and summarize key points."])
            st.success("Gem-Y's response:")
            st.write(vision_response.text)

# Handle Text Input
elif user_input:
    with st.spinner("Gem-Y is thinking... 🤔💬"):
        response = text_model.generate_content(user_input)
        st.success("Gem-Y says:")
        st.write(response.text)
def chat_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text


if st.button("🔄 Refresh Chat"):
    st.session_state.chat_history = []  # Clear history
    st.rerun()  # Refresh the app page

# Send Button
if st.button("Send"):
    if user_input:
        # Here you call your chat_with_gemini function
        response = chat_with_gemini(user_input)

        # Append user and AI response to chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Gem-Y", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}:** {message}")
# Footer
st.markdown("---")
st.markdown("Gem-Y — Crafted by Us💖, Powered by Genius⚙️💎")
