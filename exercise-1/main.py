import os
import requests
from zipfile import ZipFile

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip"
]

def get_file_name(url):
    li = url.rsplit("/",1)[1]
    file_name = li.split(".")[0]
    return file_name

def main():
    directory = "downloads"

    if not os.path.exists(directory):
        os.mkdir(directory)
    os.chdir(directory)
    
    for uri in download_uris:
            res = requests.get(uri)
            file_name = get_file_name(uri)

            open(file_name + '.zip','wb').write(res.content)

            with ZipFile(file_name+'.zip', 'r') as zipObject:
                listOfFileNames = zipObject.namelist()
                for fileName in listOfFileNames:
                     if fileName.endswith('.csv'):
                          zipObject.extract(file_name + '.csv')
            if os.path.exists(file_name+'.zip'):
                 os.remove(file_name+'.zip')

if __name__ == '__main__':
     main()