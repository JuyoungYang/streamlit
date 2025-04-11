import streamlit as st
from tarot_cards import get_all_cards, get_random_card_info
from interpretation import generate_ai_interpretation
from card_display import display_card_grid

st.set_page_config(page_title="냥타로", page_icon="🔮")
st.write("앱 시작!")

# 이미지와 타이틀 표시
try:
    with open("images/cat_tarot.jpg", "rb") as file:
        image_bytes = file.read()
    st.image(image_bytes, use_container_width=True)
except Exception as e:
    st.error("이미지를 불러올 수 없습니다.")
    print(f"이미지 로드 에러: {e}")

st.title("🔮 냥타로")
st.subheader("오백냥을 내면 뭐든지 알려주겠다냥!😼🐾")

if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()
if "selected_cards" not in st.session_state:
    st.session_state.selected_cards = []
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "selected_positions" not in st.session_state:
    st.session_state.selected_positions = set()

question = st.text_input(
    "궁금한걸 묻고 카드 3장을 뽑으면 된다냥!", key="question_input"
)

if question:
    if question != st.session_state.current_question:
        st.session_state.selected_cards = []
        st.session_state.selected_positions = set()
        st.session_state.current_question = question

    if question in st.session_state.asked_questions:
        st.error("나를 바보로 아는거냥!😾")
    else:
        st.divider()

        if len(st.session_state.selected_cards) < 3:
            st.write(
                f"### {len(st.session_state.selected_cards) + 1}번째 카드를 선택하라냥"
            )
            available_cards = [
                card
                for card in get_all_cards()
                if not any(
                    c["name"] == card["name"] for c in st.session_state.selected_cards
                )
            ]
            display_card_grid(available_cards)

        if st.session_state.selected_cards:
            for idx, card in enumerate(st.session_state.selected_cards, 1):
                direction_text = (
                    "정방향" if card["direction"] == "forward" else "역방향"
                )
                st.write(
                    f"**{idx}. {card['name']}** ({direction_text}): {card['interpretation']}"
                )

            if len(st.session_state.selected_cards) == 3:
                st.divider()
                st.header("의미를 알려주겠다냥!😺")
                ai_interpretation = generate_ai_interpretation(
                    question, st.session_state.selected_cards
                )
                st.write(ai_interpretation)
                st.session_state.asked_questions.add(question)

                if st.button("츄르값 주고 물어봐라냥😼!"):
                    st.session_state.selected_cards = []
                    st.session_state.current_question = ""
                    st.session_state.question_input = ""
                    st.rerun()
