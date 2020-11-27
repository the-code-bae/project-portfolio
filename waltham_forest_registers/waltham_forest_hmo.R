library(tidyverse)

file_csv <- "~/Documents/gh-repos/project-portfolio/waltham_forest_registers/20201126_hmo_reg.csv"

df <- read_csv(file_csv)

names(df) <- names(df) %>% 
                tolower() %>% 
                gsub(" ", "_", .)
