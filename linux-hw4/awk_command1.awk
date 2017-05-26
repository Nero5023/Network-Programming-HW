#!/usr/bin/awk -f

BEGIN {
    FS = ":"
    sumDonate = 0
    minDonate = 100000
    maxDonate = 0
}

{
    donate = $3 + $4+ $5
    sumDonate = sumDonate + donate
    if (donate > maxDonate)
        maxDonate = donate
    if (donate < minDonate)
        minDonate = donate
}

END {
    print "SumDonate  AVGDonate  MinDonate  MaxDonate"
    printf "%9d  %9.3f  %9d  %9d\n", sumDonate, sumDonate/12, minDonate, maxDonate
}