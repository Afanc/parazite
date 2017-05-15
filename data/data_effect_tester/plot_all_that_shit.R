#!/usr/bin/R

#data <- read.csv("data.csv", header=TRUE)

par(ps = 12, cex = 1, cex.main = 1)
all = list.files(pattern="*.csv")
vec = NULL
for (i in all) {
    data = read.csv(i, header=TRUE)

    x = substr(i, 1,3)
    y = tail(data, 1)
    #y = data[40,]

    vec <- rbind(vec, c(x,y[2]))

}
print(vec)

plot(vec, type = "l",col='red', xlab='Number of secondary infections',ylab='effect')
title('blabla')

