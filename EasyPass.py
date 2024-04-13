from multiprocessing import Value
from pickle import FLOAT
import tkinter as tk
from tkinter import Listbox, ttk
import math
import matplotlib.pyplot as plt
import numpy as np


global profile_values
global Widerstand 
global Kapazitat 
global Eingangs_Spannung

Kapazitat = 0
Widerstand = 0
Eingangs_Spannung = 0
profile_values_dict = {}  # Dictionary zum Speichern der Profilwerte

def save_new_profile():
    new_profile_name = entry_new_profile.get()
    profile_values = [entry.get() for entry in entry_list]
    # Überprüfen, ob mindestens 10 Werte eingegeben wurden
    if len(profile_values) < 10:
        print("Es müssen mindestens 10 Werte eingegeben werden.")
        return
    
    CB_F_Profil['values'] = (*CB_F_Profil['values'], new_profile_name)
    print("Neues Frequenzprofil erstellt:", new_profile_name)
    
    # Hier kannst du den neuen Profilnamen und die Werte in eine separate Datei speichern
    with open("frequenzprofile.txt", "a", encoding="utf-8") as file:
        file.write(new_profile_name + ":" + ",".join(profile_values) + "\n")
    
    # Aktualisiere die Frequenzliste nach dem Hinzufügen des neuen Profils
    update_frequency_list()
        
    new_profile_window.destroy()

def create_new_profile_gui(): #Öffnet das Fenster wo ein neues Frequenzprofil angelegt wird
    global new_profile_window #Schreibe eine globale Variable 
    new_profile_window = tk.Toplevel(EasyPass)
    new_profile_window.title("Neues Frequenzprofil erstellen")
    
    tk.Label(new_profile_window, text="Geben Sie den Namen des neuen Profils ein:").pack()
    
    global entry_new_profile
    entry_new_profile = tk.Entry(new_profile_window)
    entry_new_profile.pack()
    
    tk.Label(new_profile_window, text="Geben Sie mindestens 10 Werte ein:").pack()
    
    entry_frame = tk.Frame(new_profile_window)
    entry_frame.pack()
    
    global entry_list
    entry_list = []
    for i in range(15):  # Mindestens 15 Entry-Felder
        entry_label = tk.Label(entry_frame, text=f"Wert {i+1}:")
        entry_label.grid(row=i, column=0)
        entry = tk.Entry(entry_frame)
        entry.grid(row=i, column=1)
        entry_list.append(entry)
    
    tk.Button(new_profile_window, text="Profil speichern", command=save_new_profile).pack()

def wechselPass():
    global PassValue
    PassValue = LabelPass.cget("text")
    
    
    if PassValue == "Tiefpass aktiv":
        LabelPass.config(text="Hochpass aktiv")
    else: 
        LabelPass.config(text="Tiefpass aktiv")

