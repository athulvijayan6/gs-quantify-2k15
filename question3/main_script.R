# main script

data=read.table("Quant_Data_Set_Sample.txt", header = FALSE, sep = ",",col.names = paste0("V",seq_len(24)), fill = TRUE)
q1=subset(data,data[,2]==1)
q2=subset(data,data[,2]==2)
q3=subset(data,data[,2]==3)
q4=subset(data,data[,2]==4)
q5=subset(data,data[,2]==5)

#count.fields("Quant_Data_Set_Sample.txt",sep=",")
# to round off numbers say to 4 decimal places 
# use format(round(x, 4), nsmall = 4)
source('fun_Q1.R')
x_q1=price_q1(q1)
x_q2=price_q2(q2)
x_q3=price_q2(q3)

