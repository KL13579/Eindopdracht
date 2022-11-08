#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px
import country_converter as coco
import statsmodels.api as sm


# In[2]:


st.set_page_config(page_title = "Dashboard over doodsoorzaken",
                  page_icon = ":bar_chart:")


# In[3]:


#Importeren van dataset
#doodsoorzaken_totaal = pd.read_csv("cause_of_deaths.csv")


# In[4]:


#Alle mogelijke landcodes bekijken
#doodsoorzaken_totaal["Code"].unique()


# In[5]:


#Dataset inspecteren
#doodsoorzaken_totaal.describe()


# In[6]:


#Kolom namen uit de dataset
#doodsoorzaken_totaal.columns


# In[7]:


#Kolom met totaal aantal doden in een jaar toevoegen
#doodsoorzaken_totaal["Totaal"] = doodsoorzaken_totaal.iloc[:,3:].sum(axis = 1)


# In[8]:


#Kolom met continent toevoegen
#converter = coco.CountryConverter()
#doodsoorzaken_totaal["Continent"] = converter.convert(names = doodsoorzaken_totaal["Code"], src = "ISO3", to = "continent")


# In[9]:


#Dataset verkleinen door alleen variabelen te kiezen die interessant zijn
#gekozen_doodsoorzaken_EN = doodsoorzaken_totaal[["Country/Territory", "Code", "Year", "Meningitis",
#                                              "Alzheimer's Disease and Other Dementias", 
#                                              "Parkinson's Disease", "Malaria", "Drowning", "Interpersonal Violence",
#                                             "HIV/AIDS", "Diabetes Mellitus", "Poisonings", "Road Injuries",
#                                              "Totaal", "Continent"]]

#Kolomnamen naar het Nederlands vertalen indien nodig
#gekozen_doodsoorzaken = gekozen_doodsoorzaken_EN.rename(columns = {"Country/Territory" : "Land",
#                                                        "Year" : "Jaar",
#                                                        "Alzheimer's Disease and Other Dementias" : "Alzheimer en andere dementia's",
#                                                        "Parkinson's Disease" : "Parkinson",
#                                                        "Drowning" : "Verdrinking",
#                                                        "Interpersonal Violence" : "Huiselijk geweld",
#                                                        "Diabetes Mellitus" : "Diabetes type 2",
#                                                        "Poisonings" : "Vergiftiging",
#                                                       "Road Injuries" : "Verkeersongelukken"})


# In[10]:


#Csv bestand van maken zodat er minder in streamlit hoeft.
#gekozen_doodsoorzaken.to_csv("gekozen_doodsoorzaken.csv")

#Csv weer terug inladen
gekozen_doodsoorzaken = pd.read_csv("gekozen_doodsoorzaken.csv")


# In[11]:


#Hier wordt een dataframe gemaakt waarbij per continent het aantal overleden aan ziektes wordt berekend
#numeriek = gekozen_doodsoorzaken[["Jaar", "Meningitis",
#                                              "Alzheimer en andere dementia's", 
#                                              "Parkinson", "Malaria", "Verdrinking", "Huiselijk geweld",
#                                              "HIV/AIDS", "Diabetes type 2", "Vergiftiging", "Verkeersongelukken",
#                                              "Totaal", "Continent"]]
#continenten_hist = pd.DataFrame(numeriek.groupby(["Continent", "Jaar"]).sum()).reset_index()

#Omzetten naar csv
#continenten_hist.to_csv("continenten_hist.csv")

#Opnieuw inladen
continenten_hist = pd.read_csv("continenten_hist.csv")


# In[12]:


#Hierin worden de mogelijkheden voor de verschillende dropdown menu's gemaakt

#Opties voor de y variabele van de histogram
hist_opties = ["Meningitis", "Alzheimer en andere dementia's", "Parkinson", "Malaria", 
            "Verdrinking", "Huiselijk geweld", "HIV/AIDS", "Diabetes type 2", "Vergiftiging", "Verkeersongelukken"]

