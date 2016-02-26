DIR="./enctests/"
PRFX=""$DIR"test"
TESTDIR="./dectests/"
TPRFX=""$TESTDIR"test"
echo $TPRFX
ISFX=".txt" #input suffix
OSFX=".mtf" #output suffix
rm encode.prof
for i in {0..9}
do
    echo >> encode.prof
    echo TEST 0$i >> encode.prof
    echo ------------------------------ >> encode.prof
	INPUT=""$PRFX"0"$i""
    TEST=""$TPRFX"0"$i""
    TEST+=$OSFX
    OUTPUT=$INPUT$OSFX
	INPUT+=$ISFX
    kernprof -lv mtfencode.py $INPUT >> encode.prof   
    echo ------------------------------ >> encode.prof
    echo >> encode.prof
done
#was having issues with if statement syntax, so test11-19 are just done separately
for i in {0..9}
do
    echo >> encode.prof
    echo TEST 1$i >> encode.prof
    echo ------------------------------ >> encode.prof
	INPUT=""$PRFX"1"$i""
    TEST=""$TPRFX"1"$i""
    TEST+=$OSFX
    OUTPUT=$INPUT$OSFX
	INPUT+=$ISFX
    kernprof -lv mtfencode.py $INPUT >> encode.prof   
    echo ------------------------------ >> encode.prof
    echo >> encode.prof
done
