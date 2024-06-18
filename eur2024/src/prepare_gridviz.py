import pandas as pd
from pygridmap import gridtiler
from datetime import datetime


format_join = True
aggregate = False

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
    format_join = pd.merge(df2, df, on='id_bv', how='left')


    #print(join.iloc[0].to_string())

    df.to_csv(folder + "1.csv", index=False)  # Set index=False to exclude row numbers from the output


if aggregate:
    print(datetime.now(), "aggregation to", 100, "m")
    gridtiler.grid_aggregation(input_file=folder + "1.csv", resolution=1, output_file=folder+"100.csv", a=100)