#Opties voor x en y variabelen maken
x_opties = ["Jaar", "Meningitis", "Alzheimer en andere dementia's", "Parkinson", "Malaria", 
            "Verdrinking", "Huiselijk geweld", "HIV/AIDS", "Diabetes type 2", "Vergiftiging", "Verkeersongelukken"]

y_opties = hist_opties

#Opties voor kaart
kaart_opties = hist_opties

#Opties voor het regressie model
model_opties = ["Alzheimer en andere dementia's", "Vergiftiging", "Diabetes type 2", "Verkeersongelukken"]


# In[13]:


#Tabbladen maken
hoofdtab, tab1, tab2, tab3, tab4, tab5 = st.tabs(["Hoofdpagina", "Histogram", "Scatterplot",
                                                  "Correlatietabel", "Kaart", "Voorspelling"])


# In[14]:


#Code voor de hoofdpagina
with hoofdtab:
    st.header("Visualisaties over doodsoorzaken wereldwijd")
    st.write("In dit dashboard zijn verschillende visualisaties te zien die doodsoorzaken weergeven over de hele wereld. In het tabblad van 'Histogram' kan een land gekozen worden in combinatie met een doodsoorzaak, hier zal dan een histogram te voorschijn komen. In het tabblad 'Scatterplot' wordt eerst een land gekozen en daarna kunnen twee variabelen gekozen worden, hier wordt dat een scatterplot van gemaakt. Indien het gewenst is kan dat een regressie lijn hierin gemaakt worden. Bij het tabblad 'Kaart' kunnen verschillende kaarten van de wereld gekozen worden. Van de verschillende doodsoorzaken zijn verschillende kaarten gemaakt waar je de verdeling kan zien. Vanwege het grote aantal mogelijke doodsoorzaken zijn er 10 verschillende doodsoorzaken gekozen op basis van de beschikbare gegevens. Zo is bijvoorbeeld 'Malaria' één van de gekozen doodsoorzaken, in veel landen komt malaria niet meer voor. Echter is op de kaart te zien dat er ook nog landen zijn waar het relatief veel voorkomt.")
    st.markdown("bron: https://ourworldindata.org/burden-of-disease")


# In[15]:


#Code voor het eerste tabblad
with tab1:
    
    st.header("Histogram voor het gekozen land")
    st.write("In dit tabblad kan een land gekozen worden in combinatie met een variabele. Aan de hand van deze keuzes komt een histogram te voorschijn met daar in per jaar het aantal doden voor die doodsoorzaak.")
    
#Dropdown menu voor de variabele van het histogram
    hist_variabele = st.selectbox("Kies hier een variabele voor het histogram: ", hist_opties)
    
#Keuze voor per continent of voor een individueel land
    continent = st.checkbox("Klik hier als u het histogram voor een specifiek land wilt zien")
    
#Histogram voor de continenten
    if continent is False:
        hist = px.bar(continenten_hist, x = "Jaar", y = hist_variabele, color = "Continent", 
                    title = "Aantal doden per continent door: '" + hist_variabele + "'",
                    labels = {"Jaar" : "Tijd (jaren)",
                    hist_variabele : "Aantal doden door '" + hist_variabele + "'"})
        st.plotly_chart(hist)
        
    else:
        
#Hier wordt een dataset gefilterd op basis van de ingevoerde landcode
        landcode = st.text_input("Vul hier de gewenste landcode in: ", "NLD", key = "1")
        landdata = gekozen_doodsoorzaken[gekozen_doodsoorzaken["Code"] == landcode.upper()]
        
#Als een doodsoorzaak niet in een land voorkomt wordt er geen histogram weergegeven
        if landdata[hist_variabele].sum() == 0:
            st.write("'" + hist_variabele + "' komt niet voor in het gekozen land, kies een andere variabele of een ander land.")
    
