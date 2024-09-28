import tkinter as tk
from PIL import Image, ImageTk 
from datetime import timedelta, datetime,date
import numpy as np
import openpyxl
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error




csv_data= pd.read_excel(r'E:\python\hackathon\PLANT TON_EFFICIENCY\main.xlsx')
excel_data = pd.read_excel(r'E:\python\hackathon\TEMPERATURE\NEW.xlsx')


excel_data['DateTime'] = pd.to_datetime(excel_data['DateTime'])
csv_data['Time'] = pd.to_datetime(csv_data['Time'])


merged_data = pd.merge_asof(csv_data.sort_values('Time'), 
                            excel_data.sort_values('DateTime'), 
                            left_on='Time', 
                            right_on='DateTime', 
                            direction='nearest')


features = ['Temperature [°C]', 'RH [%]', 'WBT_C', 'kW_Tot', 'kW_RT', 'Precent_CH', 'RT']
target = 'CH Load'

X = merged_data[features]
y = merged_data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)



def today():
    main_window1 = tk.Tk()
    main_window1.geometry("800x600")  
    main_window1.title("The Current Days Chiller Load")
    main_window1.configure(bg="salmon")
    labels = [
    'Temperature [°C]:', 
    'Relative Humidity [%]:', 
    'Wet Bulb Temperature [°C]:', 
    'Total Power Consumption (kW_Tot):', 
    'Power Efficiency (kW per Refrigeration Ton):', 
    'Percentage of Chiller Load (Precent_CH):', 
    'Refrigeration Tons (RT):'
    ]
    wday=["monday","tuesday","wednesday","thursday","friday"]
    wend=["saturday","sunday"]
    def label1():
        def get_day_of_week(date_string):
            date_obj = datetime.strptime(date_string, '%Y-%m-%d')
            day_of_week = date_obj.strftime('%A')  
            return day_of_week
        temperature = float(entry1.get())
        rh = float(entry2.get())
        wbt_c = float(entry3.get())
        kw_tot = float(entry4.get())
        kw_rt = float(entry5.get())
        percent_ch = float(entry6.get())
        rt = float(entry7.get())
        
        
        def adjust_chiller_operations(predicted_load, chiller_capacity):
            
            if predicted_load > 0.8 * chiller_capacity:
                return "Turn on all chillers at full capacity"
            elif predicted_load > 0.5 * chiller_capacity:
                return "Turn on some chillers at moderate capacity"
            elif predicted_load > 0.3 * chiller_capacity:
                return "Run chillers at low capacity"
            else:
                return "Turn off unnecessary chillers or run at minimal power"
        input_date= date.today()
        input_date=str(input_date)
        day_of_week=get_day_of_week(input_date)
        input_data = pd.DataFrame({
        'Temperature [°C]': [temperature],
        'RH [%]': [rh],
        'WBT_C': [wbt_c],
        'kW_Tot': [kw_tot],
        'kW_RT': [kw_rt],
        'Precent_CH': [percent_ch],
        'RT': [rt]
        })

        predicted_load = model.predict(input_data)[0]

        if 10<=int(input_date[5:7])<=12:
            
            predicted_load=predicted_load+(25/100)*predicted_load
            if day_of_week.lower() in wday:
                predicted_load=predicted_load
            else:
                
                
                predicted_load=(((30+15)/2)/100)*predicted_load+predicted_load
        elif 2<=int(input_date[5:7])<=3:
            
            predicted_load=predicted_load+(20/100)*predicted_load
            if day_of_week.lower() in wday:
                predicted_load=predicted_load
            else:
                
                predicted_load=(((30+15)/2)/100)*predicted_load+predicted_load
        else:
            if day_of_week.lower() in wday:
                predicted_load=predicted_load
            else:
                
                predicted_load=(((30+15)/2)/100)*predicted_load+predicted_load
            
        chiller_capacity = 100
        adjustment = adjust_chiller_operations(predicted_load, chiller_capacity)
        
        tk.Label(main_window1, text=f"\nPredicted Chiller Load: {predicted_load:.2f}", font=("Arial", 12)).pack(pady=5)
        tk.Label(main_window1, text=f"Recommendation: {adjustment}", font=("Arial", 12)).pack(pady=5)
    
    tk.Label(main_window1, text=labels[0], font=("Arial", 12)).pack(pady=5)
    entry1 = tk.Entry(main_window1, font=("Arial", 12))
    entry1.pack(pady=5)

    tk.Label(main_window1, text=labels[1], font=("Arial", 12)).pack(pady=5)
    entry2 = tk.Entry(main_window1, font=("Arial", 12))
    entry2.pack(pady=5)

    tk.Label(main_window1, text=labels[2], font=("Arial", 12)).pack(pady=5)
    entry3 = tk.Entry(main_window1, font=("Arial", 12))
    entry3.pack(pady=5)

    tk.Label(main_window1, text=labels[3], font=("Arial", 12)).pack(pady=5)
    entry4 = tk.Entry(main_window1, font=("Arial", 12))
    entry4.pack(pady=5)

    tk.Label(main_window1, text=labels[4], font=("Arial", 12)).pack(pady=5)
    entry5 = tk.Entry(main_window1, font=("Arial", 12))
    entry5.pack(pady=5)

    tk.Label(main_window1, text=labels[5], font=("Arial", 12)).pack(pady=5)
    entry6 = tk.Entry(main_window1, font=("Arial", 12))
    entry6.pack(pady=5)

    tk.Label(main_window1, text=labels[6], font=("Arial", 12)).pack(pady=5)
    entry7 = tk.Entry(main_window1, font=("Arial", 12))
    entry7.pack(pady=5)

    button3= tk.Button(main_window1, text="Check Today's Chiller Load",command=label1,font=("Arial", 12))
    button3.pack(pady=5)
    main_window1.mainloop()
