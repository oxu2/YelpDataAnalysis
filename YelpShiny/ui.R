library(leaflet)
library(shinydashboard)
library(RColorBrewer)
library(scales)
library(fmsb)
library(lattice)
library(dplyr)
library(plyr)
library(ggplot2)


# Choices for drop-downs


navbarPage("Sandwich Advisor", id="nav",
           tabPanel("Advisor",
                    div(class="outer",
                        
                        tags$head(
                          includeCSS("styles.css"),
                          includeScript("gomap.js")
                        ),
                        
                        # If not using custom CSS, set height of leafletOutput to a number instead of percent
                        leafletOutput("map", width="100%", height="100%"),
                        
                        absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                      draggable = TRUE, top = "auto", left = 50, right = "auto", bottom = 30,
                                      width = 380, height = "auto",
                                      h2("Sandwich Advisor"),
                                 
                                      plotOutput(outputId = "radarplot", height = 350,width = 350),
                                      plotOutput(outputId = "badpieplot", height = 350,width = 350),
                                      h4(htmlOutput("advisor")),
                                      textOutput("space"),
                                      textOutput("info"),
                                      textOutput("contact1"),textOutput("contact2") 
                                      # ,textInput("bus_id", "Business ID")
                                      
                        ),
#right = 810
                        absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                      draggable = TRUE, top = 100, left = "auto", right = 180, bottom = "auto",
                                      width = 250, height = "auto",
                                      
                                      h2("sandwich restraunt map"),
                                      selectInput("rating", "Rating", choices = 1:5, selected = 5)
                        ),

absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
              draggable = TRUE, top = "auto", left = "auto", right = 150, bottom = 30,
              width = 350, height = 500,
              htmlOutput(outputId = "tips")
),
                        
                        tags$div(id="cite",
                                 '       Inspired by', tags$em('https://shiny.rstudio.com/gallery/superzip-example.html'), ' by Joe Cheng <joe@rstudio.com>.'),
                        
                    )
                    
                    
                    
           ),
           tabPanel("Sandwich explorer",
                    fluidRow(
                      h1(htmlOutput("guide1")),
                      column(3,
                             selectInput("states", "States", c("All states"="", structure(state.abb, names=state.abb), "Washington, DC"="DC"), multiple=TRUE)
                      ),
                      column(3,
                             conditionalPanel("input.states",
                                              selectInput("cities", "Cities", c("All cities"=""), multiple=TRUE)
                             )
                      ),
                      column(1,
                             numericInput("minScore", "Min Rating", min=1, max=5, value=1)
                      ),
                      column(1,
                             numericInput("maxScore", "Max Rating", min=1, max=5, value=5)
                      )),
                    h4(htmlOutput("guide2")),
                    hr(),
                  
                    DT::dataTableOutput("theatertable"),
                    textOutput("guide3")
           ),
          
  conditionalPanel("false", icon("crosshair"))
)
