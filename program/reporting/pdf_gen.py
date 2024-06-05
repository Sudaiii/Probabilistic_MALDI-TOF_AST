import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from datetime import datetime

from variables import RESOURCE_PATH

from .visualization_utils import spectrometry


TITLE_STYLE = ParagraphStyle(name='TitleStyle', fontSize=16, alignment=1)
TITLE_STYLE.fontName = "Helvetica-Bold"
SUBTITLE_STYLE = ParagraphStyle(name='SubtitleStyle', fontSize=12, alignment=1)
TABLE_STYLE = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#232629")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])



def generate_table_pdf(data, file_names, results, bacteria, algorithm, bin_size):
    # Generate table
    headers = ["File"]
    for key in results[0].keys():
        headers.append(key)

    pdf_table = [
        headers
    ]   

    for i in range(len(results)):
        pdf_row = []
        pdf_row.append(file_names[i])

        for antibiotic in results[i]:
            rounded_proba = round(results[i][antibiotic], 4)
            pdf_row.append(f"{rounded_proba*100:.2f}%")
        
        pdf_table.append(pdf_row)

    # Get current timestamp for .pdf file name
    current_timestamp = datetime.now()
    timestamp_str = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    bacteria_dictionary_file = open(RESOURCE_PATH+"bacteria.json", "r")
    bacteria_dictionary = json.load(bacteria_dictionary_file)
    bacteria_alias = bacteria_dictionary[bacteria]
    pdf_file_name = bacteria_alias + "_" + algorithm + "_bin" + str(bin_size) + "_" + timestamp_str + ".pdf"

    # Document is created
    doc = SimpleDocTemplate(pdf_file_name, pagesize=letter)

    # Title and subtitle are defined
    title_paragraph = Paragraph("Fast AST", TITLE_STYLE)
    subtitle_paragraph = Paragraph("Perfil de resistencia antimicrobiana", SUBTITLE_STYLE)

    # Table is generated
    table = Table(pdf_table)
    table.setStyle(TABLE_STYLE)

    # Parameters table is defined
    param_table = [
        ["Bacteria", "Algorithm", "Bin Size"],
        [bacteria, algorithm, str(bin_size)]
    ]
    param_table = Table(param_table)
    param_table.setStyle(TABLE_STYLE)

    content = [
        title_paragraph, 
        Spacer(1, 8), 
        subtitle_paragraph, 
        Spacer(1, 12), 
        table,
        Spacer(1, 12),
        param_table
    ]

    # Generate other pages
    for i in range(len(results)):
        content.append(PageBreak())
        page = generate_individual_pdf(data[i], file_names[i], results[i], bacteria, algorithm, bin_size, independent=False)
        for row in page:
            content.append(row)

    # Builds document
    doc.build(content)
    


def generate_individual_pdf(data, file_name, results, bacteria, algorithm, bin_size, independent=True):
    bacteria_dictionary_file = open(RESOURCE_PATH+"bacteria.json", "r")
    bacteria_dictionary = json.load(bacteria_dictionary_file)
    bacteria_alias = bacteria_dictionary[bacteria]
    pdf_file_name = file_name + "_" + bacteria_alias + "_" + algorithm + "_bin" + str(bin_size) + ".pdf"

    doc = SimpleDocTemplate(pdf_file_name, pagesize=letter)

    # Title and subtitle are defined
    title_paragraph = Paragraph("Fast AST", TITLE_STYLE)
    subtitle_paragraph = Paragraph("Perfil de resistencia antimicrobiana", SUBTITLE_STYLE)

    file_style = ParagraphStyle(name='SubtitleStyle', fontSize=12, alignment=1)
    file_style.fontName = "Helvetica-Bold"
    file_paragraph = Paragraph(file_name, file_style)

    # MS graph is created
    image = spectrometry(data, bin_size)

    # Table is generated
    antibiotics = []
    probabilities = []
    for key in results.keys():
        antibiotics.append(key)
        probabilities.append(str(round(results[key], 4)*100)+"%")
    tabulated_results = [antibiotics, probabilities]

    table = Table(tabulated_results)
    table.setStyle(TABLE_STYLE)
    
    # Parameters table is defined
    param_table = [
        ["Bacteria", "Algorithm", "Bin Size"],
        [bacteria, algorithm, str(bin_size)]
    ]
    param_table = Table(param_table)
    param_table.setStyle(TABLE_STYLE)

    # Add the line plot and legend to the drawing
    content = [
        title_paragraph, 
        Spacer(1, 8), 
        subtitle_paragraph, 
        Spacer(1, 12), 
        file_paragraph,
        Spacer(1, 12), 
        image,
        Spacer(1, 12), 
        table,
        Spacer(1, 12),
        param_table
    ]

    if independent:
        # Build the PDF document
        doc.build(content)
    return content