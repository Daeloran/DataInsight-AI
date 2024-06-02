import logging
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def analyze_data(df):
    logging.info("Analyse des données")

    # Statistiques descriptives
    summary = df.describe(include='all')

    # Modèle de prédiction pour les colonnes numériques
    prediction_results = {}
    numeric_df = df.select_dtypes(include=['number'])
    for column in numeric_df.columns:
        if numeric_df[column].isnull().sum() == 0:  # Vérifie que la colonne cible n'a pas de NaN
            X = numeric_df.drop(columns=[column])
            y = numeric_df[column]
            if X.isnull().sum().sum() == 0 and y.isnull().sum() == 0:  # Vérifie que X et y n'ont pas de NaN
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestRegressor()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                prediction_results[column] = mse
                logging.info(f"Prédiction pour {column} terminée avec MSE: {mse}")
            else:
                logging.warning(f"Colonnes contenant des NaN après imputation, non utilisées pour la prédiction: {column}")

    return summary, prediction_results

def format_summary(df, summary, prediction_results):
    logging.info("Formatage des résultats pour l'IA")
    formatted = "Analyse des données:\n"
    for stat in summary.index:
        formatted += f"\n{stat}:\n"
        for column in summary.columns:
            value = summary.at[stat, column]
            if pd.notna(value):  # Vérifie que la valeur n'est pas NaN
                formatted += f" - {column}: {value}\n"

    # Ajout des statistiques catégorielles
    for column in df.select_dtypes(include=['object']).columns:
        value_counts = df[column].value_counts()
        formatted += f"\nDistribution pour {column}:\n"
        for val, count in value_counts.items():
            formatted += f" - {val}: {count}\n"

    # Ajout des résultats de prédiction
    formatted += "\nRésultats de prédiction:\n"
    for column, mse in prediction_results.items():
        formatted += f" - {column}: MSE = {mse}\n"

    return formatted
