load 'gnuplot/init.gnuplot'

set terminal pdf enhanced color
set out PDF_DIR.'exp7-sum-6m-energy.pdf'

set auto x
set auto y
set style data linespoints
set pointsize 1.5
set xlabel "Acquisition Rate (s)"
set ylabel "Total Network Energy over 6 Months (J)"
set key center right
set style histogram cluster gap 1
set style fill pattern border -1
set boxwidth 0.9 absolute
set yrange [0:]
set xtics
set datafile missing '?'
set datafile separator ","

#MHOSC
plot CSV_DIR.'exp7-INSNEE-results.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'raw'? column(SUM_6M_ENERGY_COL):1/0) title 'SNEE raw', \
     CSV_DIR.'exp7-INSNEE-results.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'aggr'? column(SUM_6M_ENERGY_COL):1/0) title 'SNEE aggr', \
     CSV_DIR.'exp7-INSNEE-results.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'corr1'? column(SUM_6M_ENERGY_COL):1/0) title 'SNEE corr1', \
     CSV_DIR.'exp7-INSNEE-results.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'corr2'? column(SUM_6M_ENERGY_COL):1/0) title 'SNEE corr2', \
     CSV_DIR.'exp4a-MHOSC-results.csv' using XVAL_COL:SUM_6M_ENERGY_COL title 'MHOSC'
#, \
#     CSV_DIR.'exp7-INSNEE-results.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'LR'? column(SUM_6M_ENERGY_COL):1/0) title 'SNEE LR', \
#     CSV_DIR.'exp7-INSNEE-results.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'OD'? column(SUM_6M_ENERGY_COL):1/0) title 'SNEE OD'


