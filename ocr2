import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import io

# 제목 설정
st.title("OCR 이미지 글자인식 앱")

# 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    try:
        # 이미지 표시
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_container_width=True)

        # 이미지를 numpy 배열로 변환
        image_np = np.array(image)

        # 로딩 상태 표시
        with st.spinner("텍스트를 인식 중입니다..."):
            # EasyOCR 초기화
            reader = easyocr.Reader(['ko', 'en'])  # 한국어와 영어 지원
            # numpy 배열을 사용하여 텍스트 인식
            results = reader.readtext(image_np)

        # 결과 출력
        st.write("인식된 텍스트:")
        if results:
            for (bbox, text, prob) in results:
                st.text(f"{text}")
        else:
            st.warning("이미지에서 텍스트를 인식하지 못했습니다.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
else:
    st.info("이미지를 업로드하면 결과를 확인할 수 있습니다.")
