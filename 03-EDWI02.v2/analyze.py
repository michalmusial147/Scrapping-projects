import pandas as pd
import csv

def exportDataFrameForView(dataframe, filename):
    file = open(filename, 'w')
    writer = csv.writer(file)
    xMin, xMax, yMin, yMax = find_cords(dataframe)
    writer.writerow(["City"])
    writer.writerow([len(dataframe)])
    writer.writerow(["xMin", "xMax", "yMin", "yMax"])
    writer.writerow([xMin, xMax, yMin, yMax])
    #header row bellow should be writen by to_csv but it does not work so i did it manually
    writer.writerow(["post_code", "coordinates"])
    code_and_cords = dataframe[["post_code", "coordinates"]]
    code_and_cords.to_csv(filename, encoding='utf-8', index=False)
    file.close()
    return dataframe

def change(x, i):
    if isinstance(x, str):
        return x.split("/")[i]

def find_cords(dataframe):
    cords_row = dataframe["coordinates"]
    cords = cords_row.tolist()
    latitude_list = [change(el, 0) for el in cords]
    longitude_list = [change(el, 1) for el in cords]
    latitude_list = [i for i in latitude_list if i is not None]
    longitude_list = [i for i in longitude_list if i is not None]
    xMax = max(longitude_list)
    xMin = min(longitude_list)
    yMax = max(latitude_list)
    yMin = min(latitude_list)
    print("\nFound min/max cords: ", [xMin, xMax, yMin, yMax])
    return xMin, xMax, yMin, yMax


df = pd.read_csv(r'data.csv')
print("\nDownloaded:", len(df.index), " rows.")
df = df.drop_duplicates()
print("\nCount of codes in Poland: ", len(df.index))

grouped = df.groupby(['city', 'admin1', 'admin2', 'admin3'])['post_code'].count().nlargest(2)
print('\nFound answer, 2 largest cities by postcodes: \n', grouped)


exportDataFrameForView(df, "Polska.csv")
exportDataFrameForView(df.where(df['city'] == 'Warszawa').where(df['admin3'] == 'Warsaw'), "Warszawa.csv")
exportDataFrameForView(df.where(df['city'] == 'Łódź').where(df['admin3'] == 'Łódź'), "Łódź.csv")
