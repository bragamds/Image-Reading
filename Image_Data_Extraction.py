import cv2
import pytesseract
import os
import regex as re
import pandas as pd
import glob

df = pd.DataFrame(columns=['Date','Distance (KM)','Pace (KM/MIN)','Active_cal (KCAL)','Total_Cal (KCAL)',
                           'Heart Rate (BPM)','Time','Elevation'])

directory = r'/Users/dalebraganzamenezes/Desktop/Python Practice/Image OCR Reading Project/Running_Images'

for file in glob.glob(directory+'**/*.PNG'):
    try:
        image_location= f'{file}'
        img=cv2.imread(image_location)
        pytesseract.pytesseract.tesseract_cmd=r'/usr/local/bin/tesseract'
        text = pytesseract.image_to_string(img)
        
        # Key Running Parameters:
        distance = re.findall('[0-9]+.[0-9]*KM',text) #Plus sybmol from regular expressions - greedily matches expression to its left 1 or more times
        pace = re.findall('[0-9]\'[0-9]*"/KM',text)
        active_cal = re.findall('[0-9]*KCAL',text)[0:1]
        total_cal = re.findall('[0-9]*KCAL',text)[1:2]
        date = re.findall('[<,€] Workouts [A-Z,a-z]* [0-9]* [A-Z,a-z]*',text)
        heart_rate = re.findall('[0-9]*BPM',text)
        time = re.findall('[0-9]*:[0-9]*:[0-9]*',text)
        elevation = re.findall('[0-9][0-9]M',text)
        
        #Pandas DataFrame Population
        df=df.append({'Date':date,'Distance':distance,'Pace':pace,'Active_cal':active_cal,'Total_Cal':total_cal,
                     'Heart Rate':heart_rate, 'Time':time,'Elevation':elevation}, ignore_index = True)
        df=df[['Date','Distance','Pace','Active_cal','Total_Cal','Heart Rate','Time','Elevation']].astype(str)
        
        #Cleaning Data
        df=df.applymap(lambda x: x.replace("['",""))
        df=df.applymap(lambda x: x.replace("']",""))
        df=df.applymap(lambda x: x.replace("KCAL",""))
        df=df.applymap(lambda x: x.replace("\'",""))
        df=df.applymap(lambda x: x.replace('"/',""))
        df=df.applymap(lambda x: x.replace("\\","."))
        df=df.applymap(lambda x: x.replace('KM',""))
        df=df.applymap(lambda x: x.replace('€ Workouts',""))
        df=df.applymap(lambda x: x.replace('< Workouts',""))
        df=df.applymap(lambda x: x.replace('BPM',""))
        
        df.drop(columns=['Pace'],inplace=True)
        
    except:
        pass
    
