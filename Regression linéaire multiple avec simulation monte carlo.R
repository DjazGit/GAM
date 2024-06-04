#Open Visualization covid 19 in Algiers....R_script to find the data 
#Calculate  The Re_estimate in file : Nombre de reproduction effectifs (R)
#get the variables
x1 <- data_Alger$AQI_predict # independent variable 1
x2 <- data_Alger$PM2.5_predict# independent variable 2
y <- data_Alger$Re_estimate # dependent variable 


# run the Original model
model <- lm(y ~ x1 + x2)
summary_original <- summary(model)

# the Monte Carlo simulation
n_sims <- 10000
coefficients <- matrix(0, n_sims, 3)  # to store the coefficients
rsquared <- numeric(n_sims)  # to store the R-squared values

for (i in 1:n_sims) {
  #confidence interval
  random_R <- quantile(data_Alger$Re_estimate, c(0.025, 0.975)) 
  
  # Utiliser la valeur DE R tirée au hasard dans l'intervalle pour ajuster le modèle de régression
  y_sim <- runif(1, min = random_R[1], max = random_R[2]) * x1 + runif(1, min = random_R[1], max = random_R[2]) * x2 + rnorm(length(y))  # Modifiez selon votre modèle
  model_sim <- lm(y_sim ~ x1 + x2)
  
  # Stocker les coefficients
  coefficients[i, ] <- coef(model_sim)
  
  # Stocker le R-squared value
  rsquared[i] <- summary(model_sim)$r.squared
}

# Calculate summary statistics for coefficients and R-squared values
summary_coefficients <- apply(coefficients, 2, function(x) c(Mean = mean(x), SD = sd(x), Q25 = quantile(x, 0.25), Median = median(x), Q75 = quantile(x, 0.75)))
summary_rsquared <- c(Mean = mean(rsquared), SD = sd(rsquared), Q25 = quantile(rsquared, 0.25), Median = median(rsquared), Q75 = quantile(rsquared, 0.75))

# Create a combined summary
combined_summary <- list(
  Original_Model_Summary = summary_original,
  Monte_Carlo_Coefficients = summary_coefficients,
  Monte_Carlo_Rsquared = summary_rsquared
)

# Print the combined summary
print(combined_summary)

########################################################
############# check the model ##########################
# Calcul des résidus
residuals <- residuals(model_sim)

# Création d'un histogramme des résidus
hist(residuals, main = "Distribution des Résidus du modèle linéaire simple avec simulation Monte-Carlo", xlab = "Résidus", col = "skyblue", border = "black")



# Tracer les résidus par rapport aux valeurs prédites pour évaluer l'homoscédasticité
plot(model$fitted.values, residuals, main = "Homoscédasticité des Résidus du modèle linéaire simple avec simulation Monte-Carlo", xlab = "Valeurs Prédites", ylab = "Résidus", col = "steelblue")
abline(h = 0, col = "red")  # Ajouter une ligne horizontale à y = 0 pour référence
