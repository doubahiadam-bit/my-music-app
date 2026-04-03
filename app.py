import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Music VIP", page_icon="logo.png", layout="wide")

# 2. ديزاين CSS مصحح 100%
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 25px; 
        background-color: #1DB954; color: white; 
        font-weight: bold; border: none; padding: 10px;
    }
    h1 { color: #1DB954; text-align: center; font-family: 'Arial Black'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 My Music App")

# 3. محرك البحث
query = st.text_input("👤 اكتب اسم الفنان أو الأغنية:", placeholder="مثلاً: Tagne, Toto, Saad Lamjarred...")

if query:
    # كنخدمو بـ iTunes API باش نهربو من البلوك ديال يوتيوب
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=15"
    
    try:
        with st.spinner("🔍 جاري البحث..."):
            response = requests.get(url).json()
            
        if response.get('resultCount', 0) > 0:
            for song in response['results']:
                col1, col2, col3 = st.columns([1, 3, 2])
                with col1:
                    st.image(song.get('artworkUrl100'), width=70)
                with col2:
                    st.write(f"**{song.get('trackName')}**")
                    st.caption(f"Artist: {song.get('artistName')}")
                with col3:
                    preview_url = song.get('previewUrl')
                    if preview_url:
                        # زر التحميل المباشر
                        audio_data = requests.get(preview_url).content
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
        st.error("السيرفر مشغول، عاود جرب مورا شوية.")
