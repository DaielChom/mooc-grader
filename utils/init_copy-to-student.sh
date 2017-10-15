
export STUDENTDIR="./student/##COUSERNAME##"
echo "Using student dir at $STUDENTDIR"
rm -rf $STUDENTDIR/utils
## NO COPIAR LA CARPERTA DE img_conf
mkdir -p $STUDENTDIR/utils
mkdir -p $STUDENTDIR/img
mkdir -p $STUDENTDIR/data
cp ./*.ipynb $STUDENTDIR
cp ./utils/*.epy $STUDENTDIR/utils
cp ./utils/runepy $STUDENTDIR/utils
cp ./utils/client_secrets.json $STUDENTDIR/utils
cp ./run ./mooclib.py $STUDENTDIR
rm $STUDENTDIR/utils/init_mooc_grader.epy
rm $STUDENTDIR/mooc-grader-instructions.ipynb