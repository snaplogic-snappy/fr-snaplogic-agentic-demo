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

def get_demo_metadata():
    """Get comprehensive demo metadata including categories and tags"""
    demos = []
    pages_dir = "pages"
    
    if not os.path.exists(pages_dir):
        return demos
    
    for filename in sorted(os.listdir(pages_dir)):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                # Extract basic info from filename using simple string parsing
                # Format: number_emoji_name.py (with underscores or spaces)
                parts = filename.replace('.py', '').split('_')
                if len(parts) >= 3:
                    number = int(parts[0])
                    emoji = parts[1]
                    title = ' '.join(parts[2:]).replace('_', ' ')
                    
                    # Get metadata from the demo file
                    metadata = get_metadata_from_file(os.path.join(pages_dir, filename))
                    
                    demos.append({
                        'filename': filename,
                        'number': number,
                        'emoji': emoji,
                        'title': title,
                        'url_path': filename[:-3],
                        'categories': metadata.get('categories', []),
                        'tags': metadata.get('tags', []),
                        'searchable_text': create_searchable_text(title, metadata)
                    })
            except Exception as e:
                st.warning(f"Could not parse metadata for {filename}: {str(e)}")
    
    # Sort demos by demo number to ensure proper numerical ordering
    demos.sort(key=lambda x: x['number'])
    
    return demos

