import streamlit as st
import requests
import os

st.set_page_config(page_title="Music Downloader", page_icon="🎵")
st.title("🎵 Music Downloader Pro")
st.write("كتب سمية الأغنية وغادي نلقاوها ليك!")

query = st.text_input("اسم الأغنية أو الفنان:", placeholder="مثال: Tagne Nadi")

if query:
    # هاد الرابط هو محرك بحث موسيقي كيخدم بـ API فابور
    search_url = f"https://api.deezer.com/search?q={query}&limit=5"
    
    try:
        response = requests.get(search_url).json()
        if response.get('data'):
            st.success(f"لقينا 5 ديال النتائج لـ '{query}':")
            
            for song in response['data']:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{song['title']}** - {song['artist']['name']}")
                with col2:
                    # التحميل المباشر من سيرفر Deezer (ما كيبلوكيش)
                    audio_url = song['preview']
                    audio_data = requests.get(audio_url).content
                    st.download_button(
                        label="📥 تحميل",
                        data=audio_data,
                        file_name=f"{song['title']}.mp3",
                        mime="audio/mpeg",
                        key=song['id']
                    )
                st.divider()
        else:
            st.warning("مالقينا والو، جرب سمية أخرى.")
            
    except Exception as e:
        st.error("وقع مشكل في السيرفر، عاود جرب.")

st.caption("هاد النسخة كتخدم بسيرفرات Deezer باش نتفاداو بلوك يوتيوب.")
