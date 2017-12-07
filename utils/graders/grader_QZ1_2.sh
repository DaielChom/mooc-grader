#!/bin/bash
CODE="""
#include<stdio.h>\n
#include \"../student_function/student_QZ1_2.c\"\n
int main(){    
    char s = mean();    
    if (s =='D') printf(\"Excelente##5.0\");
    else printf(\"Fallaste##1.3\");    
return 0;
}"""
echo -e $CODE >> ./utils/graders/grad.c
gcc ./utils/graders/grad.c -o ./utils/graders/exe
./utils/graders/exe
rm -rf ./utils/graders/grad.c
rm -rf ./utils/graders/exe