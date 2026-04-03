import streamlit as st
import yt_dlp
import os

# 1. إعدادات الصفحة واللوغو
st.set_page_config(page_title="Music VIP", page_icon="logo.png", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1DB954; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 Full Music Downloader")

# 2. محرك البحث
query = st.text_input("🔍 اكتب اسم الأغنية (كاملة):", placeholder="مثلاً: Tagne - Nadi")

if query:
    try:
        with st.status("🔍 جاري البحث والتحميل (الأغنية كاملة)..."):
            # إعدادات yt-dlp باش نهربو من البلوك
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'default_search': 'ytsearch1',
                'outtmpl': 'song.mp3',
                # هاد السطور هما اللي كيمنعو البلوك (403 Forbidden)
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                title = info['entries'][0]['title']
            
            # زر التحميل للأغنية كاملة
            with open("song.mp3", "rb") as f:
                st.download_button(
                    label=f"📥 Download: {title}",
                    data=f,
                    file_name=f"{title}.mp3",
                    mime="audio/mpeg"
                )
            
            # مسح الملف من السيرفر مورا ما يسالي
            os.remove("song.mp3")

    except Exception as e:
        st.error("السيرفر عليه الضغط، عاود جرب مورا شوية.")
