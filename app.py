import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music Downloader", page_icon="🎵")
st.title("🎵 Music Downloader")

song_name = st.text_input("اكتب اسم الأغنية هنا:")

if song_name:
    with st.status("🔍 جاري البحث..."):
        # هاد الإعدادات كتخلي اليوتيوب يظن أنك داخل من متصفح عادي
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
                    st.success("لقيناها! واجدة للتحميل")
                    st.download_button(
                        label="📥 حفظ في الآيفون",
                        data=file,
                        file_name=f"{song_name}.mp3",
                        mime="audio/mpeg"
                    )
                # مسح الملف باش ما يعمرش السيرفر
                os.remove("song.mp3")
        except Exception as e:
            st.error(f"عيا يوتيوب وحبسنا! جرب أغنية أخرى أو تسنى دقيقة.")
