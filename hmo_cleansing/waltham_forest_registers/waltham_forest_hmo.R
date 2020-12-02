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

wf_geo_df$nearest_station <- trimws(wf_geo_df$nearest_station)

wf_geo_df %>% 
  group_by(nearest_station) %>% 
  summarise(n = n()) %>% 
  arrange(desc(n))

stations_to_keep <-  c("Wood Street", "Walthamstow Central", "St James Street")

write.csv(wf_geo_df[wf_geo_df$nearest_station %in% stations_to_keep,]
          , "~/Documents/gh-repos/project-portfolio/waltham_forest_registers/20201127_hmo_reg_geo_mapped.csv"
          , row.names = F )

