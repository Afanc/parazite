#!/usr/bin/R

data <- read.csv("data.csv", header=TRUE)
head(data)

plot(data$virulence, type = "l",col='red')
lines(data$transmission, type = "l",col='blue')
lines(data$guerison, type = "l",col='green')
legend(0,0.1, legend = c("virulence", "transmission","guerison"), lty=c(1,1), col=c("red","blue", "green"))


