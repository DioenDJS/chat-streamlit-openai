import streamlit as st
from openai import OpenAI


st.title("chatGPT Like")

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("whats is up ?"):
    intrunctions = """
        Você é um secretário de uma clinica médica.
        Vocês atendem vários especialidades médicas.
        Interaja com o usuário e quando ele quise marcar uma consulta 
        Responda normalmente as perguntas do usuário em um dialogo continuo.
        pergunte na ordem:
         1. qual o plano de saúde ele possuí
         2. Melhor data e horário para a consulta. 
        Se o plano de saúde for o Notredame, informe ao usuário que não atendemos esse plano. 

    """

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state['openai_model'],
            messages=[
                {"role": "user", "content": prompt},
                {"role": "system", "content": intrunctions}
            ],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role":"assistant", "content":response})
