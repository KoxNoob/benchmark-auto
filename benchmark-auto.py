import streamlit as st
import test
import pandas as pd
import warnings
import numpy as np

warnings.filterwarnings("ignore")

# Opérateurs
zebet = "Zebet"
winamax = "winamax"
vbet = "vbet"
unibet = "unibet"
poker_stars = "pokerstars"
pmu = "pmu"
parions_sports = "psel"
netbet = "netbet"
betclic = "betclic"
genybet = "genybet"
fp = "fp"
joa = "joa"

operateurs = [winamax, unibet, betclic, parions_sports, zebet, pmu, poker_stars, vbet, netbet, genybet, fp, joa]
name_foot = []
name_basket = []
name_tennis = []
name_rugby = []

urls_foot = pd.read_csv('https://raw.githubusercontent.com/KoxNoob/benchmark-auto/main/competitions_foot.csv', sep=';', encoding="utf-8", header=None)
for i in range(len(urls_foot)):
    name_foot.append(urls_foot.iloc[i, 0])

urls_basket = pd.read_csv('https://raw.githubusercontent.com/KoxNoob/benchmark-auto/main/competitions_basket.csv', sep=';', encoding="utf-8", header=None)
for i in range(len(urls_basket)):
    name_basket.append(urls_basket.iloc[i, 0])

urls_tennis = pd.read_csv('https://raw.githubusercontent.com/KoxNoob/benchmark-auto/main/competitions_tennis.csv', sep=';', encoding="utf-8", header=None)
for i in range(len(urls_tennis)):
    name_tennis.append(urls_tennis.iloc[i, 0])

urls_rugby = pd.read_csv('https://raw.githubusercontent.com/KoxNoob/benchmark-auto/main/competitions_rugby.csv', sep=';', encoding="utf-8", header=None)
for i in range(len(urls_rugby)):
    name_rugby.append(urls_rugby.iloc[i, 0])


sport = st.sidebar.radio('Sports', ("Football", "Basketball", "Tennis", "Rugby"))

