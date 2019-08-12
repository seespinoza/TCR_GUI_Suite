files = list.files(pattern = '*.tsv')

for(i in 1:length(files)){
  p <- read.csv(files[i], stringsAsFactors = F, header = T, check.names = F, sep = "\t")
  nam <- gsub(".tsv", "", files)
  point <- p[, c("vGeneName", "jGeneName","frequencyCount (%)", "cdr3Length", "sequenceStatus", "vFamilyName", "jFamilyName")]
  pxtt <- which(point[, 1] == "unknown")
  if(length(pxtt) > 0){
    point[pxtt, 1] <- paste(point[pxtt, 6], ".un", sep = "")}
  pxjt <- which(point[, 2] == "unknown")
  if(length(pxjt) > 0){
    point[pxjt, 2] <- paste(point[pxjt, 7], ".un", sep = "")}
  point <- point[, c(1:5)]
  idxpt <- which(point[, 1] == "" | point[, 2] == "" | point[, 1] == "unresolved" | point[, 2] == "unresolved"| point[, 1] == "unknown.un"| point[, 2] == "unknown.un")
  if (length(idxpt) > 0 ){
    point <- point[-idxpt, ]}
  p <-point
  p <- p[, c("vGeneName", "jGeneName","frequencyCount (%)", "cdr3Length", "sequenceStatus")]
  data <-p
  lx <- which(data$sequenceStatus == "In")
  data1 <- data[lx, ]
  
      data2 <- data1
      print(data2)
      data2 <- data2[, c(1,2, 3)]
      data2[, 1] <- as.character(data2[, 1])
      data2[, 2] <- as.character(data2[, 2])
      data2[, 3] <- as.numeric(as.character(data2[, 3]))
      l <- data2
      colnames(l) <- c("vName", "jName", "frequencies")
      if(nrow(l) > 1){
        l<- aggregate(x = l[, 3], by = l[, c(1,2)], FUN = sum)
      }
      a <- l
      a[, 1] <- sapply(a[, 1], function(x)
        gsub("^TCR", "", x))
      a[, 1] <- sapply(a[, 1], function(x)
        gsub("V0", "V", x, perl = TRUE))
      a[, 1] <- sapply(a[, 1], function(x)
        gsub("-0", "-", x))
      a[, 2] <- sapply(a[, 2], function(x)
        gsub("^TCR", "", x))
      a[, 2] <- sapply(a[, 2], function(x)
        gsub("J0", "J", x))
      a[, 2] <- sapply(a[, 2], function(x)
        gsub("-0", "-", x))
      vNames <- unique(a[, 1])
      jNames <- unique(a[, 2])
      coOc <- matrix(0, nrow=length(vNames), ncol=length(jNames))
      rownames(coOc) <- vNames
      colnames(coOc) <- jNames
      for (k in 1:nrow(a)) {
        for (vName in vNames){
          for (jName in jNames){
            if (a[k, 1] == vName & a[k, 2] == jName){
              coOc[vName, jName] <- a[k, 3]}}}}
      coOc <- as.matrix(coOc)
      smallest <- min(coOc[coOc > 0])
      coOc <- round(coOc / smallest)
      write.table(file = paste(nam[i], ".txt", sep = ""), coOc, quote = F)
      
      
    }


###################################################################3
### Counts
