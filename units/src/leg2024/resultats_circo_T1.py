import xml.etree.ElementTree as ET
import csv

folder = "tmp/"
file_code = "R125"


def xml_to_csv(xml_file_path, csv_file_path):
    # Parse the XML data from the file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Create a list to hold the rows for the CSV
    rows = []
    
    for circo in root.findall('.//Circonscriptions/Circonscription'):
        cod_cir_elec = circo.find('.//CodCirElec').text
        #print("*** "+cod_cir_elec)

        tour = circo.find('.//Tours/Tour')

        inscrits_number = tour.find('.//Mentions/Inscrits/Nombre').text

        for candidat in tour.findall('.//Resultats/Candidats/Candidat'):

            nom_psn = candidat.find('NomPsn').text if candidat.find('NomPsn') is not None else ''
            prenom_psn = candidat.find('PrenomPsn').text if candidat.find('PrenomPsn') is not None else ''
            civilite_psn = candidat.find('CivilitePsn').text if candidat.find('CivilitePsn') is not None else ''
            cod_nua_cand = candidat.find('CodNuaCand').text if candidat.find('CodNuaCand') is not None else ''
            nb_voix = candidat.find('NbVoix').text if candidat.find('NbVoix') is not None else ''
            elu = candidat.find('Elu').text if candidat.find('Elu') is not None else ''

            # Append the row to the list
            rows.append([
                cod_cir_elec,
                inscrits_number,
                nom_psn,
                prenom_psn,
                civilite_psn,
                cod_nua_cand,
                nb_voix,
                elu,
            ])

    # Define the CSV headers
    headers = [
        'circo',
        'inscrits',
        'nom',
        'prenom',
        'civilite',
        'nuance',
        'voix',
        'statut'
    ]
    
    # Write the rows to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)



xml_to_csv("tmp/circo_xml/"+file_code+"CIR.xml", "tmp/circo_csv/"+file_code+"CIR.csv")
