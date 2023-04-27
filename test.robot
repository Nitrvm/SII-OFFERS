*** Settings ***
Library    prog_principal.py
Library    SeleniumLibrary
Library    OperatingSystem
Library    BuiltIn
Library    Collections
Library    String




*** Variables ***
${url}    file:///D:/Users/martin.jautee/Documents/SII-OFFERS/test/code.html
${villes_def}     all
${auteurs_def}    all  
${agences_def}    all    
${statuts_def}    all    
${dernier_editeurs_def}    all     
${nb_jour}    0



*** Test Cases ***
Test filtrage par defaut
    Connexion à la page    ${url}
    Récuperation des annonces
    Filtrage des annonces

Test filtrage specifique
    Connexion à la page    ${url}
    Récuperation des annonces
    @{villes_def}    Split String   ${villes_def}    separator=,     
    @{auteurs_def}    Split String       ${auteurs_def}    separator=,
    @{agences_def}    Split String       ${agences_def}    separator=,
    @{statuts_def}    Split String       ${statuts_def}    separator=,
    @{dernier_editeurs_def}    Split String       ${dernier_editeurs_def}    separator=,
    Filtrage des annonces    ${villes_def}    ${auteurs_def}     ${agences_def}    ${statuts_def}    ${dernier_editeurs_def}    ${nb_jour}

*** keywords ***
Connexion à la page
    [Tags]    Connexion à la page
    [Arguments]    ${url}
    Connexion Page    ${url}


Récuperation des annonces
    [Tags]    Récuperer toutes les annonces par pages et creer deux fichiers json, un pour les filtres et un autres pour les annonces 
    ${result}=    Run Keyword    Recuperer Donnees Pages
    ${dictionnaire_annonces}=    Set Variable    ${result}
    Set Suite Variable    ${dictionnaire_annonces}
    Log    ${dictionnaire_annonces}

Filtrage des annonces
    [Tags]    Filtrage des annonces en fonction des élément placé en parametre    
    [Arguments]    ${villes}=all    ${auteurs}=all    ${agences}=all    ${status}=all   ${dernier_editeurs}=all    ${nb_jour}=0
    ${result}    Filtre    ${villes}    ${auteurs}     ${agences}    ${status}    ${dernier_editeurs}    ${nb_jour}
    Log    ${result}




    