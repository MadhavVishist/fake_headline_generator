import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

# ---------------- CONFIG ----------------
FONT_PATH = "fonts/Montserrat-Bold.ttf"
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

# ---------------- TEXT FITTER ----------------
def get_fitted_font(draw, text, max_width, max_height, start_size=80):
    size = start_size

    while size >= 26:
        font = ImageFont.truetype(FONT_PATH, size)

        chars_per_line = max(15, int(max_width / (size * 0.55)))
        wrapped = textwrap.fill(text, width=chars_per_line)

        bbox = draw.multiline_textbbox(
            (0, 0),
            wrapped,
            font=font,
            spacing=14,
            align="center"
        )

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if w <= max_width and h <= max_height:
            return font, wrapped

        size -= 2

    return ImageFont.truetype(FONT_PATH, 26), textwrap.fill(text, width=30)

# ---------------- IMAGE ENGINE ----------------
def generate_news_card(headline_text):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (12, 16, 30))
    draw = ImageDraw.Draw(img)

    # Background dots
    for x in range(0, W, 40):
        for y in range(0, H, 40):
            if random.random() > 0.85:
                draw.ellipse([x, y, x + 2, y + 2], fill=(60, 70, 90))

    banner_h = 300
    banner_y = (H - banner_h) // 2

    # Red banner
    draw.rectangle([0, banner_y, W, banner_y + banner_h], fill=(180, 0, 0))
    draw.rectangle([0, banner_y + banner_h - 10, W, banner_y + banner_h], fill=(140, 0, 0))

    # Fonts
    font_title = ImageFont.truetype(FONT_PATH, 38)
    font_logo = ImageFont.truetype(FONT_PATH, 46)
    font_ticker = ImageFont.truetype(FONT_PATH, 32)

    # Breaking tab
    draw.rectangle([50, banner_y - 60, 450, banner_y], fill=(240, 240, 240))
    draw.text((70, banner_y - 50), "BREAKING NEWS", fill="black", font=font_title)

    # Logo
    draw.text((W - 420, 30), "DANK TV 24x7", fill="white", font=font_logo)

    # Headline
    safe_w = W - 120
    safe_h = banner_h - 40

    font_headline, wrapped = get_fitted_font(
        draw,
        headline_text.upper(),
        safe_w,
        safe_h
    )

    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_headline, spacing=16)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    draw.multiline_text(
        ((W - text_w) // 2, banner_y + (banner_h - text_h) // 2),
        wrapped,
        fill="white",
        font=font_headline,
        align="center",
        spacing=16
    )

    # Ticker
    draw.rectangle([0, H - 80, W, H], fill=(255, 215, 0))
    draw.text(
        (30, H - 58),
        "🔴 LIVE: NO ONE IS SAFE | JANTA JAWAB CHAHTI HAI | MOYE MOYE",
        fill="black",
        font=font_ticker
    )

    # Live badge
    draw.rectangle([30, 30, 160, 80], fill=(200, 0, 0))
    draw.text((45, 38), "🔴 LIVE", fill="white", font=font_ticker)

    return img

# ---------------- STREAMLIT UI ----------------
st.set_page_config("Dank News Studio", "📺", layout="centered")

st.markdown("""
<style>
.main { background-color: #0e1117; }
.stButton>button {
    width: 100%; height: 3em;
    background-color: #ff4b4b;
    color: white; font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📺 Dank Indian News Studio")
st.markdown("*The only source of news you can't trust.*")

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Settings")
    name = st.text_input("Target Name", "Sharma Ji")
    st.slider("Brainrot Level", 0, 100, 85)
    st.info("Higher levels do nothing, but feel dangerous.")

with col1:
    if st.button("🔥 GENERATE VIRAL HEADLINE"):
        headline = f"{name} {random.choice(actions)} {random.choice(places)}"
        with st.spinner("Cooking up kalesh..."):
            img = generate_news_card(headline)

        st.image(img, use_container_width=True)

        buf = io.BytesIO()
        img.save(buf, format="PNG")

        st.download_button(
            "📥 Download Meme for Instagram",
            buf.getvalue(),
            "breaking_news_dank.png",
            "image/png"
        )
    else:
        st.info("Click the button to start the kalesh.")

st.sidebar.markdown("### NOTICE")
st.sidebar.code(
    "This is a fake news generator\n"
    "for entertainment purposes only.\n"
    "Any resemblance is coincidental."
)
st.sidebar.write("Developed by Madhav Vishist")