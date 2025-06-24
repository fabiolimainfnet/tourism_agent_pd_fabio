import streamlit as st

from agent import Agent


st.set_page_config(layout="wide")
st.title("Estatistico de futebol")
st.write("Aqui voce conseguirá pesquisar todas as informações necessária para sua análise futebolistica")

agent = Agent("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")

col1, col2 = st.columns(2)

with col1:
   request = st.text_area("Quais estatisticas voce deseja pesquisar? Voce pode pesquisar por exemplo quem foi o artilheiro do futebol brasileiro em determinado ano") 
   button = st.button("Processar")
   
   box = st.container(height=300)

   with box:
      container =st.empty()
      container.header("Resposta")
      

if button:
   if request:
      itinerary = agent.get_tips(request)
      container.write(itinerary["estatistica_futebol"])

   