#!/usr/bin/awk -f

BEGIN {
    FS=":"
    RothInfo    = ""
    ShannonInfo = ""
    donateNames = ""
}

{
    split($1, name, " "); 
    if(name[2]=="Roth")  
        RothInfo = RothInfo""$1":"$2"\n"
    if ($1~/Shannon/)
        ShannonInfo = $3+$4+$5
    if ($3 == 250 && donateNames == "")
        donateNames = $1
    if ($3 == 250 && donateNames != "")
        donateNames = donateNames", "$1
} 

END {
    print "Roth的全名和电话号码:"
    print RothInfo
    print "Shannon的捐款:"
    print ShannonInfo
    print "\n所有头一个月捐款$250的人名:"
    print donateNames
}