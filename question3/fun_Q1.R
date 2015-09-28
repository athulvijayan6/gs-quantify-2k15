# Q1
price_q1=function(q1) {
  
  len_q1=dim(q1)[1]
  wid=rowSums(!is.na(q1))[1]  # excluding NA elements 
  t=(q1[,3])
  x0=(q1[,5])
  k=(q1[,6])
  sigma=(q1[,7])
  
  
  x_calc=function(t,x0,k,sigma){
    n=10^7 # no of monte carlo simulations 
    y1=rnorm(n,0,1)
    x=matrix(data=NA,nrow=len_q1,ncol=n)
    
    for(i in 1:len_q1){
    x[i,]=x0[i]*exp(sigma[i]*sqrt(t[i])*y1-((sigma[i])^2)*t[i]/2)
    }
    return(x)
  }
  
  x=x_calc(t,x0,k,sigma)
  return(x)
}
  
  