API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {
    "Authorization": "Bearer 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",  # Substitua aqui
    "Content-Type": "application/json"
}

if st.button("🚀 Gerar Cenários com IA"):
    if not bot_name or not objetivo or not contexto:
        st.error("⚠️ Preencha todos os campos obrigatórios.")
    else:
        prompt = gerar_prompt(bot_name, objetivo, contexto, tipo_teste, imagem is not None)
        st.info("⏳ Enviando para IA da Hugging Face...")

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
