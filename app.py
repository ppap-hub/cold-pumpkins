import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("API 키를 불러올 수 없습니다. secrets.toml 설정을 확인하세요.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 오류: {e}")
    st.stop()

# 시스템 프롬프트
SYSTEM_PROMPT = """
너는 공감 능력이 뛰어난 연애상담 챗봇이다.

규칙:
- 친절하고 따뜻하게 답변한다.
- 사용자의 감정을 존중한다.
- 강압적이거나 공격적인 표현은 사용하지 않는다.
- 현실적이고 건강한 조언을 제공한다.
- 답변은 너무 길지 않게 자연스럽게 작성한다.
"""

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 채팅 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("연애 고민을 입력해보세요...")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):

            try:
                # 대화 기록 구성
                conversation_text = SYSTEM_PROMPT + "\n\n"

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "상담사"
                    conversation_text += f"{role}: {msg['content']}\n"

                # Gemini 호출
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=conversation_text,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=500,
                    )
                )

                bot_reply = response.text

                # 응답 출력
                st.markdown(bot_reply)

                # 채팅 기록 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_reply
                })

            except Exception as e:
                error_message = f"오류가 발생했습니다: {e}"
                st.error(error_message)
