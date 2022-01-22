import requests
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import haversine as hs
import streamlit as st


st.title("Trouvez la plage la plus proche d'une adresse")

link_main = 'https://api-adresse.data.gouv.fr/search/?q='



df = pd.read_csv('plages.csv', encoding = 'unicode_escape', engine ='python')
df["coord"] = list(zip(df["lat"],df["lon"]))
df = df[['commune','nom_plage','coord','lat','lon']]

def API_adresse2(adresse_postale):
  
  adresse_vraiment_ok = adresse_postale.replace(", ","&postcode=")
  adresse_vraiment_ok = adresse_vraiment_ok.replace(" ", "+")
  for char in reversed(adresse_vraiment_ok):
    if char != '+':
       adresse_vraiment_ok = adresse_vraiment_ok[ :-1 : ]
    elif char == '+':
      adresse_vraiment_ok = adresse_vraiment_ok[ :-1 : ]
      break  

  link = link_main + adresse_vraiment_ok
  
  r = requests.get(link).json()
  
  point = r['features'][0]['geometry']['coordinates'][::-1]

  df['distance'] = ''

  for i in range(len(df)):
    df['distance'].values[i] = hs.haversine(point,df['coord'][i])

  df["distance"] = pd.to_numeric(df["distance"])
  minimum_dist = df['distance'].min()
  plage_plus_proche = df.loc[df['distance'].idxmin()]['nom_plage']
  plage_lon = df.loc[df['distance'].idxmin()]['lon']
  plage_lat = df.loc[df['distance'].idxmin()]['lat']

  tooltip = 'Plage la plus proche'

  m = folium.Map(location=[plage_lat,plage_lon],zoom_start=10, tiles="Stamen Terrain")

  folium.Marker(
    location=[plage_lat,plage_lon],
    popup= plage_plus_proche + ' : ' + str(round(minimum_dist,2)) + ' Km',
    tooltip=tooltip,
    icon=folium.Icon(color="orange", icon="umbrella beach", prefix='fa')).add_to(m)
  folium_static(m)


adresse_postale = st.text_input('entrez votre adresse avec ce format : "3 rue exemple, 33000 villexemple"')

if st.button('valider'):
     API_adresse2(adresse_postale)


# conda activate data_collection
# cd D:\ecole
# streamlit run plage.py