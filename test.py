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


def parse_cote(cotes_initiales, cotes_finales, sport):
    cote_tempo = []

    for i in range(len(cotes_initiales)):
        try:
            if cotes_initiales[i] in numero:
                if (cotes_initiales[i + 1] == "," or cotes_initiales[i + 1] == ".") and cotes_initiales[i - 1] in numero:
                    cote_tempo.append(cotes_initiales[i - 1:i + 4])
                elif cotes_initiales[i + 1] == "," or cotes_initiales[i + 1] == ".":
                    cote_tempo.append(cotes_initiales[i:i + 4])
                elif "ul" in cotes_initiales[i - 3: i]:
                    cote_tempo.append(cotes_initiales[i:i + 2])
                elif "NUL" in cotes_initiales[i - 4:i]:
                    cote_tempo.append(cotes_initiales[i:i + 2])
        except:
            break

    if sport == "Rugby":
        for i in range(len(cote_tempo)):
            try:
                if cote_tempo[i][0:2] != cote_tempo[i+1][0:2]:
                    cotes_finales.append(cote_tempo[i])
            except:
                break
        cotes_finales.append(cote_tempo[-1])
        return cotes_finales
    else:
        cotes_finales = cote_tempo.copy()
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

def parse_pokerstars_2_issues(cotes_initiales):
    cotes_finales = []

    for a in range(len(cotes_initiales)):
        if a%2 == 0:
            cotes_finales.append(cotes_initiales[a])

    return cotes_finales

def parse_joa_2_issues(cotes_initiales):
    cotes_finales = []
    cotes_tempo = []
    modulo = int(len(cotes_initiales)/4)

    for a in range(modulo):
        try:
            if len(cotes_initiales[a]) > 5:
                del cotes_initiales[a]
        except:
            break

    for a in range(modulo):
        try:
            cotes_tempo.append(cotes_initiales[0])
            cotes_tempo.append(cotes_initiales[1])
            del cotes_initiales[0:5]
        except:
            break

    for a in range(len(cotes_tempo)):
        if cotes_tempo[a] < 10.0:
            cotes_finales.append(cotes_tempo[a])

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


def scrap(urlpage, balise,sport):
    """GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"
    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)"""

    driver = webdriver.PhantomJS()
    st.write(urlpage)
    st.write(balise)
    driver.get(urlpage)
    data = []
    t = 0

    while len(data) == 0 and t < 15:
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
        cotes_parse = parse_cote(cote_a_nettoyer, cote, sport)
        delete_fake_odds(cotes_parse)
        go_to_float(cotes_parse, cote_float)
    except:
        cote_float = [0]

    return cote_float

