from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.wait import WebDriverWait
from typing import Dict
import os
from datetime import datetime
import datetime
from pprint import pprint
import webbrowser
import sys
import  json
import requests

#Connexion à la page 

def connexion_page(url):
    """
    Ouvre une page web à l'aide de Selenium WebDriver.

    Args:
        url (str): URL de la page à ouvrir.

    Returns:
        None
    """
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)

#Récuperation des annonces

def liste_cle():
    """
    Récupère une liste des clés qui represente les en têtes du tableau de la page web.

    Returns:
        liste_cles (list)): Une liste des clés du tableau.
    """
    thead = driver.find_element(By.XPATH,"//thead")
    ths = thead.find_elements(By.XPATH,"//th")
    liste_cles = []
    for th in ths:
        valeur = th.text
        if valeur != "":
            liste_cles.append(valeur)
    return liste_cles

    
def extraire_donnees_ligne(ligne, liste_cles):
    """
    Cette fonction prend en entrée une instance WebElement (ligne) de Selenium et une liste de clés (liste-cles). 
    Elle extrait les données correspondant à chaque clé à partir de la ligne et les stocke dans un dictionnaire.
    
    Args:
        ligne (WebElement): une instance WebElement de la bibliothèque Selenium représentant la ligne à extraire.
        liste_cles (list): une liste de chaînes de caractères contenant les clés des données à extraire.
    
    Returns:
        id: l'identifiant de l'annonce dictionnaire contenant toutes les données associées à une annonce.
        dico_ligne: dictionnaire contenant toutes les données associées à une annonce.

    """
    
    try:
        dico_ligne = {}
        liste = liste_cles
        colonnes = ligne.find_elements(By.XPATH,"td")
        colonnes_text = [colonne.text for colonne in colonnes] # Créer une liste avec tout les objets selenium passés au format texte
        for key in range(1,len(liste)):
            dico_ligne[liste[key-1]] = colonnes_text[key]
        id = colonnes[-1].find_element(By.XPATH,('.//li/a')).get_attribute('href').split('/')[6] # Extraction du l'ID à partir d'un lien
        liste_liens = [colonne.get_attribute('href').split(":")[2] for colonne in colonnes[-1].find_elements(By.XPATH,('.//li/a'))] # Créer une liste de liens
        dico_ligne["lien republication"] = liste_liens[2]
        dico_ligne["lien suppression"] = liste_liens[4] 
    except:
        print(f"caca : {sys.exc_info}")
    return id, dico_ligne

    
 
def parcourir_tableau(dictionnaire):

    """
    Cette fonction permet de parcourir chaque tableau de la page web représenté par les balises <tr></tr>. 
    Cette fonction prend un paramètre un dictionnaire qui stock chaque annonce etraite par la fonction extraire_données_ligne().
    
    Args:
        dictionnaire (dict): dictionnaire qui stock les données chaque tableau sous forme de dictionnaire. Les clés du dicitonnaires sont définit par leur ID.
        
    
    Returns:
        dictionnaire : Dictionnaire qui contient toutes les annonces d'un page web.

    """

    lignes = driver.find_elements(By.XPATH,"//tbody/tr")
    liste_cles = liste_cle()
    for ligne in lignes:
        id, dico_ligne = extraire_donnees_ligne(ligne,liste_cles)
        dictionnaire[id] = dico_ligne
    return dictionnaire    

def recuperer_donnees_pages():
    """
    Cette fonction permet de parcourir toutes les pages web et d'extraire les données de chaque tableau dans un dictionnaire.
    La fonction "verifier_element_present(element)" permet de vérifiér que le lien vers la page suivante est toujoures présent.
    Tant que cette condition est respectée le dictionnaire continue de parcourir les tableau grâce à la fonction "parcourir_tableau(dictionnaire)"
    La génère un fichier JSON contenant toutes les annonces à partir du dictionnaire des annonces complet et également un autre fichier JSON 
    contenant les filtres associé à la valeur des des clés du dictionnaire de filtre.

    Args:
        Aucun.

    Returns:
        dictionnaire (dict): Un dictionnaire contenant toutes les annonces.
    """

    
    dictionnaire = {}
    page_suivante = True
    while page_suivante is True:
        dictionnaire = parcourir_tableau(dictionnaire)
        page_suivante = verifier_element_present("//li[@class='pager__item pager__item--next']/a")
        if page_suivante is True:
            driver.find_element(By.XPATH,"//li[@class='pager__item pager__item--next']/a").click()
    with open("data.json", "w" , encoding='utf-8') as fichier:
        json.dump(dictionnaire,fichier,indent=4, ensure_ascii=False)
    dico_filtre = {"Lieu":"","Author":"","Agency":"","Status":"", "Last update by": ""}
    for key in dico_filtre.keys():
        dico_filtre[key]=list({value[key] for value in dictionnaire.values()})
    with open("filtres.json", "w", encoding='utf-8') as fichier:
        json.dump(dico_filtre,fichier,indent=4, ensure_ascii=False)
    return dictionnaire

def verifier_element_present(element):

    """
    Cette fonction permet de vérifier si un élement est present sur une page grâce à une requette selenium

    Args:
        element (str) : Le chemin de l'élément exploitable avec XPATH

    Returns:
        bool : True si l'élément est présent sinon False
    """
    try:
        driver.find_element(By.XPATH,element)
        return True
    except:
        return False
    
#Filtrage des annonces

