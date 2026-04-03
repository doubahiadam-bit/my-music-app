import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music Downloader", page_icon="🎵")

# هاد السطر كيخلي التطبيق يبان دغيا
st.title("🎵 Music Downloader")

song_name = st.text_input("اكتب اسم الأغنية هنا:")

if song_name:
    with st.status("🔍 جاري البحث والتحميل..."):
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'song.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([song_name])
            
            if os.path.exists("song.mp3"):
                with open("song.mp3", "rb") as file:
                    st.success("واجدة!")
                    st.download_button(
                        label="📥 حفظ في الآيفون",
                        data=file,
                        file_name=f"{song_name}.mp3",
                        mime="audio/mpeg"
                    )
        except Exception as e:
            st.error(f"مشكل بسيط: {e}")
