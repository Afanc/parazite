#!/usr/bin/R

data <- read.csv("data.csv", header=TRUE)
head(data)
args=(commandArgs(TRUE))

if(length(args)!=1)
{
    print("Not enough/too many arguments supplied. Please supply d = filename")
        q()
}else
{
    for(i in 1:length(args)){
        eval(parse(text=args[[i]]))
    }
}

png(d)
plot(data$virulence, type = "l",col='red', xlab = 'temps [sec]', ylab= 'mean value')
lines(data$transmission, type = "l",col='blue')
lines(data$guerison, type = "l",col='green')
legend(0,0.2, legend = c("virulence", "transmission","guerison"), lty=c(1,1), col=c("red","blue", "green"))

