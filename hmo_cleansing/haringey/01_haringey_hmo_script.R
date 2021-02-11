# Haringey HMO PDF Parsing Script 

# ---- Load packages and functions ----

source("~/Documents/gh-repos/project-portfolio/hmo_cleansing/mapping/hmo_geospatial_analysis_functions.r")

library(pdftools)
#Download hmo register from weblink
# download.file("https://www.haringey.gov.uk/sites/haringeygovuk/files/hmo_licensing_-_register_of_licensed_hmos_12_october_2017.pdf","hmo_file_oct2017.pdf", mode = "wb")

hmo     <- pdf_text("~/Documents/gh-repos/project-portfolio/haringey-hmo-register/hmo_file_oct2017.pdf")
hmo_df  <- data.frame(hmo, stringsAsFactors = F)

fields  <- c(  "HMO Address"
             , "Licence Holder"
             , "Issue Date"
             , "Duration of Licence"
             , "Floors", "Rooms - Living Accommodation"
             , "Rooms - Sleeping Accommodation"
             , "No. of Self Contained Units"
             , "No. of Non Self Contained Units"
             , "Shared Amenities"
             , "No. of Shared Bathrooms and Showers"
             , "No. of Shared Toilets and Wash"
             , "No. of Shared Kitchens"
             , "No. of Sinks"
             , "Maximum number of occupiers"
             , "Haringey Council - Register of Licensed HMOs")

extract_hmo_data <- function(text, first, second){
  # Locates the data for a given field name based on the field and the field after it.
  #
  # Args:
  #   text:   The string of information.
  #   first:  The name of the field you want to extract.
  #   second: The field immediately after the 'first' field.
  #
  # Returns:
  #   Information you want.
  #
  start <- str_locate(text, first)[,"end"]
  start <- start + 2
  end <- str_locate(text, second)[,"start"]
  end <- end - 2
  output <- str_sub(text, start,end)
  output <- str_trim(output, side = c("both"))
  return(output)
} 

hmo_data_vector <- function(text){
  # Loops over all the fields to pull out all data and create a vector.
  #
  # Args:
  #   text:   The string of information.
  #
  # Returns:
  #   Information you want.
  #
  output_vec <- vector(mode = "character")
  for (i in 1:(NROW(fields)-1)){
    result <- extract_hmo_data(text, fields[i], fields[i+1])
    output_vec[i] <- result
  }
  return(output_vec)
}

for (j in 1:nrow(hmo_df)){
  # This loops through all the rows, extracting all the data and placing them into their columns.
  
                            hmo_df$hmo_address[j] <- hmo_data_vector(hmo_df$hmo[j])[1]
                            hmo_df$licence_holder[j] <- hmo_data_vector(hmo_df$hmo[j])[2]
                            hmo_df$issue_date[j] <- hmo_data_vector(hmo_df$hmo[j])[3]
                            hmo_df$duration_licence[j] <- hmo_data_vector(hmo_df$hmo[j])[4]
                            hmo_df$floors[j] <- hmo_data_vector(hmo_df$hmo[j])[5]
                            hmo_df$rooms_living_accomm[j] <- hmo_data_vector(hmo_df$hmo[j])[6]
                            hmo_df$rooms_sleeping_accomm[j] <- hmo_data_vector(hmo_df$hmo[j])[7]
                            hmo_df$self_contained[j] <- hmo_data_vector(hmo_df$hmo[j])[8]
                            hmo_df$non_self_contained[j] <- hmo_data_vector(hmo_df$hmo[j])[9]
                            hmo_df$shared_amenities[j] <- hmo_data_vector(hmo_df$hmo[j])[10]
                            hmo_df$shared_bathrooms[j] <- hmo_data_vector(hmo_df$hmo[j])[11]
                            hmo_df$shared_toilets[j] <- hmo_data_vector(hmo_df$hmo[j])[12]
                            hmo_df$shared_kitchens[j] <- hmo_data_vector(hmo_df$hmo[j])[13]
                            hmo_df$sinks[j] <- hmo_data_vector(hmo_df$hmo[j])[14]
                            hmo_df$maximum_occupiers[j] <- hmo_data_vector(hmo_df$hmo[j])[15]
                          }

# Removes all rows where there is no address + remove dupes
hmo_df <- hmo_df %>%
  filter(!is.na(hmo_df$hmo_address)) %>%
  distinct(hmo_address, .keep_all = T)

# Changes all NA values to 0
hmo_df[is.na(hmo_df)] <- 0

# Convert the 'Issue_Date' column to a date type
hmo_df$issue_date <- as.Date(hmo_df$issue_date, format = "%d/%m/%y")

# Joins the new geocoded data onto the hmo_df
haringey_geo_df <- create_hmo_geo_df(hmo_df, "hmo_address") %>%
  inner_join(hmo_df, by = c("hmo_address" = "hmo_address")) %>%
  assign_nearest_stations(london_stations)

haringey_geo_df %>%
    select(   hmo_address
            , licence_holder
            , issue_date
            , duration_licence
            , floors
            , rooms_living_accomm
            , rooms_sleeping_accomm
            , self_contained
            , non_self_contained
            , shared_amenities
            , shared_bathrooms
            , shared_toilets
            , shared_kitchens
            , sinks
            , maximum_occupiers
            , nearest_station) %>%
  write.csv( paste0( "~/Documents/gh-repos/project-portfolio/haringey-hmo-register/haringey_hmo_reg_full_"
            , current_date()
    , ".csv"), row.names = F)

