masterecon <- read.csv('masterecon.csv') #loading the integrated dataset into memory
nonzeroecon <- masterecon[which(masterecon$Number.of.crimes>0),]#removing blocks with zero crime
traffecon <- nonzeroecon[which(nonzeroecon$Avearge.traffic.volume.count>0),]#removing rows with zero traffic
nondomestic <- traffecon$Number.of.crimes- traffecon$Domestic.Crimes #considering only nondomestic crimes
plot(traffecon$Avearge.traffic.volume.count,nondomestic)#crimes vs traffic
plot(traffecon$Nearest.affordable.housing,nondomestic)#crimes vs distance from affordable housing
plot(traffecon$Nearest.Police.Station,nondomestic)#crimes vs distance from nearest police station
plot(1/traffecon$Nearest.Police.Station,nondomestic)#crimes vs inverse distance from police station
econprob <- traffecon$Number.of.crimes/traffecon$Avearge.traffic.volume.count#chance that a random person suffers
econArrestRatio <- traffecon$Arrests.Made/traffecon$Number.of.crimes#ratio of criminals arrested
econproportion <- traffecon$Number.of.crimes/sum(traffecon$Number.of.crimes)#what proportion of all crimes in a block
Proportion <- scale(econproportion)#scaling
Proportion<-Proportion-min(Proportion)#adding a positive constant to make it non-negative
Probability <- scale(econprob)#scaling
Probability <- Probability - min(Probability)#making nonnegative
ArrestRatio <- scale(econArrestRatio)
ArrestRatio <- ArrestRatio- min(ArrestRatio)
ArrestRatio <- ArrestRatio*10#bringing it to same order of magnitude
PayOff <- ArrestRatio+Probability+Proportion
plot(traffecon$Avearge.traffic.volume.count,PayOff)
DistPolice <- scale(traffecon$Nearest.Police.Station)
DistPolice <- DistPolice- min(DistPolice)
AverageTraffic <- scale(traffecon$Avearge.traffic.volume.count)
AverageTraffic <- AverageTraffic- min(AverageTraffic)
DistHousing <- scale(traffecon$Nearest.affordable.housing)
DistHousing <- DistHousing- min(DistHousing)
InversePolice <- scale(1/traffecon$Nearest.Police.Station)
NewData <- data.frame(PayOff, DistHousing, AverageTraffic, traffecon$Nearest.Police.Station)
NewData <- NewData[(which(NewData$traffecon.Nearest.Police.Station>0)),]
InversePolice <- scale(1/NewData$traffecon.Nearest.Police.Station)
InversePolice <- InversePolice - min(InversePolice)
NewData <- cbind(NewData,InversePolice)
NewData$DistHousing <- NewData$DistHousing/3
Predictor <- NewData$DistHousing+NewData$AverageTraffic+NewData$InversePolice
PayOff <- NewData$PayOff
plot(Predictor,PayOff)
percentile<-length(which(PayOff>0.01))/length(PayOff)#finding how many values are greater than 0.1
Ppred7<-length(which(PayOff>0.01&Predictor<4))/length(which(PayOff>0.01))#probability of high payoff given low predictor
AverageTraffic <- NewData$AverageTraffic
DistHousing <- NewData$DistHousing
InversePolice <- NewData$InversePolice
#Function for Naive Bayes
Bayes <- function(PayoffThreshold,HouseThreshold,PoliceThreshold,TrafficThreshold){
  PHighPayoff <- length(which(PayOff>PayoffThreshold))/length(PayOff)
  PlowTraff <- length(which(AverageTraffic<TrafficThreshold))/length(AverageTraffic)
  PlowHousing <- length((which(DistHousing>HouseThreshold)))/length(DistHousing)
  PlowInvPolice <- length(which(InversePolice<PoliceThreshold))/length(InversePolice)
  PlowHousing <- length((which(DistHousing<HouseThreshold)))/length(DistHousing)
  lowTraffcond <- length(which(PayOff>PayoffThreshold&AverageTraffic<TrafficThreshold))/length(PayOff)
  lowHousecond <- length(which(PayOff>PayoffThreshold&DistHousing<HouseThreshold))/length(PayOff)
  lowinvpolcond <- length(which(PayOff>PayoffThreshold&InversePolice<PoliceThreshold))/length(PayOff)
  Px <- length(which(DistHousing<HouseThreshold&InversePolice<PoliceThreshold&AverageTraffic<TrafficThreshold))/length(PayOff)
  BayesProb <- lowHousecond*lowinvpolcond*lowTraffcond*PHighPayoff*PHighPayoff*PHighPayoff/Px
  PLowPayoff <- length(which(PayOff<=PayoffThreshold))/length(PayOff)
  lowTraffcond2 <- length(which(PayOff<PayoffThreshold&AverageTraffic<TrafficThreshold))/length(PayOff)
  lowTraffcond2 <- length(which(PayOff<=PayoffThreshold&AverageTraffic<TrafficThreshold))/length(PayOff)
  lowHousecond2 <- length(which(PayOff<=PayoffThreshold&DistHousing<HouseThreshold))/length(PayOff)
  lowinvpolcond2 <- length(which(PayOff<=PayoffThreshold&InversePolice<PoliceThreshold))/length(PayOff)
  BayesProblow <- lowHousecond*lowinvpolcond*lowTraffcond*PLowPayoff*PLowPayoff*PLowPayoff/Px
  return(c(BayesProb,BayesProblow))
}
NewData$Predictor <- Predictor
NewData$NewInversePolice <- NewData$InversePolice-NewData$Predictor+4
NewData$NewInversePolice[which(NewData$NewInversePolice<0)]=NewData$InversePolice[which(NewData$NewInversePolice<0)]#negative values in new inverse PD occur only at the places which already had Predictor greater than 4, so we don't need to increase it
sd1 <- sd(1/NewData$traffecon.Nearest.Police.Station)
mu1 <- mean((1/NewData$traffecon.Nearest.Police.Station))
NewData$allposunscale <- NewData$NewPoliceDistance*sd1 + mu1
NewData$unscale <- NewData$allposunscale+min((1/NewData$traffecon.Nearest.Police.Station))
NewData$NewPoliceDistance<-1/NewData$unscale