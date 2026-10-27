import time
import streamlit as st
from google import genai

st.set_page_config(page_title="Gerador de Vídeos Curtos", layout="centered")
st.title("🚀 Gerador de Vídeos Curtos para E-commerce")

# Chave da API nos Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = ""

url_produto = st.text_input("Link do produto (Mercado Livre / Shopee):")

# Definições em 3 colunas
col1, col2, col3 = st.columns(3)
with col1:
    tom_voz = st.selectbox(
        "Tom do vídeo:",
        [
            "UGC Espontâneo (Recomendação natural)",
            "Venda Direta (Urgência e foco em oferta)",
            "Curiosidade / Humor (Quebra de padrão)"
        ]
    )
with col2:
    duracao = st.selectbox(
        "Duração estimada:",
        [
            "15 a 30 segundos (Rápido e direto)",
            "30 a 60 segundos (Demonstração detalhada)"
        ]
    )
with col3:
    objetivo_cta = st.selectbox(
        "Objetivo da Chamada (CTA):",
        [
            "Comentar 'EU QUERO' (Automação DM)",
            "Clicar no link da Bio (Tráfego direto)",
            "Partilhar com amigo (Viralização)"
        ]
    )

preco_cupom = st.text_input(
    "Preço promocional ou cupão (opcional):",
    placeholder="Ex.: De R$ 89 por R$ 39,90 ou Cupão: VIRAL10"
)

if url_produto:
    if st.button("Gerar Roteiro Personalizado"):
        with st.spinner("A estruturar o conteúdo..."):
            client = genai.Client(api_key=GEMINI_API_KEY)

            contexto_oferta = (
                f"- Oferta/Preço/Cupão: {preco_cupom} (destacar ancoragem e urgência)"
                if preco_cupom
                else "- Sem valor explícito. Focar nos benefícios práticos."
            )

            prompt = f"""
Analise o produto ou nicho indicado pelo link: {url_produto}

Crie um pacote de alta conversão em português para TikTok/Reels com:
- Tom: {tom_voz}
- Duração: {duracao}
- Foco da CTA: {objetivo_cta}
{contexto_oferta}

Utilize exatamente esta formatação com marcadores para separação:

### [ROTEIRO_INICIO]
1. 🎣 3 OPÇÕES DE GANCHOS (00:00 - 00:03) para Teste A/B:
- Opção A (Curiosidade)
- Opção B (Dor Real)
- Opção C (Contraintuitivo)

2. DESENVOLVIMENTO:
- Agitação do problema
- Demonstração visual da solução e inserção de oferta

3. CHAMADA PARA AÇÃO (CTA):
- Alinhada com: {objetivo_cta}
### [ROTEIRO_FIM]

### [LEGENDA_INICIO]
- Texto magnético para descrição do post.
- Reforço do CTA.
- 5 a 8 hashtags virais e de nicho.
### [LEGENDA_FIM]

### [BASTIDORES_INICIO]
- Ritmo de corte (jump cuts).
- Efeitos sonoros sugeridos (SFX).
- Instruções de texto/legendas dinâmicas no ecrã.
### [BASTIDORES_FIM]
"""

            conteudo = None
            ultimo_erro = None
            max_tentativas = 3

            for tentativa in range(max_tentativas):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )
                    conteudo = response.text
                    break
                except Exception as e:
                    ultimo_erro = e
                    if "503" in str(e) and tentativa < max_tentativas - 1:
                        time.sleep(3)
                    else:
                        break

            if conteudo:
                st.success("Conteúdo gerado com sucesso!")

                # Extrai cada bloco pelos marcadores
                def extrair(texto, tag_ini, tag_fim):
                    try:
                        return texto.split(tag_ini)[1].split(tag_fim)[0].strip()
                    except Exception:
                        return texto

                tab_roteiro = extrair(conteudo, "### [ROTEIRO_INICIO]", "### [ROTEIRO_FIM]")
                tab_legenda = extrair(conteudo, "### [LEGENDA_INICIO]", "### [LEGENDA_FIM]")
                tab_bastidores = extrair(conteudo, "### [BASTIDORES_INICIO]", "### [BASTIDORES_FIM]")

               # Apresentação visual limpa em separadores com cópia rápida
                t1, t2, t3 = st.tabs(["🎬 Roteiro & Ganchos", "📝 Legenda & Tags", "🛠️ Bastidores & Edição"])
                with t1:
                    st.markdown(tab_roteiro)
                with t2:
                    st.caption("Clique no ícone do canto superior direito da caixa para copiar:")
                    st.code(tab_legenda, language=None)
                with t3:
                    st.markdown(tab_bastidores)

                st.markdown("---")
                st.download_button(
                    label="📥 Baixar Pacote Completo (.txt)",
                    data=conteudo.replace("### [ROTEIRO_INICIO]", "").replace("### [ROTEIRO_FIM]", "").replace("### [LEGENDA_INICIO]", "").replace("### [LEGENDA_FIM]", "").replace("### [BASTIDORES_INICIO]", "").replace("### [BASTIDORES_FIM]", ""),
                    file_name="roteiro_completo.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"Não foi possível gerar. Detalhe: {ultimo_erro}")
