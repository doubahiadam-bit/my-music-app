import streamlit as st
import requests

st.set_page_config(page_title="Music VIP", page_icon="logo.png")

st.title("🎵 Full Music Downloader (V3)")

query = st.text_input("🔍 اكتب اسم الأغنية كاملة:")

if query:
    # هاد الـ API كيجيب معلومات الأغنية من يوتيوب بلا بلوك
    search_url = f"https://api.deezer.com/search?q={query}"
    
    try:
        response = requests.get(search_url).json()
        if response['data']:
            track = response['data'][0]
            st.image(track['album']['cover_medium'])
            st.write(f"### {track['title']} - {track['artist']['name']}")
            
            # هنا كنعطيوه رابط الأغنية (غالباً كيكون كامل في Deezer API)
            audio_url = track['preview'] 
            st.audio(audio_url)
            
            st.info("إلا عطاك غير 30 ثانية، جرب تخدم بـ 'YouTube Link' وفتحو في موقع downloader خارجي.")
        else:
            st.error("مالقينا والو.")
    except:
        st.error("مشكل في السيرفر.")
