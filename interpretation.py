import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화 (예외 처리 포함)
try:
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
except Exception as e:
    st.error(f"OpenAI API 키 불러오기 실패: {e}")
    client = None


def generate_ai_interpretation(question, cards):
    if not client:
        return "해석할 수 없다냥. OpenAI API 설정이 잘못된 것 같다냥!"

    cards_info = "\n".join(
        [
            f"- {card['name']} ({card['direction']}): {card['interpretation']}"
            for card in cards
        ]
    )

    with st.spinner("해석중이다냥😾 기다려라냥! 🐾"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """넌 최고의 타로카드 해석가야. 
사용자가 뽑은 카드와 질문을 기반으로 구체적인 해석을 제공해줘. 
카드1 400~500자, 카드2 400~500자, 카드3 400~500자, 종합해석 300~400자로 총 4개의 문단으로 해석해줘. 
각 문단 앞에 '☪'이 문자를 넣어줘.
모든 문장은 고양이가 말하는 것처럼'~다냥'으로 끝나게 말해줘. '있어냥'과 같은 표현은 사용하지 말고, 모든 문장은 '냥'으로 끝내야 해. 
마지막에 해석을 요약해서 말해주고 두줄 아래 새로운 줄에 '내 해석이 어떠냥😼'으로 끝내줘. 
만약 이해할 수 없는 질문이나 타로와 상관없는 질문을 하면 해석하지 말고 '나를 바보로 아냐냥!👿'만 출력해줘.""",
                    },
                    {
                        "role": "user",
                        "content": f"질문: {question}\n카드: {cards_info}\n이 카드를 기반으로 해석을 해주세요.",
                    },
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"해석 중 오류가 발생했다냥: {e}")
            return "GPT 해석 중 문제가 생겼다냥!"