def filtre_date(liste, nb_jour):
    """
    Cette fonction prend en parametre deux éléments, une liste qui contient des annonces et un nombre de jour qui représente la durée à partir
    de laquelle on selectionne les annonces. Dans la fonction on récupere d'abort la date de l'annonce présente dans la valeur de la clé "Updated Trier par ordre croissant".
    On formate ensuite cette date pour la convertir en objet datetime. Enfin on soustrait la date actuelle avec la date de l'annonce pour obtenir l'écart en jour. 

    Args:
        liste (str): liste d'annonces
        nb_jour (int): Le nombre de jours   

    Returns:
        annonces_expirees (list): Liste qui contient les annonces dont la date est expirée. 
    """

    annonces_expirees = []
    date_format = "%d/%m/%Y"    
    date_actuelle = datetime.datetime.now()
    for annonce in liste:
        date_annonce = annonce["Updated Trier par ordre croissant"].split(" - ")[0] # Permet de récuperer uniquement la date de l'annonce
        date_annonce_objet_datetime = datetime.datetime.strptime(date_annonce, date_format) # Permet de convertir la date de l'annonce en objet datetime
        diff_jour = (date_actuelle - date_annonce_objet_datetime).days # Permet d'obtenir l'ecart en jours entre la date actuelle et celle de l'annonce
        if diff_jour >= int(nb_jour):
            annonces_expirees.append(annonce)
    return annonces_expirees


#Filtrage à partir des fichiers json

def filtre(villes="all", auteurs="all", agences="all", statuts="all", dernier_editeurs="all", nb_jour=0):

    """
    Cette fonction permet de filtrer les annonces contenu dans le fichier "data.json" à partir des différents filtres placés en parametre.
    On peut choisir lorqu'on appel la fonction de ne pas renseigné de filtre ce qui selectionne par défaut toutes les annonces. 
    On vérifie la présence des filtres en paramètre grâce au fichier 'filtres.json' et à la fonction "verif_elements_liste(element, liste)".

    Args:
        villes (list): contient les villes à filtrer
        auteurs (list): contient les auteurs à filtrer
        agences (list): contient les agence à filtrer
        statuts (list): contient les statuts à filtrer
        nb_jour (int): représente le nombre de jour à partir duquel on selectionne les annonces.
    
    Return:
        liste_filtre (list): Liste qui contient les annonces filtrées

    """
    
    with open('filtres.json', "r", encoding='utf-8') as fichier_filtres:
        filtres = json.load(fichier_filtres)
        
    villes = filtres["Lieu"] if villes == "all" else villes
    auteurs = filtres["Author"] if auteurs == "all" else auteurs
    agences = filtres["Agency"] if agences == "all" else agences
    statuts = filtres["Status"] if statuts == "all" else statuts
    dernier_editeurs = filtres["Last update by"] if dernier_editeurs == "all" else dernier_editeurs
    


    if not verif_elements_liste(villes, filtres["Lieu"]):
        print("Villes non comprises dans le filtre. Utilisation des villes par défaut.")
        villes = filtres["Lieu"]

    if not verif_elements_liste(auteurs, filtres["Author"]):
        print("Auteurs non compris dans le filtre. Utilisation des auteurs par défaut.")
        auteurs = filtres["Author"]

    if not verif_elements_liste(agences, filtres["Agency"]):
        print("Agences non comprises dans le filtre. Utilisation des agences par défaut.")
        agences = filtres["Agency"]

    if not verif_elements_liste(statuts, filtres["Status"]):
        print("Statuts non compris dans le filtre. Utilisation des statuts par défaut.")
        statuts = filtres["Status"]

    if not verif_elements_liste(dernier_editeurs, filtres["Last update by"]):
        print("éditeurs non compris dans le filtre. Utilisation des éditeurs par défaut.")
        dernier_editeurs = filtres["Last update by"]
        
        

    #filtrage depuis le fichier data.json
        
    with open('data.json', 'r', encoding='utf-8') as fichier_annonces:
        annonces = json.load(fichier_annonces)
        liste_annonce = [annonce for annonce in annonces.values()]
    
    # Permet de verifier pour chaque annonce que l'annonce possède une valeur qui est presente dans les differents filtres qui sont les listes placé en paramètre. 
    liste_filtre = [annonce for annonce in liste_annonce if annonce['Lieu'] in villes and annonce['Author'] in auteurs and annonce['Agency'] in agences and annonce['Status'] in statuts and annonce['Last update by'] in dernier_editeurs] 
    liste_filtre = filtre_date(liste_filtre, nb_jour)
    
    pprint(liste_filtre)
    return liste_filtre


def verif_elements_liste(elements, liste):
    """
    Cette fonction vérifie qu'un element est présent dans une liste.

    Args:
        elements (list): liste qui contient les élement à vérifié
        liste (list): liste qui contient les élememnt référants
    
    Return:
        bool : True si les éléments sont bien dans la liste sinon False. 
    """
    return all(element in liste for element in elements)


#Action sur les annonces           

def action_annonces(liste, lien_action):
    
    for annonces in liste:
        lien = annonces[lien_action]
        try:
            requests.get(lien)
            print("action effectuée")
        except:
            print("lien invalide")



if __name__=="__main__":

    
    connexion_page(os.getcwd()+'/test/code.html')
    recuperer_donnees_pages()
    test = filtre()
    pprint(test)
    
    
    
    