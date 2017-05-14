#!/usr/bin/R

#data <- read.csv("data.csv", header=TRUE)

par(ps = 12, cex = 1, cex.main = 1)
all = list.files(pattern="*.csv")
par(mfrow=c(4,4))
for (i in all) {
    data = read.csv(i, header=TRUE)

    print(data$mean_recov)

    plot(data$mean_vir, type = "l",col='red', xlab='',ylab='')# xlab = 'temps [sec]', ylab= 'mean value')
    lines(data$mean_trans, type = "l",col='blue')
    lines(data$mean_recov, type = "l",col='green')
    lines(data$healthies/100, type = "l", col="black")
    #legend(0,0.2, legend = c("virulence", "transmission","guerison"), lty=c(1,1), col=c("red","blue", "green"))
    title(paste('Inf',substr(i, 14, 16), 'Rand', substr(i, 24,26), 'Rep', substr(i, 34,36), sep=' '))
}