def dated():
    main_window1 = tk.Tk()
    main_window1.geometry("800x650")  
    main_window1.title("The Chillen Load for Given Date")
    main_window1.configure(bg="salmon")
    labels = [
    'Temperature [°C]:', 
    'Relative Humidity [%]:', 
    'Wet Bulb Temperature [°C]:', 
    'Total Power Consumption (kW_Tot):', 
    'Power Efficiency (kW per Refrigeration Ton):', 
    'Percentage of Chiller Load (Precent_CH):', 
    'Refrigeration Tons (RT):',
    'Enter a date (YYYY-MM-DD):'
    ]
    wday=["monday","tuesday","wednesday","thursday","friday"]
    wend=["saturday","sunday"]
    def label2():
        def get_day_of_week(date_string):
            date_obj = datetime.strptime(date_string, '%Y-%m-%d')
            day_of_week = date_obj.strftime('%A')  
            return day_of_week
        temperature = float(entry1.get())
        rh = float(entry2.get())
        wbt_c = float(entry3.get())
        kw_tot = float(entry4.get())
        kw_rt = float(entry5.get())
        percent_ch = float(entry6.get())
        rt = float(entry7.get())
        
        
        def adjust_chiller_operations(predicted_load, chiller_capacity):
            
            if predicted_load > 0.8 * chiller_capacity:
                return "Turn on all chillers at full capacity"
            elif predicted_load > 0.5 * chiller_capacity:
                return "Turn on some chillers at moderate capacity"
            elif predicted_load > 0.3 * chiller_capacity:
                return "Run chillers at low capacity"
            else:
                return "Turn off unnecessary chillers or run at minimal power"
        input_date= str(entry8.get())
        input_date=str(input_date)
        day_of_week=get_day_of_week(input_date)
        input_data = pd.DataFrame({
        'Temperature [°C]': [temperature],
        'RH [%]': [rh],
        'WBT_C': [wbt_c],
        'kW_Tot': [kw_tot],
        'kW_RT': [kw_rt],
        'Precent_CH': [percent_ch],
        'RT': [rt]
        })

        predicted_load = model.predict(input_data)[0]

        if 10<=int(input_date[5:7])<=12:
            
            predicted_load=predicted_load+(25/100)*predicted_load
            if day_of_week.lower() in wday:
                predicted_load=predicted_load
            else:
                
                
                predicted_load=(((30+15)/2)/100)*predicted_load+predicted_load
        elif 2<=int(input_date[5:7])<=3:
            
            predicted_load=predicted_load+(20/100)*predicted_load
            if day_of_week.lower() in wday:
                predicted_load=predicted_load
            else:
                
                predicted_load=(((30+15)/2)/100)*predicted_load+predicted_load
        else:
            if day_of_week.lower() in wday:
                predicted_load=predicted_load
            else:
                
                predicted_load=(((30+15)/2)/100)*predicted_load+predicted_load
            
        chiller_capacity = 100
        adjustment = adjust_chiller_operations(predicted_load, chiller_capacity)
        
        tk.Label(main_window1, text=f"\nPredicted Chiller Load: {predicted_load:.2f}", font=("Arial", 12)).pack(pady=5)
        tk.Label(main_window1, text=f"Recommendation: {adjustment}", font=("Arial", 12)).pack(pady=5)
    


    tk.Label(main_window1, text=labels[0], font=("Arial", 12)).pack(pady=5)
    entry1 = tk.Entry(main_window1, font=("Arial", 12))
    entry1.pack(pady=5)

    tk.Label(main_window1, text=labels[1], font=("Arial", 12)).pack(pady=5)
    entry2 = tk.Entry(main_window1, font=("Arial", 12))
    entry2.pack(pady=5)

    tk.Label(main_window1, text=labels[2], font=("Arial", 12)).pack(pady=5)
    entry3 = tk.Entry(main_window1, font=("Arial", 12))
    entry3.pack(pady=5)

    tk.Label(main_window1, text=labels[3], font=("Arial", 12)).pack(pady=5)
    entry4 = tk.Entry(main_window1, font=("Arial", 12))
    entry4.pack(pady=5)

    tk.Label(main_window1, text=labels[4], font=("Arial", 12)).pack(pady=5)
    entry5 = tk.Entry(main_window1, font=("Arial", 12))
    entry5.pack(pady=5)

    tk.Label(main_window1, text=labels[5], font=("Arial", 12)).pack(pady=5)
    entry6 = tk.Entry(main_window1, font=("Arial", 12))
    entry6.pack(pady=5)

    tk.Label(main_window1, text=labels[6], font=("Arial", 12)).pack(pady=5)
    entry7 = tk.Entry(main_window1, font=("Arial", 12))
    entry7.pack(pady=5)

    tk.Label(main_window1, text=labels[7], font=("Arial", 12)).pack(pady=5)
    entry8 = tk.Entry(main_window1, font=("Arial", 12))
    entry8.pack(pady=5)
    
    button3= tk.Button(main_window1, text="Check The Given date's Chiller Load",command=label2,font=("Arial", 12))
    button3.pack(pady=5)
    main_window1.mainloop()
