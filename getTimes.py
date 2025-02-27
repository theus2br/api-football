import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

confrontos = []

def mostrar_imagens(dados_times):
    for widget in frame_imagens.winfo_children():
        widget.destroy()

    for time in dados_times['response']:
        logo_url = time['team']['logo']
        nome_time = time['team']['name']
        
        try:
            response = requests.get(logo_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            
            img = img.resize((80, 80)) 
            img_tk = ImageTk.PhotoImage(img)

            label_img = tk.Label(frame_imagens, image=img_tk)
            label_img.image = img_tk 

            label_img.bind("<Button-1>", lambda event, nome=nome_time: adicionar_time(nome))
            label_img.pack(side="left", padx=5)  
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")

def obter_dados_times(liga):
    url = f'https://v3.football.api-sports.io/teams?league={liga}&season=2023'
    headers = {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': 'c71bb04ba5fcde0f4472c79fdc30a088' 
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            mostrar_imagens(dados)  
        else:
            print("Erro ao obter dados da API.")
    except Exception as e:
        print(f"Erro ao chamar API: {e}")

def adicionar_time(nome_time):
    if len(confrontos) % 2 == 0:
        confrontos.append(nome_time)
    else:
        confrontos[-1] = confrontos[-1] + " X " + nome_time
        confrontos.append("") 

    label_confrontos.config(text="\n".join(confrontos))

def on_liga_selecionada(event):
    liga = combobox_liga.get()
    ligas = {
        "Serie A(Italia)": "135",
        "La Liga": "140", 
        "Premier League": "39",
        "Serie A(Brasil)": "71"   
    }
    
    liga_id = ligas.get(liga)
    if liga_id:
        obter_dados_times(liga_id) 

root = tk.Tk()
root.title("Exibir Logos dos Times")

combobox_liga = ttk.Combobox(root, values=["Serie A(Italia)", "La Liga", "Premier League", "Serie A(Brasil)"])
combobox_liga.pack(pady=10)
combobox_liga.bind("<<ComboboxSelected>>", on_liga_selecionada)

frame_imagens = tk.Frame(root)
frame_imagens.pack(pady=10)

label_confrontos = tk.Label(root, text="Confrontos:\n", justify="left")
label_confrontos.pack(pady=10)

root.mainloop()
