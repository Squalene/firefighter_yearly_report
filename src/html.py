import base64
from pathlib import Path
from jinja2 import Template
from typing import Any
from xhtml2pdf import pisa

from weasyprint import HTML

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
 <meta charset="UTF-8">
 <title>Statistiques Individuelles {{report_year}}</title>
 <style>
 body { font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; }
 .container { width: 100%; max-width: 100%; margin: 0; padding: 20px; border: none; box-shadow: none; }
 
 /* Updated header styling */
 .header {
   display: flex;
   justify-content: space-between;
   align-items: center;
   margin-bottom: 30px;
 }
 .header img { 
   width: 120px; 
   height: auto;
 }
 .header-text {
   text-align: right;
   font-weight: bold;
 }
 .header-title {
   font-size: 16px;
 }
 .header-subtitle {
   font-size: 20px;
   margin-top: 5px;
 }
 
 .title { font-size: 20px; font-weight: bold; margin-top: 20px; }
 .highlight { font-weight: bold; color: #FFCC00; }
 .section { margin-top: 20px; clear: both; }
 .footer { font-size: 12px; text-align: center; margin-top: 30px; color: #777; clear: both; }
 .individual-stats-container { display: flex; justify-content: space-between; margin-top: 40px; width: 100%; }
 .individual-stats-box { width: 48%; text-align: center; }
 .stats-box { width: 48%; text-align: center; }
 .individual-stats-number { font-size: 60px; font-weight: bold; color: #001F5C; }
 
 /* Fixed plot containers for PDF rendering */
 .bar-plot-container {
   text-align: center;
   margin: 20px auto;
   width: 600px;
   max-width: 90%;
   position: relative;
 }
 .bar-plot-container img {
   display: inline-block;
   width: 100%;
   height: auto;
   max-height: 400px;
 }
 .donut-plot-container {
   text-align: center;
   margin: 20px auto;
   width: 200px;
   max-width: 90%;
   position: relative;
 }
 .donut-plot-container img {
   display: inline-block;
   width: 100%;
   height: auto;
 }
 
 /* WeasyPrint specific fixes */
 img {
   image-rendering: auto;
 }
 
 /* Add page break controls for PDF */
 .page-break {
   page-break-after: always;
 }
 @page {
   margin: 1cm;
   size: A4 portrait;
 }
 </style>
</head>
<body>
 <div class="container">
 <!-- Updated header with logo and text -->
 <div class="header">
   <div class="logo">
     <img src="{{ logo }}" alt="SDIS Logo">
   </div>
   <div class="header-text">
     <div class="header-title">SDIS REGIONAL DU NORD VAUDOIS</div>
     <div class="header-subtitle">OPERATIONNEL</div>
   </div>
 </div>
 
 <!-- Title -->
 <div class="title">STATISTIQUES INDIVIDUELLES | {{report_year}}</div>
 <div class="title"><strong>{{ grade }} {{ name_surname }}</strong></div>
 
 <!-- Status Usage Section -->
 <div class="section">
   <h3>Ton utilisation des statuts:</h3>
   <p>Compare tes états de planning avec les moyennes de ton OI. Là où tu excelles et là où il y a une marge de progression.</p>
   <div class="bar-plot-container">
     <img src="{{ bar_plot }}" alt="Stats Chart">
   </div>
 </div>
 
 <!-- Planning Completion -->
 <div class="section">
   <h3>Ton planning a été rempli à :</h3>
   <p>Maintiens ta disponibilité à jour pour garantir la fluidité de l'opérationnel. Tu as atteint <span class="highlight">{{ completion_rate }}%</span>
   <br><strong> {{ completion_rate_sentence }}</strong>
   </p>
   <div class="donut-plot-container">
     <img src="{{ donut_plot }}" alt="Completion Chart">
   </div>
 </div>
 
 <!-- Interventions & Alarms -->
 <div class="individual-stats-container">
   <div class="stats-box">
     <p><strong>Tu es intervenu-e sur :</strong></p>
     <span class="individual-stats-number">{{ alarm_intervention_count }}</span>
     <p>alarmes</p>
   </div>
   <div class="individual-stats-box">
     <p><strong>Sur {{ yearly_intervention_count }} interventions en {{report_year}}, ton organe d'intervention a été engagé sur :</strong></p>
     <span class="individual-stats-number">{{ oi_intervention_count }}</span>
     <p>interventions</p>
   </div>
 </div>
 
 <!-- Contact Information -->
 <div class="section">
   <p>Pour tout complément d'information, merci de contacter :</p>
   <p><strong>Of spéc Valériane Vuilleumier</strong></p>
 </div>
 
 <!-- Footer -->
 <div class="footer">
   SDIS REGIONAL DU NORD VAUDOIS · RUE DE L'ARSENAL 8 · 1400 YVERDON-LES-BAINS · 024 423 65 95 · <a href="https://www.sdisnv.ch">www.sdisnv.ch</a> · <a href="mailto:info@sdisnv.ch">info@sdisnv.ch</a>
 </div>
 </div>
</body>
</html>
"""

def encode_image(image_path: str| Path) -> str:
    with open(image_path, "rb") as img_file:
        return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"

def write_html_and_pdf(context: dict[str, Any], save_folder: str):

    if context["completion_rate"] >=90:
        context["completion_rate_sentence"] = "Excellent travail !"

    elif context["completion_rate"] >=80:
        context["completion_rate_sentence"] = "Bientôt à 90%, continue sur la même lancée"

    else:
        context["completion_rate_sentence"] = "Il y a matière à progresser."


    # Render the template
    template = Template(HTML_TEMPLATE)
    rendered_html = template.render(context)

    with open(save_folder / "report.html", "w", encoding="utf-8") as file:
        file.write(rendered_html)

    # Render HTML
    template = Template(HTML_TEMPLATE)
    rendered_html = template.render(context)

    # Convert HTML to PDF and save
    HTML(string=rendered_html).write_pdf(save_folder/"report.pdf")
