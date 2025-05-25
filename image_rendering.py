import streamlit as st
import time
import base64
from PIL import Image
from io import BytesIO

# Convert image to base64
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Custom CSS for "AI-style rendering"
css = """
<style>
.ai-container {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
}

.ai-image {
    animation: aiReveal 4s ease-in-out forwards;
    max-width: 100%;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    opacity: 0;
    filter: grayscale(100%) blur(10px) brightness(0.7);
    transform: scale(1.1);
}

@keyframes aiReveal {
    0% {
        opacity: 0;
        filter: grayscale(100%) blur(10px) brightness(0.7);
        transform: scale(1.1);
    }
    50% {
        opacity: 0.5;
        filter: grayscale(50%) blur(4px) brightness(0.85);
        transform: scale(1.03);
    }
    100% {
        opacity: 1;
        filter: grayscale(0%) blur(0) brightness(1);
        transform: scale(1);
    }
}

.loading-text {
    font-family: monospace;
    font-size: 1.2rem;
    color: #888;
    margin-top: 1rem;
    animation: pulseText 1.2s infinite;
    text-align: center;
}

@keyframes pulseText {
    0%, 100% { opacity: 0.2; }
    50% { opacity: 1; }
}
</style>
"""

# Upload image
st.set_page_config(layout="centered")
st.title("🤖 AI Rendering Simulation")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    img_base64 = image_to_base64(img)

    # Show loading message
    loading_placeholder = st.empty()
    loading_placeholder.markdown('<div class="loading-text">🧠 Generating image with AI...</div>', unsafe_allow_html=True)
    
    # Simulate generation delay
    time.sleep(3)

    # Clear loading
    loading_placeholder.empty()

    # Inject CSS + image with animation
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="ai-container">
            <img class="ai-image" src="data:image/png;base64,{img_base64}" />
        </div>
        """,
        unsafe_allow_html=True
    )
