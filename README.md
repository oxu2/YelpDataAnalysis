# YelpDataAnalysis
This project will focus on Sandwich restaurants with data from Yelp, and the target is to analyze the reviews and provide data-driven suggestions to business owners. Specifically, it will categorize all the reviews by topic, and for each sandwich business, find out the reasons why they have received good reviews or bad reviews. Consumer behaviors and preferences are discussed in this project in order to provide businesses with unique business strategies in different seasons.
<!-- *** -->
<!-- Group 2, Module 2, BodyFatCalculator -->
***

## Table of Contents
  - [Dependencies](#dependencies)

  - [Installation](#installation)

  - [File Description in Code Folder](#file-description-in-code-folder)

  - [Web-based APP](#link-to-the-web-based-app)
  
  - [Acknowledgements](#acknowledgements)

  
  - [Contributors](#contributors)


***
## Dependencies
- [Python 3.6+](https://www.python.org/)
- [R 4.0+](https://www.r-project.org/)
- [R Shiny](https://github.com/rstudio/shiny)(Shiny is supported on the latest release version of R, as well as the previous four minor release versions of R)



## Installation
These commands assume that your Python version is 3.6+ and that the Python 3
version of `pip` is available as `pip3`.
It may be available as `pip` depending on how your system is configured.
```bash
# [OPTIONAL] Activate a virtual environment
pip3 install --upgrade virtualenv
virtualenv -p python3 .envspam
source .envspam/bin/activate

# Install requirements (both shared and tutorial-specific)
pip3 install -r requirements.txt
pip3 install -r spam/requirements.txt

# Launch the Jupyter notebook interface
jupyter notebook spam
```
This project depends upon a knowledge of  the packages in R, You can run this demo with:
```
if (!require(devtools))
  install.packages("devtools")
devtools::install_github("rstudio/leaflet")
shiny::runGitHub("rstudio/shiny-examples", subdir="063-superzip-example")
```


## File Description in Code Folder

<!-- - Folder BodyfatShiny - Code for Shiny App of body fat calculator based on final model. -->
- [BodyFat.csv](Code/BodyFat.csv) - the raw data set of available measurements include age, weight, height, bmi, and various body circumference measurements.
- [Data Preprocessing.R](Code/Data%20Preprocessing.R) - R code for data cleaning on Bodyfat.csv.
- [Model Selection and Diagnostics.R](Code/Model%20Selection%20and%20Diagnostics.R) - R code for model building, selection based on cleaned data and diagnostics for the selected model.
<!-- - [Summary.pdf](Summary.pdf) - A two-page .pdf file of the summary of the whole project, including the description of project process and conclusions. -->
<!-- - [Presentation.pdf](Presentation.pdf) - A .pdf file of the slides we used in presentation. -->

## Web-based APP

[Shiny APP Link](https://ouyangxu.shinyapps.io/YelpShiny/)

### Preview:
![ShinyPreview1](image/YelpShinyPreview1.png)
![ShinyPreview2](image/YelpShinyPreview2.png)
## Acknowledgements
This project is a project of STAT 628 Fall 2021 UW-Madison, supervised by Prof. Hyunseung Kang.


## Contributors
* **Bowen Tian** - (btian23@wisc.edu) : Contribute to data preprocessing, model diagnostics, report writing.
* **Ouyang Xu** - (oxu2@wisc.edu) : Contribute to R Shiny APP, Github construction, report writing.
* **Tianhang Li** - (tli425@wisc.edu) : Contribute to model selection, model evaluation, report writing, slides writing.