def show_main_tab():
    
        
    splash.destroy()  
    main_window = tk.Tk()
    
    
   
    main_window.geometry("800x600")
    main_window.title("Wildflower Hall, An Oberoi Resort, Shimla")  
    
    
    bg_image = Image.open("wild1.jpg")  
    bg_image = bg_image.resize((800,600))
    bg_image = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(main_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  

    bg_label.image = bg_image

    label = tk.Label(main_window, text="Welcome to Wildflower Hall", font=("Arial", 24), bg="lightblue")
    label.place(relx=0.5, rely=0.1, anchor="center")
    button1 = tk.Button(main_window, text="Check Today's Chiller Load", command=today,font=("Arial", 14))
    button1.place(x=45,y=155)
    
    button2 = tk.Button(main_window, text="Check Specific Date's \nChiller Load", command=dated,font=("Arial", 14))
    button2.place(x=550,y=150)
    
    label1= tk.Label(main_window, text="An Oberoi Resort", font=("Arial", 30), bg="blue")
    label1.place(x=410,y=500, anchor="center")
    main_window.mainloop()


splash = tk.Tk()
splash.geometry("300x168")


splash_image = Image.open("1.jpg")  
splash_photo = ImageTk.PhotoImage(splash_image)


splash_label = tk.Label(splash, image=splash_photo)
splash_label.pack()


splash.after(5000, show_main_tab)  


splash.mainloop()
