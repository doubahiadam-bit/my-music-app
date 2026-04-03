import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music Hub", page_icon="🎧")
st.title("🎧 Music Downloader Pro")

# 1. خانة البحث عن الفنان
artist_query = st.text_input("اكتب سمية المغني (مثلاً: ElGrandeToto):")

if artist_query:
    # إعدادات البحث السريع
    search_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch10',
        'quiet': True,
        'extract_flat': True,
        'nocheckcertificate': True,
    }

    try:
        with st.status(f"🔍 جاري جلب أغاني {artist_query}..."):
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                result = ydl.extract_info(f"ytsearch10:{artist_query}", download=False)
                songs = result['entries']
        
        # تحويل النتائج لقاموس (Dictionary) باش نعقلو عليهم
        song_options = {s.get('title'): s.get('url') for s in songs}
        
        # 2. قائمة الاختيار
        selected_title = st.selectbox("اختار الأغنية اللي بغيتي:", ["--- اختر الأغنية ---"] + list(song_options.keys()))

        if selected_title != "--- اختر الأغنية ---":
            target_url = song_options[selected_title]
            
            # 3. زر التحميل الحقيقي
            if st.button(f"🚀 ابدأ تحميل: {selected_title[:30]}..."):
                with st.spinner("📥 جاري تحويل الصوت... تسنى شوية"):
                    dl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'downloaded_song.%(ext)s',
                        'nocheckcertificate': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                    }
                    
                    try:
                        # مسح أي ملف قديم
                        if os.path.exists("downloaded_song.mp3"):
                            os.remove("downloaded_song.mp3")
                            
                        with yt_dlp.YoutubeDL(dl_opts) as ydl_dl:
                            ydl_dl.download([target_url])
                        
                        # ظهور زر الحفظ في الآيفون (هذا هو اللي كيهمنا)
                        if os.path.exists("downloaded_song.mp3"):
                            with open("downloaded_song.mp3", "rb") as f:
                                st.success("✅ الأغنية واجدة!")
                                st.download_button(
                                    label="📥 اضغط هنا لحفظها في الآيفون",
                                    data=f,
                                    file_name=f"{selected_title}.mp3",
                                    mime="audio/mpeg"
                                )
                    except Exception as e:
                        st.error(f"يوتيوب رفض الطلب: {e}")

    except Exception as e:
        st.error("مشكل في البحث، جرب تعاود تـشارجي الصفحة.")

st.divider()
st.caption("نصيحة: ملي تضغط على 'حفظ'، الأغنية غاتلقاها في تطبيق Files (Fichiers) في الآيفون.")
