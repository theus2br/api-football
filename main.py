import requests
import json
import openpyxl
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Importar o messagebox para o popup
from PIL import Image, ImageTk
from io import BytesIO

# Lista para armazenar os confrontos com nomes e IDs dos times
confrontos = []  # Para armazenar os nomes
confrontos_ids = []  # Para armazenar os IDs

# Função para exibir as imagens dos times
def mostrar_imagens(dados_times):
    # Limpar o conteúdo atual de imagens
    for widget in frame_imagens.winfo_children():
        widget.destroy()

    # Armazenar os dados dos times (com IDs)
    global time_ids
    time_ids = {}  # Dicionário para armazenar os IDs dos times
    for time in dados_times['response']:
        logo_url = time['team']['logo']
        nome_time = time['team']['name']
        id_time = time['team']['id']  # ID do time
        
        # Armazenar ID e nome do time
        time_ids[nome_time] = id_time
        
        try:
            # Baixar a imagem
            response = requests.get(logo_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            
            # Redimensionar a imagem
            img = img.resize((80, 80))  # Ajuste o tamanho conforme necessário
            img_tk = ImageTk.PhotoImage(img)

            label_img = tk.Label(frame_imagens, image=img_tk)
            label_img.image = img_tk  # Manter uma referência à imagem

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

# Função para adicionar o nome do time ao confronto com seus IDs
def adicionar_time(nome_time):
    if len(confrontos) % 2 == 0:
        # Adiciona o primeiro time ao confronto
        confrontos.append(nome_time)
        confrontos_ids.append(time_ids[nome_time])  # Armazenar o ID do time
    else:
        # Adiciona o segundo time ao confronto
        confrontos[-1] = confrontos[-1] + " X " + nome_time
        confrontos_ids[-1] = (confrontos_ids[-1], time_ids[nome_time])  # Atualiza os IDs do confronto
        confrontos.append("")  # Quebra de linha para o próximo confronto

    # Atualiza a label de confrontos com todos os confrontos e um salto de linha após cada confronto
    label_confrontos.config(text="\n".join(confrontos))

# Função para quando uma liga for selecionada no combobox
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
        obter_dados_times(liga_id)  # Chama a API com o ID da liga selecionada

# Função para consultar os confrontos e salvar no Excel
def consultar_confrontos(confrontos_ids):
    url = "https://v3.football.api-sports.io/fixtures/headtohead"
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": "c71bb04ba5fcde0f4472c79fdc30a088"
    }

    vitorias_time1 = 0
    vitorias_time2 = 0
    vitorias_time1_casa = 0
    vitorias_time1_fora = 0
    vitorias_time2_casa = 0
    vitorias_time2_fora = 0
    total_partidas = 0
    
    for confronto in confrontos_ids:
        if confronto == "":  # Ignora entradas vazias
            continue
        
        time1_id, time2_id = confronto  # Pega os IDs dos times
        
        print("Confronto:", {confronto}, "Time 1:", time1_id, "Time 2:", time2_id)
        params = {"h2h": f"{time1_id}-{time2_id}"}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            if data.get("response"):
                for match in data.get("response", []):
                    if match["fixture"]["status"]["short"] == "FT":
                        home_team = match["teams"]["home"]["name"]
                        away_team = match["teams"]["away"]["name"]
                        home_goals = match["goals"]["home"]
                        away_goals = match["goals"]["away"]
                        
                        if home_goals is not None and away_goals is not None:
                            if home_goals > away_goals:
                                if home_team == time1_id:
                                    vitorias_time1 += 1
                                    vitorias_time1_casa += 1
                                else:
                                    vitorias_time2 += 1
                                    vitorias_time2_casa += 1
                            elif away_goals > home_goals:
                                if away_team == time1_id:
                                    vitorias_time1 += 1
                                    vitorias_time1_fora += 1
                                else:
                                    vitorias_time2 += 1
                                    vitorias_time2_fora += 1
                        total_partidas += 1
        except Exception as e:
            print(f"Erro ao consultar confronto {time1_id} X {time2_id}: {e}")

    # Salvar os dados em um arquivo Excel
    file_path = "dados1.xlsx"
    if os.path.exists(file_path):
        wb = openpyxl.load_workbook(file_path)
    else:
        wb = openpyxl.Workbook()

    sheet = wb.active
    sheet["A1"] = "Estatísticas de confrontos diretos"
    sheet["A2"] = f"Total de partidas: {total_partidas}"
    sheet["A3"] = f"Vitórias de {confrontos[0]}: {vitorias_time1}"
    sheet["A4"] = f"Vitórias de {confrontos[1]}: {vitorias_time2}"
    sheet["A5"] = f"Vitórias de {confrontos[0]} em casa: {vitorias_time1_casa}"
    sheet["A6"] = f"Vitórias de {confrontos[0]} fora de casa: {vitorias_time1_fora}"
    sheet["A7"] = f"Vitórias de {confrontos[1]} em casa: {vitorias_time2_casa}"
    sheet["A8"] = f"Vitórias de {confrontos[1]} fora de casa: {vitorias_time2_fora}"

    wb.save(file_path)
    wb.close()

    # Exibir popup de sucesso
    messagebox.showinfo("Sucesso", "Dados atualizados no Excel com sucesso!")

    print("Total de partidas: ", {total_partidas})
    print("Vitorias de" , {confrontos[0]}, ": ",  {vitorias_time1})
    print("Vitorias de" , {confrontos[0]}, ": ",  {vitorias_time2})

# Criar a janela principal
root = tk.Tk()
root.title("Exibir Logos dos Times")

combobox_liga = ttk.Combobox(root, values=["Serie A(Italia)", "La Liga", "Premier League", "Serie A(Brasil)"])
combobox_liga.pack(pady=10)
combobox_liga.bind("<<ComboboxSelected>>", on_liga_selecionada)

frame_imagens = tk.Frame(root)
frame_imagens.pack(pady=10)

label_confrontos = tk.Label(root, text="Confrontos:\n", justify="left")
label_confrontos.pack(pady=10)

# Botão para consultar confrontos
botao_salvar = tk.Button(root, text="Salvar Dados", command=lambda: consultar_confrontos(confrontos_ids))
botao_salvar.pack(pady=10)

root.mainloop()
