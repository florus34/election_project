####### LIBRAIRIES

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
import os

######## GESTION DU PROXY
# os.environ['HTTPS_PROXY']=""

######## DONNEES

# import dataset
data_text = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/VilleMTP_MTP_Legislatives_20220612.csv").text
df = pd.read_csv(io.StringIO(data_text),sep=';')

# proccess dataset part one
class_total = df[['Candidat','Nombre de Voix']].groupby(by='Candidat').sum().sort_values(by='Nombre de Voix', ascending=False)
# graph part one
graph_total = px.bar(data_frame=class_total[0:10][::-1],x='Nombre de Voix')

# process dataset part two
class_by_bur = df[['Bureau','Candidat','Nombre de Voix']].groupby(by=['Bureau','Candidat']).sum().reset_index()
list_bur = list(class_by_bur['Bureau'].unique())
list_bur.append('Tous les bureaux')


####### WEB APP

# CONFIG
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# TITRE
#st.write('# Le titre de ma webapp')
st.markdown("<h1><center> Résultat des élections législatives",unsafe_allow_html=True)
st.markdown("<h3><center> Montpellier 2022 (1er tour)",unsafe_allow_html=True)
# st.write('')

# # AFFICHAGE PREMIER TABLEAU
# # st.write(class_total)
# st.dataframe(class_total,use_container_width=True)

# # AFFICHAGE PREMIER GRAPH
# st.plotly_chart(graph_total)

option = st.sidebar.selectbox(label="Choix d'un bureau", options=list_bur, index=len(list_bur)-1)

if option == 'Tous les bureaux' :
    box1, box2 = st.columns(2,gap='large')
    # BOX 1 : AFFICHAGE TABLEAU 1
    with box1:
        st.write("***Résultat des candidats***")
        st.dataframe(class_total,use_container_width=True)

    # BOX 2 : AFFICHAGE GRAPH 1
    with box2:
        st.write("***Classement des candidats (top 10)***")
        st.plotly_chart(graph_total, use_container_width=True)
else :
    box3, box4 = st.columns(2,gap='large')
    mask = class_by_bur['Bureau']== option
    display_tab = class_by_bur[mask][['Candidat','Nombre de Voix']].sort_values(by='Nombre de Voix', ascending=False).set_index('Candidat')

    # BOX 1 : AFFICHAGE TABLEAU 1
    with box3:
        st.write("***Résultat pour le bureau :***", option)
        st.dataframe(display_tab,use_container_width=True)

    # BOX 2 : AFFICHAGE GRAPH 1
    with box4:
        st.write("***Classement des candidats***")
        graph_bur = px.bar(data_frame = class_by_bur[mask].sort_values(by='Nombre de Voix'), x='Nombre de Voix', y = 'Candidat')
        st.plotly_chart(graph_bur, use_container_width=True)


# st.write("Vous avez sélectionné: ", option) 