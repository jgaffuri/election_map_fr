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


def xml_to_csv(T):

    rows = []

    #get all xml files
    files = list_files_in_folder(folder+"resultats_circo_T1T2_xml")

    for file in files:

        xml_file_path = folder+"resultats_circo_T1T2_xml/" + file
        print("xml to csv: ", file)


        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        departement_libelle = root.find('.//Departement/LibDpt').text

        for circo in root.findall('.//Circonscriptions/Circonscription'):

            cod_cir_elec = circo.find('.//CodCirElec').text
            #print("*** "+cod_cir_elec)
            lib_cir_elec = circo.find('.//LibCirElec').text

            for tour in circo.findall('.//Tours/Tour'):

                n_tour = tour.find('.//NumTour').text
                if(n_tour != T): continue

                inscrits_number = tour.find('.//Mentions/Inscrits/Nombre').text
                abstention_number = tour.find('.//Mentions/Abstentions/Nombre').text
                votants_number = tour.find('.//Mentions/Votants/Nombre').text
                blancs_number = tour.find('.//Mentions/Blancs/Nombre').text
                nuls_number = tour.find('.//Mentions/Nuls/Nombre').text
                exprimes_number = tour.find('.//Mentions/Exprimes/Nombre').text

                for candidat in tour.findall('.//Resultats/Candidats/Candidat'):

                    nom_psn = candidat.find('NomPsn').text if candidat.find('NomPsn') is not None else ''
                    prenom_psn = candidat.find('PrenomPsn').text if candidat.find('PrenomPsn') is not None else ''
                    civilite_psn = candidat.find('CivilitePsn').text if candidat.find('CivilitePsn') is not None else ''
                    cod_nua_cand = candidat.find('CodNuaCand').text if candidat.find('CodNuaCand') is not None else ''
                    nb_voix = candidat.find('NbVoix').text if candidat.find('NbVoix') is not None else ''
                    elu = candidat.find('Elu').text if candidat.find('Elu') is not None else ''
                    voix = candidat.find('NbVoix').text if candidat.find('NbVoix') is not None else ''
                    taux_exprimes = candidat.find('RapportExprimes').text if candidat.find('RapportExprimes') is not None else ''

                    # Append the row to the list
                    rows.append([
                        cod_cir_elec,
                        lib_cir_elec,
                        departement_libelle,
                        nom_psn,
                        prenom_psn,
                        civilite_psn,
                        cod_nua_cand,
                        nb_voix,
                        elu,
                        voix,
                        inscrits_number,
                        abstention_number,
                        votants_number,
                        blancs_number,
                        nuls_number,
                        exprimes_number,
                    ])

    # Define the CSV headers
    headers = [
        #'cand_id',
        'circo',
        'circo_lib',
        'dep_lib',
        'nom',
        'prenom',
        'civilite',
        'nuance',
        'voix',
        'statut',
        'voix',
        'inscrits',
        'abstention',
        'votants',
        'blancs',
        'nuls',
        'exprimes',
    ]

    # Write the rows to a CSV file
    with open(folder+"resultats_tour"+tour+"_par_circo.csv", 'w', newline='') as csvfile:
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
        url = "https://www.resultats-elections.interieur.gouv.fr/telechargements/LG2024/resultatsT2/"+dep+"/R2"+dep+"CIR.xml"

        response = requests.get(url)

        if response.status_code == 200:
            xml_file = folder + "resultats_circo_T1T2_xml//R2"+dep+"CIR.xml"
            with open(xml_file, "wb") as file: file.write(response.content)
        else:
            print(f"Failed to download data for ",dep,"Status code: {response.status_code}")


#download()
xml_to_csv("1")
xml_to_csv("2")
