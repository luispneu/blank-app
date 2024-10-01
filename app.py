import streamlit as st
import requests
from PIL import Image
import io
import cv2

# Defina suas credenciais da API do Roboflow
api_key = "4nrRBlLaBjzddDC8nC3i"  # Substitua pela sua API Key
project_url = "https://api.roboflow.com/visao-computacional-lxlqb"  # Substitua pelo URL do seu projeto

# Função para fazer a previsão via API do Roboflow
def make_prediction(image_file):
    response = requests.post(
        f"{project_url}/predict",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": image_file}
    )
    return response.json()

# Função para capturar imagem da câmera
def capture_image():
    cap = cv2.VideoCapture(0)  # 0 para usar a câmera padrão
    ret, frame = cap.read()
    cap.release()  # Libere a câmera após capturar
    if ret:
        return frame
    else:
        st.error("Não foi possível capturar a imagem.")

# Título do aplicativo
st.title("🎈 Classificação de Qualidade de Frutas")
st.write("Faça upload de uma imagem de uma fruta ou capture uma imagem pela câmera e descubra sua qualidade!")

# Botão para capturar imagem
if st.button("Capturar Imagem"):
    img = capture_image()
    if img is not None:
        # Converter a imagem BGR para RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, caption='Imagem Capturada', use_column_width=True)

        # Processar e classificar a imagem
        img_bytes = io.BytesIO()
        pil_img = Image.fromarray(img_rgb)
        pil_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        result = make_prediction(img_bytes)

        # Assumindo que a resposta tenha uma estrutura específica
        if 'predictions' in result:
            predictions = result['predictions']
            predicted_class = predictions[0]['class']  # ajuste conforme a estrutura da resposta
            confidence = predictions[0]['confidence']  # ajuste conforme a estrutura da resposta

            # Exibir resultado
            st.write(f"**Classificação Prevista:** {predicted_class} com {confidence * 100:.2f}% de confiança.")
        else:
            st.write("Erro ao obter a previsão.")

# Upload de imagem
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Exibir imagem carregada
    img = Image.open(uploaded_file)
    st.image(img, caption='Imagem Carregada', use_column_width=True)

    # Processar e classificar a imagem
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    result = make_prediction(img_bytes)

    # Assumindo que a resposta tenha uma estrutura específica
    if 'predictions' in result:
        predictions = result['predictions']
        predicted_class = predictions[0]['class']  # ajuste conforme a estrutura da resposta
        confidence = predictions[0]['confidence']  # ajuste conforme a estrutura da resposta

        # Exibir resultado
        st.write(f"**Classificação Prevista:** {predicted_class} com {confidence * 100:.2f}% de confiança.")
    else:
        st.write("Erro ao obter a previsão.")