#Code voor de histogrammen    
        else:
            hist = plt.figure()
            sns.barplot(data = landdata, x = "Jaar", y = hist_variabele, color = "lightgray")
            plt.xticks(rotation = 90)
            plt.title("Aantal doden door '" + hist_variabele + "' door de jaren heen")
            plt.xlabel("Tijd (jaren)")
            plt.ylabel("Doden veroorzaakt door '" + hist_variabele + "'")
            st.pyplot(hist)


# In[16]:


#Code voor het tweede tabblad
with tab2:
    
    st.header("Scatterplot voor verschillende variabelen")
    st.write("In dit tabblad kan een land gekozen worden. Daarna kunnen 2 variabelen gekozen voor de scatterplot. Op basis van die keuzes wordt een scatterplot gemaakt, indien het gewenst is kan in die scatterplot een regressielijn gezet worden.")

#Hier wordt een dataset gefilterd op basis van de ingevoerde landcode
    landcode2 = st.text_input("Vul hier de gewenste landcode in: ", "NLD", key = "2")
    landdata = gekozen_doodsoorzaken[gekozen_doodsoorzaken["Code"] == landcode2.upper()]
    
#Dropdown menu's voor de variabelen van de scatterplot
    x_variabele = st.selectbox("Kies hier een x variabele: ", x_opties)
    y_variabele = st.selectbox("Kies hier een y variabele: ", y_opties)
    
#Als er van minstens één variabele de doodsoorzaak niet in een land voorkomt wordt er geen scatterplot weergegeven
    if (landdata[x_variabele].sum() == 0) or (landdata[y_variabele].sum() == 0):
        st.write("Een gekozen doodsoorzaak komt niet voor in dit land, kies een andere doodsoorzaak of een ander land.")
    else:
        
#Checkbox voor regressielijn of niet
        regressie = st.checkbox("Regressielijn weergeven")
    
#Scatterplot zonder regressielijn
        if regressie is False:
            scatter = plt.figure()
            sns.scatterplot(data = landdata, x = x_variabele, y = y_variabele)
            plt.title("Scatterplot van de variabele '" + x_variabele + "' en '" + y_variabele + "'")
            plt.ylabel("Aantal doden door '" + y_variabele + "'")
#Scatterplot met regressielijn    
        else:
            scatter = plt.figure()
            sns.regplot(data = landdata, x = x_variabele, y = y_variabele, ci = None)
            plt.title("Scatterplot van de variabele '" + x_variabele + "' en '" + y_variabele + "' met regressielijn")
            plt.ylabel("Aantal doden door '" + y_variabele + "'")
        st.pyplot(scatter)


# In[17]:


#Hierin wordt een dataframe van de correlatietabel gemaakt voor het derde tabblad
#corrtabel = gekozen_doodsoorzaken[["Jaar", "Meningitis", "Alzheimer en andere dementia's", "Parkinson", "Malaria", 
#            "Verdrinking", "Huiselijk geweld", "HIV/AIDS", "Diabetes type 2", "Vergiftiging", "Verkeersongelukken"]].corr()
#df = pd.DataFrame(corrtabel)

#Omzetten naar csv
#df.to_csv("correlatie_tabel.csv")

#Csv inladen
correlatie_tabel = pd.read_csv("correlatie_tabel.csv")


# In[18]:


#Code voor het derde tabblad
with tab3:
    
    st.header("Correlatietabel")
    st.write("In de onderstaande tabel zijn de correlatie coëfficiënten te zien voor alle variabelen. Hierin is onder andere te zien dat de correlatie tussen 'Alzheimer' en 'Parkinson' erg sterk is.")

    #Correlatietabel
    st.dataframe(correlatie_tabel)
    st.markdown("bronnen: https://data.worldbank.org/indicator/SP.POP.65UP.TO, https://ourworldindata.org/age-structure")


# In[19]:


#Dataframe maken voor de kaart met percentages ipv getallen

