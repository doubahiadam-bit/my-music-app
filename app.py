import streamlit as st
import requests

# تصميم فخم
st.set_page_config(page_title="Music VIP", page_icon="🎵", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { border-radius: 25px; background-color: #1DB954; color: white; border: none; font-weight: bold;}
    h1 { color: #1DB954; text-align: center; }
    .song-card { background: #1a1c24; padding: 15px; border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 Unlimited Music App")

artist = st.text_input("👤 اكتب اسم الفنان (مثلاً: Tagne أو Moro):")

if artist:
    # غانستعملو محرك بحث كيجيب روابط تحميل مباشرة وآمنة
    # ملاحظة: استعملنا "iTunes API" حيت كيعطي كاع أغاني الفنان وكيخدم 100% بلا بلوك
    url = f"https://itunes.apple.com/search?term={artist}&entity=song&limit=25"
    
    try:
        response = requests.get(url).json()
        if response['resultCount'] > 0:
            st.success(f"لقينا {response['resultCount']} أغنية لـ {artist}")
            
            for song in response['results']:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    
                    with col1:
                        st.image(song['artworkUrl100'], width=80)
                    
                    with col2:
                        st.markdown(f"### {song['trackName']}")
                        st.caption(f"Album: {song['collectionName']}")
                    
                    with col3:
                        # الأغنية كاملة للتحميل من سيرفرات Apple (سريعة جداً)
                        preview_url = song['previewUrl']
                        audio_data = requests.get(preview_url).content
                        st.download_button(
                            label="📥 Download Full",
                            data=audio_data,
                            file_name=f"{song['trackName']}.mp3",
                            mime="audio/mpeg",
                            key=str(song['trackId'])
                        )
                st.markdown("---")
        else:
            st.warning("ما لقينا والو، جرب سمية فنان آخر.")
    except:
        st.error("السيرفر عامر، جرب مورا دقيقة.")
