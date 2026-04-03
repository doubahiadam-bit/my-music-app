import streamlit as st
from youtubesearchpython import VideosSearch
import yt_dlp

st.set_page_config(page_title="Music VIP", page_icon="logo.png")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-card { background: #1a1c24; padding: 20px; border-radius: 15px; border: 1px solid #1DB954; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Full Music Downloader")

query = st.text_input("🔍 اكتب اسم الأغنية كاملة:", placeholder="مثلاً: Tagne - Nadi")

if query:
    try:
        # البحث عن الأغنية في يوتيوب
        search = VideosSearch(query, limit=1)
        result = search.result()['result']

        if result:
            song = result[0]
            st.image(song['thumbnails'][0]['url'], width=200)
            st.write(f"### {song['title']}")
            st.write(f"⏱️ المدة: {song['duration']}")
            
            link = song['link']
            
            # محاولة التحميل
            if st.button("🚀 ابدأ التحميل الآن (Full MP3)"):
                with st.spinner("جاري تجهيز الملف..."):
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(link, download=False)
                        # كنعطيو للمستخدم الرابط المباشر باش يتيليشارجي من عندو (ما يتبلوكاش السيرفر)
                        audio_url = info['url']
                        st.success("لقينا الأغنية!")
                        st.audio(audio_url)
                        st.markdown(f'<a href="{audio_url}" download="{song["title"]}.mp3" style="text-decoration:none;"><button style="width:100%; border-radius:20px; background-color:#1DB954; color:white; padding:10px; border:none; cursor:pointer;">📥 اضغط هنا للتحميل المباشر</button></a>', unsafe_allow_html=True)
        else:
            st.error("مالقينا والو.")
    except Exception as e:
        st.error("يوتيوب حظر السيرفر حالياً. جرب مورا 5 دقايق.")
