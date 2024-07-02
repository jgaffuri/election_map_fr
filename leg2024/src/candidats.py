import os
import requests
import xml.etree.ElementTree as ET
import csv

folder = "tmp/"
tour = "2"

def list_files_in_folder(folder_path):
    try:
        # Get the list of all files and directories in the specified directory
        files = os.listdir(folder_path)
        # Filter out directories, only keep files
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def xml_to_csv():

    rows = []

    #get all xml files
    files = list_files_in_folder(folder+"candidats_T"+tour+"_xml")

    for file in files:

        xml_file_path = folder+"candidats_T"+tour+"_xml/" + file
        print("xml to csv: ", file)

        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        departement_libelle = root.find('.//Departement/LibDpt').text

        for circo in root.findall('.//Departement/Circonscriptions/Circonscription'):

            cod_cir_elec = circo.find('.//CodCirElec').text
            #print("*** "+cod_cir_elec)
            lib_cir_elec = circo.find('.//LibCirElec').text

            for candidat in circo.findall('.//Candidats/Candidat'):

                id = candidat.find('NumPanneauCand').text if candidat.find('NumPanneauCand') is not None else ''
                nom_psn = candidat.find('NomPsn').text if candidat.find('NomPsn') is not None else ''
                prenom_psn = candidat.find('PrenomPsn').text if candidat.find('PrenomPsn') is not None else ''
                civilite_psn = candidat.find('CivilitePsn').text if candidat.find('CivilitePsn') is not None else ''
                cod_nua_cand = candidat.find('CodNuaCand').text if candidat.find('CodNuaCand') is not None else ''

                # Append the row to the list
                rows.append([
                    cod_cir_elec +"_"+ id,
                    cod_cir_elec,
                    lib_cir_elec,
                    departement_libelle,
                    nom_psn,
                    prenom_psn,
                    civilite_psn,
                    cod_nua_cand,
                ])

    # Define the CSV headers
    headers = [
        'cand_id',
        'circo',
        'circo_lib',
        'dep_lib',
        'nom',
        'prenom',
        'civilite',
        'nuance'
    ]

    # Write the rows to a CSV file
    with open(folder+"candidats_T"+tour+".csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)






def get_liste_deps():
    out = []
    for i in range(1,96):
        if i<10: out.append("0"+str(i))
        elif i==20: 
            out.append("2A")
            out.append("2B")
        else: out.append(str(i))
    out.append("971")
    out.append("972")
    out.append("973")
    out.append("974")
    out.append("975")
    out.append("976")
    out.append("986")
    out.append("987")
    out.append("988")
    out.append("ZX")
    out.append("ZZ")

    return out


#print(get_liste_deps())

def download():
    for dep in get_liste_deps():
        print("download", dep)
        url = "https://www.resultats-elections.interieur.gouv.fr/telechargements/LG2024/candidatsT"+tour+"/"+dep+"/C"+tour+dep+".xml"

        response = requests.get(url)

        if response.status_code == 200:
            xml_file = folder + "candidats_T"+tour+"_xml/C"+tour+dep+".xml"
            with open(xml_file, "wb") as file: file.write(response.content)
        else:
            print(f"Failed to download data for ",dep,"Status code: {response.status_code}")


#download()
xml_to_csv()
