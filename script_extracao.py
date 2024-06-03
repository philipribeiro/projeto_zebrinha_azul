import requests
import json
import pandas as pd

# Função conectando com API Weather
def req_clima(cidade, chave_api):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None

#Função contando com API GoogleMaps
def req_transito(orig, dest, chave_api):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={orig}&destination={dest}&key={chave_api}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None

#

def extrair_clima(dados):
    if dados:
        return {
            "Temp": dados.get("main", {}).get("temp"),
            "Sensacao": dados.get("main", {}).get("feels_like"),
            "Min": dados.get("main", {}).get("temp_min"),
            "Max": dados.get("main", {}).get("temp_max"),
            "Pressao": dados.get("main", {}).get("pressure"),
            "Umidade": dados.get("main", {}).get("humidity"),
            "Vento": dados.get("wind", {}).get("speed"),
            "Desc": dados.get("weather", [{}])[0].get("description")
        }
    return {}

#

def extrair_transito(dados):
    if dados:
        if dados.get("routes"):
            rota = dados["routes"][0]["legs"][0]
            passos = " -> ".join([step["html_instructions"] for step in rota.get("steps", [])])
            return {
                "Dist": rota.get("distance", {}).get("text"),
                "Duracao": rota.get("duration", {}).get("text"),
                "Inicio": rota.get("start_address"),
                "Fim": rota.get("end_address"),
                "Passos": passos
            }
    return {}

# Ler parâmetros do arquivo JSON
with open('parametros.json', 'r') as arq:
    params = json.load(arq)

# Substitua as chaves de API pelos seus valores reais
chave_clima = params['chave_api_clima']
chave_transito = params['chave_api_google_maps']

# Lista para armazenar os dados tabulados
dados_tabulados = []

# Obter dados do clima e trânsito para cada par de origem e destino
for orig in params['origens']:
    for dest in params['destinos']:
        clima_orig = req_clima(orig, chave_clima)
        clima_dest = req_clima(dest, chave_clima)
        transito = req_transito(orig, dest, chave_transito)
        
        info_clima_orig = extrair_clima(clima_orig)
        info_clima_dest = extrair_clima(clima_dest)
        info_transito = extrair_transito(transito)
        
        dados_tabulados.append({
            "Origem": orig,
            "Destino": dest,
            **{f"Clima_Orig_{k}": v for k, v in info_clima_orig.items()},
            **{f"Clima_Dest_{k}": v for k, v in info_clima_dest.items()},
            **{f"Transito_{k}": v for k, v in info_transito.items()}
        })

# Criar DataFrame
df = pd.DataFrame(dados_tabulados)

# Exibir DataFrame
print(df)

# Salvar arquivo CSV
df.to_csv('dados_tabulados.csv', index=False)
