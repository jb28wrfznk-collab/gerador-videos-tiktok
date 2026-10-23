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

# Controlos de personalização da geração em 3 colunas
col1, col2, col3 = st.columns(3)
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
with col3:
    objetivo_cta = st.selectbox(
        "Objetivo da Chamada (CTA):",
        [
            "Comentar 'EU QUERO' (Automação de DM)",
            "Clicar no link da Bio (Tráfego direto)",
            "Partilhar / Marcar amigo (Viralização)"
        ]
    )

# Campo opcional para ancoragem de preço ou cupão promocional
preco_cupom = st.text_input(
    "Preço promocional ou cupão de desconto (opcional):",
    placeholder="Ex.: De R$ 89 por R$ 39,90 ou Cupão: VIRAL10"
)

if url_produto:
    if st.button("Gerar Roteiro Personalizado"):
        with st.spinner("A analisar produto e a estruturar o conteúdo completo..."):
            client = genai.Client(api_key=GEMINI_API_KEY)

            contexto_oferta = (
                f"- Oferta/Preço/Cupão: {preco_cupom} (destacar com forte ancoragem de valor e senso de urgência)"
                if preco_cupom
                else "- Oferta: Sem valor explícito informado. Focar no valor percebido e benefícios práticos do produto."
            )

            prompt = f"""
Analise este produto ou tipo de produto indicado pelo link: {url_produto}

Crie um pacote magnético de conversão em português para TikTok/Reels/Shorts com as seguintes especificações:
- Tom de voz: {tom_voz}
- Duração alvo: {duracao}
- Foco da Chamada para Ação (CTA): {objetivo_cta}
{contexto_oferta}

Estrutura obrigatória da resposta:
1. 🎣 3 OPÇÕES DE GANCHOS VISUAIS E AUDITIVOS (00:00 - 00:03) para Teste A/B:
   - Opção A: Curiosidade Extrema (Quebra de padrão inicial)
   - Opção B: Dor Real / Identificação Imediata (Problema urgente)
   - Opção C: Contraintuitivo / Choque (Afirmação que desafia o senso comum)
2. Desenvolvimento do Problema / Agitação da dor vivida pelo cliente.
3. Demonstração Prática da Solução (qualidades visuais, benefícios chave e inserção do preço/cupão se fornecido).
4. Chamada para Ação (CTA): Estritamente focada em: {objetivo_cta}.
5. Bastidores de Gravação e Edição (ritmo de cortes secos, efeitos sonoros recomendados e texto dinâmico no ecrã).
6. 📝 LEGENDA PRONTA PARA PUBLICAÇÃO:
   - Texto magnético curto com gancho de leitura.
   - Reforço do CTA escolhido.
   - Bloco com 5 a 8 hashtags altamente estratégicas (misturando termos de e-commerce viral e nicho do produto).
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
                st.success("Roteiro e legenda gerados com sucesso!")
                st.markdown("---")
                st.markdown(roteiro_gerado)
                st.download_button(
                    label="📥 Baixar Roteiro e Legenda (.txt)",
                    data=roteiro_gerado,
                    file_name="conteudo_video_completo.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"Erro ao gerar o roteiro: {ultimo_erro}")
