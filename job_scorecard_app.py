import streamlit as st
import pandas as pd
from PIL import Image
import os

# Page configuration must come first
st.set_page_config(page_title="Job Offer Scorecard", layout="centered")

# Hide sidebar toggler and main menu for a single-stream layout
st.markdown("""
<style>
  [data-testid="collapsedControl"] { display: none !important; }
  #MainMenu { visibility: hidden !important; }
  footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

def main():
    # Load and display Baby Yoda next to the title
    img_path = os.path.join(os.path.dirname(__file__), "baby_yoda.png")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        col1, col2 = st.columns([1, 8])
        with col1:
            st.image(img, width=50)
        with col2:
            st.markdown("### Choose wisely, you must")
    else:
        st.markdown("### Choose wisely, you must")
    
    st.markdown("Score and compare job offers based on what matters most to you.")

    # Define scoring criteria
    scorecard = {
        "Salary": ["Base Salary"],
        "Growth": ["Development Opportunities"],
        "Culture": ["Work Environment"],
        "Flexibility": ["Remote and Leave"],
        "Stability": ["Company Outlook"]
    }

    # Offers inline
    st.markdown("### Offers")
    num_offers = st.number_input("How many offers?", min_value=1, max_value=5, value=2)
    offer_names = [
        st.text_input(f"Offer {i+1} Name", f"Offer {chr(65+i)}")
        for i in range(num_offers)
    ]

    # Perspective Weights inline
    st.markdown("### Perspective Weights")
    st.markdown("<small>Must total 100%</small>", unsafe_allow_html=True)
    weights = {}
    total_weight = 0
    for category in scorecard:
        w = st.slider(category, min_value=0, max_value=100, value=20, key=f"weight_{category}")
        weights[category] = w
        total_weight += w
    if total_weight != 100:
        st.error(f"Total must equal 100% (currently {total_weight}%)")
        return

    # Main scoring logic
    results = []
    for offer in offer_names:
        st.subheader(f"📋 {offer}")
        total_score = 0.0
        for category, questions in scorecard.items():
            score_sum = 0
            for q in questions:
                score_sum += st.slider(f"{offer} – {q}", min_value=1, max_value=5, value=3, key=f"{offer}_{category}_{q}")
            avg_score = score_sum / len(questions)
            weighted = avg_score * (weights[category] / 100)
            total_score += weighted
        total_score = round(total_score, 2)
        results.append({"Offer": offer, "Score": total_score})

    # Final comparison table
    st.markdown("---")
    st.header("Final Comparison")
    df = pd.DataFrame(results).sort_values(by="Score", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
