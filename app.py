import streamlit as st
import requests

# إعدادات الصفحة والأيقونة (الأيقونة كتبان في المتصفح)
st.set_page_config(page_title="Music VIP", page_icon="🎵", layout="wide")

# --- CUSTOM DESIGN (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #1DB954; /* Green Spotify */
        color: white;
        border: none;
    }
    .song-card {
        background-color: #1a1c24;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #333;
    }
    h1 { color: #1DB954; text-align: center; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_label_True=True)

st.title("🎧 My Custom Music App")

# --- SEARCH ---
artist = st.text_input("👤 اكتب اسم الفنان (مثلاً: Toto أو Eljoee):", placeholder="قلب على الفنان المفضل عندك...")

if artist:
    # طلب كاع الأغاني (زدنا الـ Limit لـ 50 أغنية)
    url = f"https://api.deezer.com/search?q={artist}&limit=50"
    
    try:
        data = requests.get(url).json()
        if data.get('data'):
            st.success(f"لقينا {len(data['data'])} أغنية لـ {artist}")
            
            # عرض الأغاني على شكل بطاقات (Cards)
            for song in data['data']:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    
                    with col1:
                        st.image(song['album']['cover_medium'], width=80)
                    
                    with col2:
                        st.markdown(f"**{song['title']}**")
                        st.caption(f"Album: {song['album']['title']}")
                    
                    with col3:
                        # زر التحميل المباشر
                        audio_data = requests.get(song['preview']).content
                        st.download_button(
                            label="📥 Download",
                            data=audio_data,
                            file_name=f"{song['title']}.mp3",
                            mime="audio/mpeg",
                            key=song['id']
                        )
                st.markdown("---")
        else:
            st.warning("ما لقينا حتى أغنية، تأكد من السمية.")
    except:
        st.error("السيرفر مشغول، عاود جرب.")
