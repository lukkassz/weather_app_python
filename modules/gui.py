import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils.api_handler import BuienradarAPI
from modules.current_weather import CurrentWeather
from modules.weather_forecast import WeatherForecast
from modules.weather_statistics import WeatherStatistics
from utils.validators import DateValidator
import logging

class WeatherApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        
    def create_widgets(self):
        # Create main container with tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Current weather tab
        self.current_frame = ttk.Frame(self.notebook)
        self.create_current_weather_frame(self.current_frame)
        self.notebook.add(self.current_frame, text="Current Weather")
        
        # Forecast tab
        self.forecast_frame = ttk.Frame(self.notebook)
        self.create_forecast_frame(self.forecast_frame)
        self.notebook.add(self.forecast_frame, text="Forecast")
        
        # Statistics tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.create_stats_frame(self.stats_frame)
        self.notebook.add(self.stats_frame, text="Statistics")
        
    def create_current_weather_frame(self, frame):
        # Modern styling for controls
        style = ttk.Style()
        style.configure("Modern.TButton", padding=10, font=('Helvetica', 10))
        style.configure("Modern.TLabel", font=('Helvetica', 10))
        
        # Controls container with better spacing
        controls_frame = ttk.Frame(frame, padding="20 10 20 10")
        controls_frame.pack(fill=tk.X)
        
        # Station selection with better layout
        station_frame = ttk.LabelFrame(controls_frame, text="Weather Station", padding="10")
        station_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Get stations list
        self.stations = BuienradarAPI.get_stations()
        station_names = [f"{station[0]} ({station[1]})" for station in self.stations]
        
        self.station_combo = ttk.Combobox(station_frame, 
                                        values=station_names, 
                                        width=40,
                                        font=('Helvetica', 10))
        self.station_combo.pack(side=tk.LEFT, padx=10, pady=5, expand=True)
        
        refresh_btn = ttk.Button(station_frame, 
                               text="Refresh Data", 
                               style="Modern.TButton",
                               command=self.get_current_weather)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Results area with better styling
        result_frame = ttk.LabelFrame(frame, text="Current Weather Data", padding="10")
        result_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.current_result = tk.Text(result_frame, 
                                    height=15, 
                                    width=50,
                                    state='disabled')
        self.current_result.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, 
                                command=self.current_result.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.current_result.configure(yscrollcommand=scrollbar.set)

    def create_forecast_frame(self, frame):
        """Creates forecast tab content"""
        # Controls container
        controls_frame = ttk.Frame(frame)
        controls_frame.pack(pady=10, padx=10, fill=tk.X)
        
        refresh_btn = ttk.Button(controls_frame, text="Get Forecast", 
                               command=self.get_forecast)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Results area
        result_frame = ttk.Frame(frame)
        result_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.forecast_result = tk.Text(result_frame, height=20, width=60, state='disabled')
        self.forecast_result.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, 
                                command=self.forecast_result.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.forecast_result.configure(yscrollcommand=scrollbar.set)

    def create_stats_frame(self, frame):
        """Creates statistics tab content"""
        # File selection
        file_frame = ttk.Frame(frame)
        file_frame.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(file_frame, text="KNMI Data File:").pack(side=tk.LEFT, padx=5)
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=5)

        # Date selection with validation
        date_frame = ttk.Frame(frame)
        date_frame.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(date_frame, text="Start Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.start_date = ttk.Entry(date_frame, width=12)
        self.start_date.pack(side=tk.LEFT, padx=5)
        self.start_date.bind('<KeyRelease>', self.validate_date_entry)
        
        ttk.Label(date_frame, text="End Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.end_date = ttk.Entry(date_frame, width=12)
        self.end_date.pack(side=tk.LEFT, padx=5)
        self.end_date.bind('<KeyRelease>', self.validate_date_entry)

        # Calculate button
        ttk.Button(frame, text="Calculate Statistics", 
                   command=self.calculate_statistics).pack(pady=10)

        # Results area
        self.stats_result = tk.Text(frame, height=15, width=50, state='disabled')
        self.stats_result.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def get_current_weather(self):
        if not self.station_combo.get():
            messagebox.showwarning("Warning", "Please select a station first!")
            return
        
        try:
            station_name = self.station_combo.get().split(" (")[0]
            
            # Enable text widget temporarily to update content
            self.current_result.configure(state='normal')
            self.current_result.delete(1.0, tk.END)
            self.current_result.insert(tk.END, "Fetching data...")
            self.current_result.configure(state='disabled')  # Disable again
            self.update()
            
            station_data = BuienradarAPI.get_station_data(station_name)
            
            if not station_data:
                self.current_result.configure(state='normal')
                self.current_result.delete(1.0, tk.END)
                self.current_result.insert(tk.END, "Failed to fetch data for selected station.")
                self.current_result.configure(state='disabled')
                return
            
            # Display data
            self.current_result.configure(state='normal')
            self.current_result.delete(1.0, tk.END)
            formatted_data = CurrentWeather.format_station_data(station_data)
            self.current_result.insert(tk.END, formatted_data)
            self.current_result.configure(state='disabled')
            
        except Exception as e:
            self.current_result.configure(state='normal')
            self.current_result.delete(1.0, tk.END)
            error_message = f"An error occurred while fetching data:\n{str(e)}"
            self.current_result.insert(tk.END, error_message)
            self.current_result.configure(state='disabled')
            logging.error(f"Error in get_current_weather: {e}")

    def get_forecast(self):
        """Fetches and displays weather forecast"""
        try:
            # Enable text widget for updating
            self.forecast_result.configure(state='normal')
            
            # Show loading message
            self.forecast_result.delete(1.0, tk.END)
            self.forecast_result.insert(tk.END, "Fetching forecast...")
            self.forecast_result.configure(state='disabled')
            self.update()
            
            # Get forecast data
            forecast_data = BuienradarAPI.get_forecast()
            
            # Enable text widget for updating
            self.forecast_result.configure(state='normal')
            
            if not forecast_data:
                self.forecast_result.delete(1.0, tk.END)
                self.forecast_result.insert(tk.END, "Failed to fetch forecast data.")
            else:
                # Display forecast
                self.forecast_result.delete(1.0, tk.END)
                formatted_data = WeatherForecast.format_forecast_data(forecast_data)
                self.forecast_result.insert(tk.END, formatted_data)
            
            # Disable text widget again
            self.forecast_result.configure(state='disabled')
            
        except Exception as e:
            # Enable text widget for error message
            self.forecast_result.configure(state='normal')
            self.forecast_result.delete(1.0, tk.END)
            error_message = f"An error occurred while fetching forecast:\n{str(e)}"
            self.forecast_result.insert(tk.END, error_message)
            self.forecast_result.configure(state='disabled')
            logging.error(f"Error in get_forecast: {e}")

    def browse_file(self):
        """Opens file dialog for selecting KNMI data file"""
        filetypes = [
            ('CSV files', '*.csv'),
            ('Text files', '*.txt'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title='Select KNMI Data File',
            filetypes=filetypes,
            initialdir='./data'  # Start in data directory
        )
        
        if filename:
            try:
                # Update entry field with selected file path
                self.file_path.set(filename)
                
                # Clear previous results
                self.stats_result.delete(1.0, tk.END)
                self.stats_result.insert(tk.END, f"Selected file: {filename}\n")
                self.stats_result.insert(tk.END, "Enter date range and click 'Calculate Statistics'")
                
            except Exception as e:
                self.stats_result.delete(1.0, tk.END)
                error_message = f"Error loading file:\n{str(e)}"
                self.stats_result.insert(tk.END, error_message)
                logging.error(f"Error in browse_file: {e}")

    def calculate_statistics(self):
        """Calculates weather statistics for selected file and date range"""
        # Validate file selection
        if not self.file_path.get():
            messagebox.showwarning("Warning", "Please select a data file first!")
            return
        
        # Get dates
        start_date = self.start_date.get().strip()
        end_date = self.end_date.get().strip()
        
        # Validate dates
        is_valid, error_message = DateValidator.validate_date_range(start_date, end_date)
        if not is_valid:
            messagebox.showwarning("Warning", error_message)
            return
        
        try:
            # Enable text widget for updating
            self.stats_result.configure(state='normal')
            
            # Show loading message
            self.stats_result.delete(1.0, tk.END)
            self.stats_result.insert(tk.END, "Calculating statistics...")
            self.update()
            
            # Create WeatherStatistics instance and process data
            stats_processor = WeatherStatistics()
            stats, output_file = stats_processor.process_period(
                self.file_path.get(),
                start_date,
                end_date
            )
            
            # Clear previous results
            self.stats_result.delete(1.0, tk.END)
            
            if stats is None:
                self.stats_result.insert(tk.END, f"Error: {output_file}")
            else:
                # Display results
                result_text = f"""
Statistics calculated successfully!

Period: {start_date} to {end_date}

Maximum Temperature: {stats['max_temp']:.1f}°C
Minimum Temperature: {stats['min_temp']:.1f}°C
Average Temperature: {stats['avg_temp']:.1f}°C
Total Precipitation: {stats['total_precipitation']:.1f}mm

Results saved to: {output_file}
"""
                self.stats_result.insert(tk.END, result_text)
            
            # Disable text widget again
            self.stats_result.configure(state='disabled')
            
        except Exception as e:
            self.stats_result.configure(state='normal')
            self.stats_result.delete(1.0, tk.END)
            error_message = f"An error occurred while calculating statistics:\n{str(e)}"
            self.stats_result.insert(tk.END, error_message)
            self.stats_result.configure(state='disabled')
            logging.error(f"Error in calculate_statistics: {e}")

    def validate_date_entry(self, event):
        """Validates date entry as user types"""
        widget = event.widget
        date_str = widget.get().strip()
        
        if date_str:  # Only validate if something is entered
            is_valid, error = DateValidator.validate_date_format(date_str)
            if not is_valid:
                widget.configure(foreground='red')
                self.stats_result.delete(1.0, tk.END)
                self.stats_result.insert(tk.END, f"Date format error: {error}")
            else:
                widget.configure(foreground='black')
                self.stats_result.delete(1.0, tk.END)

    def create_status_cards(self, frame):
        cards_frame = ttk.Frame(frame)
        cards_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Temperature card
        temp_card = ttk.LabelFrame(cards_frame, text="Temperature")
        temp_card.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.temp_label = ttk.Label(temp_card, 
                                   text="--°C", 
                                   font=('Helvetica', 20))
        self.temp_label.pack(pady=10)
        
        # Humidity card
        humid_card = ttk.LabelFrame(cards_frame, text="Humidity")
        humid_card.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.humid_label = ttk.Label(humid_card, 
                                    text="--%", 
                                    font=('Helvetica', 20))
        self.humid_label.pack(pady=10)
        
        # Wind card
        wind_card = ttk.LabelFrame(cards_frame, text="Wind Speed")
        wind_card.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.wind_label = ttk.Label(wind_card, 
                                   text="-- km/h", 
                                   font=('Helvetica', 20))
        self.wind_label.pack(pady=10)

    def show_loading(self, text="Loading..."):
        self.progress = ttk.Progressbar(self, 
                                      mode='indeterminate', 
                                      length=300)
        self.progress.pack(pady=10)
        self.progress.start(10)
        self.loading_label = ttk.Label(self, 
                                     text=text,
                                     font=('Helvetica', 10))
        self.loading_label.pack()
        self.update()

    def hide_loading(self):
        if hasattr(self, 'progress'):
            self.progress.stop()
            self.progress.destroy()
            self.loading_label.destroy()