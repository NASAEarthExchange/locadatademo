
# A simple example showing a top level search on 
# LOCA's S3 cache copy. See http://loca.ucsd.edu 
# for the official distribution and general information.
# See the select_loca_data function 

library(jsonlite)

INVENTORY <- "http://nasanex.s3.amazonaws.com/LOCA/loca-s3-files.json"
MODELS <- "http://nasanex.s3.amazonaws.com/LOCA/models.json"

get_json <- function(ilink) {
   dat <- fromJSON(ilink)
   return(dat)
}

#' Select LOCA S3 keys/files given a set of criteria.
#'
#' This routine builds a list of S3 keys, or web links, from the basic 
#' LOCA json index. One might use this to determine an appropriate 
#' listing of some model, ~experiment, variable name and resolution tag. 
#' Im sure there is probably a more elegant way to do this...
#'
#' @param jidx The loaded json index from the LOCA S3 cache
#' @param model The name of the model of interest (see listing s3://nasanex/LOCA/models.json)
#' @param vname The variable of the model of interest (DTR, pr, tasmax, tasmin)
#' @param exprid The expriment id of interest, loosely defined here. Available 
#'               exprids are rcp45 or rcp85. The historical is always preprended for convenience.
#' @param rtag The resolution tag, 1x1 or 16th
#'
#' @ return list of LOCA keys/web links of interest
select_loca_data <- function(jidx, model, vname, exprid, rtag) {
   l <- list()
   keys = names(jidx)
   for(i in seq(jidx)) {
      if ( jidx[[i]]$model == model && jidx[[i]]$variable == vname &&  
           (jidx[[i]]$experiment_id == exprid || jidx[[i]]$experiment_id == 'historical') &&
           jidx[[i]]$rtag== rtag ) { 
             l <- c(l, keys[[i]])
      }   
   }   
   l <- l[order(sapply(l,'[[',1))]
   return( l ) 
}


jidx <- get_json(INVENTORY)
models <- get_json(MODELS)
m <- sample(models[[1]], 1)
kys <- select_loca_data(jidx, m, 'tasmax', 'rcp45', '16th')
for(k in kys) {
   print(k)
}