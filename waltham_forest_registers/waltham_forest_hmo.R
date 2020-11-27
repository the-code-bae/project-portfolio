library(tidyverse)

# Load file with geospatial mapping functions
source("~/Documents/gh-repos/project-portfolio/mapping/hmo_geospatial_analysis_functions.r")

file_csv <- "~/Documents/gh-repos/project-portfolio/waltham_forest_registers/20201126_hmo_reg.csv"

df <- read_csv(file_csv)

names(df) <- names(df) %>% 
                tolower() %>% 
                gsub(" ", "_", .)

wf_geo_df <- create_geo_mapped_df(df, "post_code") %>% 
                rename(  distance_in_km = minDistVec
                       , post_code = hmo_address ) %>% 
                select(  names(df)
                       , nearest_station
                       , distance_in_km
                       , distance_in_miles
                       )
