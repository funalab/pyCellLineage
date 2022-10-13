# Author: Masahiro Itabashi
library(here)
library(GPfit)
library(lhs)


GPRFitter <- function(atp,d){
  GPRes <- try(GP_fit(matrix(atp$time, ncol = 1) / max(atp$time), matrix(atp$atp, ncol = 1)/max(atp$atp),control = c(200 * d, 80 * d, 2 * d),maxit = 10000))
  if (class(GPRes) != "try-error"){
      return(GPRes)
  }
  return(NULL)
}

GPR <- function(baseDir, timePoints,thr=4,mode=NULL){

tmp <- read.csv(paste(baseDir, 0, '.csv', sep=''))
#endTime = max(tmp$time)
endTime = timePoints
d=30

numOfCells = length(dir(baseDir))

# atpMat <- matrix(0, nrow = numOfCells, ncol = timePoints)
atpMat <- matrix(NA, nrow = numOfCells + 1, ncol = max(tmp$time) + 1)
atpMat[1, ] = endTime * seq(0, 1, 1 / max(tmp$time))

missed = 0
for(i in 0:(numOfCells - 1)){
  print(paste('processing nr.', i))
  atp <- read.csv(paste(baseDir, i, '.csv', sep=''),header=TRUE)
  GPRes = 1
  while (!is.null(GPRes)) {
    GPRes <- GPRFitter(atp,d)
    GPRes2 = NULL
    if (is.null(GPRes)){
      missed = missed + 1
    }
    else if(GPRes$beta > thr){
      if(!is.null(mode) && mode == 'loop'){
        meanATP = mean(atp$atp)
        ATPlist = atp$atp
        absDiffATP = ATPlist[head(order(abs(ATPlist - meanATP), decreasing = TRUE), 1)]
        atp<-subset(atp,atp!=absDiffATP)
      }
      else{
        missed = missed + 1        
        GPRes2 <- try(predict(GPRes, seq(0, 1, 1 / max(tmp$time))))
        if (class(GPRes2) != "try-error"){
          plot(GPRes)
          print(GPRes$beta)
        }
        break
      }
    }
    else{
      GPRes2 <- try(predict(GPRes, seq(0, 1, 1 / max(tmp$time))))
      if (class(GPRes2) != "try-error"){
        plot(GPRes)
        print(GPRes$beta)
      }
      break
    }
  }
  if (!is.null(GPRes)){
    if (max(GPRes2$Y_hat)>1){
      print(max(GPRes2$Y_hat))
    }

    atpMat[i + 2 - missed,] <- GPRes2$Y_hat * max(atp$atp)           
  }
}
return(atpMat[complete.cases(atpMat * 0), , drop=FALSE])
}

# Sample Root Directory
 WorkingDirectory <- here()
 split_path <- function(x) if (dirname(x)==x) x else c(basename(x),split_path(dirname(x)))
 splitDir <- split_path(WorkingDirectory)
 i = match('pyCellLineage',splitDir)
 dirs <- c(rev(splitDir[c(i:length(splitDir))]),'Data')
 dirs <- dirs[2:length(dirs)]
 path = ''
 for (basename in dirs){ path <- file.path(path,basename)}
 rootDir <- path

# Sample Paths
 sample_poor1 = paste(rootDir,"glc_poor/sample1/",sep="")
 sample_poor2 = paste(rootDir,"glc_poor/sample3/",sep="")
 sample_poor3 = paste(rootDir,"glc_poor/sample2/",sep="")
 sample_rich1 = paste(rootDir,"glc_rich/sample1/",sep="")
 sample_rich2 = paste(rootDir,"glc_rich/sample2/",sep="")
 sample_rich3 = paste(rootDir,"glc_rich/sample3/",sep="")

# Sample
   samples <- list(sample_poor3,sample_poor2,
                   sample_rich1,sample_rich2,sample_rich3,sample_poor1)

sampleGPRFit <-function(samples){
  for (smp in samples){
    exp = paste(smp,"ATP_IndiCell/",sep="")
    tmp <- read.csv(paste(exp,"0.csv",sep=""))
    saveDir = paste(smp,"gprRes.csv",sep="")
    write.csv(GPR(exp,nrow(tmp)),saveDir)
  }
}

sampleGPRFit(samples)