if sport == "Football":
    st.markdown(
        "<h3 style='text-align: center; color: grey; size = 0'>Benchmark Football</h3>",
        unsafe_allow_html=True)

    operateur_selectionne = st.multiselect('Quel opérateur ?', operateurs, default=operateurs)
    nb_rencontres = st.slider('Combien de rencontres à prendre en compte maximum ?', 0, 20, 2)
    options = st.multiselect('Quelle compétition ?', name_foot)
    lancement = st.button('Lancez le benchmark')

    if lancement:
        bench_final = pd.DataFrame(index=[i for i in operateurs])
        for competition in options:
            ts_trj = []
            for j in range(len(urls_foot)):
                if urls_foot.iloc[j, 0] == competition:
                    for ope in operateurs:
                        trj = 0
                        try:
                            for k in range(13):
                                if urls_foot.iloc[0, k] == ope and ope in operateur_selectionne:

                                    if ope == "unibet":
                                        trj = (test.trois_issues(test.scrap(urls_foot.iloc[j, k],
                                                                              "//*[@class=\"ui-mainview-block eventpath-wrapper\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "Zebet":
                                        trj = (test.trois_issues(test.scrap(urls_foot.iloc[j, k],
                                                                              "//*[@class=\"uk-accordion-content uk-padding-remove uk-active\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "winamax":
                                        trj = (test.trois_issues(test.scrap(urls_foot.iloc[j, k],
                                                                              "//*[@class=\"sc-fakplV bCGXIW\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "vbet":
                                        trj = (test.trois_issues(test.scrap(urls_foot.iloc[j, k],
                                                                              "//*[@class=\"   module ModuleSbEventsList \"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "psel":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_foot.iloc[j, k], "//*[@class=\"wpsel-app-wrapper\"]",sport),
                                            nb_rencontres))
                                    elif ope == "pokerstars":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_foot.iloc[j, k], "//*[@class=\"sportCompetitionsView\"]",sport),
                                            nb_rencontres))
                                    elif ope == "pmu":
                                        trj = (test.trois_issues(test.scrap(urls_foot.iloc[j, k],
                                                                              "//*[@class=\"entity entity-bean bean-event-list clearfix\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "netbet":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_foot.iloc[j, k], "//*[@class=\"nb-middle-content uk-flex\"]",sport),
                                            nb_rencontres))
                                    elif ope == "genybet":
                                        trj = (test.trois_issues(test.scrap(urls_foot.iloc[j, k],
                                                                              "//*[@class=\"snc-middle-content-middle uk-width-1-1\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "fp":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_foot.iloc[j, k], "//*[@class=\"item-content uk-active\"]",sport),
                                            nb_rencontres))
                                    elif ope == "betclic":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_foot.iloc[j, k], "//*[@class=\"verticalScroller_wrapper\"]",sport),
                                            nb_rencontres))
                                    elif ope == "joa":
                                        trj = (test.trois_issues(test.parse_joa_3_issues(
                                            test.scrap(urls_foot.iloc[j, k], "//*[@class=\"bet-event-list\"]",sport)),
                                                                   nb_rencontres))


                        except:
                            pass
                        ts_trj.append(trj)

                    bench_tempo = pd.DataFrame(data=ts_trj, index=[i for i in operateurs])
                    bench_tempo = bench_tempo.astype(np.float64)
                    bench_final = bench_final.merge(bench_tempo, left_index=True, right_index=True)

        bench_final.columns = options
        bench_final = bench_final.apply(lambda x: x.replace(0.00, np.nan))

        for competition in bench_final.columns:
            bench_final.loc['Moyenne Compétition', competition] = round(
                (bench_final[competition]).sum() / (
                        len(bench_final[competition]) - bench_final[competition].isnull().sum()), 2)
        st.table(bench_final.style.format("{:.2f}"))


if sport == "Basketball":
    st.markdown(
        "<h3 style='text-align: center; color: grey; size = 0'>Benchmark Basketball</h3>",
        unsafe_allow_html=True)

    operateur_selectionne = st.multiselect('Quel opérateur ?', operateurs, default=operateurs)
    nb_rencontres = st.slider('Combien de rencontres à prendre en compte maximum ?', 0, 20, 2)
    options = st.multiselect('Quelle compétition ?', name_basket)
    lancement = st.button('Lancez le benchmark')


    if lancement:
        bench_final = pd.DataFrame(index=[i for i in operateurs])
        for competition in options:
            ts_trj = []
            for j in range(len(urls_basket)):
                if urls_basket.iloc[j, 0] == competition:
                    for ope in operateurs:
                        trj = 0
                        try:
                            for k in range(13):
                                if urls_basket.iloc[0, k] == ope and ope in operateur_selectionne:

                                    if ope == "unibet":
                                        trj = (test.deux_issues(test.scrap(urls_basket.iloc[j, k],
                                                                              "//*[@class=\"ui-mainview-block eventpath-wrapper\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "Zebet":
                                        trj = (test.deux_issues(test.scrap(urls_basket.iloc[j, k],
                                                                              "//*[@class=\"uk-accordion-content uk-padding-remove uk-active\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "winamax":
                                        trj = (test.deux_issues(test.scrap(urls_basket.iloc[j, k],
                                                                              "//*[@class=\"sc-djErbT ftrOoP\"]//*[@class=\"ReactVirtualized__Grid__innerScrollContainer\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "vbet":
                                        trj = (test.deux_issues(test.scrap(urls_basket.iloc[j, k],
                                                                              "//*[@class=\"   module ModuleSbEventsList \"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "psel":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_basket.iloc[j, k], "//*[@class=\"wpsel-app-wrapper\"]",sport),
                                            nb_rencontres))
                                    elif ope == "pokerstars":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_basket.iloc[j, k], "//*[@class=\"sportCompetitionsView\"]",sport),
                                            nb_rencontres))
                                    elif ope == "pmu":
                                        trj = (test.deux_issues(test.scrap(urls_basket.iloc[j, k],
                                                                              "//*[@class=\"entity entity-bean bean-event-list clearfix\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "netbet":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_basket.iloc[j, k], "//*[@class=\"nb-middle-content uk-flex\"]",sport),
                                            nb_rencontres))
                                    elif ope == "genybet":
                                        trj = (test.deux_issues(test.scrap(urls_basket.iloc[j, k],
                                                                              "//*[@class=\"snc-middle-content-middle uk-width-1-1\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "fp":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_basket.iloc[j, k], "//*[@class=\"item-content uk-active\"]",sport),
                                            nb_rencontres))
                                    elif ope == "betclic":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_basket.iloc[j, k], "//*[@class=\"verticalScroller_wrapper\"]",sport),
                                            nb_rencontres))
                                    elif ope == "joa":
                                        trj = (test.deux_issues(test.parse_joa_2_issues(
                                            test.scrap(urls_basket.iloc[j, k], "//*[@class=\"bet-event-list\"]",sport)),
                                                                   nb_rencontres))


                        except:
                            pass
                        ts_trj.append(trj)

                    bench_tempo = pd.DataFrame(data=ts_trj, index=[i for i in operateurs])
                    bench_tempo = bench_tempo.astype(np.float64)
                    bench_final = bench_final.merge(bench_tempo, left_index=True, right_index=True)

        bench_final.columns = options
        bench_final = bench_final.apply(lambda x: x.replace(0.00, np.nan))

        for competition in bench_final.columns:
            bench_final.loc['Moyenne Compétition', competition] = round(
                (bench_final[competition]).sum() / (
                        len(bench_final[competition]) - bench_final[competition].isnull().sum()), 2)
        st.table(bench_final.style.format("{:.2f}"))



if sport == "Tennis":
    st.markdown(
        "<h3 style='text-align: center; color: grey; size = 0'>Benchmark Tennis</h3>",
        unsafe_allow_html=True)

    operateur_selectionne = st.multiselect('Quel opérateur ?', operateurs, default=operateurs)
    nb_rencontres = st.slider('Combien de rencontres à prendre en compte maximum ?', 0, 20, 2)
    options = st.multiselect('Quelle compétition ?', name_tennis)
    lancement = st.button('Lancez le benchmark')


    if lancement:
        bench_final = pd.DataFrame(index=[i for i in operateurs])
        for competition in options:
            ts_trj = []
            for j in range(len(urls_tennis)):
                if urls_tennis.iloc[j, 0] == competition:
                    for ope in operateurs:
                        trj = 0
                        try:
                            for k in range(13):
                                if urls_tennis.iloc[0, k] == ope and ope in operateur_selectionne:

                                    if ope == "unibet":
                                        trj = (test.deux_issues(test.scrap(urls_tennis.iloc[j, k],
                                                                              "//*[@class=\"ui-mainview-block eventpath-wrapper\"]", sport),
                                                                   nb_rencontres))
                                    elif ope == "Zebet":
                                        trj = (test.deux_issues(test.scrap(urls_tennis.iloc[j, k],
                                                                              "//*[@class=\"uk-accordion-content uk-padding-remove uk-active\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "winamax":
                                        trj = (test.deux_issues(test.scrap(urls_tennis.iloc[j, k],
                                                                              "//*[@class=\"sc-djErbT ftrOoP\"]//*[@class=\"ReactVirtualized__Grid__innerScrollContainer\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "vbet":
                                        trj = (test.deux_issues(test.scrap(urls_tennis.iloc[j, k],
                                                                              "//*[@class=\"   module ModuleSbEventsList \"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "psel":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_tennis.iloc[j, k], "//*[@class=\"wpsel-app-wrapper\"]",sport),
                                            nb_rencontres))
                                    elif ope == "pokerstars":
                                        trj = (test.deux_issues(test.parse_pokerstars_2_issues(
                                            test.scrap(urls_tennis.iloc[j, k], "//*[@class=\"content-center\"]",sport)),
                                            nb_rencontres))
                                    elif ope == "pmu":
                                        trj = (test.deux_issues(test.scrap(urls_tennis.iloc[j, k],
                                                                              "//*[@class=\"entity entity-bean bean-event-list clearfix\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "netbet":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_tennis.iloc[j, k], "//*[@class=\"nb-middle-content uk-flex\"]",sport),
                                            nb_rencontres))
                                    elif ope == "genybet":
                                        trj = (test.deux_issues(test.scrap(urls_tennis.iloc[j, k],
                                                                              "//*[@class=\"snc-middle-content-middle uk-width-1-1\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "fp":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_tennis.iloc[j, k], "//*[@class=\"item-content uk-active\"]",sport),
                                            nb_rencontres))
                                    elif ope == "betclic":
                                        trj = (test.deux_issues(
                                            test.scrap(urls_tennis.iloc[j, k], "//*[@class=\"verticalScroller_wrapper\"]",sport),
                                            nb_rencontres))
                                    elif ope == "joa":
                                        trj = (test.deux_issues(test.parse_joa_2_issues(
                                            test.scrap(urls_tennis.iloc[j, k], "//*[@class=\"bet-event-list\"]",sport)),
                                                                   nb_rencontres))


                        except:
                            pass
                        ts_trj.append(trj)

                    bench_tempo = pd.DataFrame(data=ts_trj, index=[i for i in operateurs])
                    bench_tempo = bench_tempo.astype(np.float64)
                    bench_final = bench_final.merge(bench_tempo, left_index=True, right_index=True)

        bench_final.columns = options
        bench_final = bench_final.apply(lambda x: x.replace(0.00, np.nan))

        for competition in bench_final.columns:
            bench_final.loc['Moyenne Compétition', competition] = round(
                (bench_final[competition]).sum() / (
                        len(bench_final[competition]) - bench_final[competition].isnull().sum()), 2)
        st.table(bench_final.style.format("{:.2f}"))



if sport == "Rugby":
    st.markdown(
        "<h3 style='text-align: center; color: grey; size = 0'>Benchmark Rugby</h3>",
        unsafe_allow_html=True)

    operateur_selectionne = st.multiselect('Quel opérateur ?', operateurs, default=operateurs)
    nb_rencontres = st.slider('Combien de rencontres à prendre en compte maximum ?', 0, 20, 2)
    options = st.multiselect('Quelle compétition ?', name_rugby)
    lancement = st.button('Lancez le benchmark')

    if lancement:
        bench_final = pd.DataFrame(index=[i for i in operateurs])
        for competition in options:
            ts_trj = []
            for j in range(len(urls_rugby)):
                if urls_rugby.iloc[j, 0] == competition:
                    for ope in operateurs:
                        trj = 0
                        try:
                            for k in range(13):
                                if urls_rugby.iloc[0, k] == ope and ope in operateur_selectionne:

                                    if ope == "unibet":
                                        trj = (test.trois_issues(test.scrap(urls_rugby.iloc[j, k],
                                                                              "//*[@class=\"ui-mainview-block eventpath-wrapper\"]", sport),
                                                                   nb_rencontres))
                                    elif ope == "Zebet":
                                        trj = (test.trois_issues(test.scrap(urls_rugby.iloc[j, k],
                                                                              "//*[@class=\"uk-accordion-content uk-padding-remove uk-active\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "winamax":
                                        trj = (test.trois_issues(test.scrap(urls_rugby.iloc[j, k],
                                                                              "//*[@class=\"sc-djErbT ftrOoP\"]//*[@class=\"ReactVirtualized__Grid__innerScrollContainer\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "vbet":
                                        trj = (test.trois_issues(test.scrap(urls_rugby.iloc[j, k],
                                                                              "//*[@class=\"   module ModuleSbEventsList \"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "psel":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_rugby.iloc[j, k], "//*[@class=\"wpsel-app-wrapper\"]",sport),
                                            nb_rencontres))
                                    elif ope == "pokerstars":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_rugby.iloc[j, k], "//*[@class=\"sportCompetitionsView\"]",sport),
                                            nb_rencontres))
                                    elif ope == "pmu":
                                        trj = (test.trois_issues(test.scrap(urls_rugby.iloc[j, k],
                                                                              "//*[@class=\"entity entity-bean bean-event-list clearfix\"]",sport),
                                                                   nb_rencontres))
                                    elif ope == "netbet":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_rugby.iloc[j, k], "//*[@class=\"nb-middle-content uk-flex\"]",sport),
                                            nb_rencontres))
                                    elif ope == "genybet":
                                        trj = (test.trois_issues(test.scrap(urls_rugby.iloc[j, k],
                                                                              "//*[@class=\"snc-middle-content-middle uk-width-1-1\"]", sport),
                                                                   nb_rencontres))
                                    elif ope == "fp":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_rugby.iloc[j, k], "//*[@class=\"item-content uk-active\"]",sport),
                                            nb_rencontres))
                                    elif ope == "betclic":
                                        trj = (test.trois_issues(
                                            test.scrap(urls_rugby.iloc[j, k], "//*[@class=\"verticalScroller_wrapper\"]", sport),
                                            nb_rencontres))
                                    elif ope == "joa":
                                        trj = (test.trois_issues(test.parse_joa_3_issues(
                                            test.scrap(urls_rugby.iloc[j, k], "//*[@class=\"bet-event-list\"]", sport)),
                                                                   nb_rencontres))


                        except:
                            pass
                        ts_trj.append(trj)

                    bench_tempo = pd.DataFrame(data=ts_trj, index=[i for i in operateurs])
                    bench_tempo = bench_tempo.astype(np.float64)
                    bench_final = bench_final.merge(bench_tempo, left_index=True, right_index=True)

        bench_final.columns = options
        bench_final = bench_final.apply(lambda x: x.replace(0.00, np.nan))

        for competition in bench_final.columns:
            bench_final.loc['Moyenne Compétition', competition] = round(
                (bench_final[competition]).sum() / (
                        len(bench_final[competition]) - bench_final[competition].isnull().sum()), 2)
        st.table(bench_final.style.format("{:.2f}"))

