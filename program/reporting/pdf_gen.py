from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from datetime import datetime



def generate_table_pdf(results, bacteria, algorithm, bin_size):
    # Get current timestamp for filename
    current_timestamp = datetime.now()
    timestamp_str = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    filename = bacteria + "_" + algorithm + "_bin" + str(bin_size) + "_" + timestamp_str + ".pdf"

    # Document is created
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Title and subtitle are defined
    title_style = ParagraphStyle(name='TitleStyle', fontSize=16, alignment=1)
    title_paragraph = Paragraph("FAST AST", title_style)

    subtitle_style = ParagraphStyle(name='SubtitleStyle', fontSize=12, alignment=1)
    subtitle_paragraph = Paragraph("Results", subtitle_style)

    params_string = "Bacteria: " + bacteria + " --- Algorithm: " + algorithm + " --- Bin Size: " + str(bin_size)
    params_paragraph = Paragraph(params_string, subtitle_style)

    # Adds title and subtitle to the .pdf
    content = [title_paragraph, Spacer(1, 12), subtitle_paragraph, Spacer(1, 12), params_paragraph, Spacer(1, 12)]

    # Table is generated
    table = Table(results)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    content.append(table)

    # Builds document
    doc.build(content)


def generate_individual_pdf(data, file_name, results, bacteria, algorithm, bin_size):
    # Create a drawing
    drawing = Drawing(400, 200)

    # Create a line plot
    lp = LinePlot()
    lp.x = 50
    lp.y = 50
    lp.height = 125
    lp.width = 300
    lp.data = [data.to_numpy()]
    lp.lines[0].strokeWidth = 2
    lp.lines[0].strokeColor = colors.blue
    lp.joinedLines = 1
    lp.lineLabelFormat = '%2.0f'
    lp.lineLabels.visible = True


    # Add the line plot and legend to the drawing
    drawing.add(lp)

    # Create a PDF document
    doc = SimpleDocTemplate("plot_reportlab.pdf", pagesize=letter)
    story = [Paragraph("Sample Plot using ReportLab", ParagraphStyle(name='TitleStyle', fontSize=16, alignment=1)), Spacer(1, 12), drawing]

    # Build the PDF document
    doc.build(story)