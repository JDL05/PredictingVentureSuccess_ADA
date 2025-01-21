# 🚀 Predicting Venture Success

✨ **Brief description:** We use Cruchbase and Social Media data to predict the success of startups with classical Machine Learning models, a new foundation model called TabPFN and Large Language Models.

![Status Badge](https://img.shields.io/badge/status-active-green.svg)  
![Python](https://img.shields.io/badge/python-3.12-blue)
![React](https://img.shields.io/badge/react-17.0.2-blue)

---

## 📖 Table of Contents

1. [📚 About the Project](#about-the-project)
2. [💬 Languages](#languages)
3. [🔢 Data Files](#datafiles)
4. [🐍 Coding Files](#codingfiles)
5. [🧠 Models](#models)
6. [📎 Delivarables](#presentationandpaper)
7. [🧑 Team](#team)

---

## 📚 About the Project

The objective of this project is to predict the success of startups in the core startup ecosystems of Germany. Therefore, we collected data from the startup-database [Crunchbase](https://www.crunchbase.com) and scraped social media data from LinkedIn and X/Twitter. To reach the projects objective, we applied a Machine Learning Pipeline and selected a row of models to predict the binary success variable. We selected from classical methods (Logistic Regression / Gradient Boosting / Light GBM / Neural Network), new emerging models like the Tabular Prior-data Fitted Network (TabPFN) and Large Language Models (distilBERT). The projects results are explained in a research paper and presented in a React-coded Dashboard.

---

## 💬 Languages

* Python (executed in Jupyter Notebooks)
* React (Dashboard)

---

## 🐍 Coding Files

We applied a typical Machine Learning pipeline with the following order and file names:

* Pre-Processing: DataPreprocessing_Pipeline.ipynb
* Feature Engineering: FeatureEngineering.ipynb
* Model Preparation: ModelPreparation.ipynb
* Modelling: Modelling.ipynb

For the Webscraping, the following files have to be run:


For the Dashboarding, the following files have to be run:
1. Download the 'Dashboard/Code-Files'-directory and open the folder in an IDE. We used Visual Studio Code.
2. Run the following code in Terminal: cd + 'directory-path'
3. Run in the Terminal: npm run dev
4. Open the displayed link in a browser
5. Optional: under 'Dashboard/Code-Files/public' a json-file is stored. This json-file maintains the data for the dashboard and is interchangable.

For the LLM-Approach, the following files have to be run:




---

## 🔢 Data Files

All data files needed to process the code are stored in the 'Datasets'-Directory or 'Code'-Directory when the data is a result of a webscraping script. To use them, the entire directories have to be downloaded. In the code, every files are read with the use of a wildcard in the filepaths (/*.csv). 

**The following data sets / directories are needed to run 'Pre-Processing/DataPreprocessing_Pipeline.ipynb'**

On Github:
1. Datasets/Companies
2. Datasets/Funding
3. Datasets/Investors
4. Code/Social Media Webscraping/Results/LinkedIn/Companies
5. Code/Social Media Webscraping/Results/Twitter/companies_twitter.csv

On Google Drive:
1. [People Data from Crunchbase](https://drive.google.com/file/d/1hDpWc7DjrCUaiS1QdBTeA14Yq5JOXwew/view?usp=share_link)

**The following data set / directories are needed to run 'Feature Engineering/FeatureEngineering.ipynb'**

On Github:
1. Code/Social Media Webscraping/Results/LinkedIn/founders_linkedin.csv
2. Datasets/Datasets/Universities/UniversityRanking.csv

**The other files do not need additional data files**

---

## 🧠 Models

**Prediction Models**
* Logistic Regression
* Neural Network
* Gradient Boosting
* Light GBM
* TabPF (see [Github](https://github.com/PriorLabs/TabPFN))

**LLMs**
* [Bart Large MNLI](https://huggingface.co/facebook/bart-large-mnli)
* [distilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert)

---

## 📎 Deliverables

[Research Paper](LINK)
The results are explained in a research-type paper where the related work, methodology and experiment application is explained. This paper provides the most detailed information.

[Dashboard](LINK)
The Dashboard is coded with React and is [online](Link) accessible. Nevertheless, the source code is provided and can be run locally. 

---

## 🧑 Team
* Christopher Goebeler
* Leon Kvas
* Jan Linzner
* Simon Merten

