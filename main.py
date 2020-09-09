#Imported modules
from tkinter import messagebox, font
import tkinter as tk
import requests

#Class called GUI
class GUI:
    #initializes the instance of the class
    def __init__(self):

        #Constants and our root/main_window
        self.SCREEN_WIDTH = "600"
        self.SCREEN_HEIGHT = "500"
        self.root = tk.Tk()
        #Specifies the dimensions of the GUI
        self.root.geometry(self.SCREEN_WIDTH + 'x' + self.SCREEN_HEIGHT)

        #Background image that covers the GUI
        self.background_image = tk.PhotoImage(file="landscape.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
        #Our upper-frame, that contains an entry and a button
        self.frame = tk.Frame(self.root, bg="#80c1ff", bd=3)
        self.frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")
        
        #entry field
        self.entry = tk.Entry(self.frame, font=40)
        self.entry.place(relwidth=0.65, relheight=1)
        
        #button -> Has a lambda function that passes the entry data on click
        self.button = tk.Button(self.frame, text="Check Weather", font=40, command=lambda: self.get_weather(self.entry.get()))
        self.button.place(relx = 0.65, relwidth=0.35, relheight=1)
    
        #Lower_frame that contains a label
        self.lower_frame = tk.Frame(self.root, bg="#80c1ff", bd=3)
        self.lower_frame.place(relx = 0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor="n")
    
        #The label we output information into
        self.label = tk.Label(self.lower_frame, font=("Verdana", 15))
        self.label.place(relwidth=1, relheight=1)

        #Loop that keeps the GUI going
        self.root.mainloop()

    #Function that takes a city as parameter, and converts it to 
    #latitude and longitude, then returns the data
    def converter(self, city): 
        url = "https://us1.locationiq.com/v1/search.php"
        data = {
            'key': "27dde2a09574d6",
            'q': f"{city}",
            'format': "json"
        }

        response = requests.get(url, params=data)
        lat, lon = response.json()[0]["lat"], response.json()[0]["lon"]
        return lat, lon

    #Function that formats the data from the weather api and
    #returns it
    def format_response(self, weather):
        temp = weather["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        wind = weather["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]
        summary = weather["properties"]["timeseries"][0]["data"]["next_1_hours"]["summary"]["symbol_code"]
        
        return "Wind speed: %s m/s\n Forecast: %s\nTemperature: %s degrees Celsius" % (wind, summary, temp)

    #Function that graps weather data, calls the converter function
    #to get the latitude and longitude and puts everything inside the label
    def get_weather(self, city): 
        try:
            if city.isalpha():
                lat, lon = self.converter(f"{city}")
                url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
                headers = requests.utils.default_headers()
                headers.update(
                    {
                        'User-Agent': 'My User Agent 1.0',
                    }
                )
                response = requests.get(url, headers=headers)
                weather = response.json()
                self.label["text"] = self.format_response(weather)
            else: 
                messagebox.showinfo("ERROR", "It has to be alphabetical!")
        #Incase we do not find a city
        except KeyError:
            messagebox.showinfo("ERROR", "You did not specify a known city!")
#Only creates an instance of the GUI for this file. 
if __name__ == "__main__": 
    weather_GUI = GUI()