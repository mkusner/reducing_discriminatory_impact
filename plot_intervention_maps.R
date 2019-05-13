library(ggplot2)
library(ggmap)

int_data <- read.csv("final_data_interventions_max_frac_results.csv",
                         strip.white = TRUE,
                         header = TRUE,
                         stringsAsFactors = FALSE)
#> names(int_data)
#[1] "AP.IB"         "Calculus"      "Counselors"    "FracSAT.ACT"   "black"         "Hispanic"     
#[7] "white"         "lat"           "long"          "gis_x"         "gis_y"         "neigh1"       
#[13] "neigh2"        "neigh3"        "neigh4"        "neigh5"        "int_unfair"    "int_max_fair1"
#[19] "int_max_fair2"

int_data$race <- int_data$black
int_data$race[int_data$black == 1] = "black"
int_data$race[int_data$Hispanic == 1] = "Hispanic"
int_data$race[int_data$white == 1] = "white"


# separate so can color differently
unfair_int <- int_data
unfair_int$race[unfair_int$int_unfair == 0] <- NA

fair_max_int1 <- int_data
fair_max_int1$race[fair_max_int1$int_max_fair1 == 0] <- NA

fair_max_int2 <- int_data
fair_max_int2$race[fair_max_int2$int_max_fair2 == 0] <- NA

parity <- int_data
parity$race[parity$int_parity == 0] <- NA

#############unfair_no_int <- int_data[int_data$int_unfair == 0,]
#############unfair_int    <- int_data[int_data$int_unfair == 1,]
#############
#############fair_lin_no_int <- int_data[int_data$int_lin_fair4 == 0,]
#############fair_lin_int    <- int_data[int_data$int_lin_fair4 == 1,]
#############
#############fair_max_no_int <- int_data[int_data$int_max_fair4 == 0,]
#############fair_max_int    <- int_data[int_data$int_max_fair4 == 1,]



ny_plot<-ggmap(get_map("New York, NY",zoom=11,source='google',maptype='terrain'))
#ny_plot<-ggmap(get_map("New York, NY",zoom=11,source='google',maptype='hybrid'))

# All schools
#qmplot(long, lat, data=int_data, maptype = 'toner-2011', color=race, size=I(1.5), zoom = 11, darken = .6, legend = "topleft") + 
#  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"))
qmplot(long, lat, data=int_data, maptype = 'toner-2011', color=race, size=I(4.0), zoom = 11, darken = 0, legend = "none", extent = "device", alpha=I(0.7)) + 
  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"), guide=FALSE)


# Unfair Int
#qmplot(long, lat, data=unfair_no_int, maptype = "toner-background", color=race, size=I(1.0), zoom = 11, darken = .7, legend = "topleft", alpha = I(.2)) + 
#  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"))
qmplot(long, lat, data=unfair_int, maptype = "toner-2011", color=race, size=I(4.0), zoom = 11, darken = 0, legend = "none", extent = "device", alpha=I(0.7)) + 
  scale_color_manual(values=c("#0000F5","#AF23B9"), guide=FALSE)

# Fair Lin Int
#qmplot(long, lat, data=int_data, maptype = "toner-2011", color=race, size=I(1.5), zoom = 11, darken = .6, legend = "topleft", alpha=I(0.0)) + 
#  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"))
#+
#qmplot(long, lat, data=fair_lin_int, maptype = "toner-2011", color=race, size=I(2.0), zoom = 11, darken = .2, legend = "none", extent = "device", alpha=I(0.7)) + 
#  scale_color_manual(values=c("#0000F5", "#AF23B9"), guide=FALSE)

# Fair Max Int
#qmplot(long, lat, data=fair_max_int1, maptype = "toner-2011", color=race, size=I(2.0), zoom = 11, darken = .2, alpha=I(0.7)) + 
#  scale_color_manual(values=c("#0000F5", "#AF23B9"))

qmplot(long, lat, data=fair_max_int1, maptype = "toner-2011", color=race, size=I(4.0), zoom = 11, darken = 0, legend = "none", extent = "device", alpha=I(0.7)) + 
  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"), guide=FALSE)



qmplot(long, lat, data=fair_max_int2, maptype = "toner-2011", color=race, size=I(4.0), zoom = 11, darken = 0, legend = "none", extent = "device", alpha=I(0.7)) + 
  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"), guide=FALSE)



qmplot(long, lat, data=parity, maptype = "toner-2011", color=race, size=I(4.0), zoom = 11, darken = 0, legend = "none", extent = "device", alpha=I(0.7)) + 
  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"), guide=FALSE)

########### MINORITY

int_data_min <- read.csv("final_data_interventions_max_frac_minority_results.csv",
                     strip.white = TRUE,
                     header = TRUE,
                     stringsAsFactors = FALSE)



int_data_min$race <- int_data_min$black
int_data_min$race[int_data_min$black == 1] = "black"
int_data_min$race[int_data_min$Hispanic == 1] = "Hispanic"
int_data_min$race[int_data_min$white == 1] = "white"


# separate so can color differently
just_min <- int_data_min
just_min$race[just_min$int == 0] <- NA



#############unfair_no_int <- int_data[int_data$int_unfair == 0,]
#############unfair_int    <- int_data[int_data$int_unfair == 1,]
#############
#############fair_lin_no_int <- int_data[int_data$int_lin_fair4 == 0,]
#############fair_lin_int    <- int_data[int_data$int_lin_fair4 == 1,]
#############
#############fair_max_no_int <- int_data[int_data$int_max_fair4 == 0,]
#############fair_max_int    <- int_data[int_data$int_max_fair4 == 1,]



ny_plot<-ggmap(get_map("New York, NY",zoom=11,source='google',maptype='terrain'))
#ny_plot<-ggmap(get_map("New York, NY",zoom=11,source='google',maptype='hybrid'))

# All schools
#qmplot(long, lat, data=int_data, maptype = 'toner-2011', color=race, size=I(1.5), zoom = 11, darken = .6, legend = "topleft") + 
#  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"))
qmplot(long, lat, data=int_data_min, maptype = 'toner-2011', color=race, size=I(4.0), zoom = 11, darken = 0, legend = "none", extent = "device", alpha=I(0.7)) + 
  scale_color_manual(values=c("#EA3323","#0000F5"), guide=FALSE)


# Unfair Int
#qmplot(long, lat, data=unfair_no_int, maptype = "toner-background", color=race, size=I(1.0), zoom = 11, darken = .7, legend = "topleft", alpha = I(.2)) + 
#  scale_color_manual(values=c("#EA3323", "#0000F5", "#AF23B9"))
qmplot(long, lat, data=just_min, maptype = "toner-2011", color=race, size=I(4.0), zoom = 11, darken = 0, legend = "none", extent = "device", alpha=I(0.7)) + 
  scale_color_manual(values=c("#EA3323","#0000F5"), guide=FALSE)
