library(aphid)
library(foreach)
library(doParallel)
registerDoParallel(cores=20) # Change accordingly to your hardware capacity

# Functions

state_vector <- function(x){
  state_vect = c()
  for (i in 1:x){
    state_vect = c(state_vect,letters[i])
  }
  return(state_vect)
}

read_files <- function(baseDir,thr=NULL,cutoff=3,randomize=FALSE){
  tmp_list <- list()
  dir_len = length(list.files(path = baseDir,pattern = "csv"))
  if(is.null(thr)){
    filename = paste(baseDir, 0, '.csv', sep='')
    tmp <- read.csv(filename,stringsAsFactors = FALSE)
    thr = length(tmp$ATP_Class)/cutoff
  }
  for (i in 0:(dir_len-1)){
    filename = paste(baseDir, i, '.csv', sep='')
    tmp <- read.csv(filename,stringsAsFactors = FALSE)
    atpList = list(tmp$ATP_Class[thr:length(tmp$ATP_Class)])
    if(randomize){
      atpList <- list(sample(tmp$ATP_Class[thr:length(tmp$ATP_Class)]))
    }
    tmp_list <- c(tmp_list,atpList)
  }
  names(tmp_list) <- paste("e_coli",1:dir_len,sep="")
  return(tmp_list)
}

make_initHMM <- function(states,symbols){
  init_HMM = list()
  for (i in 1:length(states)) {
    init_HMM=c(init_HMM,list(symbols))
  }
  names(init_HMM) = states
  return(init_HMM)
}

create_probmatrix <- function(x,y=x){
  vect = c()
  for (i in 1:x){
    total_prob = 0
    for (j in 1:y){
      if (j == y){
        vect = c(vect,1-total_prob)
      }
      else{
        rnum <- runif(1,0,1-total_prob)
        vect = c(vect, rnum)
        total_prob = total_prob + rnum
      }
    }
  }
  prob_matrix = matrix(c(vect),nrow=y, ncol=x);
  return(t(prob_matrix))
}

initHMM <- function(residues,i){
  states=c("begin")
  states = c(states,state_vector(i))
  print(paste("Initializing State w/",i,sep=""))
  A <- create_probmatrix(i+1,i)
  A = cbind(rep(0,i+1),A)
  dimnames(A) <- list(from=states, to=states)
  E <- create_probmatrix(i,length(residues))
  dimnames(E) <- list(states = states[-1], residues = residues)
  x <- structure(list(A=A,E=E), class = "HMM")
  return(x)
}

plot_hmm <- function(hmm,just = "center",textexp = 1){
  plot.HMM(hmm,just = just,textexp = textexp)
  if (length(hmm$A) == 9){
    text(x = 0.02, y = 0.5, labels = round(hmm$A["a", "a"], 2))
    text(x = 0.51, y = 0.5, labels = round(hmm$A["b", "b"], 2))
    text(x = 0.5, y = 0.6, labels = round(hmm$A["a", "b"], 2))
    text(x = 0.5, y = 0.4, labels = round(hmm$A["b", "a"], 2))
  }
}

HMM_maxim <- function(dirname,saveDir,thr=NULL,max_states = 2,showAIC=FALSE,randomize=FALSE,randitr=4000,trainitr=4000,changes=FALSE,plot=TRUE){
  observation_list <- read_files(dirname,thr=thr)
  Count=NULL
  for(i in 2:max_states){
    residues = c("high","low")      
    hmm <- initHMM(residues,i)
    plot_hmm(hmm,just = "right",textexp = 1.5)
    trained_hmm<- train_hmm(hmm,observation_list,method = "BaumWelch",maxiter = trainitr,quiet = TRUE)
    if (showAIC){
      print("AIC:")
      print(-2*trained_hmm$LL+2*(i**2))
    }
    if (randomize && max_states == 2){
      abList = c()
      baList = c()
      parFor <- foreach (a =  1:randitr) %dopar%{
        observation_list <- read_files(dirname,thr=thr,randomize = TRUE)
        trained_Rhmm<- train_hmm(hmm,observation_list,method = "BaumWelch",maxiter=trainitr,quiet = TRUE)
        diffa = abs(trained_Rhmm$E["a","low"] - trained_Rhmm$E["a","high"])
        diffb = abs(trained_Rhmm$E["b","low"] - trained_Rhmm$E["b","high"])
        
        if(diffa > diffb){
          if(trained_Rhmm$E["a","low"]>trained_Rhmm$E["a","high"]){
            list(trained_Rhmm$A["a","b"],trained_Rhmm$A["b","a"])
          }
          else{
            list(trained_Rhmm$A["b","a"],trained_Rhmm$A["a","b"])
          }
        }
        else{
          if(trained_Rhmm$E["b","low"]>trained_Rhmm$E["b","high"]){
            list(trained_Rhmm$A["b","a"],trained_Rhmm$A["a","b"])
          }
          else{
            list(trained_Rhmm$A["a","b"],trained_Rhmm$A["b","a"])
          }
        }
      }
      transList = parFor
      for (i in 1:length(transList)){
      	  abList = c(abList,transList[[i]][[1]])
      	  baList = c(baList,transList[[i]][[2]])
      }

      write.csv(abList, file =file.path(saveDir,"abList.csv"), row.names=FALSE)
      pvalueab=length(abList[abList < trained_hmm$A["a","b"]])/length(abList)
      write.csv(trained_hmm$A["a","b"], file =file.path(saveDir,"Expab.csv"), row.names=FALSE)
      print("P.value of AB transition:")
      print(pvalueab)
      

      write.csv(baList, file =file.path(saveDir,"baList.csv"), row.names=FALSE)
      pvalueba = length(baList[baList > trained_hmm$A["b","a"]])/length(baList)
      write.csv(trained_hmm$A["b","a"], file =file.path(saveDir,"Expba.csv"), row.names=FALSE)      
      print("P.value of BA transition:")
      print(pvalueba)

      if (plot){
            hist(as.numeric(abList),main=trained_hmm$A["a","b"])
	    hist(as.numeric(baList),main=trained_hmm$A["b","a"])
      }
    }
    
    plot_hmm(trained_hmm,just = "right",textexp = 1.5)
    if(changes){
      Count = countChanges(trained_hmm,observation_list)      
    }
  }
  
  return(Count)
}

