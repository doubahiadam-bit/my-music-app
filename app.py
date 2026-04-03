import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music Downloader", page_icon="🎵")
st.title("🎵 Music Downloader")

song_name = st.text_input("اكتب اسم الأغنية (مثلاً: Saad Lamjarred Casablanca)")

if song_name:
    with st.status("🔍 جاري البحث والتحميل من السيرفر..."):
        # هاد الإعدادات هي "الضربة القاضية" للبلوك
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch1', # غايقلب غير على فيديو واحد باش ما يعيقش
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'quiet': True,
            'extract_audio': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128', # جودة متوسطة باش يكون التحميل سريع وما يتبلوكاش
            }],
            'outtmpl': 'mysong.%(ext)s',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

        try:
            # مسح أي ملف قديم باش ما يوقعش خلط
            if os.path.exists("mysong.mp3"):
                os.remove("mysong.mp3")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([song_name])
            
            if os.path.exists("mysong.mp3"):
                with open("mysong.mp3", "rb") as file:
                    st.success("✅ لقيناها!")
                    st.download_button(
                        label="📥 حفظ في الآيفون (Files)",
                        data=file,
                        file_name=f"{song_name}.mp3",
                        mime="audio/mpeg"
                    )
            else:
                st.error("❌ يوتيوب بلوكا السيرفر مؤقتاً. جرب تكتب سمية أغنية أخرى دابا.")

        except Exception as e:
            st.error("⚠️ وقع مشكل في الاتصال، جرب مرة أخرى مورا 10 ثواني.")
