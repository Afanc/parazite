#!/usr/bin/R

#data <- read.csv("data.csv", header=TRUE)

all = list.files(pattern="*.csv")
for (i in all) {
    data = read.csv(i, header=TRUE)

    print(data$mean_recov)

    plot(data$mean_vir, type = "l",col='red', xlab = 'temps [sec]', ylab= 'mean value')
    lines(data$mean_trans, type = "l",col='blue')
    lines(data$mean_recov, type = "l",col='green')
    legend(0,0.2, legend = c("virulence", "transmission","guerison"), lty=c(1,1), col=c("red","blue", "green"))
}
