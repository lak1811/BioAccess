import jinja2
import os
def get_html_template():
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Salary Report</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            color: #333;
            margin: 20px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }

        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 10px;
        }

        p {
            margin: 10px 0;
        }

        strong {
            color: #e74c3c;
        }

        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }

        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #2c3e50;
            color: #fff;
        }

        .total-section {
            margin-top: 20px;
            text-align: right;
        }

        .total-section strong {
            font-size: 1.2em;
            color: #27ae60;
        }
    </style>
</head>
<body>
    <h1>Lønn</h1>
    <p><strong>Periode:</strong> {{ start_dato }} - {{ slutt_dato }}</p>
    <p><strong>AnsattID:</strong> {{ ansattid }}</p>
    <p><strong>Navn:</strong> {{ navn }}</p>
    <p><strong>Stilling:</strong> {{ stilling }}</p>
    <p><strong>Timelonn:</strong> {{ timelonn }} kr</p>
    <p><strong>Antall timer:</strong> {{ timer }}</p>

    <table>
        <tr>
            <th>Beskrivelse</th>
            <th>Total</th>
        </tr>
        <tr>
            <td>Bruttolonn</td>
            <td>{{ bruttolonn }} kr</td>
        </tr>
        <tr>
            <td>Skatteprosent</td>
            <td>{{ skatteprosent}}%</td>
        </tr>
        <tr>
            <td>Nettolonn</td>
            <td>{{ nettolonn }} kr</td>
        </tr>

    </table>

    <div class="total-section">
        <p><strong>Utbetalt: {{ nettolonn }} kr</strong></p>
    </div>
</body>
</html>
"""

    return html_template


def generate(html_template,start_dato,slutt_dato,ansattid,navn,stilling,\
             timelonn,timer,brutto,skatteprosent,nettolonn):
    #get data from the parameters to the html file
    data={
        'ansattid' : ansattid,
        'stilling': stilling,
        'navn': navn,
        'timelonn': timelonn,
        'timer': timer,
        'bruttolonn': brutto,
        'skatteprosent': skatteprosent,
        'nettolonn': nettolonn,
        'start_dato': start_dato,
        'slutt_dato': slutt_dato,
    }
    #make an instance of the template
    template_instance=jinja2.Template(html_template)
    #send all the variables to the html file and generate a filename
    output = template_instance.render(data)
    filnavn=f"{data['ansattid']}_{data['start_dato']}_{data['slutt_dato']}"

    #make a folder if it doesnt exist
    folder_name='lonninger'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save the generated HTML to a file in the specified folder
    output_file_path = os.path.join(folder_name, filnavn)
    with open(output_file_path, 'w') as f:
        f.write(output)
    #confirmation and return
    print(f"Your file is saved as: {output_file_path} as an HTML file")
    return output_file_path,filnavn



