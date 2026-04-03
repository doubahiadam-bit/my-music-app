import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music Hub", page_icon="🎧")
st.title("🎧 Music Downloader Pro")

artist_name = st.text_input("اكتب سمية المغني (مثلاً: Lartiste):")

if artist_name:
    # إعدادات البحث فقط (بلا تحميل)
    search_opts = {
        'format': 'bestaudio/best',
        'default_search': f'ytsearch10', # غايجيب ليك 10 ديال النتائج
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, # هادي مهمة: كيجيب غير السميات بلا ما يشارجي الفيديو
    }

    with st.status(f"🔍 كنقلب على أحسن أغاني {artist_name}..."):
        try:
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                result = ydl.extract_info(f"ytsearch10:{artist_name}", download=False)
                songs = result['entries']
            
            # عرض النتائج في قائمة (Selectbox)
            song_titles = [f"{s.get('title')} ({s.get('duration_string')})" for s in songs]
            selected_song_title = st.selectbox("اختار الأغنية اللي بغيتي:", ["--- اختار من هنا ---"] + song_titles)

            if selected_song_title != "--- اختار من هنا ---":
                # الحصول على رابط الأغنية المختارة
                index = song_titles.index(selected_song_title)
                target_url = songs[index]['url']

                if st.button(f"🚀 تحميل: {selected_song_title.split(' (')[0]}"):
                    with st.status("📥 جاري التحميل دابا..."):
                        dl_opts = {
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'outtmpl': 'temp_song.%(ext)s',
                            'nocheckcertificate': True,
                        }
                        
                        with yt_dlp.YoutubeDL(dl_opts) as ydl_dl:
                            ydl_dl.download([target_url])
                        
                        if os.path.exists("temp_song.mp3"):
                            with open("temp_song.mp3", "rb") as f:
                                st.success("✅ واجدة!")
                                st.download_button(
                                    label="📥 حفظ الأغنية في الآيفون",
                                    data=f,
                                    file_name=f"{selected_song_title}.mp3",
                                    mime="audio/mpeg"
                                )
                            os.remove("temp_song.mp3")

        except Exception as e:
            st.error("يوتيوب بلوكا العملية، جرب مورا شوية.")
