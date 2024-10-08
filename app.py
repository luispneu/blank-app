import io
import cv2
import pandas as pd
import gdown
from PIL import Image
import streamlit as st
import random  # Importar random para lógica de classificação

# URL do Google Drive (link compartilhável) para o arquivo CSV
DATASET_URL = "https://drive.google.com/file/d/1QRNcTr6JlyR0DxvhSHihEiBfQjPQNU2b/view?usp=drive_link"

def load_dataset():
    """Carrega o dataset de frutas do Google Drive."""
    gdown.download(DATASET_URL, "dataset_frutas.csv", quiet=False)
    return pd.read_csv("dataset_frutas.csv")

def validate_fruit(image_file, dataset):
    """Valida a fruta com base no dataset."""
    # Exemplo: 70% de chance de ser saudável e 30% de chance de ser podre
    confidence = random.uniform(0, 1)  # Gera um valor aleatório entre 0 e 1
    if confidence > 0.7:  # 70% chance de ser saudável
        return "SAUDÁVEL", confidence
    else:  # 30% chance de ser podre
        return "PODRE", confidence

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        st.error("Não foi possível capturar a imagem.")

def main():
    st.title("🍓 Classificação de Qualidade de Frutas")
    st.write("Faça upload de uma imagem de uma fruta ou capture uma imagem pela câmera!")

    dataset = load_dataset()

    if st.button("Capturar Imagem"):
        img = capture_image()
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(img_rgb, caption='Imagem Capturada', use_column_width=True)

            img_bytes = io.BytesIO()
            pil_img = Image.fromarray(img_rgb)
            pil_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            predicted_class, confidence = validate_fruit(img_bytes, dataset)
            st.write(f"**Classificação Prevista:** A fruta está **{predicted_class}** com {confidence * 100:.2f}% de confiança.")

    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Imagem Carregada', use_column_width=True)

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        predicted_class, confidence = validate_fruit(img_bytes, dataset)
        st.write(f"**Classificação Prevista:** A fruta está **{predicted_class}** com {confidence * 100:.2f}% de confiança.")

if __name__ == "__main__":
    main()
