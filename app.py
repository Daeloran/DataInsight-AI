import os
import pandas as pd
import markdown2
import plotly.express as px
import plotly.io as pio
import logging
from flask import Flask, render_template, request, redirect, flash, send_from_directory
from data_processing.data_cleaning import clean_data
from data_processing.data_analysis import analyze_data, format_summary
from data_processing.time_series_analysis import analyze_time_series, format_time_series_results, merge_time_series_with_analysis
from data_processing.interpretation import interpret_data
from data_processing.export_results import export_analysis_results

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXPORT_FOLDER'] = 'exports'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['EXPORT_FOLDER']):
    os.makedirs(app.config['EXPORT_FOLDER'])

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Fonction de lecture du fichier Excel
def read_excel(file_path):
    logging.info(f"Lecture du fichier Excel : {file_path}")
    df = pd.read_excel(file_path)
    return df

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
                include_time_series_in_export = 'include_time_series_in_export' in request.form

                # Lecture et nettoyage des données
                df = read_excel(file_path)
                df_clean = clean_data(df)
                
                # Analyse des données
                analysis_result, prediction_results = analyze_data(df_clean)
                formatted_summary = format_summary(df_clean, analysis_result, prediction_results)

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

                    if include_time_series_in_export:
                        # Fusion des résultats d'analyse standard et de séries temporelles
                        analysis_result = merge_time_series_with_analysis(analysis_result, time_series_results)

                # Convertir l'interprétation en HTML avec markdown2
                interpretation_summary_html = markdown2.markdown(interpretation_summary)
                interpretation_time_series_html = None
                if interpretation_time_series:
                    interpretation_time_series_html = markdown2.markdown(interpretation_time_series)

                # Exporter les résultats d'analyse
                csv_path, excel_path, json_path = export_analysis_results(df_clean, analysis_result, app.config['EXPORT_FOLDER'])
                csv_filename = os.path.basename(csv_path)
                excel_filename = os.path.basename(excel_path)
                json_filename = os.path.basename(json_path)

                # Visualisation des données
                graphs = []
                numeric_columns = df_clean.select_dtypes(include=['number']).columns
                for col in numeric_columns:
                    fig = px.line(df_clean, x=df_clean.index, y=col, title=f'Visualisation de {col}')
                    graphs.append(pio.to_html(fig, full_html=False))

                return render_template('index.html', interpretation_summary=interpretation_summary_html,
                                       interpretation_time_series=interpretation_time_series_html,
                                       graphs=graphs, csv_filename=csv_filename, excel_filename=excel_filename, json_filename=json_filename)
        except Exception as e:
            logging.error(f"Erreur lors du traitement des données: {e}")
            flash(f"Erreur lors du traitement des données: {e}", 'danger')
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['EXPORT_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
