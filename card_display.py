import streamlit as st
import random
from tarot_cards import get_random_card_info


def display_card_grid(available_cards):
    shuffled_cards = available_cards.copy()
    random.shuffle(shuffled_cards)
    cols = st.columns(8)

    if "selected_positions" not in st.session_state:
        st.session_state.selected_positions = set()

    st.markdown(
        """
        <style>
        .card-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 80px;
            margin: 0 auto;
            gap: 5px;
        }
        .card {
            width: 80px;
            height: 112px;
            margin: 0;
            padding: 0;
        }
        .selected-card {
            filter: grayscale(100%);
        }
        .st-emotion-cache-1r6slb0 {
            gap: 0.5rem !important;
        }
        .stButton button:disabled {
            background-color: #e0e0e0 !important;
            color: #888888 !important;
            opacity: 0.7;
            cursor: not-allowed;
            border-color: #cccccc !important;
        }
        .stButton button:disabled:hover {
            background-color: #e0e0e0 !important;
            color: #888888 !important;
            border-color: #cccccc !important;
        }
        .stButton button {
            min-height: 0px !important;
            width: 40px !important;
            padding: 0px 8px !important;
            margin: 2px auto !important;
            line-height: 1.6 !important;
            display: block !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    for i, card in enumerate(shuffled_cards):
        col = cols[i % 8]
        with col:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)

            is_selected = i in st.session_state.selected_positions

            st.markdown(
                f"""
                <div class="card {'selected-card' if is_selected else ''}">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 140" width="80" height="112">
                        <rect width="100" height="140" rx="10" fill="#2a0845"/>
                        <rect x="5" y="7" width="90" height="126" rx="8" fill="none" stroke="#9d4edd" stroke-width="2"/>
                        <path d="M50 45L57 65L78 65L61 78L68 98L50 85L32 98L39 78L22 65L43 65Z" fill="none" stroke="#9d4edd" stroke-width="2"/>
                        <circle cx="15" cy="15" r="5" fill="#9d4edd"/>
                        <circle cx="85" cy="15" r="5" fill="#9d4edd"/>
                        <circle cx="15" cy="125" r="5" fill="#9d4edd"/>
                        <circle cx="85" cy="125" r="5" fill="#9d4edd"/>
                        <text x="50" y="135" fill="#9d4edd" font-size="8" text-anchor="middle">카드 {i + 1}</text>
                    </svg>
                </div>
            """,
                unsafe_allow_html=True,
            )

            st.button("💜", key=f"card_{i}", disabled=is_selected)

            st.markdown("</div>", unsafe_allow_html=True)

            if not is_selected and st.session_state.get(f"card_{i}"):
                card_info = get_random_card_info(card)
                st.session_state.selected_cards.append(card_info)
                st.session_state.selected_positions.add(i)
                st.rerun()
