# YelpDataAnalysis
This project will focus on Sandwich restaurants with data from Yelp, and the target is to analyze the reviews and provide data-driven suggestions to business owners. Specifically, it will categorize all the reviews by topic, and for each sandwich business, find out the reasons why they have received good reviews or bad reviews. Consumer behaviors and preferences are discussed in this project in order to provide businesses with unique business strategies in different seasons.
<!-- *** -->
<!-- Group 5, Module 3, YelpDataAnalysis -->
***

## Table of Contents
  - [Dependencies](#dependencies)

  - [Installation](#installation)

  - [File Description in Code Folder](#file-description-in-code-folder)

  - [Web-based APP](#web-based-app)
  
  - [Acknowledgements](#acknowledgements)

  
  - [Contributors](#contributors)


***
## Dependencies
- [Python 3.6+](https://www.python.org/)
- [R 4.0+](https://www.r-project.org/)
- [R Shiny](https://github.com/rstudio/shiny)(Shiny is supported on the latest release version of R, as well as the previous four minor release versions of R)



## Installation
These commands assume that your Python version is 3.6+ and basic Machine Learning modules are already installed.
It may be available as `pip` depending on how your system is configured.
```bash
# [OPTIONAL] Activate a virtual environment
pip install pyldavis
pip install nltk
```
This project depends upon a knowledge of  the packages in R, You can install with:
```
if (!require(devtools))
  install.packages("devtools")
devtools::install_github("rstudio/leaflet")
```


## File Description in Code Folder
TODO
<!-- - Folder BodyfatShiny - Code for Shiny App of body fat calculator based on final model. -->

<!-- - [Data Preprocessing.R](Code/Data%20Preprocessing.R) - R code for data cleaning on Bodyfat.csv. -->
<!-- - [Model Selection and Diagnostics.R](Code/Model%20Selection%20and%20Diagnostics.R) - R code for model building, selection based on cleaned data and diagnostics for the selected model. --> 
<!-- - [Summary.pdf](Summary.pdf) - A two-page .pdf file of the summary of the whole project, including the description of project process and conclusions. -->
<!-- - [Presentation.pdf](Presentation.pdf) - A .pdf file of the slides we used in presentation. -->

## Web-based APP

[Shiny APP Link](https://ouyangxu.shinyapps.io/YelpShiny/)

### Preview:
![ShinyPreview1](image/YelpShinyPreview1.png)
![ShinyPreview2](image/YelpShinyPreview2.png)
## Acknowledgements
This is a project of STAT 628 Fall 2021 at UW-Madison, supervised by Prof. Hyunseung Kang.


## Contributors
- **Shuren He** - (she249@wisc.edu) : Contribute to most part of the LDA model including selecting and training model.
- **Ziyue Zheng** - (zzheng232@wisc.edu) : Contribute to the t-test part, the analysis of the LDA model outcome, R Shiny app, report writing.
- **Ouyang Xu** - (oxu2@wisc.edu) : Contribute to part of the LDA model, R Shiny app Github construction, Github construction, report writing.


