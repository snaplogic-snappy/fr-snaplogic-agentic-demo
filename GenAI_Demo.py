import streamlit as st
import os
import re
import importlib.util
from dotenv import dotenv_values

# Load environment
env = dotenv_values(".env")
# Streamlit Page Properties
page_title = env.get("PAGE_TITLE", "SnapLogic GenAI Builder Portal")
title = env.get("TITLE", "SnapLogic GenAI Builder Portal")

# Main page setup
st.set_page_config(
    page_title=page_title,
    initial_sidebar_state="expanded"
)
st.title(title)

st.sidebar.title("Catalogue de démos Agents")
st.sidebar.success("Choisissez une démo ci-dessus!

# Original landing page content
st.markdown("---")
st.markdown(
    """
    Ce portail présente 4 agents IA créés avec SnapLogic Agent Creator, démontrant les incroyables capacités des applications basées sur les LLM.

    *Prêt à explorer ? Choisissez une démo dans la barre latérale pour commencer !*
    
    ## 🛠️ À propos de SnapLogic Agent Creator
    
    **SnapLogic Agent Creator** vous permet de créer des agents IA en un rien de temps !
    
    ### Fonctionnalités clés :
    - **Développement sans code** : créez des agents IA sans écrire de code complexe
    - **Enterprise Integration** : connectez-vous à n’importe quelle source de données ou API
    - **Langage naturel** : interagissez avec vos données en français
    - **Architecture scalable**: déployez des applications IA clé en main pour la production
    
    ### Vous voulez en savoir plus ?
    - 📚 [Documentation Agent Creator](https://docs.snaplogic.com/agentcreator/agentcreator-about.html)
    - 🏢 [Documentation sur la plateforme SnapLogic](https://docs.snaplogic.com)
    - 💬 [Forum communautaire](https://community.snaplogic.com)
    - 🎥 [Tutoriels vidéos](https://www.youtube.com/@snaplogic)
    
    """
)
