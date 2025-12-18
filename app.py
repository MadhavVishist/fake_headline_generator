import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os

# ---------------- CONFIG ----------------
FONT_PATH = "fonts/Montserrat-Bold.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = None
# --- 1. DATASETS (The "Peak Brainrot" Collection) ---

subjects_list = [
    "Modi Ji (Melody Version)", "A 14-year-old Sigma Male", "The 'System' Guy", 
    "Alakh Sir's Aggressive Whiteboard", "Lord Puneet Superstar", "A Depressed JEE Aspirant", 
    "A Corporate Majdoor on Notice Period", "Dolly Chaiwala", "Orry (Just Orry)", 
    "The Ghost of a 90s Govinda", "A South Delhi 'Healer'", "Bhupendra Jogi", 
    "A Guy from Haryana with a Scorpio", "Zomato Rider on a Hayabusa", "AI-generated Bhabhi",
    "Skibidi Toilet", "The Cameraman who never dies", "That one friend who asks for 'Party'",
    "A 'Papa ki Pari' on a Scooty", "The Admin of 'Family WhatsApp Group'", 
    "An Unemployed Engineer", "Elvish Bhai's PR Team"
]

actions = [
    "is manifesting a 12 LPA package from", "is speed-running a divorce with", 
    "is ghosting the existential dread of", "is explaining 'The Matrix' to", 
    "is getting beaten with a chappal by", "is gatekeeping the password to", 
    "is accidentally sending a 'Rishta' profile to", "is having a mid-life crisis with", 
    "is stealing the Mug (Balti) from", "is asking for the 'Sauce' from", 
    "is doing a 'Ghar-Wapsi' of", "is trying to rizz up the manager of", 
    "is being edited into a Phonk remix with", "is declaring war on",
    "is comparing CIBIL scores with", "is selling a course on 'How to Breathe' to",
    "is dancing to 'Moye Moye' with"
]

places = [
    "a plate of black-water Maggi", "an NFT of a Flying Chappal", "the Silk Board traffic jam", 
    "a toxic HR's 'Fun Friday' email", "a 3 AM existential crisis", "the Deep Web of WhatsApp", 
    "an Elvish Yadav fan-meet", "a packet of expired Kurkure", "the 'Delete for Everyone' button", 
    "a pyramid scheme meeting in CCD", "the neighbor's plastic-wrapped TV remote", 
    "a 0.5 GPA scorecard", "a stolen Indian Railways Towel", "Elon Musk's Chai Tapri",
    "the unseen syllabus of Engineering Graphics", "a Bajaj Avenger with 'Mahakal' sticker",
    "the backrooms of Sarojini Market"
]

# --- 2. THE HELPER: SMART TEXT RESIZING (Fixes Cut-off Issues) ---
def get_fitted_font(draw, text, font_path, max_width, max_height, start_size=80):
    size = start_size

    while size >= 24:
        font = ImageFont.truetype(font_path, size)

        # Wrap text based on width
        avg_char_width = size * 0.55
        chars_per_line = max(15, int(max_width / avg_char_width))
        wrapped = textwrap.fill(text, width=chars_per_line)

        bbox = draw.multiline_textbbox(
            (0, 0),
            wrapped,
            font=font,
            spacing=12,
            align="center"
        )

        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if text_w <= max_width and text_h <= max_height:
            return font, wrapped

        size -= 2

    # Last-resort fallback (never breaks layout)
    return ImageFont.truetype(font_path, 24), textwrap.fill(text, width=30)


