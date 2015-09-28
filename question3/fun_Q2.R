# Q2
price_q2=function(q2) {
  
  len_q2=dim(q2)[1]
  wid=rowSums(!is.na(q2))[1]  # excluding NA elements 
  t=(q2[,4])
  x0=(q2[,6:7])
  k=(q2[,8])
  sigma=(q2[,9:10])
  rho=q2[,3]
  
  
  x_calc=function(t,x0,k,sigma){
    n=10^5 # no of monte carlo simulations 
   # random number generation
    library('MASS')
    mu=(rep(0,9))
    rho=0.01
    sigma=matrix(data=rho,nrow=2,ncol=2)
    for (i in 1:2)
    {
      sigma[i,i]=1
    }
    sigma
    
    z=mvrnorm(n=10^5,mu,sigma,tol=10^(-6))
    z=t(z)
    
    x=matrix(data=NA,nrow=len_q1,ncol=n)
    
    for(i in 1:len_q1){
      x[i,]=x0[i]*exp(sigma[i]*sqrt(t[i])*y1-((sigma[i])^2)*t[i]/2)
    }
    return(x)
  }
  
  x=x_calc(t,x0,k,sigma)
  return(x)
}
