import streamlit as st
import requests

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(page_title="Music VIP", page_icon="logo.png", layout="wide")

# 2. ديزاين فخم (CSS)
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

# 3. محرك البحث
query = st.text_input("👤 اكتب اسم الفنان أو الأغنية:", placeholder="مثلاً: Tagne, Toto, Saad Lamjarred...")

if query:
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=25"
    try:
        with st.spinner("🔍 جاري البحث..."):
            response = requests.get(url).json()
            
        if response.get('resultCount', 0) > 0:
            for song in response['results']:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    with col1:
                        st.image(song.get('artworkUrl100'), width=80)
                    with col2:
                        st.markdown(f"**{song.get('trackName')}**")
                        st.caption(f"Artist: {song.get('artistName')}")
                    with col3:
                        audio_url = song.get('previewUrl')
                        if audio_url:
                            audio_data = requests.get(audio_url).content
                            st.download_button(
                                label="📥 Download",
                                data=audio_data,
                                file_name=f"{song.get('trackName')}.mp3",
                                mime="audio/mpeg",
                                key=str(song.get('trackId'))
                            )
                st.markdown("---")
        else:
            st.warning("مالقينا والو، جرب سمية أخرى.")
    except:
        st.error("مشكل في الاتصال، عاود جرب.")
