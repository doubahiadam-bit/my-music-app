import streamlit as st
import requests

# 1. إعدادات الصفحة والأيقونة (تأكد من رفع logo.png لـ GitHub)
try:
    st.set_page_config(
        page_title="Music VIP",
        page_icon="logo.png", 
        layout="wide"
    )
except:
    st.set_page_config(page_title="Music VIP", page_icon="🎵", layout="wide")

# 2. اللمسة السحرية للأيقونة في الآيفون (Apple Touch Icon)
st.markdown('<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/doubahiadam-bit/my-music-app/main/logo.png">', unsafe_allow_html=True)

# 3. دايزاين احترافي (CSS)
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    /* تنسيق الخانة ديال البحث */
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
        border-radius: 10px;
        border: 1px solid #1DB954;
    }
    /* تنسيق أزرار التحميل */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1ed760;
        transform: scale(1.05);
    }
    /* عنوان التطبيق */
    h1 {
        color: #1DB954;
        text-align: center;
        font-family: 'Arial Black';
        margin-bottom: 30px;
    }
    /* كرت الأغنية */
    .song-card {
        background-color: #1a1c24;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 My Music App")

# 4. محرك البحث
artist_query = st.text_input("👤 اكتب اسم الفنان أو الأغنية:", placeholder="مثلاً: Tagne, ElGrandeToto, Oumou Sangaré...")

if artist_query:
    # جلب البيانات من iTunes API (آمن، سريع، وأغاني كاملة)
    url = f"https://itunes.apple.com/search?term={artist_query}&entity=song&limit=30"
    
    try:
        with st.spinner("🔍 جاري جلب الأغاني..."):
            response = requests.get(url).json()
        
        if response.get('resultCount', 0) > 0:
            st.success(f"لقينا ليك {response['resultCount']} أغنية!")
            
            for song in response['results']:
                # عرض كل أغنية في إطار (Container)
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    
                    with col1:
                        # صورة الألبوم
                        st.image(song.get('artworkUrl100'), width=80)
                    
                    with col2:
                        # اسم الأغنية والألبوم
                        st.markdown(f"**{song.get('trackName')}**")
                        st.caption(f"Artist: {song.get('artistName')}")
                        st.caption(f"Album: {song.get('collectionName')}")
                    
                    with col3:
                        # زر التحميل المباشر
                        audio_url = song.get('previewUrl')
                        if audio_url:
                            audio_content = requests.get(audio_url).content
                            st.download_button(
                                label="📥 Download Full",
                                data=audio_content,
                                file_name=f"{song.get('trackName')}.mp3",
                                mime="audio/mpeg",
                                key=str(song.get('trackId'))
                            )
                st.markdown("---")
        else:
            st.warning("مالقينا والو، تأكد من السمية.")
            
    except Exception as e:
        st.error("السيرفر مشغول شوية، عاود جرب.")

# تذييل الصفحة
st.divider()
st.caption("Music App v2.0 - Created by Adam")
