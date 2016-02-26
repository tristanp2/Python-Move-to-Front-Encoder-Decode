DIR="./enctests/"
PRFX=""$DIR"test"
TESTDIR="./dectests/"
TPRFX=""$TESTDIR"test"
echo $TPRFX
ISFX=".txt" #input suffix
OSFX=".mtf" #output suffix
for i in {0..9}
do
    echo
    echo ------------------------------
    echo Testing case $i
	INPUT=""$PRFX"0"$i""
    TEST=""$TPRFX"0"$i""
    TEST+=$OSFX
    OUTPUT=$INPUT$OSFX
	INPUT+=$ISFX
    ./mtfencode.py $INPUT    
    cmp $OUTPUT $TEST
    echo ------------------------------
    echo
done
#was having issues with if statement syntax, so test11-19 are just done separately
for i in {0..9}
do
    echo
    echo ------------------------------
    echo Testing case 1$i
	INPUT=""$PRFX"1"$i""
    TEST=""$TPRFX"1"$i""
    TEST+=$OSFX
    OUTPUT=$INPUT$OSFX
	INPUT+=$ISFX
    ./mtfencode.py $INPUT    
    cmp $OUTPUT $TEST
    echo ------------------------------
    echo
done