# --- 3. THE IMPROVED IMAGE ENGINE (HD & Full Width) ---
def generate_news_card(headline_text):
    # Canvas Size (HD 1280x720 for crisp text)
    W, H = 1280, 720
    img = Image.new('RGB', (W, H), color=(10, 15, 30))
    draw = ImageDraw.Draw(img)

    # 1. Background (Subtle World Map Dots)
    for i in range(0, W, 40):
        for j in range(0, H, 40):
            if random.random() > 0.8:
                draw.ellipse([i, j, i+2, j+2], fill=(50, 60, 80))

    # 2. Main Red Banner (Full Width - No empty black space)
    banner_h = 300
    banner_y = (H - banner_h) // 2
    
    draw.rectangle([0, banner_y, W, banner_y + banner_h], fill=(180, 0, 0)) # Red
    draw.rectangle([0, banner_y + banner_h - 10, W, banner_y + banner_h], fill=(140, 0, 0)) # Shadow

    # 3. "BREAKING NEWS" Title Tab
    draw.rectangle([50, banner_y - 60, 450, banner_y], fill=(240, 240, 240))
    
    # Load Fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 40)
        font_logo = ImageFont.truetype("arialbd.ttf", 50)
        font_ticker = ImageFont.truetype("arial.ttf", 35)
    except:
        font_title = ImageFont.load_default()
        font_logo = ImageFont.load_default()
        font_ticker = ImageFont.load_default()

    draw.text((70, banner_y - 50), "BREAKING NEWS", fill="black", font=font_title)

    # 4. Logo (Top Right)
    draw.text((W - 450, 30), "DANK TV 24x7", fill="white", font=font_logo)

    # 5. SMART HEADLINE RENDERING
    # This ensures the text fits perfectly in the red box
    safe_w = W - 100
    safe_h = banner_h - 40
    font_headline, wrapped_text = get_fitted_font(draw, headline_text.upper(), "arialbd.ttf", safe_w, safe_h, start_size=80)
    
    # Center the text
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font_headline, spacing=15)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (W - text_w) // 2
    text_y = banner_y + (banner_h - text_h) // 2

    draw.multiline_text((text_x, text_y), wrapped_text, fill="white", font=font_headline, align="center", spacing=15)

    # 6. Yellow Ticker Tape (Bottom)
    draw.rectangle([0, H - 80, W, H], fill=(255, 215, 0))
    ticker_text = "🔴 LIVE: NO ONE IS SAFE | JANTA JAWAB CHAHTI HAI | MOYE MOYE 🧢"
    draw.text((30, H - 60), ticker_text, fill="black", font=font_ticker)

    # 7. Live Bug (Top Left)
    draw.rectangle([30, 30, 160, 80], fill=(200, 0, 0))
    draw.text((45, 38), "🔴 LIVE", fill="white", font=font_ticker)

    return img

# --- 4. STREAMLIT FRONTEND (Your Preferred Structure) ---
st.set_page_config(page_title="Dank News Studio", page_icon="📺", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
    div[data-testid="stImage"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("📺 Dank Indian News Studio")
st.markdown("### *The only source of News you can't trust.*")

# Layout columns (2:1 Ratio as requested)
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Settings")
    custom_name = st.text_input("Target Name:", placeholder="e.g. Sharma Ji")
    intensity = st.slider("Brainrot Level", 0, 100, 85)
    st.info("Tip: Higher levels don't do anything , yet they feel dangerous.")

with col1:
    if st.button('🔥 GENERATE VIRAL HEADLINE'):
        # Selection Logic
        s = custom_name if custom_name else random.choice(subjects_list)
        a = random.choice(actions)
        p = random.choice(places)
        
        full_headline = f"{s} {a} {p}"
        
        # Generate Visual
        with st.spinner("Cooking up Kalesh..."):
            img = generate_news_card(full_headline)
        
        # Show Preview
        st.image(img, use_container_width=True)
        
        # Download Button
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="📥 Download Meme for Instagram",
            data=byte_im,
            file_name="breaking_news_dank.png",
            mime="image/png"
        )
    else:
        st.info("Click the button to start the Kalesh.")

# Sidebar (Your preferred footer placement)
st.sidebar.markdown("### **NOTICE**")
st.sidebar.code("This is a fake \nnews generator for \nentertainment purposes \nonly. Any resemblance\n to real persons, \nliving or dead, \nis purely coincidental.")
st.sidebar.write("Developed for fun by Madhav Vishist.")