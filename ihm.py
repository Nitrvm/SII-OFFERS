from tkinter import *
from tkinter import messagebox
import prog_principal
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

with open("D:/Users/martin.jautee/Documents/SII-OFFERS/filtres.json") as f:
    filtres = json.load(f)

# authentification
def authentification(login, mdp):
   
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get("https://monportail.siinergy.net/user/login?destination=/")

    

    champs_login = driver.find_element(By.ID,"edit-name")
    champs_login.send_keys(login)

    champs_mdp = driver.find_element(By.ID, "edit-pass")
    champs_mdp.send_keys(mdp)
    
    time.sleep(1)
    btn = driver.find_element(By.ID,"edit-submit")
    
    try:
        btn.click()
        print('success')
        time.sleep(2)
    except:
        print('fail')
    time.sleep(2)

    
    try:
        mattermost = driver.find_elements(By.CLASS_NAME,"field__item")[12]
        mattermost.click()
        time.sleep(2)
        print('yes')
    except:
        print('caca')

# Pop up confirmation
def confirmation_popup():
    # Créer une fenêtre pop-up
    confirmation_window = Tk()
    confirmation_window.withdraw()

    # Afficher une boîte de dialogue de confirmation
    confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir republier les annonces ?")

    # Afficher la réponse de l'utilisateur
    if confirmation:
        return True
    else:
        return False

# Fonction de connexion
def login():
    # Récupérer les valeurs des champs de saisie
    username = username_entry.get()
    password = password_entry.get()

    # Vérifier les informations de connexion
    if username == "admin" and password == "12345":
        messagebox.showinfo("Connexion réussie", "Vous êtes connecté !")
        # TODO: Ajouter le code à exécuter après la connexion réussie
    else:
        messagebox.showerror("Erreur de connexion", "Identifiant ou mot de passe incorrect !")

def republication(liste):

    """
    Cette fonction permet de recuperer les liens présent dans les dictionnaires contenant les annonces.
    Un compteur s'incrémente à chaque fois qu'un annonce est republiée. 

    Args:
        liste (list): liste qui contient des annonces
        
    Return:
        None 
    """
    
    if confirmation_popup() is True:
        compteur = 0
        for annonces in liste:
            lien = annonces["lien republication"]
            try:
                driver.get(lien)
                compteur += 1
                #driver.execute_script(f"window.open('{lien}', '_blank')")
            except:
                print("lien invalide")
        print(f"{compteur} annonce(s) republiée(s)")
    else:
        print("les annonces ne seront pas républiée(s))")

# IHM
Fenetre_principale = Tk()

# Personnalisation
Fenetre_principale.geometry("1080x720")
Fenetre_principale.title("Republication des annonces SII")

# label principal
label_principal = Label(Fenetre_principale, text="SII OFFERS Republication").pack()

# Section de connexion
login_frame = Frame(Fenetre_principale)
login_frame.pack(pady=20)

# Labels et champs de saisie pour le login et le mot de passe
Label(login_frame, text="Login:").grid(row=0, column=0, padx=10)
Label(login_frame, text="Mot de passe:").grid(row=1, column=0, padx=10)

username_entry = Entry(login_frame)
username_entry.grid(row=0, column=1, padx=10)

password_entry = Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10)

# Bouton de connexion
login_button = Button(login_frame, text="Connexion", command=lambda: authentification(username_entry.get(), password_entry.get()))
login_button.grid(row=2, column=0, columnspan=2, pady=10)


# Section de sélection des villes
Label_villes = Label(Fenetre_principale, text='Sélection des villes')
Label_villes.pack()

for ele in filtres["Lieu"]:
    villes = Checkbutton(Fenetre_principale, text=ele)
    villes.pack()

# Bouton de republication
btn_rep = Button(Fenetre_principale, text="Republication", command=lambda: republication(['test']))
btn_rep.pack()

# Lancement de la fenêtre principale
Fenetre_principale.mainloop()



