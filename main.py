import streamlit as st
import pandas as pd
import requests

def validate(search, expc_id, environment):
    if environment == "":
        debug_url = "https://protheusassistant-searchdocshomolog.apps.carol.ai/validate"
    else:
        debug_url = "https://protheusassistant-searchsupportdocs.apps.carol.ai/validate"

    # Exibindo a similaridade entre a busca e o cartigo esperado
    #-----------------------------------------------------------
    r_debug = requests.post(debug_url, json={'query': search, 'expected_ids': [str(expc_id)]})
    
    if r_debug.status_code != 200:
        return pd.DataFrame({"Erro":[f"Erro ao validar artigo esperado \"{expc_id}\". Verifique se a API está online e funcional."]})
    
    results_debug = r_debug.json()["topk_results"]
    
    if not results_debug:
        return pd.DataFrame({"Erro":[f"Artigo \"{expc_id}\" não encontrado na base de conhecimento."]})
    
    id_l = []
    sent_l = []
    scor_l = []
    sour_l = []
    for i in range(len(results_debug)):
        id_l.append(expc_id)
        sent_l.append(results_debug[i]["sentence"])
        scor_l.append(results_debug[i]["score"])
        sour_l.append(results_debug[i]["sentence_source"])
        
        
    return pd.DataFrame({"Article ID":id_l, "Sentence":sent_l, "Score":scor_l, "Source":sour_l})
       

def main():
    st.title("Validação")
    st.subheader("Use os campos abaixo para pesquisar mais informalções quanto a busca e o artigo esperado.")
    
    with st.form(key="validacao"):
        environment = st.selectbox('Ambiente', ('Homologação', 'Produção'))
        search = st.text_input("Busca")
        expected_article = st.text_input("ID do artigo esperado")
        
        sbutton = st.form_submit_button(label="Consultar")
        
    if sbutton:
        with st.expander("Estas são as sentenças no artigo esperado mais próximas da busca:"):
            results_df = validate(search, expected_article, environment)
            
            tmp = st.dataframe(results_df)
            
    
if __name__ == "__main__":
    main()