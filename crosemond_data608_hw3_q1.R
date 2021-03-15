#
# DATA 608 - Assignment 3 - Question 1
#

library(tidyverse)
library(shiny)
library(plotly)
library(rsconnect)

data <- read_csv("cleaned-cdc-mortality-1999-2010-2.csv")

df1 <- data %>% filter(Year == 2010)

ui <- fluidPage(
  titlePanel("U.S. state death rates by cause of death, 2010"),
  print("Source: WONDER, Centers for Disease Control and Prevention, U.S. Department of Health and Human Services"),
  sidebarPanel(
    selectizeInput(inputId = "choice", label = "Cause of death", choices = unique(df1$ICD.Chapter)),
    plotlyOutput(outputId = "bar"),
    width = 12
  )
)
server <- function(input, output) {
  df_filter <- reactive(df1 %>% dplyr::filter(ICD.Chapter == input$choice))
  output$bar <- renderPlotly({
    xlab <- list(title = "U.S. state", tickangle = 270)
    ylab <- list(title = "Crude death rate (per 100K population)")
    fig <- plot_ly(df_filter(), x = ~fct_rev(fct_reorder(State, Crude.Rate, min)), y = ~Crude.Rate, type = 'bar') %>%
      layout(xaxis = xlab, yaxis = ylab)
  })
}
shinyApp(ui = ui, server = server)
