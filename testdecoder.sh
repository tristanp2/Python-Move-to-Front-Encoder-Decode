DIR="./dectests/"
PRFX=""$DIR"test"
TESTDIR="./enctests/"
TPRFX=""$TESTDIR"test"
echo $TPRFX
ISFX=".mtf" #input suffix
OSFX=".txt" #output suffix
for i in {0..9}
do
    echo Testing case $i
	INPUT=""$PRFX"0"$i""
    TEST=""$TPRFX"0"$i""
    TEST+=$OSFX
    OUTPUT=$INPUT$OSFX
	INPUT+=$ISFX
    ./mtfdecode.py $INPUT    
    cmp $OUTPUT $TEST
done
#was having issues with if statement syntax, so test10 is just done separately
for i in {0..9}
do
    echo Testing case 1$i
	INPUT=""$PRFX"1"$i""
    TEST=""$TPRFX"1"$i""
    TEST+=$OSFX
    OUTPUT=$INPUT$OSFX
	INPUT+=$ISFX
    ./mtfdecode.py $INPUT    
    cmp $OUTPUT $TEST
done
