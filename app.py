import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="Gerador de Testes para Chatbot (Cloud)", layout="centered")

st.title("🤖 Gerador de Cenários de Teste para Chatbot")
st.markdown("Gere cenários no formato **Dado que... Quando... Então...** com IA gratuita da Hugging Face.")

# Entrada de dados
api_token = st.text_input("🔐 Token da Hugging Face (https://huggingface.co/settings/tokens)", type="password")
bot_name = st.text_input("🧠 Nome do Bot", placeholder="Ex: Chatbot Citroën")
objetivo = st.text_area("🎯 Objetivo do fluxo", placeholder="Ex: Agendar revisão para veículo...")
contexto = st.text_area("📄 Descrição do fluxo", placeholder="Ex: Usuário inicia a conversa, escolhe a data...")
tipo_teste = st.multiselect("🔍 Tipos de teste desejados", ["Principal", "Alternativo", "Exceção"], default=["Principal", "Alternativo", "Exceção"])
imagem = st.file_uploader("📎 (Opcional) Anexe imagem do Figma com o fluxo", type=["png", "jpg", "jpeg"])

if imagem:
    st.image(Image.open(imagem), caption="Imagem do fluxo (Figma)", use_column_width=True)

# Geração do prompt
def gerar_prompt(bot_name, objetivo, contexto, tipos, imagem_presente):
    tipos_formatado = ', '.join(tipos)
    extra = "Foi anexada uma imagem representando o fluxo do chatbot, extraída do Figma." if imagem_presente else ""
    return (
        f"Você é um especialista em QA. Crie cenários de teste no formato Gherkin (Dado que... Quando... Então...) "
        f"para o chatbot \"{bot_name}\".\n\n"
        f"Objetivo: {objetivo}\n"
        f"Fluxo textual descrito: {contexto}\n"
        f"Tipos de teste solicitados: {tipos_formatado}\n"
        f"{extra}\n\n"
        f"Crie pelo menos:\n"
        f"- 2 cenários principais\n"
        f"- 1 alternativo\n"
        f"- 1 de exceção\n\n"
        f"Use linguagem clara e profissional. Separe os cenários por tipo."
    )

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

if st.button("🚀 Gerar Cenários com IA"):
    if not api_token:
        st.error("⚠️ Forneça seu token da Hugging Face.")
    elif not bot_name or not objetivo or not contexto:
        st.error("⚠️ Preencha todos os campos obrigatórios.")
    else:
        prompt = gerar_prompt(bot_name, objetivo, contexto, tipo_teste, imagem is not None)
        st.info("⏳ Enviando para IA da Hugging Face...")

        # 👇 agora sim: api_token já existe
        headers = {
            "Authorization": f"Bearer {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}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt.strip()
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code != 200:
                st.error(f"Erro {response.status_code} - {response.text}")
            else:
                result = response.json()
                output = result[0]["generated_text"].strip()
                st.success("✅ Cenários gerados com sucesso!")
                st.code(output, language="gherkin")
        except Exception as e:
            st.error(f"Erro ao chamar a IA: {e}")

