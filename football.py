import requests
import json
import openpyxl
import os

url = "https://v3.football.api-sports.io/fixtures/headtohead"
params = {"h2h": "124-127"} 
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "c71bb04ba5fcde0f4472c79fdc30a088"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

first_match = data.get("response", [])[0]
time1 = first_match["teams"]["home"]["name"]
time2 = first_match["teams"]["away"]["name"]

vitorias_time1 = 0
vitorias_time2 = 0
vitorias_time1_casa = 0
vitorias_time1_fora = 0
vitorias_time2_casa = 0
vitorias_time2_fora = 0

def definir_vencedor(match):
    """Determina qual time venceu e atualiza os contadores de vitória."""
    global vitorias_time1, vitorias_time2, vitorias_time1_casa, vitorias_time1_fora, vitorias_time2_casa, vitorias_time2_fora
    
    home_team = match["teams"]["home"]["name"]
    away_team = match["teams"]["away"]["name"]
    home_goals = match["goals"]["home"]
    away_goals = match["goals"]["away"]
    
    if home_goals is not None and away_goals is not None:
        if home_goals > away_goals:
            if home_team == time1:
                vitorias_time1 += 1
                vitorias_time1_casa += 1
            else:
                vitorias_time2 += 1
                vitorias_time2_casa += 1
        elif away_goals > home_goals:
            if away_team == time1:
                vitorias_time1 += 1
                vitorias_time1_fora += 1
            else:
                vitorias_time2 += 1
                vitorias_time2_fora += 1

total_partidas = 0
for match in data.get("response", []):
    if match["fixture"]["status"]["short"] == "FT": 
        definir_vencedor(match)
        total_partidas += 1

file_path = "dados1.xlsx"
if os.path.exists(file_path):
    wb = openpyxl.load_workbook(file_path)
else:
    wb = openpyxl.Workbook()
sheet = wb.active

sheet["A1"] = "Estatísticas de confrontos diretos"
sheet["A2"] = f"Total de partidas: {total_partidas}"
sheet["A3"] = f"Vitórias de {time1}: {vitorias_time1}"
sheet["A4"] = f"Vitórias de {time2}: {vitorias_time2}"
sheet["A5"] = f"Vitórias de {time1} em casa: {vitorias_time1_casa}"
sheet["A6"] = f"Vitórias de {time1} fora de casa: {vitorias_time1_fora}"
sheet["A7"] = f"Vitórias de {time2} em casa: {vitorias_time2_casa}"
sheet["A8"] = f"Vitórias de {time2} fora de casa: {vitorias_time2_fora}"

wb.save(file_path)
wb.close()

print("Dados atualizados no Excel com sucesso!")