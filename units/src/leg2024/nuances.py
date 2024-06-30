import requests
import xml.etree.ElementTree as ET
import csv


folder = "tmp/"
url = "https://www.resultats-elections.interieur.gouv.fr/telechargements/LG2024/nuances/nuances.xml"
xml_file = folder + "nuances.xml"
csv_file= folder + "nuances.csv"

def download():
    response = requests.get(url)

    if response.status_code == 200:
        with open(xml_file, "wb") as file: file.write(response.content)
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")



def xml_to_csv():
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["NumOrdNuaCand", "CodNuaCand", "LibNuaCand"])

        # Iterate over each NuanceCandidat element and write its data to the CSV
        for nuance_candidat in root.findall('.//NuanceCandidat'):
            num_ord_nua_cand = nuance_candidat.find('NumOrdNuaCand').text
            cod_nua_cand = nuance_candidat.find('CodNuaCand').text
            lib_nua_cand = nuance_candidat.find('LibNuaCand').text
            writer.writerow([num_ord_nua_cand, cod_nua_cand, lib_nua_cand])

    print(f"CSV file '{csv_file}' has been created successfully.")


# Convert the XML to CSV
xml_to_csv()


