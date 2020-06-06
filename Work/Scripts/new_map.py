# -*- coding: utf-8 -*-
"""
Created on Tue May 19 20:00:03 2020

@author: User
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb

import folium
from folium.plugins import MarkerCluster

from Scripts import base_handling as hand_base
from Scripts import globalvars as glob


def choice_map(root: tk.Tk, pane: ttk.Panedwindow):
    global CHOSEN_VALUE_map

    if not glob.is_db_open():
        return "break"

    win = tk.Toplevel(root)
    win.title("Выбор")
    win.geometry("300x300+500+200")

    background = tk.Frame(win, bg="#F8F8FF")
    background.place(x=0, y=0, relwidth=1, relheight=1)

    choice = ("По высоте", "По смертности")

    make_map = tk.Label(background, text='Это окно для построения карт', bg="#F8F8FF")
    make_map.place(relx=0.1, rely=0.1)
    make_map.pack()
    CHOSEN_VALUE_map = tk.StringVar(value='Выберите тип карты')
    make_table_op = tk.OptionMenu(background, CHOSEN_VALUE_map, *choice)
    make_table_op.place(relx=0.25, rely=0.4)
    make_table_op.pack()

    button_statistics = tk.Button(background, text='Сохранить', bg="#AFEEEE")

    button_statistics.bind("<Button-1>", lambda *args: new_map(root, pane))
    button_statistics.place(relx=0.2, rely=0.5, relheight=0.1, relwidth=0.6)
    background.pack(side="top", fill="both", expand=True, padx=10, pady=5)


def new_map(root: tk.Tk, pane: ttk.Panedwindow):
    global CHOSEN_VALUE_map

    lat = hand_base.bd['Latitude']
    lon = hand_base.bd['Longitude']

    # win = tk.Toplevel(root)
    # win.title("График")
    # win.geometry("600x500+500+200")

    # background = tk.Frame(win, bg="#F8F8FF")
    # background.place(x=0, y=0, relwidth=1, relheight=1)

    if CHOSEN_VALUE_map.get() == 'Фильтры для линейного графика':
        mb.showerror("Ошибка!", "Сначала выберите вариант карты!")

    elif CHOSEN_VALUE_map.get() == 'По высоте':
        map_elevation(lat, lon)
        mb.showinfo("Инфо", "Карта высот сохранена")

    # elif CHOSEN_VALUE_map.get()== 'По смертности':
    # return map_deaths(lat, lon)


# для высоты
def map_elevation(lat, lon):
    elevation = hand_base.bd['Elevation']
    Name = hand_base.bd['Name']

    def color_change(elevation):
        if (elevation < 500):
            return ('green')
        elif (500 <= elevation < 1000):
            return ('yellow')
        elif (1000 <= elevation < 3000):
            return ('red')
        elif (elevation > 3000):
            return ('black')

    map = folium.Map(location=[-6.2146200, 106.8451300], zoom_start=6, titles="Mapbox bright")
    marker_cluster = MarkerCluster().add_to(map)

    for lat, lon, elevation, Name in zip(lat, lon, elevation, Name):
        folium.Marker(location=[lat, lon], radius=9,
                      popup='Name: ' + str(Name) + '\n' + 'Elevation: ' + str(elevation) + " m",
                      fill_color=color_change(elevation),
                      color="gray", fill_opacity=0.9).add_to(marker_cluster)

    # либо
    # for lat, lon, elevation in zip(lat, lon, elevation):
    # folium.Marker(location = [lat, lon], popup = str(elevation) +" m",
    # icon = folium.Icon(color = color_change(elevation))).add_to(map)
    map.save("../Data/map_elevation.html")


# для количества смертей

def map_deaths(lat, lon):
    def deaths_change(DEATHS):
        if (DEATHS < 1000):
            return 'green'
        elif (1000 <= DEATHS < 5000):
            return 'yellow'
        elif (DEATHS > 5000):
            return 'red'
        map = folium.Map(location=[-6.2146200, 106.8451300], zoom_start=6, titles="Mapbox bright")
        marker_cluster = MarkerCluster().add_to(map)

    def show_message():
        map.save("map_deaths.html")
        tk.messagebox.showinfo("Information", "The map was saved")
        root.destroy()

    DEATHS = hand_base.bd['DEATHS']
    Name = hand_base.bd['Name']
    lat = hand_base.bd['Latitude']
    lon = hand_base.bd['Longitude']
    DEATHS = DEATHS.fillna(0)
    choose_option(lat, lon, DEATHS, Name)


def choose_option(lat, lon, DEATHS, Name):
    root = tk.Tk()
    root.geometry('250x250+500+300')

    entry_1 = tk.Entry(root)
    entry_1.place(relx=.5, rely=.1, anchor="c")
    entry_2 = tk.Entry(root)
    entry_1.pack()
    entry_2.pack()
    entry_2.place(relx=.10, rely=.1, anchor="c")
    number_1 = entry_1.get()
    number_1 = number_1.astype(float)
    number_2 = entry_1.get()
    number_2 = number_1.astype(float)
    message_button = tk.Button(root, text="Ok", command=show_message())
    message_button.place(relx=.7, rely=.5, anchor="c")
    for lat, lon, DEATHS, Name in zip(lat, lon, DEATHS, Name):
        if (number_1 <= DEATHS <= number_2):
            folium.Marker(location=[lat, lon], radius=9,
                          popup='Name: ' + str(Name) + '\n' + 'Deaths: ' + str(DEATHS),
                          fill_color=deaths_change(DEATHS), color="gray",
                          fill_opacity=0.9).add_to(marker_cluster)