def Finale_Eingabe():
    
    Widerstand = float(Entry_Widerstand.get())
    Kapazitat = float(Entry_Kapazitat.get())
    Eingangs_Spannung = float(Entry_Eingangsspannung.get())
    print(Widerstand, Kapazitat, Eingangs_Spannung)
    LabelWiderstandAnzeige = tk.Label(EasyPass, text = "Widerstand = " + str(Widerstand) + " " + str(REinheit))
    LabelWiderstandAnzeige.grid(row = 6, column = 0)
    LabelEingangssapnungAnzeige = tk.Label(EasyPass, text= " Eingangssapnnung = " + str(Eingangs_Spannung) + " " +str(VEinheit))
    LabelEingangssapnungAnzeige.grid(row = 6, column = 1)
    LabelKapazitatAnzeige = tk.Label(EasyPass, text = "Kapazitat = "+ str(Kapazitat)+ " "+ str(CEinheit))
    LabelKapazitatAnzeige.grid(row = 6, column = 2)
    LabelPlaceholder = tk.Label(EasyPass, text = " ")
    LabelPlaceholder.grid(row=7, column=0)
    LabelFrequenz = tk.Label(EasyPass, text = "Frequenzen als fa")
    LabelFrequenz.grid(row=8, column=0)
    LabelAusgangsspannungAnzeige = tk.Label(EasyPass, text = "Ue / \u221A(1 + (fa / fg)\u00B2)")
    LabelAusgangsspannungAnzeige.grid(row=8, column=1)
    LabelAmplitudenAnzeige = tk.Label(EasyPass, text = "G(j\u03C9) = 20\u00B7log\u2081\u2080(Ua/Ue)")
    LabelAmplitudenAnzeige.grid(row=8, column=2)
    LabelPhaseAnzeige = tk.Label(EasyPass, text = "\u03C6 = -arctan(fa/fg)")
    LabelPhaseAnzeige.grid(row=8, column=3)
    

    if CEinheit == 'pF':
        Kapazitat = float(Kapazitat) * 10**-12
    elif CEinheit == 'nF':
        Kapazitat = float(Kapazitat) * 10**-9
    elif CEinheit == '\u03bcF':
        Kapazitat = float(Kapazitat) * 10**-6
    elif CEinheit == 'mF':
        Kapazitat = float(Kapazitat) * 10**-3

    
    if REinheit == 'm\u03A9':
        Widerstand = float(Widerstand) * 10**-3
    elif REinheit == 'k\u03A9':
        Widerstand = float(Widerstand) * 10**3
    elif REinheit == 'M\u03A9':
        Widerstand = float(Widerstand) * 10**6
    elif REinheit == 'G\u03A9':
        Widerstand = float(Widerstand) * 10**9
    
    Grenzfrequenz = round(1/(float(Widerstand)*float(Kapazitat)*(2*math.pi)), 2)
    LabelGrenzfrequenz = tk.Label(EasyPass, text = "Grenzfrequenz als fg" + " " +str(Grenzfrequenz) + " Hz")
    LabelGrenzfrequenz.grid(row = 6, column = 3)
        # Liste für die berechneten Werte von Fa und Ua
