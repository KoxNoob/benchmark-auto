from selenium import webdriver
import time
import streamlit as st

numero = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
liste_trj = []
trj_final = 0


def test(testo):
    return testo


def go_to_float(cote, cote_float):
    for elem in cote:
        elem = elem.replace(',', '.')
        cote_float.append(float(elem))
    return cote_float


def parse_cote(cotes_initiales, cotes_finales):
    for i in range(len(cotes_initiales)):
        try:
            if cotes_initiales[i] in numero:
                if cotes_initiales[i + 1] == "," and cotes_initiales[i - 1] in numero:
                    cotes_finales.append(cotes_initiales[i - 1:i + 4])
                elif cotes_initiales[i + 1] == ",":
                    cotes_finales.append(cotes_initiales[i:i + 4])
        except:
            break

    for i in range(len(cotes_initiales)):
        try:
            if cotes_initiales[i] in numero:
                if cotes_initiales[i + 1] == "." and cotes_initiales[i - 1] in numero:
                    cotes_finales.append(cotes_initiales[i - 1:i + 4])
                elif cotes_initiales[i + 1] == ".":
                    cotes_finales.append(cotes_initiales[i:i + 4])
        except:
            break

    return cotes_finales


def delete_fake_odds(cotes_initiales):
    for i in range(len(cotes_initiales)):
        for j in range(len(cotes_initiales)):
            try:
                if cotes_initiales[i][j] == ' ':
                    del cotes_initiales[i]
                    break
            except:
                break
    return cotes_initiales


def parse_joa_2_issues(cotes_initiales):
    cotes_finales = []
    modulo = int(len(cotes_initiales)/4)
    for a in range(modulo):
        try:
            if len(cotes_initiales[a]) > 5:
                del cotes_initiales[a]
        except:
            break

    for a in range(modulo):
        try:
            cotes_finales.append(cotes_initiales[0])
            cotes_finales.append(cotes_initiales[1])
            del cotes_initiales[0:4]
        except:
            break

    return cotes_finales


def parse_joa_3_issues(cotes_initiales):
    cotes_finales = []
    modulo = int(len(cotes_initiales) / 6)
    for a in range(modulo):
        try:
            if len(cotes_initiales[a]) > 5:
                del cotes_initiales[a]
        except:
            break

    for a in range(modulo):
        try:
            cotes_finales.append(cotes_initiales[0])
            cotes_finales.append(cotes_initiales[1])
            cotes_finales.append(cotes_initiales[2])
            del cotes_initiales[0:6]
        except:
            break

    return cotes_finales


def trois_issues(cote_float, nb_rencontres):
    liste_trj = []
    for a in range(int(len(cote_float) / 3)):
        liste_trj.append(
            1 / ((1 / (float(cote_float[3 * a]))) + (1 / (float(cote_float[3 * a + 1]))) + (
                    1 / (float(cote_float[3 * a + 2])))) * 100)

    trj_final = "{:.2f}".format(
        round((sum(liste_trj[0:nb_rencontres]) / len(liste_trj[0:nb_rencontres])), 2))
    return trj_final


def deux_issues(cote_float, nb_rencontres):
    liste_trj = []
    for a in range(int(len(cote_float) / 2)):
        liste_trj.append(
            1 / ((1 / (float(cote_float[2 * a]))) + (1 / (float(cote_float[2 * a + 1])))) * 100)

    trj_final = "{:.2f}".format(
        round((sum(liste_trj[0:nb_rencontres]) / len(liste_trj[0:nb_rencontres])), 2))
    return trj_final


def scrap(urlpage, balise):
    driver = webdriver.PhantomJS()
    driver.get(urlpage)
    data = []
    t = 0

    while len(data) == 0 and t < 8:
        time.sleep(1)
        results = driver.find_elements_by_xpath(balise)
        for result in results:
            product_name = result.text
            if product_name != "":
                data.append(product_name)
        t += 1


    driver.quit()
    try:
        cote_a_nettoyer = data[0]
        cote = []
        cote_float = []
        parse_cote(cote_a_nettoyer, cote)
        delete_fake_odds(cote)
        go_to_float(cote, cote_float)
    except:
        cote_float = [0]
    return cote_float

