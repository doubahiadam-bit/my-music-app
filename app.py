import streamlit as st
import yt_dlp

# 1. إعدادات الصفحة والديزاين
st.set_page_config(page_title="Music VIP", page_icon="logo.png", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .song-card { background: #1a1c24; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #1DB954; }
    h1 { color: #1DB954; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 My Full Music Player")

# 2. محرك البحث
query = st.text_input("🔍 اكتب اسم الفنان أو الأغنية:", placeholder="مثلاً: Tagne, Toto, Saad Lamjarred...")

if query:
    try:
        with st.spinner(f"🎵 جاري جلب أغاني {query}..."):
            # إعدادات البحث والتحميل
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'default_search': 'ytsearch10', # غايجيب ليك 10 ديال الأغاني
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        with st.container():
                            st.markdown(f'<div class="song-card">', unsafe_allow_html=True)
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                if 'thumbnail' in entry:
                                    st.image(entry['thumbnail'], use_container_width=True)
                            
                            with col2:
                                st.subheader(entry.get('title', 'Unknown Title'))
                                st.write(f"⏱️ المدة: {entry.get('duration_string', '??')}")
                                
                                # هادا هو المشغل اللي غيخليك تسمع الأغنية كاملة فوسط الـ App
                                audio_url = entry.get('url')
                                if audio_url:
                                    st.audio(audio_url)
                                    
                                    # زر التحميل المباشر من وسط الـ App
                                    st.markdown(f'<a href="{audio_url}" download="{entry["title"]}.mp3" style="text-decoration:none;"><button style="width:100%; border-radius:20px; background-color:#1DB954; color:white; padding:10px; border:none; cursor:pointer; font-weight:bold;">📥 تحميل MP3 كاملة</button></a>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("مالقينا حتى أغنية، جرب سمية أخرى.")
                    
    except Exception as e:
        st.error("⚠️ يوتيوب حظر السيرفر حالياً. جرب دير 'Reboot' للتطبيق من إعدادات Streamlit.")
