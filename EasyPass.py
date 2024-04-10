import tkinter as tk
from tkinter import ttk

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

def create_new_profile_gui():
    global new_profile_window
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
    PassValue = LabelPass.cget("text")
    
    if PassValue == "Tiefpass aktiv":
        LabelPass.config(text="Hochpass aktiv")
    else: 
        LabelPass.config(text="Tiefpass aktiv")

def Finale_Eingabe():
    global Widerstand, Kapazitat, Eingangs_Spannung
    Widerstand = Entry_Widerstand.get()
    Kapazitat = Entry_Kapazitat.get()
    Eingangs_Spannung = Entry_Eingangsspannung.get()

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
                profile_values_dict[profile_name] = profile_values  # Füge die Werte zum Dictionary hinzu
            CB_F_Profil['values'] = list(profile_values_dict.keys())  # Füge die Profile zur Combobox hinzu
    except FileNotFoundError:
        print("Frequenzprofil-Datei nicht gefunden!")
# Listen für Einheiten
CEinheiten = ['pF', 'nF', '\u03bcF', 'mF', 'F']
REinheiten = ['m\u03A9', '\u03A9', 'k\u03A9', 'M\u03A9', 'G\u03A9']
VoltEinheiten = ['pV', 'nV', '\u03bcV', 'mV', 'V', 'kV']


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

# Positionierung der Widgets
LabelTitel.grid(row=0, column=1, columnspan=2)
LabelPass.grid(row=1, column=0)
LabelWiderstand.grid(row=2, column=0)
LabelKapazitat.grid(row=3, column=0)
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
ListeFrequenzen.grid(row=6, column=2 , columnspan=5)


# Aktualisiere die Frequenzliste, wenn ein neues Profil ausgewählt wird
CB_F_Profil.bind("<<ComboboxSelected>>", lambda event: update_frequency_list())

EasyPass.mainloop()  # Mainloop für die GUI