logdetect <- function(x){
  if(inherits(x, "HMM")){
    if(all(x$A <= 0) & all(x$E <= 0)){
      return(TRUE)
    } else if(all(x$A >= 0) & all(x$A <= 1) & all(x$E >= 0) & all(x$E <= 1)){
      return(FALSE)
    } else stop("unable to detect if model probabilities are in log space")
  } else if(inherits(x, "PHMM")){
    if(all(x$A <= 0) & all(x$E <= 0) & all(x$qa <= 0) & all(x$qe <= 0)){
      return(TRUE)
    } else if(all(x$A >= 0) & all(x$A <= 1) & all(x$E >= 0) & all(x$E <= 1) &
              all(x$qa >= 0) & all(x$qa <= 1) & all(x$qe >= 0) & all(x$qe <= 1)){
      return(FALSE)
    } else stop("unable to detect if model probabilities are in log space")
  } else stop("x must be an object of class 'HMM' or 'PHMM'")
}

train_hmm <- function (x, y, method = "Viterbi", seqweights = NULL, wfactor = 1, 
          maxiter = 100, deltaLL = 1e-07, logspace = "autodetect", 
          quiet = FALSE, modelend = FALSE, pseudocounts = "Laplace", 
          ...) 
{
  if (identical(logspace, "autodetect")) 
    logspace <- logdetect(x)
  if (identical(pseudocounts, "background")) 
    pseudocounts <- "Laplace"
  if (is.list(y)) {
  }
  else if (is.vector(y, mode = "character")) {
    y <- list(y)
  }
  else stop("Invalid y argument")
  n <- length(y)
  if (is.null(seqweights)) 
    seqweights <- rep(1, n)
  stopifnot(sum(seqweights) == n)
  seqweights <- seqweights * wfactor
  states <- rownames(x$A)
  nstates <- length(states)
  residues <- colnames(x$E)
  nres <- length(residues)
  model <- x
  if (!logspace) {
    model$E <- log(model$E)
    model$A <- log(model$A)
  }
  if (method == "Viterbi") {
    for (i in 1:maxiter) {
      samename <- logical(n)
      for (j in 1:n) {
        vitj <- Viterbi(model, y[[j]], logspace = TRUE, 
                        ... = ...)
        pathchar <- states[-1][vitj$path + 1]
        if (identical(pathchar, names(y[[j]]))) 
          samename[j] <- TRUE
        names(y[[j]]) <- pathchar
      }
      if (all(samename)) {
        if (!logspace) {
          model$A <- exp(model$A)
          model$E <- exp(model$E)
        }
        if (!quiet) 
          cat("Iteration", i, "\nPaths were identical after", 
              i, "iterations\n")
        return(model)
      }
      else {
        if (!quiet) 
          cat("Iteration", i, "\n")
        model <- deriveHMM(y, seqweights = seqweights, 
                           residues = residues, states = states, modelend = modelend, 
                           pseudocounts = pseudocounts, logspace = TRUE)
      }
    }
    stop("Failed to converge. Try increasing 'maxiter' or modifying start parameters")
  }
  else if (method == "BaumWelch") {
    Apseudocounts <- matrix(0, nrow = nstates, ncol = nstates)
    Epseudocounts <- matrix(0, nrow = nstates - 1, ncol = nres)
    dimnames(Apseudocounts) <- list(from = states, to = states)
    dimnames(Epseudocounts) <- list(state = states[-1], residue = residues)
    if (identical(pseudocounts, "Laplace")) {
      Apseudocounts[] <- Epseudocounts[] <- 1
      if (!modelend) 
        Apseudocounts[, 1] <- 0
    }
    else if (is.list(pseudocounts)) {
      stopifnot(length(pseudocounts) == 2)
      stopifnot(identical(dim(pseudocounts[[1]]), dim(x$A)))
      stopifnot(identical(dim(pseudocounts[[2]]), dim(x$E)))
      Apseudocounts[] <- pseudocounts[[1]]
      Epseudocounts[] <- pseudocounts[[2]]
    }
    else if (!identical(pseudocounts, "none")) 
      stop("Invalid 'pseudocounts' argument")
    E <- model$E
    A <- model$A
    LL <- -1e+12
    for (i in 1:maxiter) {
      tmpA <- Apseudocounts
      tmpE <- Epseudocounts
      tmplogPx <- rep(NA, n)
      for (j in 1:n) {
        yj <- y[[j]]
        nj <- length(yj)
        if (nj == 0) {
          tmpA[1, 1] <- tmpA[1, 1] + if (modelend) 
            seqweights[j]
          else 0
        }
        else {
          forwj <- forward(model, yj, logspace = TRUE, 
                           ... = ...)
          Rj <- forwj$array
          logPxj <- forwj$score
          tmplogPx[j] <- logPxj
          backj <- backward(model, yj, logspace = TRUE)
          Bj <- backj$array
          tmpAj <- tmpA
          tmpEj <- tmpE
          tmpAj[] <- tmpEj[] <- 0
          for (k in states[-1]) {
            tmpAj[1, -1] <- exp(A[1, -1] + E[, yj[1]] + 
                                  Bj[, 1] - logPxj)
            tmpAj[-1, 1] <- exp(Rj[, nj] + A[-1, 1] - 
                                  logPxj)
            for (l in states[-1]) {
              tmpAj[k, l] <- exp(logsum(Rj[k, -nj] + 
                                          A[k, l] + E[l, yj[-1]] + Bj[l, -1]) - 
                                   logPxj)
            }
            for (b in residues) {
              cond <- yj == b
              if (any(cond)) 
                tmpEj[k, b] <- exp(logsum(Rj[k, cond] + 
                                            Bj[k, cond]) - logPxj)
            }
          }
          tmpA <- tmpA + tmpAj * seqweights[j]
          tmpE <- tmpE + tmpEj * seqweights[j]
        }
      }
      A[] <- log(tmpA/apply(tmpA, 1, sum))
      E[] <- log(tmpE/apply(tmpE, 1, sum))
      model$A <- A
      model$E <- E
      logPx <- sum(tmplogPx)
      if (!quiet) 
        cat("Iteration", i, "log likelihood =", logPx, 
            "\n")
      if (abs(LL - logPx) < deltaLL) {
        if (!logspace) {
          model$A <- exp(model$A)
          model$E <- exp(model$E)
        }
        if (!quiet) 
          cat("Convergence threshold reached after", 
              i, "EM iterations\n")
        return(model)
      }
      LL <- logPx
      model$LL <- LL
    }
    if (!logspace) {
      model$A <- exp(model$A)
      model$E <- exp(model$E)
    }
    warning("Failed to converge on a local maximum. Try increasing 'maxiter',\n        decreasing 'deltaLL' or modifying start parameters")
    return(model)
  }
  else stop("Invalid argument given for 'method'")
}

