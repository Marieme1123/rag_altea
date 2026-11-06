# ============================================================
# ÉTAPE 8 - MISE À DISPOSITION
# Q12. Complétez app.py et lancez-le avec : streamlit run app.py
#      Faites une capture d'écran d'une réponse avec ses sources.
# ============================================================
import streamlit as st

from etape6_generation import repondre

st.set_page_config(page_title="Assistant Altéa", page_icon="💬")
st.title("Assistant documentation Altéa Services")
st.caption("Posez une question : la réponse vient de la documentation interne, avec ses sources.")

service = st.sidebar.selectbox("Service", ["Tous", "RH", "IT", "General"])
k = st.sidebar.slider("Nombre d'extraits utilisés (k)", 1, 10, 3)

question = st.text_input("Votre question", placeholder="Ex : Combien de jours de télétravail par semaine ?")

if question:
    with st.spinner("Recherche et rédaction de la réponse..."):
        res = repondre(question, k=k, service=None if service == "Tous" else service)

    st.subheader("Réponse")
    st.write(res["reponse"])

    st.subheader("Sources")
    for s in res["sources"]:
        with st.expander(f"{s['source']} (page {s['page']}, {s['service']}) - score {s['score']:.2f}"):
            st.write(s["texte"])
