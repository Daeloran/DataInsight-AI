import pandas as pd
import matplotlib.pyplot as plt
from langchain.llms import Ollama
from langchain.chains import ConversationChain

# Fonction de lecture du fichier Excel
def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df

# Fonction de nettoyage des données
def clean_data(df):
    df = df.dropna()  # Suppression des lignes avec des valeurs manquantes
    return df

# Fonction d'analyse des données
def analyze_data(df):
    summary = df.describe(include='all')
    return summary

# Fonction de formatage des résultats pour l'IA
def format_summary(summary):
    formatted = "Analyse des données:\n"
    for stat in summary.index:
        formatted += f"\n{stat}:\n"
        for column in summary.columns:
            value = summary.at[stat, column]
            if pd.notna(value):  # Vérifie que la valeur n'est pas NaN
                formatted += f" - {column}: {value}\n"
    return formatted

# Fonction d'interprétation des résultats
def interpret_data(formatted_summary):
    llm = Ollama(model='llama3')
    chain = ConversationChain(llm=llm)

    # Question à l'agent IA
    question = f"Voici les résultats de l'analyse des données :\n{formatted_summary}\nPeux-tu les interpréter et me donner un résumé des points clés (en français) ?"
    response = chain.run(question)
    return response

# Fonction de visualisation des données
def visualize_data(df):
    df.plot(kind='line')
    plt.show()

# Fonction principale
def main():
    # Chemin du fichier Excel de test
    file_path = './exemple_donnees.xslx'
    
    # Lecture et nettoyage des données
    df = read_excel(file_path)
    df_clean = clean_data(df)
    
    # Analyse des données
    analysis_result = analyze_data(df_clean)
    
    # Formatage des résultats pour l'IA
    formatted_summary = format_summary(analysis_result)
    
    # Interprétation des résultats
    interpretation = interpret_data(formatted_summary)
    
    # Affichage des résultats
    print("Analyse des données:\n", analysis_result)
    print("\nInterprétation de l'IA:\n", interpretation)
    
    # Visualisation des données
    visualize_data(df_clean)

if __name__ == "__main__":
    main()
