library(leaflet)
library(RColorBrewer)
library(scales)
library(lattice)
library(dplyr)
library(plyr)
library(fmsb)
library(ggplot2)
library(scales)

# Leaflet bindings are a bit slow; for now we'll just sample to compensate
# By ordering by centile, we ensure that the (comparatively rare) Superids
# will be drawn last and thus be easier to see

yelp = yelp[order(yelp$stars),]
bus_id_search <<- 0


function(input, output, session) {
  ## Data Explorer ###########################################
  # Show a popup at the given location
  updateTabsetPanel(session, "nav", selected = "sandwich restraunt explorer")
  
  locationwindow <- function(bus_id, lat, lng) {
    
    selectedZip <- yelp[yelp$business_id == bus_id,]
    content <- as.character(tagList(
      tags$h4("Rating:", as.integer(selectedZip$stars)),
      tags$strong(HTML(sprintf("%s, %s %s",
                               selectedZip$city, selectedZip$state, selectedZip$postal_code
      ))), tags$br(),
      sprintf("Name: %s", selectedZip$name), tags$br(),
      sprintf("Business ID: %s", selectedZip$business_id), tags$br(),
      sprintf("Address: %s", selectedZip$address)
    ))
    leafletProxy("map") %>% addPopups(lng, lat, content, layerId = bus_id)
  }
  
  observe({
    cities <- if (is.null(input$states)) character(0) else {
      filter(cleantable, State %in% input$states) %>%
        `$`('City') %>%
        unique() %>%
        sort()
    }
    stillSelected <- isolate(input$cities[input$cities %in% cities])
    updateSelectizeInput(session, "cities", choices = cities,
                         selected = stillSelected, server = TRUE)
  })
  
  observe({
    busns_id <- if (is.null(input$states)) character(0) else {
      cleantable %>%
        filter(State %in% input$states,
               is.null(input$cities) | City %in% input$cities) %>%
        `$`('Zipcode') %>%
        unique() %>%
        sort()
    }
    stillSelected <- isolate(input$busns_id[input$busns_id %in% busns_id])
    updateSelectizeInput(session, "busns_id", choices = busns_id,
                         selected = stillSelected, server = TRUE)
  })
  
  observe({
    if (is.null(input$goto))
      return()
    isolate({
      map <- leafletProxy("map")
      map %>% clearPopups()
      dist <- 0.5
      bus_id_search <<- input$goto$zip
      lat <- input$goto$lat
      lng <- input$goto$lng
      id = which(scale_final_score[,16] == bus_id_search)
      output$barplot = renderPlot({
        cn = colnames(scale_final_score[,2:13])
        draw = data.frame(x = cn[-1], y = round(as.vector(t(scale_final_score[id,-1])),4))
        ggplot(data = draw, aes(x,y))  +
          geom_bar(stat = "identity", aes(fill = x)) + 
          geom_text(aes(label = paste(y * 100, "%"),
                        vjust = ifelse(y >= 0, 0, 1))) +
          scale_y_continuous("Score", labels = percent_format()) +
          theme_bw() + theme(legend.position="none") + labs(x = '')
      })
      
      output$tips = renderText({
        return("<font size='5'>Tips<br> <font size='3'>First<br>Many consumers are not satisfied with the taste of your sandwiches. Try to improve the taste and freshness of the food, or increase the variety.<br><br>Second<br>Many bad reviews show that the service of your restaurant needs to be improved. Try to train the waiters more.")
      })
      
      output$radarplot = renderPlot({

        if(sum(scale_final_score[id,][2:7])>0){
        pie(as.vector(unlist(scale_final_score[id,][2:7])),
            labels = c("Sandwiches taste","Burger taste","Customer service","Drinks and atmosphere","Breakfast taste","Convenience"),
            main = "topics of good reviews",
            col = c('red','green','yellow','grey','blue','pink'))
        }else{
        pie(as.vector(unlist(scale_final_score[sample(1:100,1),][2:7])),
              labels = c("Sandwiches taste","Burger taste","Customer service","Drinks and atmosphere","Breakfast taste","Convenience"),
              main = "topics of good reviews",
              col = c('red','green','yellow','grey','blue','pink'))    
          }
        
        })
      output$badpieplot = renderPlot({

        if(sum(scale_final_score[id,][8:13])>0){
        pie(as.vector(unlist(scale_final_score[id,][8:13])),
            labels = c("Take out order","Sandwiches taste","Service","Burger taste","Wait minute","Snack & Sides"),
            main = "topics of bad reviews",
            col = c('red','green','yellow','grey','blue','pink'))
        }else{
          pie(as.vector(unlist(scale_final_score[sample(1:100,1),][8:13])),
                  labels = c("Take out order","Sandwiches taste","Service","Burger taste","Wait minute","Snack & Sides"),
                  main = "topics of good reviews",
                  col = c('red','green','yellow','grey','blue','pink'))}
        
      })
      
      output$advisor = renderUI({
        HTML(paste0(strsplit(advisor[advisor == bus_id_search, 2], '\n', fixed = TRUE)[[1]], sep = '<br/>............................................................................<br/>'))
      })
      locationwindow(bus_id_search, lat, lng)
      map %>% fitBounds(lng - dist, lat - dist, lng + dist, lat + dist)
    })
    
  })
  
  
  output$theatertable <- DT::renderDataTable({
    df <- cleantable %>%
      filter(
        Rating >= input$minScore,
        Rating <= input$maxScore,
        is.null(input$states) | State %in% input$states,
        is.null(input$cities) | City %in% input$cities
      ) %>%
      mutate(ClickMe = paste('<a class="go-map" href="" data-lat="', Lat, '" data-long="', Long, '" data-zip="', Business_id, '"><i class="fa fa-crosshairs"></i></a>', sep=""))
      # mutate(ClickMe)
    action <- DT::dataTableAjax(session, df)
    DT::datatable(df, options = list(ajax = list(url = action)), escape = FALSE)
  })
  
  ## Interactive Map ###########################################
  

    # Create the map
  output$map <- renderLeaflet({
    leaflet() %>%
      addTiles() %>%
      setView(lng = -93.85, lat = 37.45, zoom = 4)
  })
  
  # A reactive expression that returns the set of zips that are
  # in bounds right now

  zipsInBounds <- reactive({
    if (is.null(input$map_bounds))
      return(yelp[FALSE,])
    bounds <- input$map_bounds
    latRng <- range(bounds$north, bounds$south)
    lngRng <- range(bounds$east, bounds$west)
    subset(yelp,
           latitude >= latRng[1] & latitude <= latRng[2] &
             longitude >= lngRng[1] & longitude <= lngRng[2])
  })
  # Precalculate the breaks we'll need for the two histograms
  output$space = renderText({"-------------------------------"})
  output$info = renderText({ "Contacts"})
  output$contact1 = renderText({ "Ouyang Xu: oxu2[at]wisc[dot]edu"})
  output$contact2 = renderText({ "Ziyue Zheng: zzheng232[at]wisc[dot]edu"})
  output$guide1 = renderUI({HTML( paste(HTML('&nbsp;'), "Search for your restraunt"))})
  output$guide2 = renderUI({HTML( paste(HTML('&nbsp;'), HTML("Find your business record and click the blue button on the right to check the advice and more details")))})
  output$guide3 = renderText({"Tips: you can either find your sandwich restraunt by filtering by location and rating, or input the relevant information such as business id on the top right of the table. By clicking of the blue button in the location button, the page would be redirected to the interactive map with a popup show more details about the sandwich restraunt."})

  

  # This observer is responsible for maintaining the circles and legend,
  # according to the variables the user has chosen to map to color and size.
  observe({
    colorBy <- input$business_id
    
    colorData = as.factor(ifelse(round(yelp$stars) == input$rating, input$rating, "others"))
    pal = colorFactor("viridis", colorData)
    
    radius = 3000
    
    leafletProxy("map", data = yelp) %>%
      clearShapes() %>%
      addCircles(~longitude, ~latitude, radius=200, layerId=~business_id,
                 stroke=FALSE, fillOpacity=0.4, fillColor=pal(colorData)) %>%
      addLegend("bottomleft", pal=pal, values=colorData, 
                title="Rating", layerId="colorLegend")
   })
  

  
  # When map is clicked, show a popup with city info
  observe({
    leafletProxy("map") %>% clearPopups()
    event <- input$map_shape_click
    if (is.null(event))
      return()
    bus_id_search <<- event$id
    id = which(scale_final_score[,1] == bus_id_search)
    isolate({
      output$advisor = renderUI({
        HTML(paste0(strsplit(advisor[advisor == bus_id_search, 2], '\n', fixed = TRUE)[[1]], sep = '<br/>............................................................................<br/>'))
      })
      locationwindow(event$id, event$lat, event$lng)
      
    })
  })
  

}
