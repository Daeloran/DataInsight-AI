import logging
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from flask import flash

def analyze_time_series(df):
    logging.info("Analyse des séries temporelles")
    time_series_results = []
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            for target_column in df.select_dtypes(include=['number']).columns:
                try:
                    df.set_index(column, inplace=True)
                    decomposition = seasonal_decompose(df[target_column], model='additive', period=7)
                    result = {
                        'target_column': target_column,
                        'trend': decomposition.trend.dropna().to_list(),
                        'seasonal': decomposition.seasonal.dropna().to_list(),
                        'residual': decomposition.resid.dropna().to_list()
                    }
                    time_series_results.append(result)
                    df.reset_index(inplace=True)  # Réinitialiser l'index
                except Exception as e:
                    logging.error(f"Erreur lors de la décomposition de {target_column} avec {column}: {e}")
                    flash(f"Erreur lors de la décomposition de {target_column} avec {column}: {e}", 'danger')
    return time_series_results

def format_time_series_results(time_series_results):
    logging.info("Formatage des résultats des séries temporelles pour l'IA")
    formatted = "Analyse des séries temporelles:\n"
    for result in time_series_results:
        formatted += f"\nColonne cible: {result['target_column']}\n"
        formatted += "Tendance:\n"
        formatted += f"{result['trend']}\n"
        formatted += "Saisonnalité:\n"
        formatted += f"{result['seasonal']}\n"
        formatted += "Résidu:\n"
        formatted += f"{result['residual']}\n"
    return formatted

def merge_time_series_with_analysis(analysis_result, time_series_results):
    time_series_df = pd.DataFrame()
    for result in time_series_results:
        target_column = result['target_column']
        trend = pd.Series(result['trend'], name=f'{target_column}_trend')
        seasonal = pd.Series(result['seasonal'], name=f'{target_column}_seasonal')
        residual = pd.Series(result['residual'], name=f'{target_column}_residual')
        time_series_df = pd.concat([time_series_df, trend, seasonal, residual], axis=1)

    # Fusionner les résultats d'analyse standard et de séries temporelles
    merged_result = pd.concat([analysis_result, time_series_df], axis=1)
    return merged_result
