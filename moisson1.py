# coding utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "especes-menacees-qc.csv"

#Parce que je ne parvenais pas à isoler le segment dans la page [http://www3.mffp.gouv.qc.ca/faune/especes/menacees/liste.asp] pour mener à la fiche des espèces menacées recensées, j'ai décidé de "patcher" moi-même l'url avec un range entre 0 et 88. 
especes = list(range(1,89))

entetes = {
    "User-Agent": "Guillaume Lepage - Requête pour un cours de journalisme à l'UQAM",
    "From": "guillaume.p.lepage@gmail.com"
}

#J'ai laissé les traces de ma première tentative que j'ai réussi à contourner avec la var espèces qui renvoie à mon "range" pour patcher directement l'url initial.
# url = "http://www3.mffp.gouv.qc.ca/faune/especes/menacees/liste.asp"
# contenu = requests.get(url, headers=entetes)
# page = BeautifulSoup(contenu.text, "html.parser")
# ligne = page.find_all("td")
# for td in ligne:
#     fin = td.find_all(href=True)
#     print(fin.a["href"])
#Mais une fois arrivé à cette étape, je ne savais pas comment je pouvais isoler le bout d'URL unique à chaque espèces dont j'allais me servir pour compléter mon hyperlien initial.
    
for espece in especes:
    url = "http://www3.mffp.gouv.qc.ca/faune/especes/menacees/fiche.asp?noEsp={}".format(espece)
    contenu = requests.get(url, headers=entetes)
    #Avec les deux étapes ci-dessous, je vérifie si j'ai une réponse positive de ma requête auprès du site du MFFP, donc si les manipulations de ma première "loop" fonctionne.
    # if contenu.status_code==200:
    # print(contenu)
    page2 = BeautifulSoup(contenu.text, "html.parser")
    # Je crée ma variable finale dans laquelle je vais mettre les infos au fur et à mesure que je vais moissonner les profils des espèces menacées.
    info = []
    info.append(url)
    #Pour trouver le nom de chacune des espèces menacées sur leur profil respectif du site du MFFP.
    for nom in page2.find_all("p", class_="titre"):
        # print("%"*50)
        # print(url)
        # print(nom.text)
        info.append(nom.text.strip())
        for rang in page2.find_all("td", class_="rang"):
            if rang.text.strip()[0:4] != "Rang":
                if rang.text.strip()[0:6] != "Statut":
                    info.append((rang.text.strip()))
                    print(info)
        # print(page2.find("table", id="AutoNumber2").find("p").text.strip())

        #Et on remplit les lignes et les colonnes de notre fichier csv avec les données récoltées dans nos "loops" précédentes et assignées à la var «info».
        ecrire = open(fichier,"a")
        lucBlanchette = csv.writer(ecrire)
        lucBlanchette.writerow(info)