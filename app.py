import io
import requests
import cv2
from PIL import Image
import streamlit as st

# Defina suas credenciais da API do Roboflow
API_KEY = "4nrRBlLaBjzddDC8nC3i"  # Substitua pela sua API Key
PROJECT_URL = "https://api.roboflow.com/projeto-ifms/visao-computacional-lxlqb/1"  # Ajuste para o URL do seu projeto

def make_prediction(image_file):
    """
    Faz a previsão via API do Roboflow.
    
    Parameters:
        image_file (BytesIO): A imagem em formato bytes para previsão.
    
    Returns:
        dict: O resultado da previsão.
    """
    response = requests.post(
        f"{PROJECT_URL}/predict",
        headers={"Authorization": f"Bearer {API_KEY}"},
        files={"file": image_file}
    )
    
    # Verificação de status
    if response.status_code != 200:
        st.error(f"Erro ao acessar a API: {response.status_code} - {response.text}")
        return {}
    
    result = response.json()
    st.write("Resposta da API:", result)  # Para depuração
    return result

def capture_image():
    cap = cv2.VideoCapture(0)  # 0 para usar a câmera padrão
    ret, frame = cap.read()
    cap.release()  # Libere a câmera após capturar
    if ret:
        return frame
    else:
        st.error("Não foi possível capturar a imagem.")

def main():
    # Título do aplicativo
    st.title("🎈 Classificação de Qualidade de Frutas")
    st.write("Faça upload de uma imagem de uma fruta ou capture uma imagem pela câmera e descubra sua qualidade!")

    # Botão para capturar imagem
    if st.button("Capturar Imagem"):
        img = capture_image()
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(img_rgb, caption='Imagem Capturada', use_column_width=True)

            img_bytes = io.BytesIO()
            pil_img = Image.fromarray(img_rgb)
            pil_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            result = make_prediction(img_bytes)

            if 'predictions' in result:
                predictions = result['predictions']
                predicted_class = predictions[0]['class']  # Classe prevista
                confidence = predictions[0]['confidence']  # Confiança da previsão

                # Exibir resultado
                if predicted_class.lower() == "saudável":
                    st.write(f"**Classificação Prevista:** A fruta está **SAUDÁVEL** com {confidence * 100:.2f}% de confiança.")
                elif predicted_class.lower() == "não saudável":
                    st.write(f"**Classificação Prevista:** A fruta está **NÃO SAUDÁVEL** com {confidence * 100:.2f}% de confiança.")
                else:
                    st.write(f"**Classificação Prevista:** {predicted_class} com {confidence * 100:.2f}% de confiança.")
            else:
                st.write("Erro ao obter a previsão.")

    # Upload de imagem
    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Imagem Carregada', use_column_width=True)

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        result = make_prediction(img_bytes)

        if 'predictions' in result:
            predictions = result['predictions']
            predicted_class = predictions[0]['class']  # Classe prevista
            confidence = predictions[0]['confidence']  # Confiança da previsão

            if predicted_class.lower() == "saudável":
                st.write(f"**Classificação Prevista:** A fruta está **SAUDÁVEL** com {confidence * 100:.2f}% de confiança.")
            elif predicted_class.lower() == "não saudável":
                st.write(f"**Classificação Prevista:** A fruta está **NÃO SAUDÁVEL** com {confidence * 100:.2f}% de confiança.")
            else:
                st.write(f"**Classificação Prevista:** {predicted_class} com {confidence * 100:.2f}% de confiança.")
        else:
            st.write("Erro ao obter a previsão.")

if __name__ == "__main__":
    main()
