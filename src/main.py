import shutil
import pandas as pd
import numpy as np

from src.constants import OUTPUT_SAVE_DIR, RESSOURCE_DIR, ROOT_DIR
from src.html import encode_image, write_html_and_pdf
from src.plots import plot_donut, plot_occupation_categories

REPORT_YEAR = 2024
YEARLY_INTERVENTION_COUNT = 601
DATA_PATH = ROOT_DIR / "data/2023_STAT_IND.xlsx"

def main():
    
    df, merged_df = preprocess_data(DATA_PATH)

    for _, row in df.iterrows():
        id = row["ID"]
        print(id)
        save_path = OUTPUT_SAVE_DIR/ f"pompier_{id}"
        save_path.mkdir(parents=True, exist_ok=True)

        individual_merged_df = merged_df[merged_df["ID"]==id]
        bar_save_path = save_path / "bar_plot.png"
        donut_save_path = save_path / "donut_plot.png"
        logo_save_path = save_path/"logo.jpg"

        #Copy logo to html folder
        shutil.copy(RESSOURCE_DIR/"logo.jpg", logo_save_path)
        
        plot_occupation_categories(individual_merged_df, save_path=bar_save_path)
        plot_donut(row["RENSEIGNE"], save_path=donut_save_path)

        html_payload = {
            "report_year": REPORT_YEAR,
            "grade": row["GRADE"],
            "name_surname": row["NOM"],
            "completion_rate": round(100*row["RENSEIGNE"], 2),
            "alarm_intervention_count": row["MOBILISATION"],
            "oi_intervention_count":  row["INTERVENTION OI"],
            "yearly_intervention_count": YEARLY_INTERVENTION_COUNT,
            "logo": encode_image(logo_save_path),
            "bar_plot": encode_image(bar_save_path),
            "donut_plot": encode_image(donut_save_path),
        }
        write_html_and_pdf(html_payload, save_path)

def preprocess_data(data_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    STATUS_COLUMNS = ["ABSENT", "CADRE_ECA", "DISPO_ALARME", "ELEVE_ECA", "EXERCICE", "GR_SERV", "MAL_ACC", "PERM_COMPL", "PLAN_SPEC_ACTIF", "RENF_1", "RENF_2", "RESERVE"] 
    ID_COLUMNS = ["ID", "EMAIL", "GRADE", "NOM"]
    df = pd.read_excel(data_path)
    df["ID"] = np.arange(len(df))


    # Pivot to have one row/category
    occupation_melted_df = df[[*ID_COLUMNS, *STATUS_COLUMNS]].melt(id_vars=ID_COLUMNS, var_name="occupation_type", value_name="occupation_ratio")
    occupation_avg_s= df[STATUS_COLUMNS].mean()
    occupation_avg_df = pd.DataFrame({'occupation_type':occupation_avg_s.index, 'avg_occupation_ratio':occupation_avg_s.values})
    merged_df = pd.merge(occupation_melted_df, occupation_avg_df, on= "occupation_type")

    return df, merged_df

if __name__ == "__main__":
    main()
