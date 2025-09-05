import streamlit as st
import requests
import time
from dotenv import dotenv_values

# Demo metadata for search and filtering
DEMO_METADATA = {
    "categories": ["Technical"],
    "tags": ["SnapLogic", "Expert", "Support"]
}

# Load environment
env = dotenv_values(".env")
URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/snapLogic4snapLogic/AutoRFPAgent/ApiRfpAgent"
BEARER_TOKEN = "nNpLBJrd8FAtFh3TVC9xR97QAwWtJHgF"
timeout = 300

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

st.set_page_config(page_title="L'assistant intelligent SnapLogic")
st.title("L'assistant intelligent SnapLogic")

st.markdown("""
### Assistant IA spécialisé en RFP et en expertise technique, avec interface vocale

Obtenez des réponses détaillées aux questions de RFP et aux demandes techniques, avec des informations issues de la documentation officielle, des discussions Slack et de diverses autres ressources SnapLogic.
""")

# Create columns with adjusted ratios for better widget display
col1, col2 = st.columns([1.2, 1.22])

with col1:
    # Embed ElevenLabs widget with adjusted container
    elevenlabs_html = """
    <elevenlabs-convai agent-id="nnoWPUe6P27G1OlPw25C"></elevenlabs-convai><script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
    """
    st.components.v1.html(elevenlabs_html, height=225, width=340)

st.markdown("""
💡 **Interaction vocale disponible**
- Posez vos questions à l’oral avec le widget vocal ci-dessus
- Écoutez les réponses vocales générées par l’IA
- Conçu pour un usage mains libres

Exemples de requêtes :
- Quelles sont les certifications de sécurité de SnapLogic ?
- Décrivez l'approche de SnapLogic en matière de gestion des API
- Quelle est la stratégie de reprise après sinistre de SnapLogic ?
- Comment SnapLogic gère-t-il le chiffrement des données au repos et en transit ?
- Quelles capacités de surveillance sont disponibles sur la plateforme ?
- Expliquez l'intégration de SnapLogic avec les fournisseurs d'identité
""")

# Initialize chat history
if "expert_assistant" not in st.session_state:
    st.session_state.expert_assistant = []

# Display chat messages from history
for message in st.session_state.expert_assistant:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Ask me anything about SnapLogic's technical capabilities")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.expert_assistant.append({"role": "user", "content": prompt})
    
    with st.spinner("Working..."):
        data = {"prompt": prompt}
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }
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
                if "response" in result:
                    assistant_response = result["response"]
                    with st.chat_message("assistant"):
                        typewriter(text=assistant_response, speed=30)
                    st.session_state.expert_assistant.append({"role": "assistant", "content": assistant_response})
                else:
                    with st.chat_message("assistant"):
                        st.error("❌ Invalid response format from API")
            except ValueError:
                with st.chat_message("assistant"):
                    st.error("❌ Invalid JSON response from API")
        else:
            st.error(f"❌ Error while calling the SnapLogic API")
        st.rerun()
