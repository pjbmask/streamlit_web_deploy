import streamlit as st

def normalize_text(text):
    """
    입력 텍스트를 정규화: 공백 제거 및 소문자 변환
    """
    import re
    # 여러 개의 공백을 단일 공백으로 치환
    text = re.sub(r"\s+", " ", text)
    # 양쪽 공백 제거 및 소문자로 변환
    text = text.strip().lower()
    return text

from rapidfuzz import fuzz

def get_response(user_input):
    """
    사용자 입력에 가장 적합한 답변 반환
    """
    # 유형자산 회계처리 관련 정보
    asset_info = {
        "정의": "유형자산은 기업이 영업활동에 사용할 목적으로 보유하는 물리적 실체가 있는 자산입니다.",
        "감가상각": "감가상각은 정액법, 정률법 등 다양한 방법으로 계산되며, 자산의 내용연수 동안 비용으로 배분됩니다.",
        "취득원가": "취득원가는 구매 가격, 부대비용, 설치비용 등이 포함됩니다.",
        "잔존가치": "잔존가치는 자산 사용 후 남는 가치로, 감가상각 계산 시 고려됩니다.",
        "재평가": "유형자산은 공정가치로 재평가할 수 있으며, 재평가 차익은 기타포괄손익으로 처리됩니다.",
        "손상": "유형자산의 장부금액이 회수가능액보다 큰 경우 손상차손을 인식합니다."
    }

    # 질문 키워드 정의
    questions = {
        "정의": ["유형자산?","정의", "무엇인가요"],
        "감가상각": ["감가상각", "감가", "상각 방법"],
        "취득원가": ["취득원가", "구매 비용", "포함 항목"],
        "잔존가치": ["잔존가치", "내용연수", "남는 가치"],
        "재평가": ["재평가", "공정가치", "재평가 차익"],
        "손상": ["손상", "손상차손", "회수가능액"]
    }

    # 입력 텍스트 정규화
    user_input = normalize_text(user_input)

    # 퍼지 매칭으로 가장 적합한 키워드 찾기
    best_match = None
    highest_score = 0
    for key, keywords in questions.items():
        for keyword in keywords:
            score = fuzz.partial_ratio(user_input, keyword)
            if score > highest_score:
                highest_score = score
                best_match = key

    # 유사도가 높은 키워드에 대한 응답 반환
    if best_match and highest_score > 70:  # 유사도가 70% 이상인 경우만 응답 제공
        return asset_info[best_match]
    else:
        return "죄송합니다, 그 질문에 대한 정보는 없습니다. 다른 것을 물어봐 주세요."

# Streamlit 애플리케이션 생성
st.title("유형자산 회계처리 챗봇")
user_input = st.text_input("유형자산 회계처리에 대해 무엇이 궁금하신가요?")

if user_input:
    response = get_response(user_input)
    st.write(response)