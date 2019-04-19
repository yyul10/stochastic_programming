
load("elecequip.rda")
install.packages("tseries")
install.packages("forecast")
library("tseries")
library("forecast")

k<-0
k<-k+1
i=2001
j=1
x<-ts(elecequip,frequency=12, start=c(1996,1),end=c(i,j))
x_de<-stl(x, "periodic")
x1<-x-x_de$time.series[,2]
fit<-auto.arima(x1)
x_pred<-forecast(fit,5, level = 90)
x_real<-x_pred$mean+x_de$time.series[60+k,2]
write(x_real,file="out_mean.csv",append=TRUE,sep=",")
write(x-x_de$time.series[,2]-x_pred$fitted,file="out_error.csv",ncolumns=1,sep=",")

k=0
for(i in 2001:2010){
  for (j in 1:12)
  {
    k<-k+1
    x<-ts(elecequip,frequency=12, start=c(1996,1),end=c(i,j))
    x_de<-stl(x, "periodic")
    x1<-x-x_de$time.series[,2]
    fit<-auto.arima(x1)
    x_pred<-forecast(fit,5, level = 90)
    x_real<-x_pred$mean+x_de$time.series[60+k,2]
    write(x_real,file="out_mean.csv",append=TRUE,sep=",")
    write(x-x_de$time.series[,2]-x_pred$fitted,file="out_error.csv",ncolumns=1,sep=",")
  }
}