countChanges <- function(hmmModel,observation_list){
  totalCount = c()
  for(observation in observation_list){
    path <- Viterbi(hmmModel,observation)$path
    countChange = 0
    prev <- path[1]
    for (i in path){
      if (i != prev){
        countChange = countChange + 1        
      }
      prev = i
    }
    totalCount = c(totalCount,countChange)
  }
  return(totalCount)
}

main <- function(saveDir,segmode="GMM",thr=10){
  fileDir = saveDir
  if (!is.null(segmode)){
    fname = paste("IndiCell", segmode, "/",sep="")
    imgName = paste(segmode,"_HMM.pdf",sep="")
  }
  else{
    fname = "IndiCell/"
    imgName = "HMM.pdf"
  }
    figDir = file.path(saveDir,imgName)
    pdf(file=figDir)
    
  dataDir = file.path(fileDir,fname)
  count = HMM_maxim(dataDir,saveDir,thr = thr,randomize = TRUE)
  dev.off()    
  
  return(count)
}

# Executed code below

set.seed(2021)
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

sample_poor1 = paste(rootDir,"glc_poor/sample1",sep="")
sample_poor2 = paste(rootDir,"glc_poor/sample3",sep="")
sample_poor3 = paste(rootDir,"glc_poor/sample2",sep="")
sample_rich1 = paste(rootDir,"glc_rich2/sample1",sep="")
sample_rich2 = paste(rootDir,"glc_rich2/sample2",sep="")
sample_rich3 = paste(rootDir,"glc_rich2/sample3",sep="")
mode="GMM"

samples <- list(sample_rich1,sample_rich2,sample_rich3,sample_poor1,sample_poor2,sample_poor3)
totalCounts <- list()

for (smp in samples){
    print(smp)
    count = main(smp,segmode=mode,thr =10)
    totalCounts<- c(totalCounts, list(count))
}
graphics.off()

