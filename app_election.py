# import des librairies
import streamlit as st
import pandas as pd
import seaborn as sb
import requests
import matplotlib.pyplot as plt
import numpy as np

# create csv file with url response
# url_csv = "https://data.montpellier3m.fr/sites/default/files/ressources/VilleMTP_MTP_Legislatives_20220612.csv"
# response = requests.get(url_csv)
# with open("mtp_elect.csv",'wb') as output_file:
#     output_file.write(response.content)

# load csv file and transform data to dataframe
df = pd.read_csv("mtp_elect.csv", delimiter=";",encoding='utf-8')

# prepare data to visualisize objectif 1
data_tab = df[['Candidat','Nombre de Voix']].groupby(by='Candidat').sum().sort_values(by='Nombre de Voix',ascending=False)
data_graph = data_tab[0:10]

fig, ax = plt.subplots(figsize=(12,7))
sb.barplot(data_graph,y=data_graph.index, x='Nombre de Voix', ax=ax)

###############################
# ---------- Web app ---------#
###############################

# # Affichage brut objectif 1
# st.title('Montpellier : Résultat des élections législatives')
# st.dataframe(data_tab)
# st.pyplot(fig)

# custom page
st.set_page_config(layout='wide')

# custom title
st.markdown('<h1 style="text-align: center;">Montpellier : Résultat des élections législatives</h1>', unsafe_allow_html=True)
st.write('\n')

st.subheader('Résultats tous bureaux confondus')

# custom layout
col1,col2 = st.columns((0.4,0.5),gap='large')

with col1:
    st.dataframe(data_tab,use_container_width=True)
with col2:
    st.pyplot(fig)

# Affichage brut objectif 2

# prepare data to visualisize
data_by_bureau = df[["Bureau","Candidat","Nombre de Voix"]].groupby(by=['Bureau','Candidat']).sum().reset_index()
bureaux = data_by_bureau['Bureau'].unique()

def get_data_by_bureau(data,nom_bureau):
    df = data[data['Bureau']==nom_bureau]
    df= df[['Candidat','Nombre de Voix']].set_index('Candidat')
    df = df.sort_values(by='Nombre de Voix',ascending=False)
    return df

# value_sbox = st.selectbox("Choisir un bureau", options=bureaux)

# design selectbox
value_sbox = st.sidebar.selectbox("Choisir un bureau", options=bureaux)

st.subheader('Résultats par bureau: '+ value_sbox)

# design display
col1, col2 = st.columns((0.4,0.5),gap='large')

with col1:
    result_to_display = get_data_by_bureau(data_by_bureau,value_sbox)
    st.dataframe(result_to_display, use_container_width=True)

with col2:
    fig, ax = plt.subplots()
    sb.barplot(result_to_display,y=result_to_display.index, x='Nombre de Voix', ax=ax)
    st.pyplot(fig, use_container_width=True)


######################################
# ---------- Web app design ---------#
######################################

# # load file and transform data into dataframe
# df = pd.read_csv("mtp_elect.csv", delimiter=";",encoding='latin9')

# # prepare data to visualisize
# data_tab = df[['Candidat','Nombre de Voix']].groupby(by='Candidat').sum().sort_values(by='Nombre de Voix',ascending=False)
# data_graph = data_tab[data_tab['Nombre de Voix']>1000]

# fig, ax = plt.subplots(figsize=(12,7))
# sb.barplot(data_graph,y=data_graph.index, x='Nombre de Voix', ax=ax)

# ########### design

# st.set_page_config(page_title="Elections", page_icon="random", layout="wide", initial_sidebar_state="auto", menu_items=None)

# col1,col2,col3 = st.columns((0.2,0.6,0.2))
# with col2:
#     st.title('Montpellier : Elections législatives')

# st.write('\n')

# col1, col2 = st.columns((0.4,0.5),gap='large')

# with col1:
#     st.subheader('Liste des candidats')
#     st.dataframe(data_tab,width=300, height=400)

# with col2:
#     st.subheader('Le top 18')
#     st.pyplot(fig)

# st.sidebar.subheader('Barre latérale')

######################################
# ---------- Web app widget ---------#
######################################

# st.set_page_config(page_title="Elections", page_icon="random", layout="wide", initial_sidebar_state="auto", menu_items=None)

# # load file and transform data into dataframe
# df = pd.read_csv("mtp_elect.csv", delimiter=";",encoding='latin9')
# df = df[['Bureau','Candidat', 'Nombre de Voix']]

# # define function
# def get_data_by_bureau(data,nom_bureau):
#     df = data[data['Bureau']==nom_bureau]
#     df = df[['Candidat','Nombre de Voix']].groupby(by='Candidat').sum().sort_values(by='Nombre de Voix',ascending=False)
#     return df

# # prepare sequence selectbox
# bureaux = df.Bureau.unique()
# bureaux = np.append(bureaux,'Tous')
# bureaux = np.sort(bureaux)


# bureau_sb = st.sidebar.selectbox("Choix d'un bureau", options=bureaux)

# if bureau_sb == 'Tous':
#     data_tab = df[['Candidat','Nombre de Voix']].groupby(by='Candidat').sum().sort_values(by='Nombre de Voix',ascending=False)
#     data_graph = data_tab[data_tab['Nombre de Voix']>1000]
#     graph_title = 'Le top 18'
# else:
#     data_tab = get_data_by_bureau(df, bureau_sb).sort_values(by='Nombre de Voix',ascending=False)
#     # data_tab = data_tab[['Candidat','Nombre de Voix']].set_index('Candidat')
#     data_graph = data_tab
#     graph_title = bureau_sb

# # construct figure
# fig, ax = plt.subplots(figsize=(12,7))
# sb.barplot(data_graph,y=data_graph.index, x='Nombre de Voix', ax=ax)

# ########### design

# col1,col2,col3 = st.columns((0.2,0.6,0.2))
# with col2:
#     st.title('Montpellier : Elections législatives')

# st.write('\n')

# col1, col2 = st.columns((0.4,0.5),gap='medium')

# with col1:
#     st.subheader('Liste des candidats')
#     st.dataframe(data_tab,width=400, height=400)

# with col2:
#     st.subheader(graph_title)
#     st.pyplot(fig)
