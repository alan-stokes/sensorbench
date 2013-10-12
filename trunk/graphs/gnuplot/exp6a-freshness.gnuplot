load 'gnuplot/init.gnuplot'

set terminal pdf enhanced color
set out PDF_DIR.'exp6a-freshness.pdf'

set auto x
set auto y
set style data linespoints
set pointsize 1.5
set xlabel "Radio Packet Loss Rate (%)"
set ylabel "Data Freshness (s)"
set key center right
set style histogram cluster gap 1
set style fill pattern border -1
set boxwidth 0.9 absolute
set yrange [0:]
set xtics
set datafile missing '?'
set datafile separator ","

plot CSV_DIR.'exp6a-INSNEE-results-avg.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'raw'? column(FRESHNESS_COL):1/0) title 'SNEE raw' linetype LT_INSNEE_RAW, \
     CSV_DIR.'exp6a-INSNEE-results-avg.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'aggr'? column(FRESHNESS_COL):1/0) title 'SNEE aggr' linetype LT_INSNEE_AGGR, \
     CSV_DIR.'exp6a-MHOSC-results-avg.csv' using XVAL_COL:FRESHNESS_COL title 'MHOSC' linetype LT_MHOSC, \
     CSV_DIR.'exp6a-OD2-results-avg.csv' using XVAL_COL:FRESHNESS_COL title 'OD2' linetype LT_OD2, \
     CSV_DIR.'exp6a-LR-results-avg.csv' using XVAL_COL:FRESHNESS_COL title 'LR' linetype LT_LR
