import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# 유튜브 비디오 ID 추출
def get_video_id(youtube_url):
    if "v=" in youtube_url:
        return youtube_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        return youtube_url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("유효한 유튜브 URL이 아닙니다.")

# 유튜브 자막 추출 (언어를 지정)
def get_transcript(youtube_url, language='ko'):  # 기본 언어는 'ko' (Korean)
    video_id = get_video_id(youtube_url)
    try:
        # 자막 가져오기 (언어 코드로 자막 요청)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        return formatted_transcript
    except Exception as e:
        return f"자막을 가져오는 데 실패했습니다: {e}"

# Streamlit 웹 앱
st.title("회세밥 YouTube 자막 추출기")

# 유튜브 URL 입력
youtube_url = st.text_input("유튜브 URL을 입력하세요:")

# 언어 선택
language = st.selectbox("자막 언어를 선택하세요:", ["ko", "en", "ja", "es", "fr", "de", "zh-Hans"])

# 자막 추출 버튼 클릭 시 처리
if st.button("자막 추출"):
    if youtube_url:
        transcript_text = get_transcript(youtube_url, language)
        st.subheader("추출된 자막:")
        st.text_area("자막", transcript_text, height=300)
    else:
        st.error("유튜브 URL을 입력해주세요.")

