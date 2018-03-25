export QUIZDIR="./student/Quiz_#"
echo "Using quiz student dir at $QUIZDIR"
rm -rf $QUIZDIR/utils
## NO COPIAR LA CARPERTA DE img_conf
mkdir -p $QUIZDIR/utils/graders
mkdir -p $QUIZDIR/utils/student_function
mkdir -p $QUIZDIR/img
mkdir -p $QUIZDIR/data
cp ./data/* $QUIZDIR/data
cp ./img/* $QUIZDIR/img
cp ./*.ipynb $QUIZDIR
cp ./utils/*.epy $QUIZDIR/utils
cp ./utils/runepy $QUIZDIR/utils
cp ./utils/client_secrets.json $QUIZDIR/utils
cp ./run ./mooclib.py $QUIZDIR
cp ./render_cell.py $QUIZDIR
rm $QUIZDIR/utils/init_mooc_grader.epy
rm $QUIZDIR/instrucciones.ipynb
rm $QUIZDIR/Template_Seccion.ipynb
