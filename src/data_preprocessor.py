import pandas as pd
from ast import literal_eval
from pathlib import Path

def clean_features(data):
  lst = ['id', 'location', 'name', 'name_suffix', 'categories', 'tag_keys']
  return data[lst]

def clean_location(data):
    df3 = data.copy()
    lat = []
    lng = []
    for index, row in df3.iterrows():
      d = literal_eval(row['location'])
      lat.append(d['lat'])
      lng.append(d['lng'])

    #print(len(lat),len(lng))
    df3['lat'] = lat
    df3['lng'] = lng
    df3.drop('location',axis = 1, inplace=True)
    return df3

def find_Tunis_pois(df):
  regions = ['Ben Arous', 'Aryanah', 'Carthage', 'Twns', 'Tunis', 'Manouba', 
           'Medina of Tunis', 'La Goulette', 'Hy alkhdra Az Zuhoor']
  res = []
  geo = df.copy()
  for index,row in geo.iterrows():
    current = row['name_suffix'].split(',')
    yes = False
    for r in regions:
      if r in current:
        yes = True
        break
    
    if yes:
      name = row['name']
      suffix = row['name_suffix']
      lat = row['lat']
      lng = row['lng']
      index = row['id']
      tags = row['categories'] +', '+row['tag_keys']
      res.append({'id':index,'name':name,'suffix':suffix,'lat':lat,'lng':lng,'tags':tags})
  vis = pd.DataFrame(res)
  return vis

def thnity_preprocessing(data):
  df = clean_features(data)
  df = clean_location(df)
  df = find_Tunis_pois(df)
  df.drop_duplicates(subset="id",inplace=True)
  df.set_index('id',inplace=True)
  return df


def main(verbose=False,save_copy=False):
    try:
        path = str(input('Give path to the intial geolocation dataset!'))
        data = pd.read_csv(path)
        df = thnity_preprocessing(data)
        if verbose:
          print(df.head(5))
        if save_copy:
          path = Path('preprocessed_data.csv')
          df.to_csv(path)
        return df
    except Exception as e:
        print('An Error has occured: ',e)
        return

if __name__ == "__main__":
    main(verbose = True,save_copy=True)




