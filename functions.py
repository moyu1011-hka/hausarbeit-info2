import requests
import json
import os
from datetime import datetime
import pandas as pd

from api_key import API_KEY # API-Schlüssel für die CoinGecko-API

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] # Richtige Reihenfolge der Wochentage

def fetch_token_data(token: str, days: int) -> str:
    """Ruft Token-Daten von der CoinGecko-API ab und speichert sie in einer JSON-Datei."""

    url = f"https://api.coingecko.com/api/v3/coins/{token}/market_chart" # API-URL

    headers = { # Header für die API-Anfrage
        "accept": "application/json",
        "x-cg-demo-api-key": API_KEY
    }

    params = { # Parameter für die API-Anfrage
        'vs_currency' : 'usd',
        'days' : str(days)
    }

    response = requests.get(url, params=params, headers=headers) # API-Anfrage
    data = response.json()
    filename = f"{token} data - {days} days.json" # Dateiname für die JSON-Datei
    with open(f"data/{filename}", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4) # Speichern der Daten in einer JSON-Datei
    
    return filename


def parse_token_data(token: str, days: int = 365) -> pd.DataFrame:
    """Analysiert Token-Daten aus einer JSON-Datei und gibt ein DataFrame mit Preis- und Volumendaten zurück."""

    filename = f"{token} data - {days} days.json"
    if not os.path.exists(f"data/{filename}"): # Überprüfen, ob die Datei existiert
        filename = fetch_token_data(token, days)

    # Berechnung der Differenz in Tagen zwischen dem heutigen Datum und dem Änderungsdatum der Datei:
    delta = (datetime.today() - datetime.fromtimestamp(os.path.getmtime(f"data/{filename}"))).days

    # Wenn die Zahl der zu analysierenden Tage kleiner oder gleich 7 ist oder die obige Differenz größer als 7 Tage ist, wird die Datei aktualisiert:
    if days <= 7 or delta >= 7:
        filename = fetch_token_data(token, days)
    
    with open(f"data/{filename}", "r", encoding='utf-8') as f:
        data = json.load(f)

    df_prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price']) # Erstellen eines DataFrames mit den Preisdaten
    df_volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume']) # Erstellen eines DataFrames mit den Volumendaten
    df_market_caps = pd.DataFrame(data['market_caps'], columns=['timestamp', 'market_cap']) # Erstellen eines DataFrames mit den Marktkapitalisierungsdaten
    df = pd.merge(pd.merge(df_prices, df_volumes, on='timestamp'), df_market_caps, on='timestamp') # Zusammenführen der DataFrames zu einem einzigen DataFrame
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms') # Umwandeln des Zeitstempels in ein Datetime-Format
    df.set_index('timestamp', inplace=True) # Setzen des Zeitstempels als Index

    return df


def calculate_volatility(token: str, days: int) -> pd.DataFrame:
    """Berechnet die tägliche Volatilität eines Tokens über eine angegebene Anzahl von Tagen."""

    results = []
    df = parse_token_data(token, days)
    df['date'] = df.index.date # Umwandeln des Zeitstempels in ein Datumsformat
    
    for day, daily_data in df.groupby("date"):
        daily_data['return'] = daily_data['price'].pct_change() # Berechnung der täglichen Rendite
        volatility = daily_data['return'].std() # Berechnung der Volatilität
        results.append({ # Die Ergebnisse werden in einer Liste gespeichert
            'date': day, 
            'weekday' : day.strftime('%A'), # Umwandeln des Datums in den Wochentag
            'volatility' : volatility
            })
        
    df = pd.DataFrame(results)
    df['weekday'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True) # Setzen der Reihenfolge der Wochentage
    
    return df


def calculate_volume(token: str, days: int) -> pd.DataFrame:
    """Berechnet das tägliche Handelsvolumen eines Tokens über eine angegebene Anzahl von Tagen."""
    
    results = []
    df = parse_token_data(token=token, days=days)
    df['date'] = df.index.date # Umwandeln des Zeitstempels in ein Datumsformat
    
    for day, daily_data in df.groupby("date"):
        daily_volume = daily_data['volume'].sum() # Berechnung des täglichen Handelsvolumens
        results.append({ # Die Ergebnisse werden in einer Liste gespeichert
            'date': day, 
            'weekday' : day.strftime('%A'), # Umwandeln des Datums in den Wochentag
            'daily_volume' : daily_volume
            })
        
    df = pd.DataFrame(results)
    df['weekday'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True) # Setzen der Reihenfolge der Wochentage
    
    return df


def sharpe_ratio(token: str) -> float:
    """Berechnet das Sharpe-Ratio eines Tokens basierend auf den täglichen Renditen der ersten Tage des Monats."""

    df = parse_token_data(token, 365) # Holen der Preisdaten für 365 Tage

    df_first_days = df[df.index.day == 1] # Filtern der Daten für die ersten Tage des Monats
    df_first_days = df_first_days.copy() # Kopieren der Daten, um eine Warnung zu vermeiden
    df_first_days['return'] = df_first_days['price'].pct_change() # Berechnung der monatlichen Rendite

    mean_return = df_first_days['return'].mean() # Berechnung der durchschnittlichen Rendite
    volatility = df_first_days['return'].std() # Berechnung der Volatilität
    sharpe = mean_return/volatility * 12**0.5 # Berechnung des Sharpe-Ratios
    # Das Sharpe-Ratio wird mit der Quadratwurzel von 12 multipliziert, um es auf eine jährliche Basis zu bringen.

    return sharpe