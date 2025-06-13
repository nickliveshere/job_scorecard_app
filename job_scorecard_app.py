import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Job Scorecard", layout="wide")
    st.title("\U0001F4BC Job Offer Balanced Scorecard")
    st.markdown("Customize weights, enter offer names, and score them against key criteria.")

    scorecard = {
        "Salary": ["Salary"],
        "Development Opportunities": ["Development Opportunities"],
        "Work Environment": ["Work Environment"],
        "Remote & Hours": ["Remote & Hours"],
        "Company Outlook": ["Company Outlook"]
    }

    st.sidebar.header("Perspective Weights (must total 100%)")
    weights = {}
    total_weight = 0
    for p in scorecard:
        w = st.sidebar.slider(p, 0, 100, 20, key=f"weight_{p}")
        weights[p] = w
        total_weight += w

    if total_weight != 100:
        st.sidebar.error(f"Total must be 100% (currently {total_weight}%)")
        return

    st.sidebar.header("Offers")
    num_offers = st.sidebar.number_input("# of Offers", min_value=1, max_value=5, value=2)
    offer_names = [st.sidebar.text_input(f"Offer {i+1} Name", value=f"Offer {chr(65+i)}") for i in range(num_offers)]

    results = {}
    scores_table = []

    for offer in offer_names:
        st.subheader(f"\U0001F4CB {offer} Scores")
        offer_total = 0
        for p, criteria in scorecard.items():
            p_score = sum([
                st.slider(f"{offer} – {c}", 1, 5, 3, key=f"{offer}_{p}_{c}") for c in criteria
            ])
            avg = p_score / len(criteria)
            weighted = avg * (weights[p] / 100)
            offer_total += weighted
        results[offer] = round(offer_total, 2)
        scores_table.append({"Offer": offer, "Score": round(offer_total, 2)})

    st.markdown("---")
    st.header("\U0001F4C8 Final Summary")
    df = pd.DataFrame(scores_table).sort_values(by="Score", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()