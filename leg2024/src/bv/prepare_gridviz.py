import pandas as pd
from pygridmap import gridtiler
from datetime import datetime
import os

format_join = False
aggregate = False
tiling = True

folder = "/home/juju/geodata/elections_fr/leg2024/"



def get_bloc(nuance):
    if nuance in ["UG", "EXG", "DVG", "ECO", "COM", "FI", "SOC", "RDG", "VEC"]:
        return "NFP"
    if nuance in ["HOR", "UDI", "ENS", "DVC", "REN", "MDM"]:
        return "MP"
    if nuance in ["LR", "DVD"]:
        return "D"
    if nuance in ["EXD", "UXD", "REC", "RN", "DSV"]:
        return "ED"
    if nuance in ["DIV", "REG"]:
        return "DIV"
    
    #print(f"Could not find bloc for: {nuance}")
    return



if format_join:

    #load election results
    df = pd.read_csv(folder + "resultats-provisoires-par-bureau-de-votevmn.csv", sep=";", low_memory=False, dtype={'Code commune': str, 'Code BV': str})

#Code département	Libellé département	Code commune	Libellé commune	Code BV	Inscrits
# Votants	% Votants	Abstentions	% Abstentions	Exprimés	% Exprimés/inscrits	% Exprimés/votants
# Blancs	% Blancs/inscrits	% Blancs/votants	Nuls	% Nuls/inscrits	% Nuls/votants
# Numéro de panneau 1	Nuance candidat 1	Nom candidat 1	Prénom candidat 1	Sexe candidat 1	Voix 1	% Voix/inscrits 1	% Voix/exprimés 1	Elu 1
# Numéro de panneau 2	Nuance candidat 2	Nom candidat 2	Prénom candidat 2	Sexe candidat 2	Voix 2	% Voix/inscrits 2	% Voix/exprimés 2	Elu 2
# ...
# Numéro de panneau 19	Nuance candidat 19	Nom candidat 19	Prénom candidat 19	Sexe candidat 19	Voix 19	% Voix/inscrits 19	% Voix/exprimés 19	Elu 19


    #remove unecessary columns
    df = df.drop(columns=[col for col in df.columns if '%' in col])
    df = df.drop(columns=[col for col in df.columns if 'Numéro de panneau' in col])
    df = df.drop(columns=[col for col in df.columns if 'Libellé' in col])
    df = df.drop(columns=[col for col in df.columns if 'Sexe' in col])
    df = df.drop(columns=[col for col in df.columns if 'Elu' in col])
    df = df.drop(columns=[col for col in df.columns if 'Nom' in col])
    df = df.drop(columns=[col for col in df.columns if 'Prénom' in col])
    df = df.drop(columns=["Code département"])    #"Votants", "Abstentions", "Exprimés"

    #rename Voix X -> vX
    #for i in range(1,20): df.rename(columns={'Voix '+str(i): 'v'+str(i)}, inplace=True)
    for i in range(1,20): df.rename(columns={'Nuance candidat '+str(i): 'nuance'+str(i)}, inplace=True)

    #get blocs
    for i in range(1,20): df['bloc'+str(i)] = df['nuance'+str(i)].apply(get_bloc)
    df = df.drop(columns=[col for col in df.columns if 'nuance' in col])

    #aggregate votes per bloc
    for bloc in ["NFP","MP","D","ED","DIV"]:
        def aggBlocs(row):
            sum = 0
            for i in range(1,20):
                if row['bloc'+str(i)]==bloc: sum += row['Voix '+str(i)]
            return int(sum)

        df[bloc] = df.apply(aggBlocs, axis=1)

    #clean
    df = df.drop(columns=[col for col in df.columns if 'Voix' in col])
    df = df.drop(columns=[col for col in df.columns if 'bloc' in col])

    #make new field codeBureauVote
    df['codeBureauVote'] = df.apply(lambda row: str(row['Code commune']) + "_" + str(row['Code BV']), axis=1)
    df = df.drop(columns=["Code BV", "Code commune"])

    #print(df.iloc[0].to_string())

    #load bv data
    df2 = pd.read_csv("/home/juju/geodata/elections_fr/bv/bv.csv", dtype={'codeCirconscription': str})
    df2 = df2.drop(columns=["numeroBureauVote","id_bv"])
    #print(df2.iloc[0].to_string())

    #join
    df = pd.merge(df2, df, on='codeBureauVote', how='left')
    #print(df.iloc[0].to_string())

    #add column
    df['nb_bv'] = 1

    # Remove rows where 'Inscrits' is NaN, 0 or ""
    df = df[pd.notna(df['Inscrits'])]
    #df = df[df['Inscrits'] != None]
    #df = df[df['Inscrits'] != ""]
    #df = df[df['Inscrits'] != 0]

    #TODO fix that
    df = df.drop(columns=["codeBureauVote"])

    #save
    df.to_csv(folder + "1.csv", index=False)


#aggregation
if aggregate:

    #codeDepartement	nomDepartement	codeCirconscription	nomCirconscription	codeCommune	nomCommune	codeBureauVote
    aggregation_fun = {
        "codeDepartement": gridtiler.aggregation_single_value,
        "nomDepartement": gridtiler.aggregation_single_value,
        "codeCirconscription": gridtiler.aggregation_single_value,
        "nomCirconscription": gridtiler.aggregation_single_value,
        "codeCommune": gridtiler.aggregation_single_value,
        "nomCommune": gridtiler.aggregation_single_value,
        #TODO "codeBureauVote": gridtiler.aggregation_single_value,
        }

    print(datetime.now(), "aggregation to", 100, "m")
    gridtiler.grid_aggregation(input_file=folder + "1.csv", resolution=1, output_file=folder+"100.csv", a=100, aggregation_fun=aggregation_fun)

    for a in [2,5,10]:
        print(datetime.now(), "aggregation to", a*100, "m")
        gridtiler.grid_aggregation(input_file=folder+"100.csv", resolution=100, output_file=folder+str(a*100)+".csv", a=a, aggregation_fun=aggregation_fun)
    for a in [2,5,10]:
        print(datetime.now(), "aggregation to", a*1000, "m")
        gridtiler.grid_aggregation(input_file=folder+"1000.csv", resolution=1000, output_file=folder+str(a*1000)+".csv", a=a, aggregation_fun=aggregation_fun)
    for a in [2,5,10]:
        print(datetime.now(), "aggregation to", a*10000, "m")
        gridtiler.grid_aggregation(input_file=folder+"10000.csv", resolution=1000, output_file=folder+str(a*10000)+".csv", a=a, aggregation_fun=aggregation_fun)

    print(datetime.now(), "clean")
    for resolution in [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]:
        f = folder+str(resolution)+".csv"
        df = pd.read_csv(f)
        df.loc[df['nb_bv'] > 1, ['codeDepartement', 'nomDepartement', 'codeCirconscription', 'codeCommune', 'nomCirconscription', 'nomCommune', 'codeBureauVote']] = None
        df.to_csv(f, index=False)



#tiling
if tiling:
    for resolution in [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]:
        print("tiling for resolution", resolution)

        #create output folder
        out_folder = 'pub/gridviz/leg2024/T1_bv/' + str(resolution)
        if not os.path.exists(folder): os.makedirs(folder)

        gridtiler.grid_tiling(
            folder+str(resolution)+".csv",
            out_folder,
            resolution,
            tile_size_cell = 256,
            x_origin = 0,
            y_origin = 0,
            #crs = "EPSG:3035",
            format = "parquet"
        )
