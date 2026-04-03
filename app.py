import streamlit as st
import requests

# إعدادات الصفحة (Icon المتصفح)
st.set_page_config(page_title="Music VIP", page_icon="🎵", layout="wide")

# --- CUSTOM DESIGN (CSS) ---
st.markdown("""
    <style>
    /* تغيير الخلفية للأسود الفخم */
    .stApp {
        background-color: #0e1117;
    }
    /* تحسين شكل الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background-color: #1DB954; /* أخضر سبوتيفاي */
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1ed760;
        transform: scale(1.02);
    }
    /* تنسيق كروت الأغاني */
    .song-container {
        background-color: #1a1c24;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #333;
    }
    h1 { color: #1DB954; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 My Custom Music App")

# --- SEARCH ---
artist = st.text_input("👤 اكتب اسم الفنان (مثلاً: Tagne أو Moro):", placeholder="قلب على الفنان المفضل عندك...")

if artist:
    # طلب 50 أغنية (يعني كاع الموسيقى ديالو تقريبا)
    url = f"https://api.deezer.com/search?q={artist}&limit=50"
    
    try:
        response = requests.get(url).json()
        if response.get('data'):
            st.success(f"لقينا {len(response['data'])} أغنية لـ {artist}")
            
            for song in response['data']:
                # تصميم "كرت" لكل أغنية
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    
                    with col1:
                        st.image(song['album']['cover_medium'], width=80)
                    
                    with col2:
                        st.markdown(f"### {song['title']}")
                        st.caption(f"Album: {song['album']['title']}")
                    
                    with col3:
                        # تحميل الصوت
                        audio_url = song['preview']
                        audio_data = requests.get(audio_url).content
                        st.download_button(
                            label="📥 Download MP3",
                            data=audio_data,
                            file_name=f"{song['title']}.mp3",
                            mime="audio/mpeg",
                            key=str(song['id']) # ID فريد لكل زر
                        )
                st.markdown("---")
        else:
            st.warning("ما لقينا والو، جرب سمية فنان آخر.")
    except Exception as e:
        st.error("السيرفر عامر، عاود جرب مورا شوية.")
