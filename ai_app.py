import streamlit as st
import google.generativeai as genai
import PIL.Image
import fitz
import docx2txt
import io



# 🎉 Welcome Page
st.set_page_config(page_title="Gem-Y AI Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🌟 Welcome to Gem-Y AI Chatbot 🌟</h1>
    <p style='text-align: center; font-size: 18px;'>Your personal AI assistant — ask questions, upload images or documents, and let Gem-Y handle the rest! 💬📄🖼️</p>
    <hr>
""", unsafe_allow_html=True)


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

# Upload file
uploaded_file = st.file_uploader("Upload a document 📄", type=["txt", "pdf", "docx"])

file_text = ""

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]

    if file_type == 'txt':
        file_text = uploaded_file.read().decode('utf-8')

    elif file_type == 'pdf':
        pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf_reader:
            file_text += page.get_text()

    elif file_type == 'docx':
        file_text = docx2txt.process(uploaded_file)

    # Show user options
    if file_text:
        st.write("What would you like to do with this document? 💭👇")
        action = st.selectbox("Choose an action", ["Summarize", "Extract Info", "Ask a Question"])

        if action == "Summarize":
            response = model.generate_content(f"Summarize this in simple terms:\n\n{file_text}")
            st.text_area("Gem-Y's Summary 📝", response.text, height=250)

        elif action == "Extract Info":
            topic = st.text_input("Enter the topic you'd like to extract info about 🔍:")
            if topic:
                prompt = f"From this document, extract all information about {topic}:\n\n{file_text}"
                response = model.generate_content(prompt)
                st.text_area(f"Info about {topic} 📚", response.text, height=250)

        elif action == "Ask a Question":
            user_question = st.text_input("Ask anything about this document 🤔:")
            if user_question:
                prompt = f"Based on this document, answer the following question:\n{user_question}\n\nDocument:\n{file_text}"
                response = model.generate_content(prompt)
                st.text_area("Gem-Y's Answer 💬", response.text, height=250)


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
