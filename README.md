# YelpDataAnalysis


The body fat percentage is a measure of fitness level, which can be calculated as the total mass of fat divided by total body mass. In this project, a simple, robust, and accurate method to estimate the percentage of body fat using available measurements is proposed, related to man's weight, circumferences of abdomen, and thigh. We will follow several steps such as data cleaning, model building and selection, and model diagnostics. The final measurement will be a linear model with three variables which are the circumference of the abdomen, the circumference of the thigh, and body weight.
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
- [R](https://www.r-project.org/)
- [R Shiny](https://github.com/rstudio/shiny)(Shiny is supported on the latest release version of R, as well as the previous four minor release versions of R)



## Installation

This project depends upon a knowledge of  the packages in R.

```
install.packages("shiny")
install.packages("car")
install.packages("tidyverse")
install.packages("caret")
install.packages("broom")
install.packages("MVA")
install.packages("biwt")
install.packages("robustbase")
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
![ShinyPreview](image/YelpShinyPreview1.png)

## Acknowledgements
This project is a project of STAT 628 Fall 2021 UW-Madison, supervised by Prof. Hyunseung Kang.


## Contributors
* **Bowen Tian** - (btian23@wisc.edu) : Contribute to data preprocessing, model diagnostics, report writing.
* **Ouyang Xu** - (oxu2@wisc.edu) : Contribute to R Shiny APP, Github construction, report writing.
* **Tianhang Li** - (tli425@wisc.edu) : Contribute to model selection, model evaluation, report writing, slides writing.