# Liste für die berechneten Werte von Fa, Ua und Phi
    frequenzen = []
    ausgangsspannungen = []
    amplituden = []
    phasen = []

    ausgangsspannungen_listbox = Listbox(EasyPass)
    amplituden_listbox = Listbox(EasyPass)
    phasen_listbox = Listbox(EasyPass)  # Phasenliste außerhalb der Schleife erstellen

    # Berechnung der Ausgangsspannung, Amplitude und Phase für jede Frequenz im Frequenzprofil
    selected_profile = CB_F_Profil.get()
    if selected_profile in profile_values_dict:
        profile_values = profile_values_dict[selected_profile]
        for value in profile_values:
            fa = float(value)
            if PassValue == "Tiefpass aktiv":
            phase = -math.atan(fa / Grenzfrequenz)  # Berechnung der Phase
            Ua = Eingangs_Spannung / math.sqrt(1 + (fa / Grenzfrequenz) ** 2)
            if PassValue == "Hochpass aktiv":
            phase = (math.pi/2)*-math.atan(fa / Grenzfrequenz)  # Berechnung der Phase
            Ua = Eingangs_Spannung / math.sqrt(1 + (Grenzfrequenz/ fa) ** 2)
            
            amplitude = 20 * math.log10(Ua / Eingangs_Spannung)
            
            # Hinzufügen der Werte zu den entsprechenden Listen
            frequenzen.append(fa)
            ausgangsspannungen.append(Ua)
            amplituden.append(amplitude)
            phasen.append(phase)

    # Anzeigen der berechneten Werte in den Listenboxen
    for i, fa in enumerate(frequenzen):
        # Anzeigen der Frequenz in der Liste
        text_frequenz = "Fa: {:.2f} Hz".format(fa)
        ListeFrequenzen.insert(tk.END, text_frequenz)
    
        # Anzeigen der Ausgangsspannung in der Listenbox
        ausgangsspannungen_listbox.insert(tk.END, "{:.2f}".format(ausgangsspannungen[i]))
    
        # Anzeigen der Amplitude in der Listenbox
        amplituden_listbox.insert(tk.END, "{:.2f} dB".format(amplituden[i]))
    
        # Anzeigen der Phase in der Listenbox
        phasen_listbox.insert(tk.END, "{:.2f}".format(math.degrees(phasen[i])))  # Umwandlung von Bogenmaß in Grad

    # Platzieren der Listenboxen neben der Liste der Frequenzen
    ausgangsspannungen_listbox.config(height=17)
    amplituden_listbox.config(height=17 )
    phasen_listbox.config(height=17 )

    ausgangsspannungen_listbox.grid(row=9, column=1)
    amplituden_listbox.grid(row=9, column=2)
    phasen_listbox.grid(row=9, column=3)

    # Annahme: Sie haben bereits eine Liste von Frequenzen (frequenzen) und eine Liste von Amplituden (amplituden)
    # Sie haben auch die Grenzfrequenz (Grenzfrequenz), die Sie verwenden möchten

    # Erstellen Sie ein logarithmisches Array von Frequenzen für die x-Achse des Bode-Diagramms
    log_frequencies = np.logspace(np.log10(min(frequenzen)), np.log10(max(frequenzen)), num=1000)

    # Berechnen Sie die Amplituden für diese logarithmischen Frequenzen unter Verwendung von Interpolation
    interpolated_amplituden = np.interp(log_frequencies, frequenzen, amplituden)

    # Erstellen des Bode-Diagramms
    plt.figure(figsize=(10, 6))

    # Plotten Sie die Amplituden gegen die logarithmischen Frequenzen
    plt.semilogx(log_frequencies, interpolated_amplituden, label='Amplitude (dB)', color='blue', linewidth=2)

    # Stellen Sie die Grenzfrequenz als vertikale gestrichelte Linie dar
    plt.axvline(x=Grenzfrequenz, color='red', linestyle='--', linewidth=1, label='Grenzfrequenz')

    plt.title('Bode-Diagramm')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()  # Optimiert die Platzierung der Subplots
    plt.show()

    
    
def CEinheitenChange(event):
    global CEinheit
    CEinheit = CB_C_Einheit.get()
    print("Selected Value:", CEinheit)

def REinheitenChange(event):
    global REinheit
    REinheit = CB_R_Einheit.get()
    print("Selected Value:", REinheit)    

def VEinheitenChange(event):
    global VEinheit
    VEinheit = CB_V_Einheit.get()
    print("Selected Value:", VEinheit)  

def FProfilChange(event):
    global FEingage
    FEingabe = CB_F_Profil
    print("Selected Value:", FEingabe)

# Funktion zum Aktualisieren der Frequenzliste entsprechend dem ausgewählten Profil
def update_frequency_list():
    selected_profile = CB_F_Profil.get()
    ListeFrequenzen.delete(0, tk.END)  # Lösche alle vorhandenen Einträge
    if selected_profile in profile_values_dict:
        profile_values = profile_values_dict[selected_profile]
        for value in profile_values:
            # Füge jeden Wert mit einem Zeilenumbruch getrennt ein
            ListeFrequenzen.insert(tk.END, value + '\n')
            
# Laden der vorhandenen Profile aus der Datei
def load_existing_profiles_List():
    global profile_values_dict  # Globale Variable verwenden
    try:
        with open("frequenzprofile.txt", "r", encoding="utf-8") as file:
            profiles = file.readlines()
            for profile in profiles:
                profile_name, *profile_values = profile.strip().split(":")
                profile_values = profile.split(":")[1].strip().split(",")
             
                profile_values_dict[profile_name] = profile_values  # Füge die Werte zum Dictionary hinzu
            CB_F_Profil['values'] = list(profile_values_dict.keys())  # Füge die Profile zur Combobox hinzu
    except FileNotFoundError:
        print("Frequenzprofil-Datei nicht gefunden!")

