from os import name
import re
import requests
from bs4 import BeautifulSoup as bs
import mysql.connector
from sklearn import tree, preprocessing


cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='final_project')
cursor=cnx.cursor()

#Requesting data from Web and Creating Database

for i in range(1,20):
    a=('https://www.autoscout24.com/lst/?sort=standard&desc=0&offer=U&ustate=N%2CU&size=20&page=')
    b=str(i)
    c=('&cy=D&atype=C&recommended_sorting_based_id=dec047cd-841f-47c5-9fa9-3b88fca74015&')
    site=a+b+c

    r=requests.get(site)
    soup=bs(r.text,'html.parser')

    cars=soup.find_all('div',{'class':'cl-list-element cl-list-element-gap'})
    
    for car in cars:
    
        name=car.find('h2',{'class':'cldt-summary-makemodel sc-font-bold sc-ellipsis'})
        if name==None:
            namee='NA'
        else:
            namee=name.text.strip()
            namee=''.join(re.findall(r'[^\']',namee))
    
        model=car.find('li',{'data-type':'first-registration'})
        if model == None:
            modell=0
        else:
            modell=model.text.strip()
            modell=int(''.join(re.findall(r'/(\d*)',modell)))
    
        kilo=car.find('li',{'data-type':'mileage'})
        if kilo==None:
            kiloo=0
        else:
            kiloo=kilo.text.strip()
            kiloo=int(''.join(re.findall(r'\d',kiloo)))
    
        price=car.find('span',{'class':'cldt-price sc-font-xl sc-font-bold'})
        if price==None:
            pricee=0
        else:
            pricee=price.text.strip()
            pricee=int(''.join(re.findall(r'\d',pricee)))
    
        cursor.execute('INSERT INTO germany_cars VALUES (\'%s\',\'%i\',\'%i\',\'%i\')' %(namee,modell,kiloo,pricee))
    
        cnx.commit()
    
###Machine Learning

query='SELECT * FROM germany_cars;'
cursor.execute(query)

x=[] #name of cars to make dictionary
z=[] #list of input with convert string to integers
y=[] #output, price
for item in cursor:
    x.append(item[0])
    z.append(list(item[0:3]))
    y.append(item[3])

cnx.close()

le = preprocessing.LabelEncoder()
le.fit(x) #Encode name of cars to array of digits

car_dict = {}  
for item in x:  
    car_dict[item] = int(le.transform([item]))

for item in z: #Substitution of str with int
    item[0]=int(le.transform([item[0]]))

clf = tree.DecisionTreeClassifier()
clf = clf.fit(z,y)

question = 1
while question:
    car_name = input('car name: ')
    car_model = int(input('model: '))
    car_mileage = int(input('car mileage: '))
    new_data = [[car_dict[car_name], car_model, car_mileage]]
    answer = clf.predict(new_data)
    print()
    print('Price is probably about:', answer[0])
    print()
    question = int(input('To continue press "1", Otherwise press "0": '))

print('Done!')