import streamlit as st
import random
from openai import OpenAI
import time

# OpenAI API 키 설정
client = OpenAI(
    api_key = st.secrets["openai"]["api_key"]
)

# 카드 뒷면 SVG 정의
CARD_BACK_SVG = '''
<div class="card-back">
  <svg viewBox="0 0 100 140">
    <rect width="100" height="140" rx="10" fill="#2a0845"/>
    <rect x="5" y="5" width="90" height="130" rx="8" fill="none" stroke="#9d4edd" stroke-width="2"/>
    <path d="M 50 45 L 57 65 L 78 65 L 61 78 L 68 98 L 50 85 L 32 98 L 39 78 L 22 65 L 43 65 Z" 
        fill="none" stroke="#9d4edd" stroke-width="2"/>
    <circle cx="15" cy="15" r="5" fill="#9d4edd"/>
    <circle cx="85" cy="15" r="5" fill="#9d4edd"/>
    <circle cx="15" cy="125" r="5" fill="#9d4edd"/>
    <circle cx="85" cy="125" r="5" fill="#9d4edd"/>
    </svg>
</div>
'''

# [메이저 아르카나 카드 정의와 마이너 아르카나 카드 정의는 동일하게 유지]
[이전 코드의 major_arcana와 minor_arcana 딕셔너리를 그대로 유지]

def get_all_cards():
    """모든 카드 목록을 반환하는 함수"""
    all_cards = []
    
    # 메이저 아르카나 카드 추가
    for card_num, card_info in major_arcana.items():
        all_cards.append({
            "type": "Major Arcana",
            "name": card_info["name"],
            "forward": card_info["forward"],
            "reversed": card_info["reversed"]
        })
    
    # 마이너 아르카나 카드 추가
    for suit, cards in minor_arcana.items():
        for rank, meanings in cards.items():
            all_cards.append({
                "type": "Minor Arcana",
                "suit": suit,
                "rank": rank,
                "name": f"{rank} of {suit}",
                "forward": meanings["forward"],
                "reversed": meanings["reversed"]
            })
    
    return all_cards

def get_random_card_info(card):
    """카드에 랜덤한 방향을 추가하는 함수"""
    direction = random.choice(['forward', 'reversed'])
    card_info = card.copy()
    card_info['direction'] = direction
    card_info['interpretation'] = card_info['forward'] if direction == 'forward' else card_info['reversed']
    return card_info

def display_card_grid(available_cards):
    """카드를 그리드 형태로 표시하는 함수"""
    cols_per_row = 5
    
    st.markdown("""
        <style>
        div[data-testid="column"] > div:has(button) {
            height: 100%;
        }
        .stButton > button {
            background-color: transparent;
            border: none;
            width: 100%;
            height: 100%;
            padding: 5px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            transition: transform 0.2s;
            background-color: rgba(157, 78, 221, 0.1);
        }
        .stButton > button > div {
            width: 100%;
        }
        .card-number {
            margin-top: 5px;
            text-align: center;
            color: #9d4edd;
        }
        .card-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    selected_card = None
    
    for i in range(0, len(available_cards), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(available_cards):
                card = available_cards[i + j]
                with col:
                    container = st.container()
                    with container:
                        st.markdown(CARD_BACK_SVG, unsafe_allow_html=True)
                        st.markdown(f'<p style="text-align: center; color: #9d4edd;">카드 {i + j + 1}</p>', unsafe_allow_html=True)
                        if st.button("선택", key=f"card_{i}_{j}", use_container_width=True):
                            selected_card = card
    
    return selected_card

def generate_ai_interpretation(question, cards):
    cards_info = "\n".join([f"- {card['name']} ({card['direction']}): {card['interpretation']}" for card in cards])

    with st.spinner("해석중이다냥😾 기다려라냥! 🐾"):
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "당신은 타로카드 해석가입니다. 사용자가 뽑은 카드와 질문을 기반으로 해석을 제공합니다. 모든 문장은 '~다'로 끝나며, 그 뒤에 '냥'을 붙여서 말해줘. '있어냥'과 같은 표현은 사용하지 말고, 모든 문장은 '냥'으로 끝내야 한다냥. 문단 마지막에 고양이 이모지(예: 🐱, 😺, 😼, 😻)를 자연스럽게 넣어줘. 마지막 새로운 줄에 '내 해석이 어떠냥😼'으로 끝내줘. 만약 이해할 수 없는 질문이나 타로와 상관없는 질문을 하면 해석하지 말고 '나를 바보로 아냐냥!👿'만 출력해줘"},
                {"role": "user", "content": f"질문: {question}\n카드: {cards_info}\n이 카드를 기반으로 해석을 해주세요."}
            ],
            model="gpt-4o-mini",
        )
        return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🔮 냥타로")
st.subheader("오백냥을 내면 뭐든지 알려주겠다냥!😼🐾")

# 세션 스테이트 초기화
if 'asked_questions' not in st.session_state:
    st.session_state.asked_questions = set()
if 'selected_cards' not in st.session_state:
    st.session_state.selected_cards = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""

# 사용자의 질문 입력
question = st.text_input("묻고 싶은게 뭐냥😸")

if question:
    # 질문이 바뀌었을 때 카드 초기화
    if question != st.session_state.current_question:
        st.session_state.selected_cards = []
        st.session_state.current_question = question
    
    # 질문 중복 체크
    if question in st.session_state.asked_questions:
        st.error("나를 바보로 아는거냥!😾")
    else:
        st.divider()
        
        # 카드 선택 UI
        if len(st.session_state.selected_cards) < 3:
            st.write(f"### {len(st.session_state.selected_cards) + 1}번째 카드를 선택하라냥")
            available_cards = [card for card in get_all_cards() 
                            if card not in st.session_state.selected_cards]
            
            selected_card = display_card_grid(available_cards)
            if selected_card:
                card_info = get_random_card_info(selected_card)
                st.session_state.selected_cards.append(card_info)
                st.rerun()

        # 카드가 선택되었다면 결과 표시
        if st.session_state.selected_cards:
            st.divider()
            st.header("오호라🐱")
            for idx, card in enumerate(st.session_state.selected_cards, 1):
                direction_text = "정방향" if card['direction'] == 'forward' else "역방향"
                st.write(f"**{idx}. {card['name']}** ({direction_text}): {card['interpretation']}")
            
            # 모든 카드가 선택되었을 때만 해석 표시
            if len(st.session_state.selected_cards) == 3:
                st.divider()
                st.header("의미를 알려주겠다냥!😺")
                ai_interpretation = generate_ai_interpretation(question, st.session_state.selected_cards)
                st.write(ai_interpretation)
                
                # 해석이 완료되면 질문을 기록
                st.session_state.asked_questions.add(question)
            
                # 리셋 버튼
                if st.button("다시 보겠다냥!"):
                    st.session_state.selected_cards = []
                    st.session_state.current_question = ""
                    st.rerun()