from tkinter import *
import tkinter as tk
import requests

API_KEY = "e35d15655dfe40efb322e1b3e97dd857"

def click():
    CITY = entry1.get()

    try:
        url = f"https://api.weatherbit.io/v2.0/current?key={API_KEY}&city={CITY}"
        response = requests.get(url)
        data = response.json()
        print(response.status_code)

        if response.status_code == 200:
            city_name.config(text = f"Weather in {data['data'][0]['city_name']}:")
            desc.config(text = f"Weather: {data['data'][0]['weather']['description']}")
            temp.config(text = f"Temperature: {data['data'][0]['temp']} degrees Celsius")
            spd.config(text = f"Wind speed: {data['data'][0]['wind_spd']} m/s")
            pres.config(text = f"Pressure: {data['data'][0]['pres']} mb")
            hm.config(text = f"Humidity: {data['data'][0]['rh']}%")
        
        else:
            print(f"Error: {data['message']}")

    except Exception as e:
        print(response.status_code)
        print(f"Error happened: {e}")
        city_name.config(text = "Enter correct city name")
        desc.config(text = "")
        temp.config(text = "")
        spd.config(text = "")
        pres.config(text = "")
        hm.config(text = "")
#

api = tk.Tk()
api.title("Doing API stuff")
api.geometry("1000x700")
api.resizable(False, False)
api.configure(bg="#dce3e6")

label1 = tk.Label(api, 
                  text="Enter your city", 
                  fg = "#000000",
                  font = "Arial 16"
                  )
label1.pack(pady=(10, 0))

entry1 = tk.Entry(api,
                  fg = "#000000",
                  bg = "#ffffff",
                  font = "Arial 18"
                  )
entry1.pack(pady=(10, 0))

button1 = tk.Button(api,
                text = "See your weather",
                fg = "#000000",
                bg = "#ffffff",
                font = "Arial 16",
                command = click
                )
button1.pack(pady=(10, 0))

city_name = tk.Label(api, 
                  text="city", 
                  fg = "#000000",
                  font = "Arial 16"
                  )
city_name.pack(pady=(20, 0))

desc = tk.Label(api, 
                  text="weather", 
                  fg = "#000000",
                  font = "Arial 16"
                  )
desc.pack(pady=(10, 0))

temp = tk.Label(api, 
                  text="temperature", 
                  fg = "#000000",
                  font = "Arial 16"
                  )
temp.pack(pady=(10, 0))

spd = tk.Label(api, 
                  text="wind speed", 
                  fg = "#000000",
                  font = "Arial 16"
                  )
spd.pack(pady=(10, 0))

pres = tk.Label(api, 
                  text="pressure", 
                  fg = "#000000",
                  font = "Arial 16"
                  )
pres.pack(pady=(10, 0))

hm = tk.Label(api, 
                  text="humidity", 
                  fg = "#000000",
                  font = "Arial 16"
                  )
hm.pack(pady=(10, 0))

api.mainloop()