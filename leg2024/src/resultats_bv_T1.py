import os
import requests
import xml.etree.ElementTree as ET
import csv

folder = "tmp/"















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
    files = list_files_in_folder(folder+"circo_xml")

    for file in files:

        xml_file_path = folder+"circo_xml/" + file
        print("xml to csv: ", file)

        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        departement_libelle = root.find('.//Departement/LibDpt').text

        for circo in root.findall('.//Circonscriptions/Circonscription'):

            cod_cir_elec = circo.find('.//CodCirElec').text
            #print("*** "+cod_cir_elec)
            lib_cir_elec = circo.find('.//LibCirElec').text

            tour = circo.find('.//Tours/Tour')
            inscrits_number = tour.find('.//Mentions/Inscrits/Nombre').text

            for candidat in tour.findall('.//Resultats/Candidats/Candidat'):

                id = candidat.find('NumPanneauCand').text if candidat.find('NumPanneauCand') is not None else ''
                nom_psn = candidat.find('NomPsn').text if candidat.find('NomPsn') is not None else ''
                prenom_psn = candidat.find('PrenomPsn').text if candidat.find('PrenomPsn') is not None else ''
                civilite_psn = candidat.find('CivilitePsn').text if candidat.find('CivilitePsn') is not None else ''
                cod_nua_cand = candidat.find('CodNuaCand').text if candidat.find('CodNuaCand') is not None else ''
                nb_voix = candidat.find('NbVoix').text if candidat.find('NbVoix') is not None else ''
                elu = candidat.find('Elu').text if candidat.find('Elu') is not None else ''

                # Append the row to the list
                rows.append([
                    cod_cir_elec +"_"+ id,
                    cod_cir_elec,
                    lib_cir_elec,
                    departement_libelle,
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
        'cand_id',
        'circo',
        'circo_lib',
        'dep_lib',
        'inscrits',
        'nom',
        'prenom',
        'civilite',
        'nuance',
        'voix',
        'statut'
    ]

    # Write the rows to a CSV file
    with open(folder+"resultats_tour1_par_circo.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)



#file_code = "R125"
#xml_to_csv("tmp/circo_xml/"+file_code+"CIR.xml", "tmp/circo_csv/"+file_code+"CIR.csv")



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
        url = "https://www.resultats-elections.interieur.gouv.fr/telechargements/LG2024/resultatsT1/"+dep+"/R1"+dep+"CIR.xml"

        response = requests.get(url)

        if response.status_code == 200:
            xml_file = folder + "circo_xml//R1"+dep+"CIR.xml"
            with open(xml_file, "wb") as file: file.write(response.content)
        else:
            print(f"Failed to download data for ",dep,"Status code: {response.status_code}")


#download()
#xml_to_csv()
