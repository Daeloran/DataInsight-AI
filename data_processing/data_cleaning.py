import logging
import pandas as pd
from sklearn.impute import KNNImputer
from pyod.models.iforest import IForest

def clean_data(df):
    logging.info("Nettoyage des données")
    
    # Séparer les colonnes numériques et non numériques
    numeric_df = df.select_dtypes(include=['number'])
    non_numeric_df = df.select_dtypes(exclude=['number'])

    # Imputation des valeurs manquantes uniquement pour les colonnes numériques
    imputer = KNNImputer(n_neighbors=5)
    numeric_df_imputed = pd.DataFrame(imputer.fit_transform(numeric_df), columns=numeric_df.columns)
    logging.info("Imputation des valeurs manquantes terminée")

    # Détection et suppression des anomalies uniquement pour les colonnes numériques
    clf = IForest(contamination=0.1)
    clf.fit(numeric_df_imputed)
    y_pred = clf.labels_
    numeric_df_cleaned = numeric_df_imputed[y_pred == 0]
    logging.info("Détection et suppression des anomalies terminée")

    # Réintégrer les colonnes non numériques
    cleaned_df = pd.concat([numeric_df_cleaned.reset_index(drop=True), non_numeric_df.reset_index(drop=True)], axis=1)
    return cleaned_df
