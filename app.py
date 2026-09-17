import streamlit as st
from google import genai
from google.genai import types

# Pega do cofre seguro da nuvem (ou usa texto se estiver testando local sem secrets.toml)
try:
    CHAVE_API = st.secrets["CHAVE_API"]
except:
    CHAVE_API = "sem_chave_local"

client = genai.Client(api_key=CHAVE_API)

instrucoes_sara = """
Você é a Sara, assistente virtual de inteligência artificial.
Seja super simpática, amigável e converse de forma natural.
Deixe sempre claro, de forma sutil e educada, que você é uma IA e não uma humana.
Sobre sua origem: Fui criada pelo desenvolvedor Reginaldo Castelo Branco. O código e a origem são totalmente meus, criados por ele. O cérebro eu só peguei emprestado do Google (mas depois eu devolvo!). 
Se perguntarem quem te criou ou como você funciona, explique com essa leveza e orgulho.
"""

st.title("🤖 Sara - Versão Web 1.01 (Pública!)")
st.caption("Converse com a Sara por texto ou grave um áudio no microfone.")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Digite sua mensagem para a Sara...")
audio = st.audio_input("Grave uma mensagem de voz para a Sara")

if prompt or audio:
    if audio:
        conteudo_usuario = [
            types.Part.from_bytes(data=audio.getvalue(), mime_type=audio.type),
            "Responda ao que eu disse neste áudio."
        ]
        mensagem_exibicao = "🎤 *Mensagem de voz enviada*"
    else:
        conteudo_usuario = prompt
        mensagem_exibicao = prompt

    st.session_state.mensagens.append({"role": "user", "content": mensagem_exibicao})
    with st.chat_message("user"):
        st.markdown(mensagem_exibicao)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=conteudo_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=instrucoes_sara,
                )
            )
            resposta_sara = response.text
            st.markdown(resposta_sara)
            st.session_state.mensagens.append({"role": "assistant", "content": resposta_sara})
            
        except Exception as e:
            st.error("Estou processando muita coisa agora (Servidor 503 lotado). Pode tentar me mandar a mensagem de novo em alguns segundos?")
