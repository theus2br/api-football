import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Função para exibir as imagens dos times
def mostrar_imagens(dados_times):
    # Limpar o conteúdo atual de imagens
    for widget in frame_imagens.winfo_children():
        widget.destroy()

    # Exibir as imagens dos times
    for time in dados_times['response']:
        logo_url = time['team']['logo']
        try:
            # Baixar a imagem
            response = requests.get(logo_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            
            # Redimensionar a imagem
            img = img.resize((80, 80))  # Ajuste o tamanho conforme necessário
            img_tk = ImageTk.PhotoImage(img)

            # Criar um Label para exibir a imagem
            label_img = tk.Label(frame_imagens, image=img_tk)
            label_img.image = img_tk  # Manter uma referência à imagem
            label_img.pack(side="left", padx=5)  # Exibir a imagem lado a lado
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")

# Função para chamar a API e pegar os dados dos times da liga
def obter_dados_times(liga):
    url = f'https://v3.football.api-sports.io/teams?league={liga}&season=2023'
    headers = {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': 'c71bb04ba5fcde0f4472c79fdc30a088'  # Substitua pela sua chave
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            mostrar_imagens(dados)  # Passa os dados para a função de exibição das imagens
        else:
            print("Erro ao obter dados da API.")
    except Exception as e:
        print(f"Erro ao chamar API: {e}")

# Função para quando uma liga for selecionada no combobox
def on_liga_selecionada(event):
    liga = combobox_liga.get()
    # Mapeamento das ligas para seus respectivos IDs (você pode expandir conforme necessário)
    ligas = {
        "Serie A(Italia)": "135",
        "La Liga": "140",
        "Premier League": "39",
        "Serie A(Brasil)": "71"
    }
    
    liga_id = ligas.get(liga)
    if liga_id:
        obter_dados_times(liga_id)  # Chama a API com o ID da liga selecionada

# Criar a janela principal
root = tk.Tk()
root.title("Exibir Logos dos Times")

# Criar o Combobox para seleção de liga
combobox_liga = ttk.Combobox(root, values=["Serie A(Italia)", "La Liga", "Premier League", "Serie A(Brasil)"])
combobox_liga.pack(pady=10)
combobox_liga.bind("<<ComboboxSelected>>", on_liga_selecionada)

# Frame para armazenar as imagens
frame_imagens = tk.Frame(root)
frame_imagens.pack(pady=10)

# Iniciar a interface gráfica
root.mainloop()
