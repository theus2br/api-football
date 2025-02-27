import requests
import json
import openpyxl
import os
print(os.path.exists("dados1.xlsx"))


# Configurar API
url = "https://v3.football.api-sports.io/fixtures/headtohead"
params = {"h2h": "124-127"}
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "c71bb04ba5fcde0f4472c79fdc30a088"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Pegar os times
first_match = data.get("response", [])[0]
time1 = first_match["teams"]["home"]["name"]
time2 = first_match["teams"]["away"]["name"]

# Criar variáveis para os gols
estadio1, estadio2, estadio3 = None, None, None
gols_time1, gols_time2 = {}, {}

for match in data.get("response", []):
    venue_name = match["fixture"]["venue"].get("name", "")
    home_team = match["teams"]["home"]["name"]
    away_team = match["teams"]["away"]["name"]
    home_goals = match["goals"]["home"] or 0
    away_goals = match["goals"]["away"] or 0

    if estadio1 is None:
        estadio1 = venue_name
    elif estadio1 and estadio2 is None and venue_name != estadio1:
        estadio2 = venue_name
    elif estadio1 and estadio2 and estadio3 is None and venue_name not in [estadio1, estadio2]:
        estadio3 = venue_name

    if venue_name not in gols_time1:
        gols_time1[venue_name] = 0
        gols_time2[venue_name] = 0
    
    if home_team == time1:
        gols_time1[venue_name] += home_goals
        gols_time2[venue_name] += away_goals
    else:
        gols_time1[venue_name] += away_goals
        gols_time2[venue_name] += home_goals

# Abrir o arquivo Excel existente
file_path = "dados1.xlsx"  # Substitua pelo nome real do arquivo
wb = openpyxl.load_workbook(file_path)
sheet = wb.active

# Escrever os dados no Excel
sheet["A1"] = f"{time1} gols {estadio1}: {gols_time1.get(estadio1, 0)}"
sheet["B1"] = f"{time2} gols {estadio1}: {gols_time2.get(estadio1, 0)}"
sheet["C1"] = f"{time1} gols {estadio3}: {gols_time1.get(estadio3, 0)}" if estadio2 else ""

wb.save(file_path)
wb.close()

print("Dados atualizados no Excel com sucesso!")
