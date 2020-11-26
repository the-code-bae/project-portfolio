# library(tabulizer)
library(dplyr)

file <- "/Users/makaibe/Dropbox/Property/Property/HMO Registers/Waltham Forest HMO Register/20201126 HMO Public Register 16.11.2020(1).pdf"
file_csv <- "/Users/makaibe/Dropbox/My Mac (Nwamakas-MacBook-Pro.local)/Documents/gh-repos/project-portfolio/waltham-forest-registers/20201126 hmo reg.csv"

df <- read.csv(file_csv)

names(df) <- names(df) %>% 
                tolower() %>% 
                gsub("[.]", "_", .)
