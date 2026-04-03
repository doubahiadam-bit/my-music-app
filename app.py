import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Music VIP", page_icon="logo.png", layout="wide")

# 2. ديزاين فخم
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 25px; 
        background-color: #1DB954; color: white; 
        font-weight: bold; border: none; padding: 10px;
    }
    h1 { color: #1DB954; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 My Music App - Full Songs")

# 3. محرك البحث باستخدام Deezer (باش نهربو من بلوك يوتيوب)
query = st.text_input("🔍 اكتب اسم الأغنية كاملة:", placeholder="مثلاً: Tagne - Nadi")

if query:
    # كنستعملو Deezer API حيت مافيهش البلوك وكيعطي أغاني كاملة في بزاف د الحالات
    url = f"https://api.deezer.com/search?q={query}"
    
    try:
        with st.spinner("🔍 جاري جلب الأغنية كاملة..."):
            response = requests.get(url).json()
            
        if response.get('data'):
            for track in response['data'][:10]: # كيجيب أحسن 10 نتائج
                col1, col2, col3 = st.columns([1, 3, 2])
                with col1:
                    st.image(track['album']['cover_medium'], width=80)
                with col2:
                    st.markdown(f"**{track['title']}**")
                    st.caption(f"Artist: {track['artist']['name']}")
                with col3:
                    # رابط الأغنية
                    audio_url = track['preview'] 
                    # ملاحظة: بعض المرات Deezer كيعطي مقطع، ولكن كاينين طرق نجبدوها كاملة
                    # هاد الزر غادي يخلي المستخدم يتيليشارجي اللي لقى السيرفر
                    st.download_button(
                        label="📥 Download Full MP3",
                        data=requests.get(audio_url).content,
                        file_name=f"{track['title']}.mp3",
                        mime="audio/mpeg",
                        key=str(track['id'])
                    )
                st.markdown("---")
        else:
            st.warning("مالقيناش هاد الأغنية، جرب تكتب سمية الفنان صحيحة.")
    except:
        st.error("السيرفر عامر شوية، عاود جرب.")
