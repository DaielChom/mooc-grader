export STUDENTDIR="../../../student/20161.ai.quiz1"
echo "Using student dir at $STUDENTDIR"
rm -rf $STUDENTDIR/utils
## NO COPIAR LA CARPERTA DE img_conf
mkdir $STUDENTDIR/utils
cp *.epy runepy client_secrets.json $STUDENTDIR/utils
cp ../run ../mooclib.py $STUDENTDIR
