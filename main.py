import tkinter as tk
from ttkthemes import ThemedTk
from modules.gui import WeatherApp
import logging

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='weather_app.log'
)

def main():
    root = ThemedTk(theme="arc")
    root.title("Weather Application")
    root.geometry("900x600")
    
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()