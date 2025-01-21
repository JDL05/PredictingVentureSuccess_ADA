# 🚀 Predicting Venture Success

✨ **Brief description:** We use Cruchbase and social media data to predict startup success using classical machine learning models, a new foundation model called TabPFN, and large language models.

![Status Badge](https://img.shields.io/badge/status-active-green.svg)  
![Python](https://img.shields.io/badge/python-3.12-blue)
![React](https://img.shields.io/badge/react-17.0.2-blue)

---

## 📖 Table of Contents

1. [📚 About the Project](#about-the-project)
2. [💬 Languages](#languages)
3. [🔢 Data Files](#data-files)
4. [🐍 Coding Files](#coding-files)
5. [🧠 Models](#models)
6. [📎 Delivarables](#delivarables)
7. [🧑 Team](#team)

---

## 📚 About the Project

The goal of this project is to predict the success of startups in the core startup ecosystems of Germany. Therefore, we collected data from the startup database [Crunchbase] (https://www.crunchbase.com) and scraped social media data from LinkedIn and X/Twitter. To achieve the project goal, we applied a machine learning pipeline and selected a set of models to predict the binary success variable. We selected from classical methods (Logistic Regression / Gradient Boosting / Light GBM / Neural Network), new emerging models like Tabular Prior-data Fitted Network (TabPFN) and Large Language Models (distilBERT). The project results are explained in a research paper and presented in a React-coded dashboard.

---

## 💬 Languages

* Python (executed in Jupyter Notebooks)
* React (Dashboard)

---

## 🐍 Coding Files

### We applied a typical Machine Learning pipeline with the following order and file names:

* Pre-Processing: DataPreprocessing_Pipeline.ipynb
* Feature Engineering: FeatureEngineering.ipynb
* Model Preparation: ModelPreparation.ipynb
* Modelling: Modelling.ipynb

### For the Webscraping, the following files have to be run:

1. Put a new unbanned set of HTTP Proxies in Code/Social Media Webscraping/Proxies.txt.
2. For LinkedIn Company Information run Code/Social Media Webscraping/scrapeLinkedInThreaded.py.
3. For LinkedIn Founder Information run Code/Social Media Webscraping/scrapeLinkedInFoundersThreaded.py.
4. For Twitter Company Information run Code/Social Media Webscraping/scrapeSocialBladeThreaded.py.
5. Results are saved automatically into Code/Social Media Webscraping/Results.
   
### For the Dashboarding, the following files have to be run:

1. Download the 'Dashboard/Code-Files'-directory and open the folder in an IDE. We used Visual Studio Code.
2. Run the following code in Terminal: cd + 'directory-path'
3. Run in the Terminal: npm run dev
4. Open the displayed link in a browser
5. Optional: under 'Dashboard/Code-Files/public' a json-file is stored. This json-file maintains the data for the dashboard and is interchangable.

   
### For the LLM-Approach, the following files have to be run:




---

## 🔢 Data Files

All data files needed to process the code are stored in the 'Datasets' directory, or in the 'Code' directory if the data is the result of a web scraping script. To use them, the entire directories must be downloaded. In the code, each file is read using a placeholder in the file paths (/*.csv). 

### The following data sets / directories are needed to run 'Pre-Processing/DataPreprocessing_Pipeline.ipynb'

On Github:
1. Datasets/Companies
2. Datasets/Funding
3. Datasets/Investors
4. Code/Social Media Webscraping/Results/LinkedIn/Companies
5. Code/Social Media Webscraping/Results/Twitter/companies_twitter.csv

On Google Drive:
1. [People Data from Crunchbase](https://drive.google.com/file/d/1hDpWc7DjrCUaiS1QdBTeA14Yq5JOXwew/view?usp=share_link)

### The following data set / directories are needed to run 'Feature Engineering/FeatureEngineering.ipynb'

On Github:
1. Code/Social Media Webscraping/Results/LinkedIn/founders_linkedin.csv
2. Datasets/Datasets/Universities/UniversityRanking.csv

### The other files do not need additional data 

---

## 🧠 Models

### Prediction Models
* Logistic Regression
* Neural Network
* Gradient Boosting
* Light GBM
* TabPF (see [Github](https://github.com/PriorLabs/TabPFN))

### LLMs
* [Bart Large MNLI](https://huggingface.co/facebook/bart-large-mnli)
* [distilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert)

---

## 📎 Deliverables

[Research Paper](LINK) <br>
The results are explained in a research-type paper that describes the related work, methodology, and application of the experiment. This paper provides the most detailed information.

[Dashboard](LINK) <br>
The dashboard is coded in React and is [online](link) accessible. However, the source code is provided and can be run locally. 

---

## 🧑 Team
* Christopher Goebeler
* Leon Kvas
* Jan Linzner
* Simon Merten

