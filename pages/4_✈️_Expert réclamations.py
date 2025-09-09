import streamlit as st
import requests
import time
from dotenv import dotenv_values

# Demo metadata for search and filtering
DEMO_METADATA = {
    "categories": ["Technical"],
    "tags": ["Data Science", "Analytics", "Machine Learning"]
}

# Load environment
env = dotenv_values(".env")
# SnapLogic RAG pipeline
URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/Aleksandra%20Kulawska/tsa_claims/TSAAgent"
BEARER_TOKEN = "i1nVy1k0xi9ot9G0BM8FTPOoccRe4nOw"
timeout = 300

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

st.set_page_config(page_title="Assistant en Data Science")
st.title("Assistant IA pour l’analyse des réclamations TSA")
st.markdown("""  
    ### L’assistant IA qui transforme vos questions en insights précis sur les réclamations TSA, sans besoin de requêtes complexes
    Il analyse actuellement les données des réclamations de l’agence américaine responsable de la sécurité des transports - TSA. Posez vos questions en langage naturel et obtenez des insights précis automatiquement.
    
    Exemples de requêtes :
    - Quels sont les trois aéroports avec le plus grand nombre de réclamations ?
    - Quels sont les types de réclamations les plus fréquents dans les grands aéroports ?
    - Quels aéroports ont les taux de refus de réclamations les plus élevés ?
""")

# Initialize chat history and toggle states
if "data_analytics" not in st.session_state:
    st.session_state.data_analytics = []
if "toggle_states" not in st.session_state:
    st.session_state.toggle_states = {}

# Display chat messages from history
for idx, message in enumerate(st.session_state.data_analytics):
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message.get("answer", message.get("content", "")))
            if message.get("summary"):
                toggle_key = f"toggle_{idx}"
                if st.toggle("Show thinking process", False, key=toggle_key):
                    st.markdown("### Agent's Thought Process")
                    st.markdown(message["summary"])
        else:
            st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Posez moi vos questions sur les réclamations TSA")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.data_analytics.append({"role": "user", "content": prompt})
    with st.spinner("Working..."):
        data = {"prompt": prompt}
        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        response = requests.post(
            url=URL,
            data=data,
            headers=headers,
            timeout=timeout,
            verify=False
        )
        if response.status_code == 200:
            try:
                result = response.json()
                if len(result) > 0 and isinstance(result[0], dict):
                    response_data = result[0]
                    answer = response_data.get("answer", "")
                    summary = response_data.get("summary", "")
                    
                    with st.chat_message("assistant"):
                        typewriter(text=answer, speed=10)
                        if summary:
                            toggle_key = f"toggle_{len(st.session_state.data_analytics)}"
                            if st.toggle("Show thinking process", False, key=toggle_key):
                                st.markdown("### Agent's Thought Process")
                                st.markdown(summary)
                    
                    st.session_state.data_analytics.append({
                        "role": "assistant",
                        "answer": answer,
                        "summary": summary
                    })
                else:
                    with st.chat_message("assistant"):
                        st.error("❌ Invalid response format from API")
            except ValueError:
                with st.chat_message("assistant"):
                    st.error("❌ Invalid JSON response from API")
        else:
            st.error("❌ Error while calling the SnapLogic API")
        st.rerun()
