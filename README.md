# <img src="https://github.com/amit-99/SE_Project2/blob/develop/sentimental_analysis/realworld/static/images/logo-black-2.png" height="42" width="42"/> C.E.L.T: The Sentimental Analyser 
## Software Engineering Project for CSC 510
<p>
  <a href="https://www.youtube.com/watch?v=VLoJCemCdHg">
    👨🏻‍💻 YouTube
  </a> 
</p>

[![DOI](https://zenodo.org/badge/295188611.svg)](https://zenodo.org/badge/latestdoi/295188611)
[![GitHub Release](https://img.shields.io/github/release/amit-99/SE_Project2)](https://github.com/amit-99/SE_Project2/releases)
![Build](https://github.com/amit-99/SE_Project2/actions/workflows/main.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-v3.11+-brightgreen.svg)  
![GitHub contributors](https://img.shields.io/github/contributors/amit-99/SE_Project2)
![GitHub issues](https://img.shields.io/github/issues/amit-99/SE_Project2)
![GitHub closed issues](https://img.shields.io/github/issues-closed/amit-99/SE_Project2)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/amit-99/SE_Project2)](https://github.com/amit-99/SE_Project2)  
![GitHub language count](https://img.shields.io/github/languages/count/amit-99/SE_Project2)
![Lines of code](https://tokei.rs/b1/github/amit-99/SE_Project2)
[![GitHub-size](https://img.shields.io/github/languages/code-size/amit-99/SE_Project2)](https://github.com/amit-99/SE_Project2)
[![codecov](https://codecov.io/gh/lyonva/ClassMateBot/branch/master/graph/badge.svg)](https://app.codecov.io/gh/amit-99/SE_Project2)

---

## Contents
1. [Introduction](#intro)
2. [Features](#feat)
3. [Steps for execution](#exec)
4. [Product Walkthrough](#usecases)
5. [Roadmap and Progress](#roadmap)
6. [Case Study](#casestudy)
7. [Contributing to the product](#contribute)
8. [Team Members](#team)

---
<a name="intro"></a>
## Introduction - Sentimental Analysis

Sentiment analysis, also known as opinion mining, is the process of determining the sentiment or emotional tone in a piece of text, audio, or other forms of data. It involves identifying whether the sentiment expressed is positive, negative, or neutral. 

### Why is it important?
<ul>
  <li>Sentiment analysis can help businesses and organizations understand how their customers or users feel about their products, services, or experiences. </li>
  <li>Companies can gauge public opinion about their products or services, track trends, and identify emerging issues or opportunities in the market.</li>
  <li>News agencies and media companies use sentiment analysis to analyze public sentiment towards news articles or events. This helps in generating content that aligns with the interests of the audience.</li>
  <li>Sentiment analysis is used in politics to understand public sentiment towards political candidates, parties, or policies. It is also used to gauge public opinion on social issues.</li>
</ul>


The complete development was achieved using the following technologies, and it is recommended that the next set of developers who take up this project have these technologies installed and keep them running before proceeding further:
- Python3
- Django
- HTML
- CSS
- Scrapy
- Vader Analysis Tool

Although we have used HTML and CSS for the FrontEnd, the users can merge the backend logic with any of the front end frameworks they wish to use such as React, angularJS, etc.

---

<a name="use"></a>
## Why C.E.L.T.?
Different types of data sources provide diverse perspectives. An all-encompassing tool can provide a more comprehensive understanding of public sentiment.
In today's world, opinions and sentiments are expressed across various channels, including social media, customer reviews, audio recordings, and news articles. A tool that can analyze these diverse data sources offers a more accurate picture of public sentiment.
Instead of using multiple specialized tools, a single tool that can handle multiple data types is cost-effective and streamlines the analysis process.

---

<a name="feat"></a>
## Features
|Feature|Description  |
|--|--|
|Product Analysis |```Sentimental analysis of Amazon product reviews```|
|News Analysis  |```Sentimental analysis of any recent news topic```|
|Text Analysis | ```Sentimental analysis of text input```|
|Audio Analysis   |``` Sentimental analysis of audio file``` |
|File Analysis   |``` Sentimental analysis of text file``` |
|Live Sentimental Analysis   |``` Sentimental analysis of live recorded audio``` |

---

<a name="exec"></a>
## Steps for Execution
1. Clone this project into your system
```
git clone https://github.com/amit-99/SE_Project2.git
```
2. Make sure you are using Python 3.11 or higher
3. Intall dependencies for the project from root directory of the project:
    a. To install python library dependencies use requirements.txt 
    b. We also need install and import nltk and supporting libraries
```
cd <your_download_dir>\SE_Project2\
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```
4. Install ffmpeg:  
   For Windows:  
   ```
   winget install ffmpeg
   ```  
   For Linux (Ubuntu):  
   ```
   sudo apt install ffmpeg
   ```  
   For Mac:  
   ```
   brew install ffmpeg
   ```   
6. Run Django Server using manage.py (Note: Make sure you are in root directory of the project)
```
python .\sentimental_analysis\manage.py runserver
```
6. Next, open your browser and type in `localhost:8000` in the search bar to open the webUI of the application.5. The UI typically looks as shown below and here you have a choice between URL, file or normal text input.
7. Great!! Now you are into the application

---

<a name="usecases"></a>
![First](https://user-images.githubusercontent.com/43075652/97276268-31ce6100-17f4-11eb-8b57-7741069bf311.png)
![second](https://user-images.githubusercontent.com/43075652/97276507-82de5500-17f4-11eb-88e0-0ea41bc9b424.png)

The UI for URL input is as shown below:
![product](https://user-images.githubusercontent.com/43075652/97276542-925d9e00-17f4-11eb-910f-103be084ad13.png)

The UI for file input is as shown below:
![docum](https://user-images.githubusercontent.com/43075652/97277008-2891c400-17f5-11eb-901a-1ebd3da5a32b.png)

The UI for text input is as shown below:
![text](https://user-images.githubusercontent.com/43075652/97277038-33e4ef80-17f5-11eb-8fbc-76bad26adcc9.png)

The UI for audio input is as shown below:
![audio](https://user-images.githubusercontent.com/43075652/97277059-3d6e5780-17f5-11eb-8dcf-a5935d6613ae.png)

The Output as below:
![output](https://user-images.githubusercontent.com/43075652/97277225-74446d80-17f5-11eb-89f5-2b27c957827e.png)
![out](https://user-images.githubusercontent.com/43075652/97277310-8e7e4b80-17f5-11eb-8910-03ec42ea0ff7.png)

---
<a name="roadmap"></a>
## Roadmap and Progress
### Past Achievement(Previous Work)
- [x] Creating C.E.L.T. Django Project/Website
- [x] Sentiment Analysis Model's Algorithm addition
- [x] Text Analysis and Document Analysis Feature inclusion
- [x] Audio Analysis Feature inclusion
- [x] Amazon Product Analysis Feature addition
- [x] Case Study done for Amazon Product Review Sentiment Analysis 
- [x] Simple Documentation, Unit tests addition

### Current Achievements
☑️  Live Sentiment Analysis Feature inclusion<br>
☑️  News Analysis Feature inclusion<br>
☑️  UI Improvement for enriching User interaction with the Application<br>
☑️  Documentation Improvement for reflecting project's value accurately<br>
☑️  Addition of Builds and Workflows for better development activities<br>
☑️  Unit Tests were written and Test Coverage was improved<br>
☑️  <br>
☑️  <br>
☑️  <be>

### Future Scope
- [ ] Implement User Authentication to store the history of each User
- [ ] Recommendation System based on Product Analysis Results 
- [ ] Enhance the Product Analysis by considering the number of users rated for each Product!
- [ ] Extend the Sentiment Analysis to Facebook, Twitter, LinkedIn Posts
- [ ] To Be Added..

---  
<a name="casestudy"></a>
## Case Study: Amazon Product Review Sentiment and Text Analysis
We have done a Case Study for our Sentiment Analysis Project. It can be found [here](https://github.com/amit-99/SE_Project2/blob/develop/Case_Study.md).

---
<a name="contribute"></a>
## Eager to Contribute?
To Contribute to our application, please refer to [CONTRIBUTING.md](https://github.com/amit-99/SE_Project2/blob/develop/CONTRIBUTING.md)

---

## FUTURE SCOPE

Implement user authentication to store history for each user.

Recommendation system based on analysis results.

Live speech to text sentiment analysis.

Enhance the analysis by taking into consideration the number of users rated for each product!

Extend the analysis to the Facebook, Twitter and LinkedIn Posts

---

<a name="team"></a>
## Team Members

- Akash Kore
- Amit Bhujbal
- Sohamkumar Patel
- Yogesh Hasabe