# Listen für Einheiten
CEinheiten = ['pF', 'nF', '\u03bcF', 'mF', 'F']
REinheiten = ['m\u03A9', '\u03A9', 'k\u03A9', 'M\u03A9', 'G\u03A9']
VoltEinheiten = ['\u03bcV', 'mV', 'V', 'kV']


# Erstelle die Anwendungsoberfläche
EasyPass = tk.Tk()
EasyPass.title("EasyPass von Tom Matthey V0.1")
EasyPass.geometry("600x600")

# Label erstellung
LabelTitel = tk.Label(EasyPass, text="Easy Pass fuer Uebertragungstechnik")
LabelPass = tk.Label(EasyPass, text="Tiefpass aktiv")
LabelWiderstand = tk.Label(EasyPass, text="Widerstand = ")
LabelKapazitat = tk.Label(EasyPass, text="Kapazitaet = ")
LabelU_Eingang = tk.Label(EasyPass, text="Eingangsspannung = ")
Label_F_Profil = tk.Label(EasyPass, text="Frequenzprofil = ")

# Eingabefelder
Entry_Widerstand = tk.Entry(EasyPass, bd=1, width=5)
Entry_Kapazitat = tk.Entry(EasyPass, bd=1, width=5)
Entry_Eingangsspannung = tk.Entry(EasyPass, bd=1, width=5)

# Button bestimmung
Button_Pass = tk.Button(EasyPass, text="Aendere zu anderen Pass", command=wechselPass)
Button_Final = tk.Button(EasyPass, text="Finale Eingabe", command=Finale_Eingabe)
Button_New_F_Profil = tk.Button(EasyPass, text="Neues Profil erstellen", command=create_new_profile_gui)

# Combox Value bestimmung
CB_C_Einheit = ttk.Combobox(values=CEinheiten)
CB_R_Einheit = ttk.Combobox(values=REinheiten)
CB_V_Einheit = ttk.Combobox(values=VoltEinheiten)
CB_F_Profil = ttk.Combobox()


# Rufe Value von Comboboxen ab
CB_C_Einheit.bind("<<ComboboxSelected>>", CEinheitenChange)
CB_R_Einheit.bind("<<ComboboxSelected>>", REinheitenChange)
CB_V_Einheit.bind("<<ComboboxSelected>>", VEinheitenChange)
CB_F_Profil.bind("<<ComboboxSelected>>", FProfilChange)
CB_F_Profil.bind("<<ComboboxSelected>>", lambda event: update_frequency_list())


# Positionierung der Widgets
LabelTitel.grid(row=0, column=1, columnspan=2)
LabelPass.grid(row=1, column=0)
LabelWiderstand.grid(row=3, column=0)
LabelKapazitat.grid(row=2, column=0)
LabelU_Eingang.grid(row=4, column=0)
Label_F_Profil.grid(row=5, column=0)


Button_Pass.grid(row=1, column=1)
Button_Final.grid(row=99, column=2)
Button_New_F_Profil.grid(row=5, column=1)

Entry_Kapazitat.grid(row=2, column=1)
Entry_Widerstand.grid(row=3, column=1)
Entry_Eingangsspannung.grid(row=4, column=1)

CB_C_Einheit.grid(row=2, column=2)
CB_R_Einheit.grid(row=3, column=2)
CB_V_Einheit.grid(row=4, column=2)
CB_F_Profil.grid(row=5, column=2)

load_existing_profiles_List()  # Laden der vorhandenen Profile

# Erstelle die Listbox und füge die gespeicherten Profile hinzu
ListeFrequenzen = tk.Listbox(EasyPass)
ListeFrequenzen.config(height= 17)
ListeFrequenzen.grid(row=9, column=0)


# Aktualisiere die Frequenzliste, wenn ein neues Profil ausgewählt wird


EasyPass.mainloop()  # Mainloop für die GUI

