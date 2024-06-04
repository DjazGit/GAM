library(openxlsx)
library(readr)
library(dplyr)
library(lubridate)
library(rmweather)
library(Metrics)
library(ranger)
library(outliers)
library(base)


############## AQI DATA #######################################################
combined_data = read.csv("C:\\Users\\HONOR-ECC\\Downloads\\Air Pollution and Covid 19\\combined_data.csv")

combined_data$date <- as.POSIXct(combined_data$date)

# Keep things reproducible
set.seed(1234)
# Prepare the data
prepared_data <- combined_data %>%
  rmw_prepare_data(
    value ="AQI",
    na.rm = FALSE, 
    replace = FALSE,
    fraction = 0.8
  )

# Remove rows with missing values
prepared_data <- na.omit(prepared_data)


# Example: Grubbs' test for detecting outliers
outlier_test_result <- grubbs.test(prepared_data$value)
outlier_test_result
# Assuming "value" is the name of your variable
prepared_data <- prepared_data[prepared_data$value != -999, ]

# run the model 
model <- rmw_train_model(
  prepared_data,
  variables = c(
    "WD10M", "WS10M", "WS2M", "WD2M" ,"T2M","RH2M"  ,"PRC","PS", 
    "date_unix", "day_julian", "weekday", "hour"
  ),
  n_trees = 500
)

# Evaluate the model performances

test_pred <- rmw_predict_the_test_set(model, prepared_data)



pred_plot <- rmw_predict_the_test_set(model, prepared_data) %>% 
  rmw_plot_test_prediction()

pred_plot <- pred_plot + 
  ggtitle("Prédictions AQI")

print(pred_plot)


test_rmse <- rmsle(test_pred$value, test_pred$value_predict)



# Normalize the data 
data_norm_AQI = rmw_normalise(model, prepared_data)
P = rmw_plot_normalised(data_norm_AQI, colour = "#6B180EFF")
P <- P + ggtitle("AQI")
print(P)



data_norm_AQI$date <- as.Date(data_norm_AQI$date, format = "%Y-%m-%d")
write_csv(data_norm_AQI, path = "C:\\Users\\HONOR-ECC\\Downloads\\Air Pollution and Covid 19\\data_norm_AQI.csv")
library(readr)

# Calculate partial dependencies for all independent variables used in model

data_partial <- rmw_partial_dependencies(
  model = model,
  df = prepared_data,
  variable = NA,
  verbose = TRUE
)

View(data_partial)




############## PM2.5 DATA #######################################################
combined_data = read.csv("C:\\Users\\HONOR-ECC\\Downloads\\Air Pollution and Covid 19\\combined_data.csv")

combined_data$date <- as.POSIXct(combined_data$date)

# Keep things reproducible
set.seed(1234)
# Prepare the data
prepared_data <- combined_data %>%
  rmw_prepare_data(
    value ="PM2.5",
    na.rm = FALSE, 
    replace = FALSE,
    fraction = 0.8
  )

# Remove rows with missing values
prepared_data <- na.omit(prepared_data)


# Example: Grubbs' test for detecting outliers
outlier_test_result <- grubbs.test(prepared_data$value)
outlier_test_result
# Assuming "value" is the name of your variable
prepared_data <- prepared_data[prepared_data$value != -179, ]

# run the model 
model <- rmw_train_model(
  prepared_data,
  variables = c(
    "WD10M", "WS10M", "WS2M", "WD2M" ,"T2M","RH2M"  ,"PRC","PS", 
    "date_unix", "day_julian", "weekday", "hour"
  ),
  n_trees = 500
)

# Evaluate the model performances

test_pred <- rmw_predict_the_test_set(model, prepared_data)



pred_plot <- rmw_predict_the_test_set(model, prepared_data) %>% 
  rmw_plot_test_prediction()

pred_plot <- pred_plot + 
  ggtitle("Prédictions PM2.5")

print(pred_plot)


test_rmse <- rmsle(test_pred$value, test_pred$value_predict)



# Normalize the data 
data_norm_AQI = rmw_normalise(model, prepared_data)
P = rmw_plot_normalised(data_norm_AQI, colour = "#6B180EFF")
P <- P + ggtitle("PM2.5")
print(P)



data_norm_AQI$date <- as.Date(data_norm_AQI$date, format = "%Y-%m-%d")
write_csv(data_norm_PM2.5, path = "C:\\Users\\HONOR-ECC\\Downloads\\Air Pollution and Covid 19\\data_norm_PM2.5.csv")
library(readr)

# Calculate partial dependencies for all independent variables used in model

data_partial <- rmw_partial_dependencies(
  model = model,
  df = prepared_data,
  variable = NA,
  verbose = TRUE
)

View(data_partial)



