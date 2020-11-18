# Haringey HMO PDF Parsing Script 

# ---- Load packages and functions ----

source("~/Dropbox/Data Science/Mapping/hmo_geospatial_analysis_functions.r")

library(pdftools)
#Download hmo register from weblink
# download.file("https://www.haringey.gov.uk/sites/haringeygovuk/files/hmo_licensing_-_register_of_licensed_hmos_12_october_2017.pdf","hmo_file_oct2017.pdf", mode = "wb")

hmo     <- pdf_text("~/Dropbox/Data Science/Haringey_hmo/hmo_file_oct2017.pdf")
hmo_df  <- data.frame(hmo, stringsAsFactors = F)

fields  <- c("HMO Address","Licence Holder", "Issue Date", "Duration of Licence",
            "Floors", "Rooms - Living Accommodation", "Rooms - Sleeping Accommodation",
            "No. of Self Contained Units","No. of Non Self Contained Units", "Shared Amenities", 
            "No. of Shared Bathrooms and Showers","No. of Shared Toilets and Wash", 
            "No. of Shared Kitchens", "No. of Sinks", "Maximum number of occupiers", 
            "Haringey Council - Register of Licensed HMOs")

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

is_digit <- function(string){
  # Remove any addresses where they don't start with a digit.
  output <- str_sub(string, 1, 1) %>%
    str_detect("[[:digit:]]")
  return(output)
}

for (j in 1:nrow(hmo_df)){
  # This loops through all the rows, extracting all the data and placing them into their columns.
  
                            hmo_df$hmo_address[j] <- hmo_data_vector(hmo_df$hmo[j])[1]
                            hmo_df$licence_holder[j] <- hmo_data_vector(hmo_df$hmo[j])[2]
                            hmo_df$issue_date[j] <- hmo_data_vector(hmo_df$hmo[j])[3]
                            hmo_df$duration_licence[j] <- hmo_data_vector(hmo_df$hmo[j])[4]
                            hmo_df$floors[j] <- hmo_data_vector(hmo_df$hmo[j])[5]
                            hmo_df$rooms_living_cccomm[j] <- hmo_data_vector(hmo_df$hmo[j])[6]
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

# Removes all rows where there is no address
# Removes duplicates
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

write.csv(haringey_geo_df, paste0("~/Dropbox/Data Science/Haringey_hmo/haringey_hmo_reg_full_",
                                  current_date(),
                                  ".csv"),
          row.names = F)

haringey_geo_df$is_digit <- sapply(haringey_geo_df$hmo_address, is_digit)

# ---- TODO Marketing Selections Script ----
# TODO Create marketing selections in a new R script using this file
# '/Users/makaibe/Dropbox/Data Science/Haringey_hmo/haringey_hmo_reg_stations'

segments_df <- haringey_geo_df %>%
  filter(rooms_living_cccomm > 4, shared_bathrooms > 1, is_digit = 1)
  
top_stations <- haringey_geo_df %>%
  group_by(nearest_station) %>%
  count(name = "num_of_properties") %>%
  arrange(desc(num_of_properties)) %>%
   filter(nearest_station != 'Northumberland Park', nearest_station != 'White Hart Lane') %>%
   head(., 4)

haringey_geo_df %>%
  filter(nearest_station %in% top_stations[["nearest_station"]])

no_bathrooms <- haringey_geo_df %>%
  filter(shared_bathrooms == 0)

#  Split address in address 1, address 2, address 3 etc for use in docmail...
segment_df <- segment_df %>% 
  separate(hmo_address, c('address_1'
                          , 'address_2'
                          , 'address_3'
                          , 'address_4'
                          , 'address_5'
                          , 'address_6')
           , sep = ","
           , extra = 'drop', fill = 'right', remove = F)

# assign each address a campaign group
segment_df$row_num <- 1:NROW(segment_df$HMO_Address)
segment_df$campaign_group <- segment_df$row_num %% 5

df_campaign0 <- segment_df[segment_df$campaign_group == 0, 3:6]
df_campaign1 <- subset(segment_df, campaign_group == 1, select = 3:6)
df_campaign2 <- subset(segment_df, campaign_group == 2, select = 3:6)
df_campaign3 <- subset(segment_df, campaign_group == 3, select = 3:6)
df_campaign4 <- subset(segment_df, campaign_group == 4, select = 3:6)

# write each df to csv
campaign_dfs <- list(campaign0 = df_campaign0, campaign1 = df_campaign1,
                     campaign2 = df_campaign2, campaign3 = df_campaign3,
                     campaign4 = df_campaign4)

# for(i in 1:length(names(campaign_dfs))){
#   write.csv(campaign_dfs[[i]], paste0(current_date(),
#                                       "_",
#                                       names(campaign_dfs)[i], "_", ".csv"),
#             row.names = F)
# }


# Harringay Green Lanes ---------------------------------------------------

harringay_green_lanes_df <- sqldf("SELECT * FROM final_df 
                      WHERE pointassignstations = 'Harringay Green Lanes'
                    ORDER BY mindistvec ASC")

harringay_green_lanes_df$Maximum_Occupiers <- as.numeric(as.character(harringay_green_lanes_df$Maximum_Occupiers))
View(harringay_green_lanes_df[harringay_green_lanes_df$Maximum_Occupiers >= 5 & !is.na(harringay_green_lanes_df$Maximum_Occupiers), ])



turnpike_lane_df <- sqldf("SELECT * FROM final_df 
                      WHERE pointassignstations = 'Turnpike Lane'
                                  ORDER BY mindistvec ASC")

harringay_df <- sqldf("SELECT * FROM final_df 
                      WHERE pointassignstations = 'Harringay'
                                  ORDER BY mindistvec ASC")

bruce_grove_df <- sqldf("SELECT * FROM final_df 
                      WHERE pointassignstations = 'Bruce Grove'
                          ORDER BY mindistvec ASC")


save.image(file = "~/Dropbox/Data Science/Haringey_hmo/haringey_hmo_data.RData")