def get_metadata_from_file(filepath):
    """Extract DEMO_METADATA from a demo file without importing it"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Find DEMO_METADATA dictionary
        metadata_match = re.search(r'DEMO_METADATA\s*=\s*{([^}]+)}', content, re.DOTALL)
        if metadata_match:
            metadata_str = metadata_match.group(1)
            
            # Extract categories
            categories_match = re.search(r'"categories":\s*\[([^\]]*)\]', metadata_str)
            categories = []
            if categories_match:
                categories_str = categories_match.group(1)
                categories = [cat.strip().strip('"\'') for cat in categories_str.split(',') if cat.strip()]
            
            # Extract tags
            tags_match = re.search(r'"tags":\s*\[([^\]]*)\]', metadata_str)
            tags = []
            if tags_match:
                tags_str = tags_match.group(1)
                tags = [tag.strip().strip('"\'') for tag in tags_str.split(',') if tag.strip()]
            
            return {
                'categories': categories,
                'tags': tags
            }
    except Exception as e:
        st.warning(f"Error reading metadata from {filepath}: {str(e)}")
    
    return {'categories': [], 'tags': []}

def create_searchable_text(title, metadata):
    """Create comprehensive searchable text from title, categories, and tags"""
    searchable_parts = []
    
    # Add title words
    searchable_parts.extend(title.lower().split())
    
    # Add categories
    searchable_parts.extend([cat.lower() for cat in metadata.get('categories', [])])
    
    # Add tags
    searchable_parts.extend([tag.lower() for tag in metadata.get('tags', [])])
    
    return ' '.join(searchable_parts)

def filter_demos(demos, search_term):
    """Advanced filtering based on search term across all metadata"""
    if not search_term:
        return demos
    
    search_lower = search_term.lower()
    filtered = []
    
    for demo in demos:
        # Check if search term matches any part of the searchable text
        if search_lower in demo['searchable_text']:
            filtered.append(demo)
        # Also check exact matches for demo number
        elif str(demo['number']) == search_lower:
            filtered.append(demo)
        # Check emoji
        elif search_lower in demo['emoji'].lower():
            filtered.append(demo)
    
    return filtered

def render_demo_grid(filtered_demos, all_demos_count):
    """Display filtered demos using pure Streamlit components"""
    if not filtered_demos:
        st.info("No demos match your search. Try a different keyword.")
        return

    # Add custom CSS for styling the pure Streamlit components
    st.markdown("""
    <style>
    /* Style Streamlit page links to look like our custom buttons */
    [data-testid="stPageLink"] {
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        text-decoration: none !important;
        display: block !important;
        font-weight: 700 !important;
        text-align: center !important;
        font-size: 1.2rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        box-sizing: border-box !important;
        cursor: pointer !important;
        margin-top: 0.5rem !important;
    }
    [data-testid="stPageLink"]:hover {
        background: #2563eb !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        border: 2px solid #1d4ed8 !important;
    }
    
    /* Force white text on all page link elements */
    [data-testid="stPageLink"] * {
        color: white !important;
    }
    [data-testid="stPageLink"] a {
        color: white !important;
    }
    [data-testid="stPageLink"] span {
        color: white !important;
    }
    
    /* Border for demo cards using a wrapper div */
    .demo-card {
        border: 3px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        background: white !important;
        height: 280px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    .demo-card:hover {
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a responsive grid using Streamlit columns
    cols = st.columns(2)
    
    for i, demo in enumerate(filtered_demos):
        with cols[i % 2]:
            # Clean up title by replacing underscores with spaces
            clean_title = demo['title'].replace('_', ' ')
            
            # Wrap everything in a demo card container
            st.markdown(f"""
            <div class="demo-card">
                <h3>{demo['emoji']} {clean_title}</h3>
                <p><em>Demo #{demo['number']}</em></p>
                {f'<p><strong>Categories:</strong> {", ".join(demo["categories"])}</p>' if demo.get('categories') else ''}
                {f'<p><strong>Tags:</strong> {", ".join(demo["tags"])}</p>' if demo.get('tags') else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Button using native Streamlit navigation
            st.page_link(f"pages/{demo['filename']}", label="Open Demo", use_container_width=True)

# Main page setup
st.set_page_config(
    page_title=page_title,
    initial_sidebar_state="expanded"
)
st.title(title)

st.sidebar.title("Agent Creator Catalog")
st.sidebar.success("Select a demo above.")

# Enhanced search functionality
st.markdown("## 🔍 Search Demos")
st.markdown("Search by **any word** in the demo title, **categories**, or **tags**")

search_term = st.text_input(
    "Search demos...", 
    placeholder="e.g., HR, Business, Analytics, Healthcare, Sales, SnapLogic...",
    key="search_input"
)

# Get and filter demos
demos = get_demo_metadata()
filtered_demos = filter_demos(demos, search_term)

# Display results
if search_term:
    st.caption(f"Showing {len(filtered_demos)} of {len(demos)} demos")
else:
    st.caption(f"All {len(demos)} demos")

render_demo_grid(filtered_demos, len(demos))

# Show search tips
if search_term:
    st.markdown("---")
    st.markdown("### 💡 Search Tips")
    st.markdown(f"""
    - **Title words**: Search for any word in demo titles
    - **Categories**: Try "Business", "Content", "Technical", "Industry"  
    - **Tags**: Search specific tags like "HR", "Sales", "Analytics", "Healthcare"
    - **Functions**: Look for "Assistant", "Agent", "Bot", "Tool"
    - **Industries**: Search "Healthcare", "Finance", "Government", "Education"
    """)

# Original landing page content
st.markdown("---")
st.markdown(
    """
    ## 🚀 Bienvenue sur le portail Agents de SnapLogic
    
    Ce portail présente 4 agents IA créés avec SnapLogic Agent Creator, démontrant les incroyables capacités des applications basées sur les LLM.
    
    ### 🎯 Ce que vous trouverez ici : 
    
    **Des solutions business**
    - Rapprochement de factures
    - Assistant commercial IA 
    
    **Des outils techniques** 
    - Des assistants de Data science, Assistant expert de SnapLogic
    
    ### 🔍 Comment utiliser ce portail ?
    
    1. **Recherche**: utilisez la barre de recherche pour trouver des démos par mot-clé, catégorie ou tag
    2. **Parcourir par catégorie**: utilisez la barre latérale pour naviguer dans les différentes catégories de démos
    3. **Recherche par fonction**: recherchez des fonctions spécifiques comme « RH », « Vente », « Analytics »
    4. **Recherche par technologie**: recherchez « SnapLogic », « SQL », « PDF » pour trouver les outils correspondants
    5. **Focus secteur d'activité**: explorez les solutions pour la santé, l’administration ou l'industrie
    
    ### 💡 Pour commencer
    
    **👈 Sélectionnez une démo dans la barre latérale pour voir Agent Creator en action !
    
    Chaque démo présente :
    - Des cas d’usage réels
    - Une interaction en langage naturel
    - Une intégration avec différentes sources de données
    - Des capacités IA professionnelles
    
    ---
    
    ## 🛠️ À propos de SnapLogic Agent Creator
    
    **SnapLogic Agent Creator** vous permet de créer des applications basées sur les LLM en un rien de temps !
    
    ### Fonctionnalités clés :
    - **Développement sans code** : créez des agents IA sans écrire de code complexe
    - **Enterprise Integration** : connectez-vous à n’importe quelle source de données ou API
    - **Langage naturel** : interagissez avec vos données en langage courant
    - **Architecture scalable**: déployez des applications IA clé en main pour la production
    
    ### Vous voulez en savoir plus ?
    - 📚 [Documentation Agent Creator](https://docs.snaplogic.com/agentcreator/agentcreator-about.html)
    - 🏢 [Documentation plateforme SnapLogic](https://docs.snaplogic.com)
    - 💬 [Forum communautaire](https://community.snaplogic.com)
    - 🎥 [Tutoriels vidéos](https://www.youtube.com/@snaplogic)
    
    ---
    
    *Prêt à explorer ? Choisissez une démo dans la barre latérale ou utilisez la recherche ci-dessus pour commencer !*
    """
)

# Add some visual elements
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**44 AI Agents**\nReady to explore")

with col2:
    st.success("**4 Categories**\nBusiness, Content, Technical, Industry")

with col3:
    st.warning("**100+ Tags**\nFind exactly what you need")
