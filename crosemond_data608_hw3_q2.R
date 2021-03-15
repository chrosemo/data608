#
# DATA 608 - Assignment 3 - Question 2
#

library(tidyverse)
library(shiny)
library(plotly)
library(rsconnect)

data <- read_csv("cleaned-cdc-mortality-1999-2010-2.csv")

avgs <- data %>% dplyr::mutate(pop_w = Population * Crude.Rate) %>%
  dplyr::group_by(Year, ICD.Chapter) %>%
  dplyr::summarise(natl_avg = round(sum(pop_w)/sum(Population),1))
df2 <- data %>% left_join(avgs, by = c("Year","ICD.Chapter"))

ui <- fluidPage(
  titlePanel("Longitudinal change in U.S. state death rates by cause of death, 1999-2010"),
  sidebarPanel(
    print("Data source: WONDER, Centers for Disease Control and Prevention, U.S. Department of Health and Human Services"),
    width = 12
  ),
  sidebarPanel(
    selectizeInput(inputId = "choice1", label = "Cause of death", choices = unique(df2$ICD.Chapter)),
    selectizeInput(inputId = "choice2", label = "States", choices = unique(df2$State), multiple = TRUE, selected = "AL"),
    checkboxInput(inputId = "USA", label = strong("National Average (Black Dash)"), value = TRUE),
    plotlyOutput(outputId = "line"),
    width = 12
  )
)
server <- function(input, output) {
  df_filter <- reactive(df2 %>%
                          dplyr::filter(ICD.Chapter == input$choice1) %>%
                          dplyr::filter(State %in% input$choice2))
  output$line <- renderPlotly({
    xlab <- list(title = "Year")
    ylab <- list(title = "Crude death rate (per 100K population)")
    fig <- plot_ly(df_filter(), x = ~Year, y = ~Crude.Rate, color = ~State, type = "scatter", mode = "lines") %>% layout(xaxis = xlab, yaxis = ylab, showlegend = TRUE)
    if(input$USA) {
      (fig %>% add_trace(y = ~natl_avg, name = "National Average", mode = "lines", line = list(color = "black", width = 3, dash = "dash"), showlegend = FALSE))
    }
    else {
      (fig)
    }
  })
}
shinyApp(ui = ui, server = server)
