data(AirPassengers)

# Exploring data is the first step to know whether a series is stationary or not.
AirPassengers
frequency(AirPassengers)
summary(AirPassengers)
plot((AirPassengers))
plot(log(AirPassengers))
# trend estimation using linear regression
reg=lm(log(AirPassengers)~time(AirPassengers))
abline(reg)

# seasonal effect
cycle(AirPassengers)
boxplot(AirPassengers ~cycle(AirPassengers))
boxplot((log(AirPassengers))~cycle(AirPassengers))
boxplot((log(AirPassengers)-reg$fit)~cycle(AirPassengers))


######################################################
# The year on year trend clearly shows that the 
# passengers have been increasing.

######################################################
# The variances of monthly amounts are significantly reduced 
# after taking the logirithm and subtracting the annual trend. 

######################################################
# The mean value in July and August is much higher than 
# the regular months, and the mean value in November and December 
# is much lower than the regular months.


# ARMA model
#install.packages("tseries")
library('tseries')

# stationarity using differencing 
plot(diff(log(AirPassengers)))
plot(diff(log(AirPassengers),lag =12,differences =1))
air_diff=diff(diff(log(AirPassengers),lag =12), differences =1)
plot(air_diff)

# Augmented Dickey-Fuller Test for stationarity
adf.test(air_diff, alternative="stationary", k=0)

# use sample acf function and sample pacf function to estimate the orders of ARMA model
acf(air_diff, 50)
pacf(air_diff, 50)

# acf and pacf plots suggest the residuals after logrithm 
# could be ARIMA(0,1,1)(0,1,1) OR ARIMA(1,1,1)(0,1,1) OR ARIMA(0,1,1)(1,1,1) OR ARIMA(0,1,1)(0,1,1)

# use BIC and AIC criterion to choose the model
ARIMA1 = arima(log(AirPassengers), c(0, 1, 1),seasonal = list(order = c(0, 1, 1), period = 12))
ARIMA2 = arima(log(AirPassengers), c(1, 1, 1),seasonal = list(order = c(0, 1, 1), period = 12))
ARIMA3 = arima(log(AirPassengers), c(1, 0, 1),seasonal = list(order = c(0, 1, 1), period = 12))
ARIMA4 = arima(log(AirPassengers), c(0, 1, 1),seasonal = list(order = c(1, 1, 1), period = 12))
bic = c(BIC(ARIMA1),BIC(ARIMA2),BIC(ARIMA3), BIC(ARIMA4))
aic = c(AIC(ARIMA1),AIC(ARIMA2),AIC(ARIMA3), AIC(ARIMA4))

# Auto ARIMA model choice
#install.packages("forecast")
library("forecast")
auto.arima(log(AirPassengers))

# Prediction 
pred <- predict(ARIMA1, n.ahead = 10*12)
ts.plot(log(AirPassengers),pred$pred, lty = c(1,3),col =c(1,2))
# Another method for forecasting
fore1 <- forecast(ARIMA1, h = 10*12,level = 10)
fore2 <- forecast(ARIMA1, h = 10*12,level = 80)
plot(fore1)
plot(fore2)

# use stl decomposition method

stl_air = stl(log(AirPassengers), "periodic")
plot(stl_air)
#summary(stl_air)

str(stl_air$time.series)
adf.test(stl_air$time.series[,3], alternative="stationary", k=0)

# forecasting 
plot(forecast(stl_air, method="arima",h = 10*12, level = c(80, 95) ))
#plot(forecast(stl_air, method="ets",h = 10*12, level = c(80, 95) ))
