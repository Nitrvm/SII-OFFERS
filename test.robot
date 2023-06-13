*** Settings ***
Library    prog_principal.py
Library    authentification.py
Library    SeleniumLibrary
Library    OperatingSystem
Library    BuiltIn
Library    Collections
Library    String
Library    Dialogs


*** Variables ***
${url}    file:///D:/Users/martin.jautee/Documents/SII-OFFERS/test/code.html
${url2}    https://monportail.siinergy.net/user/login?destination=/
${villes_def}     all
${auteurs_def}    Admin-lqSbNvM-…
${agences_def}    all    
${statuts_def}    all   
${dernier_editeurs_def}    all     
${nb_jour}    0
${nb_jour_mail}  0
${login}   
${mdp}



*** Test Cases ***
test 
    
    Log    ${auteurs_def}
Initialisation
    Connexion à la page    ${url}
    Récuperation des annonces
    
Initialisation2
    ${result}=   authentification.Authentification    ${login}    ${mdp}

Initialisation3
    ${result}=   prog_principal.Authentification    ${login}    ${mdp}
    IF    ${result} == True
        Connexion à la page    ${url}
        Récuperation des annonces
    ELSE
        Log  la connexion à échoué 
    END

Filtrage
    Connexion à la page    ${url}
    @{villes_def}    Split String   ${villes_def}    separator=,    
    @{auteurs_def}    Split String       ${auteurs_def}    separator=,
    @{agences_def}    Split String       ${agences_def}    separator=,
    @{statuts_def}    Split String       ${statuts_def}    separator=,
    @{dernier_editeurs_def}    Split String       ${dernier_editeurs_def}    separator=,
    Filtrage des annonces    ${villes_def}    ${auteurs_def}     ${agences_def}    ${statuts_def}    ${dernier_editeurs_def}    ${nb_jour}
    

Republication
    Connexion à la page    ${url}
    @{villes_def}    Split String   ${villes_def}    separator=,    
    @{auteurs_def}    Split String       ${auteurs_def}    separator=,
    @{agences_def}    Split String       ${agences_def}    separator=,
    @{statuts_def}    Split String       ${statuts_def}    separator=,
    @{dernier_editeurs_def}    Split String       ${dernier_editeurs_def}    separator=,
    Filtrage des annonces    ${villes_def}    ${auteurs_def}     ${agences_def}    ${statuts_def}    ${dernier_editeurs_def}    ${nb_jour}
    Republication des annonces  ${liste}

    
Filtrage par defaut
    Connexion à la page    ${url}
    Filtrage des annonces
    Republication    ${liste}

Filtrage specifique
    Connexion à la page    ${url}
    @{villes_def}    Split String   ${villes_def}    separator=,     
    @{auteurs_def}    Split String       ${auteurs_def}    separator=,
    @{agences_def}    Split String       ${agences_def}    separator=,
    @{statuts_def}    Split String       ${statuts_def}    separator=,
    @{dernier_editeurs_def}    Split String       ${dernier_editeurs_def}    separator=,
    Filtrage des annonces    ${villes_def}    ${auteurs_def}     ${agences_def}    ${statuts_def}    ${dernier_editeurs_def}    ${nb_jour}
    republication    ${liste}  

Avertissement Mail
    Mail Notif    ${nb_jour_mail}

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
    
Filtrage des annonces
    [Tags]    Filtrage des annonces en fonction des élément placé en parametre    
    [Arguments]    ${villes}=all    ${auteurs}=all    ${agences}=all    ${status}=all   ${dernier_editeurs}=all    ${nb_jour}=0
    ${result}=    Run Keyword   Filtre    ${villes}    ${auteurs}     ${agences}    ${status}    ${dernier_editeurs}    ${nb_jour}
    ${liste}=    Set Variable    ${result}
    Set Suite Variable    ${liste}
    Log  ${liste}

Republication des annonces
    [Tags]    Republication des annonces en fonction d'une liste d'annonce(s)
    [Arguments]    ${liste}
    Run Keyword      Republication     ${liste}
    


    

