import streamlit as st
import yt_dlp
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Music VIP", page_icon="logo.png", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .song-card { background: #1a1c24; padding: 20px; border-radius: 15px; border-left: 5px solid #1DB954; }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 Direct Music Downloader")

query = st.text_input("🔍 اكتب اسم الأغنية أو الفنان:", placeholder="مثلاً: Tagne - Nadi")

if query:
    try:
        # البحث عن فيديو واحد باش نتيليشارجيوه
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.%(ext)s', # سمية الملف اللي غيتسيفا في السيرفر
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'default_search': 'ytsearch1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        }

        with st.status("⏳ جاري تحميل الأغنية كاملة للسيرفر..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                # في حالة يوتيوب سيرش، كيكون الفيديو داخل 'entries'
                if 'entries' in info:
                    video_info = info['entries'][0]
                else:
                    video_info = info
                
                title = video_info.get('title', 'music')
                # السيرفر غالبا غيسميه song.mp3 بفضل الإعدادات فوق
                file_path = "song.mp3"

            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.success(f"✅ واجدة: {title}")
                    st.audio(f) # مشغل صوتي كامل
                    st.download_button(
                        label="📥 برك هنا باش تليشارجي MP3",
                        data=f,
                        file_name=f"{title}.mp3",
                        mime="audio/mpeg"
                    )
                # كنمحو الملف من السيرفر مورا ما المستخدم كيشوفو باش ما يعمرش الستوراج
                os.remove(file_path)

    except Exception as e:
        st.error("⚠️ يوتيوب حابس السيرفر دابا. الحل هو دير 'Reboot App' من إعدادات Streamlit باش يتبدل الـ IP.")
