import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music VIP", page_icon="🎵", layout="wide")

# --- DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stButton>button { border-radius: 20px; background-color: #1DB954; color: white; }
    h1 { color: #1DB954; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Full Music Downloader")

artist = st.text_input("👤 اكتب اسم الفنان (مثلاً: Lbenj):")

if artist:
    # إعدادات البحث عن كاع الأغاني (Full Info)
    search_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch15', # كيجيب 15 أغنية
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }

    try:
        with st.status(f"🔍 جاري جلب قائمة أغاني {artist}..."):
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                results = ydl.extract_info(f"ytsearch15:{artist}", download=False)
                songs = results['entries']

        for song in songs:
            with st.container():
                col1, col2 = st.columns([4, 1])
                title = song.get('title')
                url = song.get('url')
                
                with col1:
                    st.markdown(f"🎵 **{title}**")
                
                with col2:
                    if st.button("📥 Download", key=url):
                        with st.spinner("جاري التحميل (كاملة)..."):
                            # إعدادات التحميل الكامل
                            dl_opts = {
                                'format': 'bestaudio/best',
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                                'outtmpl': 'full_song.%(ext)s',
                                'nocheckcertificate': True,
                                # هاد السطر كيهرب من البلوك ديال 403
                                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                            }
                            
                            try:
                                if os.path.exists("full_song.mp3"): os.remove("full_song.mp3")
                                with yt_dlp.YoutubeDL(dl_opts) as ydl_dl:
                                    ydl_dl.download([url])
                                
                                if os.path.exists("full_song.mp3"):
                                    with open("full_song.mp3", "rb") as f:
                                        st.download_button(
                                            label="✅ اضغط للحفظ",
                                            data=f,
                                            file_name=f"{title}.mp3",
                                            mime="audio/mpeg"
                                        )
                            except Exception as e:
                                st.error("يوتيوب مزير هاد الساعة، جرب مورا شوية.")

                st.markdown("---")
    except:
        st.error("مشكل في البحث.")
