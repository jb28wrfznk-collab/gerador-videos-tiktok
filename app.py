import time
import streamlit as st
from google import genai

st.set_page_config(page_title="Gerador de Vídeos TikTok", layout="centered")
st.title("🚀 Gerador de Vídeos Curtos para E-commerce")

# Carrega a chave de forma segura a partir do Streamlit Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = ""

url_produto = st.text_input("Cole o link do produto do Mercado Livre ou da Shopee:")

# Controlos de personalização da geração
col1, col2 = st.columns(2)
with col1:
    tom_voz = st.selectbox(
        "Tom do vídeo:",
        [
            "UGC Espontâneo (Recomendação natural)",
            "Venda Direta (Comercial focado em urgência/oferta)",
            "Curiosidade / Humor (Entretenimento com quebra de padrão)"
        ]
    )
with col2:
    duracao = st.selectbox(
        "Duração estimada:",
        [
            "15 a 30 segundos (Rápido e direto ao ponto)",
            "30 a 60 segundos (Mais detalhado com demonstração)"
        ]
    )

if url_produto:
    if st.button("Gerar Roteiro Personalizado"):
        with st.spinner("A analisar produto e a estruturar o roteiro..."):
            client = genai.Client(api_key=GEMINI_API_KEY)

            prompt = f"""
Analise este produto ou tipo de produto indicado pelo link: {url_produto}

Crie um roteiro magnético de vídeo curto em português para TikTok/Reels/Shorts com as seguintes especificações:
- Tom de voz: {tom_voz}
- Duração alvo: {duracao}

Estrutura obrigatória do roteiro:
1. [00:00 - 00:03] Gancho Visual e Auditivo forte (Hook magnético para reter a atenção).
2. Dor / Problema real vivido pelo cliente.
3. Demonstração da Solução (apresentação prática das qualidades do produto).
4. Chamada para Ação (CTA) clara (ex: comentar para receber link, clicar na bio).
5. Dicas extras de bastidores (sugestão de áudio de fundo, ritmo de edição e efeitos visuais).
"""

            roteiro_gerado = None
            ultimo_erro = None
            max_tentativas = 4

            for tentativa in range(max_tentativas):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )
                    roteiro_gerado = response.text
                    break
                except Exception as e:
                    ultimo_erro = e
                    if "503" in str(e) and tentativa < max_tentativas - 1:
                        time.sleep(3)
                    else:
                        break

            if roteiro_gerado:
                st.success("Roteiro personalizado gerado com sucesso!")
                st.markdown("---")
                st.markdown(roteiro_gerado)
                st.download_button(
                    label="📥 Baixar Roteiro (.txt)",
                    data=roteiro_gerado,
                    file_name="roteiro_video.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"Erro ao gerar o roteiro: {ultimo_erro}")