#gekozen_percentage = gekozen_doodsoorzaken.copy()
#gekozen_percentage["Meningitis"] = gekozen_doodsoorzaken["Meningitis"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Alzheimer en andere dementia's"] = gekozen_doodsoorzaken["Alzheimer en andere dementia's"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Parkinson"] = gekozen_doodsoorzaken["Parkinson"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Malaria"] = gekozen_doodsoorzaken["Malaria"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Verdrinking"] = gekozen_doodsoorzaken["Verdrinking"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Huiselijk geweld"] = gekozen_doodsoorzaken["Huiselijk geweld"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["HIV/AIDS"] = gekozen_doodsoorzaken["HIV/AIDS"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Diabetes type 2"] = gekozen_doodsoorzaken["Diabetes type 2"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Vergiftiging"] = gekozen_doodsoorzaken["Vergiftiging"] / gekozen_doodsoorzaken["Totaal"] * 100
#gekozen_percentage["Verkeersongelukken"] = gekozen_doodsoorzaken["Verkeersongelukken"] / gekozen_doodsoorzaken["Totaal"] * 100


# In[20]:


#Omzetten naar een csv
#gekozen_percentage.to_csv("gekozen_percentage.csv")

#CSV weer terug inladen
gekozen_percentage = pd.read_csv("gekozen_percentage.csv")


# In[27]:


#Code voor het vierde tabblad
with tab4:
    
    st.header("Kaart met aantal doden per doodsoorzaak.")
    st.write("In dit tabblad kan een doodsoorzaak gekozen die weergegeven wordt in de kaart. Er kan ook gekozen worden voor percentages in plaats van absolute getallen. Dit geeft de onderlinge verhoudingen beter weer.")

#Dropdown voor de kaart
    kaart_variabele = st.selectbox("Kies hier een variabele voor de kaart: ", kaart_opties)
    
#Keuze voor absolute getallen of percentage
    percentage = st.checkbox("Klik hier als u percentages wilt zien in plaats van absolute getallen")

#Kaart maken door middel van plotly
    if percentage is False:
        kaart = px.choropleth(gekozen_doodsoorzaken, locations = "Code", color = kaart_variabele, hover_name = "Land",
                  animation_frame = "Jaar", color_continuous_scale = "matter", height = 600,
                  range_color = [gekozen_doodsoorzaken[kaart_variabele].min(), gekozen_doodsoorzaken[kaart_variabele].max()])
    
    else:
        kaart = px.choropleth(gekozen_percentage, locations = "Code", color = kaart_variabele, hover_name = "Land",
                  animation_frame = "Jaar", color_continuous_scale = "matter", height = 600,
                  range_color = [gekozen_percentage[kaart_variabele].min(), gekozen_percentage[kaart_variabele].max()])
    
    kaart.update_layout(title = kaart_variabele, showlegendtitle = False)
    
    st.plotly_chart(kaart)
    


# In[26]:


#Code voor het vijfde tabblad
with tab5:
    st.header("Regressie model")
    st.write("In dit tabblad wordt een regressie model gemaakt om het aantal mensen dat aan Parkinson overlijdt te voorspellen. Hiervoor kunnen verschillende variabelen gekozen worden door middel van de knop hieronder.")

#Hier wordt een knop gemaakt die verschillende variabelen kan selecteren    
    model_variabelen = st.multiselect("Selecteer hier de gewenste variabelen voor het voorspellen van Parkinson",
               model_opties, "Alzheimer en andere dementia's")

#Model opstellen    
    x = gekozen_doodsoorzaken[model_variabelen]
    y = gekozen_doodsoorzaken["Parkinson"]
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    predictions = model.predict(x)
    print_model = model.summary()
    
    st.write(print_model)
    
    st.markdown("##")
    
    st.markdown("bron: student verpleegkunde HU (uitleg: zij heeft geholpen bij het bepalen welke ziektes een verband hebben met elkaar)")

