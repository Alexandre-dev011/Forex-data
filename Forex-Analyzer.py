import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

def download_forex_data(symbol, start_date, end_date):
    """
    Télécharge les données Forex historiques en utilisant Yahoo Finance.
    """
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def calculate_statistics(data):
    """
    Calcule les statistiques pour donner des recommandations.
    """
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['MA_200'] = data['Close'].rolling(window=200).mean()
    data['Trend'] = np.where(data['MA_50'] > data['MA_200'], 'Hausse', 'Baisse')
    success_rate = np.mean(data['Trend'] == 'Hausse') * 100
    return data, success_rate

def generate_recommendation(data, success_rate):
    """
    Génère une recommandation basée sur les statistiques.
    """
    latest_trend = data['Trend'].iloc[-1]
    if latest_trend == 'Hausse':
        recommendation = f"Acheter (Tendance haussière) - Taux de réussite : {success_rate:.2f}%"
    else:
        recommendation = f"Vendre (Tendance baissière) - Taux de réussite : {success_rate:.2f}%"
    return recommendation

def plot_data(data, symbol):
    """
    Affiche les données Forex avec des indicateurs techniques.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Prix de clôture', alpha=0.5)
    plt.plot(data['MA_50'], label='Moyenne mobile (50 jours)', linestyle='--')
    plt.plot(data['MA_200'], label='Moyenne mobile (200 jours)', linestyle='--')
    plt.title(f'Analyse Forex pour {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Prix')
    plt.legend()
    plt.show()

def display_menu():
    """
    Affiche un menu stylé pour l'utilisateur.
    """
    print("""
    ███████╗ ██████╗ ██████╗ ███████╗██╗  ██╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
    █████╗  ██║   ██║██████╔╝█████╗   ╚███╔╝ 
    ██╔══╝  ██║   ██║██╔══██╗██╔══╝   ██╔██╗ 
    ██║     ╚██████╔╝██║  ██║███████╗██╔╝ ██╗
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """)
    print("1. Analyser une paire Forex")
    print("2. Afficher les graphiques")
    print("3. Obtenir une recommandation")
    print("4. Quitter")

def main():
    symbol = None
    data = None
    success_rate = None

    while True:
        display_menu()
        choice = input("Choisissez une option (1-4) : ")

        if choice == "1":
            symbol = input("Entrez la paire Forex (ex: EURUSD=X) : ")
            start_date = input("Entrez la date de début (YYYY-MM-DD) : ")
            end_date = input("Entrez la date de fin (YYYY-MM-DD) : ")
            data = download_forex_data(symbol, start_date, end_date)
            data, success_rate = calculate_statistics(data)
            print("Données téléchargées et analysées avec succès !")

        elif choice == "2":
            if data is not None:
                plot_data(data, symbol)
            else:
                print("Veuillez d'abord télécharger les données (Option 1).")

        elif choice == "3":
            if data is not None:
                recommendation = generate_recommendation(data, success_rate)
                print(f"Recommandation : {recommendation}")
            else:
                print("Veuillez d'abord télécharger les données (Option 1).")

        elif choice == "4":
            print("Merci d'avoir utilisé Forex Analyzer. À bientôt !")
            break

        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
