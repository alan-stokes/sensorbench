
load 'gnuplot/init.gnuplot'

set terminal pdf enhanced color
set out PDF_DIR.'exp1a-lifetime.pdf'

set auto x
set auto y
set style data linespoints
set pointsize 1.5
set xlabel "Network Size"
set ylabel "Lifetime (days)"
set key center left
set style histogram cluster gap 1
set style fill pattern border -1
set boxwidth 0.9 absolute
set yrange [0:]
set xtics
set datafile missing '?'
set datafile separator ","

#MHOSC
plot CSV_DIR.'exp1a-INSNEE-results-avg.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'raw'? column(LIFETIME_COL):1/0) title 'SNEE raw' linetype LT_INSNEE_RAW, \
     CSV_DIR.'exp1a-INSNEE-results-avg.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'aggr'? column(LIFETIME_COL):1/0) title 'SNEE aggr' linetype LT_INSNEE_AGGR, \
     CSV_DIR.'exp1a-MHOSC-results-avg.csv' using XVAL_COL:LIFETIME_COL title 'MHOSC' linetype LT_MHOSC, \
     CSV_DIR.'exp1a-OD2-results-avg.csv' using XVAL_COL:LIFETIME_COL title 'OD2' linetype LT_OD2, \
     CSV_DIR.'exp1a-LR-results-avg.csv' using XVAL_COL:LIFETIME_COL title 'LR' linetype LT_LR

