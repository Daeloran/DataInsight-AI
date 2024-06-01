import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.express as px
import plotly.io as pio
import markdown2
import os
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Fonction de lecture du fichier Excel
def read_excel(file_path):
    logging.info(f"Lecture du fichier Excel : {file_path}")
    df = pd.read_excel(file_path)
    return df

# Fonction de nettoyage des données
def clean_data(df):
    logging.info("Nettoyage des données")
    df = df.dropna()  # Suppression des lignes avec des valeurs manquantes
    return df

# Fonction d'analyse des données
def analyze_data(df):
    logging.info("Analyse des données")
    summary = df.describe(include='all')
    return summary

# Fonction de formatage des résultats pour l'IA
def format_summary(df, summary):
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
    
    return formatted

# Fonction pour détecter et analyser les séries temporelles
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

# Fonction de formatage des résultats de séries temporelles pour l'IA
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

# Fonction d'interprétation des résultats
def interpret_data(formatted_data):
    logging.info("Interprétation des résultats par l'IA")
    llm = Ollama(model='llama3')
    chain = ConversationChain(llm=llm)

    # Question à l'agent IA
    question = (
        f"Voici les résultats de l'analyse des données :\n{formatted_data}\n"
        "Peux-tu les interpréter et me donner un résumé des points clés (en français), "
        "en structurant ta réponse de manière claire et concise ?"
    )
    response = chain.invoke(question)
    return response['response']

# Route principale
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Check if a file is uploaded
            if 'file' not in request.files:
                flash('Aucun fichier sélectionné', 'danger')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('Aucun fichier sélectionné', 'danger')
                return redirect(request.url)
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                
                # Options sélectionnées
                analyze_standard = 'analyze_standard' in request.form
                analyze_time_series_option = 'analyze_time_series' in request.form

                # Lecture et nettoyage des données
                df = read_excel(file_path)
                df_clean = clean_data(df)
                
                # Analyse des données
                analysis_result = analyze_data(df_clean)
                formatted_summary = format_summary(df_clean, analysis_result)

                # Interprétation des résultats
                interpretation_summary = interpret_data(formatted_summary)
                
                # Initialisation des résultats des séries temporelles
                time_series_results = None
                formatted_time_series = None
                interpretation_time_series = None

                if analyze_time_series_option:
                    # Analyse des séries temporelles
                    time_series_results = analyze_time_series(df_clean)
                    formatted_time_series = format_time_series_results(time_series_results)
                    
                    # Interprétation des séries temporelles
                    interpretation_time_series = interpret_data(formatted_time_series)

                # Convertir l'interprétation en HTML avec markdown2
                interpretation_summary_html = markdown2.markdown(interpretation_summary)
                interpretation_time_series_html = None
                if interpretation_time_series:
                    interpretation_time_series_html = markdown2.markdown(interpretation_time_series)

                # Visualisation des données
                graphs = []
                numeric_columns = df_clean.select_dtypes(include=['number']).columns
                for col in numeric_columns:
                    fig = px.line(df_clean, x=df_clean.index, y=col, title=f'Visualisation de {col}')
                    graphs.append(pio.to_html(fig, full_html=False))

                return render_template('index.html', interpretation_summary=interpretation_summary_html,
                                       interpretation_time_series=interpretation_time_series_html,
                                       graphs=graphs)
        except Exception as e:
            logging.error(f"Erreur lors du traitement des données: {e}")
            flash(f"Erreur lors du traitement des données: {e}", 'danger')
            return redirect(request.url)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
