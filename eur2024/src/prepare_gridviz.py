import pandas as pd
from pygridmap import gridtiler
from datetime import datetime


format_join = False
aggregate = True

folder = "/home/juju/geodata/elections_fr/eur2024/"


if format_join:
    #load election results
    in_file = folder + "eur_resultats-definitifs-par-bureau-de-vote.csv"
    df = pd.read_csv(in_file, sep=";")

    #remove unecessary columns
    df = df.drop(columns=[col for col in df.columns if '%' in col])
    df = df.drop(columns=[col for col in df.columns if 'Sièges' in col])
    df = df.drop(columns=[col for col in df.columns if 'Numéro de panneau' in col])
    df = df.drop(columns=[col for col in df.columns if 'Libellé' in col])
    df = df.drop(columns=[col for col in df.columns if 'Nuance' in col])
    df = df.drop(columns=["Code localisation", "Code département"])


    #make new field
    #df['id_bv'] = df['Code commune'].str.cat(df['Code BV'], sep='_')
    df['id_bv'] = df.apply(lambda row: str(row['Code commune']) + "_" + str(row['Code BV']), axis=1)
    df = df.drop(columns=["Code BV", "Code commune"])

    #print(df.iloc[0].to_string())



    #load bv data
    df2 = pd.read_csv("/home/juju/geodata/elections_fr/bv/bv.csv")
    df2 = df2.drop(columns=["fid","numeroBureauVote","codeBureauVote"])
    #print(df2.iloc[0].to_string())


    #join
    join = pd.merge(df2, df, on='id_bv', how='left')
    #print(join.iloc[0].to_string())

    #save
    join.to_csv(folder + "1.csv", index=False)


if aggregate:

    aggregation_fun = {
        "codeDepartement": gridtiler.aggregation_single_value,
        "codeCirconscription": gridtiler.aggregation_single_value,
        "nomCirconscription": gridtiler.aggregation_single_value,
        "codeCommune": gridtiler.aggregation_single_value,
        "nomCommune": gridtiler.aggregation_single_value,
        "id_bv": gridtiler.aggregation_single_value,
        }

    print(datetime.now(), "aggregation to", 100, "m")
    gridtiler.grid_aggregation(input_file=folder + "1.csv", resolution=1, output_file=folder+"100.csv", a=100, aggregation_fun=aggregation_fun)

    print("simplify 100m")
    df = pd.read_csv(folder+"100.csv")
    df = df.drop(columns=["codeDepartement","codeCirconscription","nomCirconscription","codeCommune","nomCommune","id_bv"])
    df.to_csv(folder + "100_simplified.csv", index=False)


    for a in [2,5,10]:
        print(datetime.now(), "aggregation to", a*100, "m")
        gridtiler.grid_aggregation(input_file=folder+"100_simplified.csv", resolution=100, output_file=folder+str(a*100)+".csv", a=a)
    for a in [2,5,10]:
        print(datetime.now(), "aggregation to", a*1000, "m")
        gridtiler.grid_aggregation(input_file=folder+"1000.csv", resolution=1000, output_file=folder+str(a*1000)+".csv", a=a)
    for a in [2,5,10]:
        print(datetime.now(), "aggregation to", a*10000, "m")
        gridtiler.grid_aggregation(input_file=folder+"10000.csv", resolution=1000, output_file=folder+str(a*10000)+".csv", a=a)
