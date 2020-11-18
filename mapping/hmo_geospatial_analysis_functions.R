# HMO Geospatial Analysis Nearest Neighbour Script

library(tidyverse)
library(httr)
library(jsonlite)
library(sp)
library(httr)

london_stations <- read.csv("~/Documents/gh-repos/project-portfolio/mapping/london_stations.csv"
                     , stringsAsFactors = F)

names(london_stations) <- names(london_stations) %>%
  gsub("[.]", "", .) %>%
  tolower(.)

is_digit <- function(string){
  # Remove any addresses where they don't start with a digit
  output <- str_sub(string, 1, 1) %>%
    str_detect("[[:digit:]]")
  return(output)
}

extract_postcode <- function(text){
  postcode <- tail(str_split(text, ",")[[1]], n = 1)
  return(trimws(postcode))
}

gridref_format <- function(text){
  # Prepares data for geocoding online through
  # - https://gridreferencefinder.com/postcodeBatchConverter/
  postcode <- tail(str_split(text, ",")[[1]], n = 1)
  first_line <- head(str_split(text, ",")[[1]], n = 1)
  output <- paste(postcode, first_line, sep = ", ")
  return(output)
}

create_endpoint <- function(postcode){
  postcode <- extract_postcode(postcode)
  # https://postcodes.io/
  # https://postcodes.io/docs
  # https://github.com/ropensci/PostcodesioR
  endpoint <- paste0('http://api.postcodes.io/postcodes/', gsub(" ", "", toupper(postcode)))
  return(endpoint)
}

extract_geodata <- function(endpoint){
  
  endpoint <- create_endpoint(endpoint)
  
  data <- GET(url = endpoint)
  geodata <- content(data)
  x <- names(geodata[['result']])[1:22] # does not include "codes" list
  
  geodataValues <- vector()
  geodataNames <- vector()
  
  for (item in x ){
    for (i in item){
      if (is.null(geodata[['result']][[i]])) {
        geodataValues[length(geodataValues)+1] <- 'no value'
        geodataNames[length(geodataNames)+1] <- item
      } else{
        geodataValues[length(geodataValues)+1] <- geodata[['result']][i]
        geodataNames[length(geodataNames)+1] <- item
      }
    }
  }
  
  for (item in names(geodata[['result']][['codes']]) ){
    for (i in item){
      if (is.null(geodata[['result']][['codes']][[i]])) {
        geodataValues[length(geodataValues)+1] <- 'no value'
        geodataNames[length(geodataNames)+1] <- item
      } else{
        geodataValues[length(geodataValues)+1] <- geodata[['result']][['codes']][i]
        geodataNames[length(geodataNames)+1] <- paste0('codes_', item)
      }
    }
  }
  
  geodataValues <- do.call("c", geodataValues)
  output_df <- data.frame(geodataNames, geodataValues)
  return(output_df)
}

create_wide_geo_df <- function(address){
  endpoint_data <- extract_geodata(address)
  output <- spread(endpoint_data, geodataNames, geodataValues)
  output[] <- lapply(output, as.character)
  output$hmo_address <- address
  return(output)
}

create_hmo_geo_df <- function(df, postcode_field_name){
  
  # Loops through all the endpoints, fetches the data, creates a df for each postcode then 
  # stores all dfs in a list
  
  df_lists <- list()
  for (i in 1:nrow(df)) {
    try(df_lists[[df[[postcode_field_name]][i]]] <- create_wide_geo_df(df[[postcode_field_name]][i])
        , silent = T)
  }
  
  # Combines all dfs into one single large df
  # Remove all rows where there is no geolocation data available
  output <- do.call(rbind, c(df_lists, make.row.names = F)) %>%
    select(hmo_address, admin_ward, longitude, latitude) %>%
    filter(!is.na(longitude))

  # Convert lat and long from character strings to numeric data
  output$longitude <- as.numeric(output$longitude)
  output$latitude <- as.numeric(output$latitude)
  
  return(output)
}

convert_km_to_miles <- function(distance){
  output <- round(distance/1.609, 2)
  return(output)
}

current_date <- function(){
  output <- as.character(Sys.time()) %>%
    substr(1, 10) %>%
    gsub("-", "", x = .)
  return(output)
}

assign_nearest_stations <- function(geo_df,
                                    locations_df,
                                    geo_df_col_names = c("longitude", "latitude"),
                                    locations_df_col_names = c("longitude", "latitude")){
  
  for (i in 1:length(geo_df_col_names)){
    geo_df[[geo_df_col_names[i]]] <- as.numeric(geo_df[[geo_df_col_names[i]]])
  }
    
  # Promote the input dfs to SpatialPointsDataFrames
  coordinates(geo_df) <- geo_df_col_names
  coordinates(locations_df) <- locations_df_col_names
  
  #  Define vectors used in the loop
  closestSiteVec <- vector(mode = "numeric", length = nrow(geo_df))
  minDistVec     <- vector(mode = "numeric", length = nrow(geo_df))
  
  # For each address in the hmo register, measure the distance 
  # to all train/tube stations in London. Stores the distance to the 
  # closest station and its index in separate vectors
  for (i in 1 : nrow(geo_df)){
    distVec <- spDistsN1(locations_df, geo_df[i, ],longlat = TRUE)
    minDistVec[i] <- min(distVec)
    closestSiteVec[i] <- which.min(distVec)
  }
  
  nearest_station <- as(locations_df[["station"]][closestSiteVec],"character")
  
  geo_df <- as_tibble(geo_df)
  
  final_df <- tibble(geo_df, closestSiteVec, minDistVec, nearest_station)
  
  final_df <- data.frame(final_df$geo_df,
                         closestSiteVec,
                         minDistVec,
                         nearest_station,
                         stringsAsFactors = F)
  final_df$minDistVec <- sapply(final_df$minDistVec, convert_km_to_miles)
  
  return(final_df)
}

create_geo_mapped_df <- function(df, postcode_field_name){
  a_df <- assign_nearest_stations(create_hmo_geo_df(df, postcode_field_name)
                          , london_stations)
  
  a_df[['distance_in_miles']] <- sapply(a_df[['minDistVec']],convert_km_to_miles, USE.NAMES = F )
  
  output <- left_join(a_df, df, by = c("hmo_address" = postcode_field_name)) %>%
    distinct(.keep_all = T)
  
return(output)
  }
