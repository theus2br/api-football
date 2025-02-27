import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Lista para armazenar os confrontos
confrontos = []

# Função para exibir as imagens dos times
def mostrar_imagens(dados_times):
    # Limpar o conteúdo atual de imagens
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Exibir as imagens dos times
    for time in dados_times['response']:
        logo_url = time['team']['logo']
        nome_time = time['team']['name']
        
        try:
            # Baixar a imagem
            response = requests.get(logo_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            
            # Redimensionar a imagem
            img = img.resize((80, 80))  # Ajuste o tamanho conforme necessário
            img_tk = ImageTk.PhotoImage(img)

            # Criar um Label para exibir a imagem
            label_img = tk.Label(canvas_frame, image=img_tk)
            label_img.image = img_tk  # Manter uma referência à imagem

            # Criar um botão para cada time, que quando clicado adiciona o time ao confronto
            label_img.bind("<Button-1>", lambda event, nome=nome_time: adicionar_time(nome))
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

# Função para adicionar o nome do time ao confronto
def adicionar_time(nome_time):
    if len(confrontos) % 2 == 0:
        # Adiciona o primeiro time ao confronto
        confrontos.append(nome_time)
    else:
        # Adiciona o segundo time ao confronto
        confrontos[-1] = confrontos[-1] + " X " + nome_time
        # Adiciona um salto de linha após cada confronto
        confrontos.append("")  # Essa linha adiciona uma "quebra" para o próximo confronto

    # Atualiza a label de confrontos com todos os confrontos e um salto de linha após cada confronto
    label_confrontos.config(text="\n".join(confrontos))

# Função para quando uma liga for selecionada no combobox
def on_liga_selecionada(event):
    liga = combobox_liga.get()
    # Mapeamento das ligas para seus respectivos IDs (você pode expandir conforme necessário)
    ligas = {
        "Serie A": "135",
        "La Liga": "140",  # Exemplo, substitua com o código correto da liga
        "Premier League": "39"  # Exemplo, substitua com o código correto da liga
    }
    
    liga_id = ligas.get(liga)
    if liga_id:
        obter_dados_times(liga_id)  # Chama a API com o ID da liga selecionada

# Criar a janela principal
root = tk.Tk()
root.title("Exibir Logos dos Times")

# Criar o Combobox para seleção de liga
combobox_liga = ttk.Combobox(root, values=["Serie A", "La Liga", "Premier League"])
combobox_liga.pack(pady=10)
combobox_liga.bind("<<ComboboxSelected>>", on_liga_selecionada)

# Canvas com Scrollbar para armazenar as imagens dos times
canvas = tk.Canvas(root)
canvas.pack(pady=10, fill="both", expand=True)

# Scrollbar associada ao Canvas
scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scrollbar.pack(side="bottom", fill="x")

canvas.configure(xscrollcommand=scrollbar.set)

# Frame dentro do Canvas para armazenar as imagens
canvas_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

# Configurar para que o canvas possa ser rolado
canvas_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Label para mostrar os confrontos
label_confrontos = tk.Label(root, text="Confrontos:\n", justify="left")
label_confrontos.pack(pady=10)

# Iniciar a interface gráfica
root.mainloop()
