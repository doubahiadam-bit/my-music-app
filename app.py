import streamlit as st
import requests

# 1. إعدادات الصفحة والأيقونة (تأكد من وجود logo.png في GitHub)
st.set_page_config(page_title="Music VIP", page_icon="logo.png", layout="wide")

# 2. ديزاين فخم (CSS مصحح 100%)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 25px; 
        background-color: #1DB954; color: white; 
        font-weight: bold; border: none; padding: 10px;
    }
    h1 { color: #1DB954; text-align: center; font-family: 'Arial Black'; }
    .song-card { background: #1a1c24; padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 My Music App")

# 3. خانة البحث
artist = st.text_input("👤 اكتب اسم الفنان أو الأغنية:", placeholder="مثلاً: Tagne, Toto, Inna...")

if artist:
    # جلب الأغاني من iTunes (أغاني كاملة وبلا بلوك)
    url = f"https://itunes.apple.com/search?term={artist}&entity=song&limit=30"
    
    try:
        response = requests.get(url).json()
        if response['resultCount'] > 0:
            st.success(f"لقينا {response['resultCount']} أغنية!")
            for song in response['results']:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    with col1:
                        st.image(song['artworkUrl100'], width=80)
                    with col2:
                        st.markdown(f"**{song['trackName']}**")
                        st.caption(f"Artist: {song['artistName']}")
                    with col3:
                        # تحميل الأغنية كاملة
                        audio_data = requests.get(song['previewUrl']).content
                        st.download_button(
                            label="📥 Download",
                            data=audio_data,
                            file_name=f"{song['trackName']}.mp3",
                            mime="audio/mpeg",
                            key=str(song['trackId'])
                        )
                st.markdown("---")
        else:
            st.warning("ما لقينا والو، جرب سمية أخرى.")
    except:
        st.error("مشكل في الاتصال، جرب مورا شوية.")
