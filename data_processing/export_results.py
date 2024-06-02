import os

def export_to_csv(df, filename):
    df.to_csv(filename, index=False)

def export_to_excel(df, filename):
    df.to_excel(filename, index=False)

def export_to_json(df, filename):
    df.to_json(filename, orient='records', lines=True)

def export_analysis_results(df, results, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_path = os.path.join(folder_path, "analysis_results.csv")
    excel_path = os.path.join(folder_path, "analysis_results.xlsx")
    json_path = os.path.join(folder_path, "analysis_results.json")

    export_to_csv(results, csv_path)
    export_to_excel(results, excel_path)
    export_to_json(results, json_path)

    return csv_path, excel_path, json_path
