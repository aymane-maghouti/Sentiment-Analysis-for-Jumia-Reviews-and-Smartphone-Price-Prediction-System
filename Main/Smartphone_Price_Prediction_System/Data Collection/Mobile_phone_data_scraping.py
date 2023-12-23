import warnings
import requests
from bs4 import BeautifulSoup
import re

warnings.filterwarnings("ignore")

def get_links_from_page(page_no):
    data  = requests.get(f'https://www.jumia.co.ke/catalog/?q=mobile+phones&page={page_no}').text
    soup  = BeautifulSoup(data)
    links = []
    for a in soup.findAll('a', attrs={'class':'core'}):
        if 'href' in a.attrs:
            links.append('https://www.jumia.co.ke'+a['href'])
    return list(set(links))

def brands():
  lst= [
    "Apple",
    "Samsung",
    "Huawei",
    "Xiaomi",
    "Oppo",
    "Vivo",
    "Realme",
    "Nokia",
    "Gionee",
    "Infinix",
    "Tecno",
    "Realme",
    "Nokia",
    "Maxfone",
    "Freeyond",
    'Sowhat',
    ]
  lst_lower = [brand.lower() for brand in lst]
  return lst_lower

def get_reviews(url):
  data    = requests.get(url).text
  soup    = BeautifulSoup(data)
  rates=soup.findAll('div', attrs={'class':'stars _m _al -mvs'})
  text=soup.findAll('h3', attrs={'class':"-m -fs16 -pvs"})
  for i in range (len(rates)):
    rates[i]=rates[i].text
    text[i]=text[i].text
  reviews=[]
  for i in range(len(rates)):
    reviews.append("[ ("+rates[i]+") "+text[i]+" ]")
  return ', '.join(reviews)


def extract_mp_values(data_list):
    data_string = ' '.join(data_list)
    import re
    mp_values = re.findall(r'(\d.\d+\s?MP|\d+\s?MP)', data_string)

    mp_values= [i.replace(' ','') for i in mp_values]
    return mp_values


def get_phone_details(url):
  try:

    data    = requests.get(url).text
    soup    = BeautifulSoup(data)
    phone_name=soup.find('h1').text
    pattern = re.compile(r'[^a-zA-Z0-9.]+')

    features = re.split(pattern, phone_name)
    name=features[0]
    sec_name=features[1]

    if name.lower() in brands():
      brand=features[0]
    elif sec_name.lower() in brands():
      brand=features[1]
      features=features[1:]
    else:
      return None

    #brand name
    brand=features[0]

    #model name
    product_model=''
    for i in features[1:]:
      if '.'  in i or (i[-1].lower()=='b') :
        break
      product_model= product_model+i+' '

    #screen size
    screen_size=''
    for i in features[1:]:
      if '.'  in i:
        screen_size= screen_size+i
        break

    #ram and rom
    storages=[]
    for i in features[1:]:
      try:
          if i and (i[-1].lower() == 'b' ):
              storages.append(i)
      except IndexError:
          pass
    ram=''
    rom=''
    storages.sort()
    for i in range(len(storages)):
      storages[i]=int(storages[i][:-2])
    storages.sort()
    if len(storages)==2:
      ram= ram + str(storages[0])
      rom= rom + str(storages[1])

    if len(storages)==3:
      ram= ram + str(storages[0]+storages[1])
      rom= rom + str(storages[2])



    #SIM
    features_copy=features.copy()
    for f in range (len(features_copy)):
      features_copy[f]=features_copy[f].upper()

    sim_index = features_copy.index("SIM")
    sim_type=features_copy[sim_index-1].title()

    #battary
    pattern = re.compile(r'[mah$]')
    battary=0

    # Use the pattern to split the string
    for f in features:
      if f[-3:].lower()=='mah':
        battary=f[:-3]
        break

    #cams
    #first we extract 'FEATURES'
    try:
      tech=soup.find('div', attrs={'class':'markup -pam'}).findAll('li')
      final_tech=[]
      for i in range(len(tech)):
        tech[i]=tech[i].text.split(',')
        final_tech.append([])
      for i in range(len(tech)):
        for j in range (len(tech[i])):
          tech[i][j]=tech[i][j].split()
        for j in range(len(tech[i])):
          final_tech[i] = final_tech[i] + tech[i][j]
      cams=[]
      for i in final_tech:
        cams = cams + extract_mp_values(i)
      cams=' + '.join(cams)
    except:
      cams=""

    try:
      try:
        price=soup.find('div', attrs={'class':'df -i-ctr -fw-w'}).text.split('KSh ')[1]

        p_price=price
        sale_percentage = 0

        try:
          sale_percentage=soup.find('span', attrs={'class':'bdg _dsct _dyn -mls'}).text
          p_price=soup.find('div', attrs={'class':'df -i-ctr -fw-w'}).text.replace('KSh ','').replace(sale_percentage,'').replace(price,"")

        except:
          p_price=price
          sale_percentage = 0

      except:

        try:
          price=soup.find('div', attrs={'class':'df -i-ctr -fw-w -pas -brbl-fsale -rad4-bot'}).text.split('KSh ')[1]

          p_price=price
          sale_percentage = 0

          try:
            sale_percentage=soup.find('span', attrs={'class':'bdg _dsct _dyn -mls'}).text
            p_price=soup.find('div', attrs={'class':'-dif -i-ctr'}).text.replace('KSh ','').replace(sale_percentage,'').replace(price,"")

          except:
            p_price=price
            sale_percentage = 0

        except:
            p_price=price
            sale_percentage = 0
    except:
      pass

    try:
      r_link='https://www.jumia.co.ke/'+(soup.find('section', attrs={'class':'card aim -mtm'}).find('a')['href'])
      reviews=get_reviews(r_link)
    except:
      reviews='No reviews'
    if reviews=='':
      reviews='No reviews'

    seller_name = soup.find('div').find('div', attrs={'class':'-hr -pas'}).find('p').text
    scores=soup.find('div').find('div', attrs={'class':'-df -d-co -j-bet -prs'}).findAll('p')
    for score in range(len(scores)):
      scores[score]= "% ".join(scores[score].text.split('%'))
      scores[score]=scores[score].split()[0]
    seller_followers,seller_score=0,0

    try:
      seller_score=scores[0]
    except:
      seller_score= 0

    try:
      seller_followers=scores[1]
    except:
      seller_followers = 0

    try:
      rating=soup.find('div', attrs={'class','-fsh0 -bg-gy05 -df -d-co -i-ctr -rad4 -pam'}).find('div', attrs={'class':'stars _m -mvs'}).text.split(' out')[0]
      rating=str(rating)
    except:
      rating = 0


    return {'brand':brand,
            'model_name':product_model,
            'screen_size':screen_size,
            'ram':ram,
            'rom':rom,
            'cams':cams,
            'sim_type':sim_type,
            'battary':battary,
            'current_price':price,
            'previous_price':p_price,
            'sale_percentage':sale_percentage,
            'product_rating':rating,
            'seller_name':seller_name,
            'seller_score':seller_score,
            'seller_followers':seller_followers,
            'Reviews':reviews,

            }
  except:
    pass




import pandas as pd
df = pd.DataFrame()
for i in range(1,50):
    for link in get_links_from_page(i):
        new_df = pd.DataFrame(get_phone_details(link),index=[0])
        df= pd.concat([df,new_df],ignore_index=True)

df.to_csv('jumia_mobile_phone.csv')