
export STUDENTDIR="./student/##COUSERNAME##"
echo "Using student dir at $STUDENTDIR"
rm -rf $STUDENTDIR/utils
## NO COPIAR LA CARPERTA DE img_conf
mkdir -p $STUDENTDIR/utils/graders
mkdir -p $STUDENTDIR/utils/student_function
mkdir -p $STUDENTDIR/img
mkdir -p $STUDENTDIR/data
cp ./data/* $STUDENTDIR/data
cp ./img/* $STUDENTDIR/img
cp ./*.ipynb $STUDENTDIR
cp ./utils/*.epy $STUDENTDIR/utils
cp ./utils/graders/*.grader $STUDENTDIR/utils/graders
cp ./utils/runepy $STUDENTDIR/utils
cp ./utils/client_secrets.json $STUDENTDIR/utils
cp ./run ./mooclib.py $STUDENTDIR
rm $STUDENTDIR/utils/init_mooc_grader.epy
rm $STUDENTDIR/instrucciones.ipynb
rm $STUDENTDIR/instrucciones_quices_dinamicos.ipynb
rm $STUDENTDIR/quiz.ipynb
rm $STUDENTDIR/Template_Seccion.ipynb
