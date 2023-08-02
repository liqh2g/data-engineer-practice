import aiohttp
import asyncio
import os
from zipfile import ZipFile

async def download_image(url, destination_folder):   
    li = url.rsplit("/",1)[1]
    file_name = li.split(".")[0]
    # destination_path = os.path.join(destination_folder, file_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_name + ".zip", 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                with ZipFile(file_name + ".zip","r") as zipObject:
                    listOfFileNames = zipObject.namelist()
                    for file in listOfFileNames:
                        if file.endswith('.csv'):
                            zipObject.extract(file_name + ".csv")
                if os.path.exists(file_name + ".zip"):
                    os.remove(file_name + ".zip")
            else:
                print(f"Failed to download {file_name}.")

async def main():
    destination_folder = 'downloads'
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    os.chdir(destination_folder)
    image_urls = [
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip"
    ]

    tasks = [download_image(url, destination_folder) for url in image_urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
