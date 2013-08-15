
load 'init.gnuplot'

set terminal pdf enhanced color
set out 'exp4a-sum-6m-energy.pdf'

set auto x
set auto y
set style data linespoints
set pointsize 1.5
set xlabel "Acquisition rate (s)"
set ylabel "Total Network Energy over 6 Months (J)"
set key center right
set style histogram cluster gap 1
set style fill pattern border -1
set boxwidth 0.9 absolute
set yrange [0:]
set xtics
set datafile missing '?'
set datafile separator ","

plot 'exp4a-INSNEE-results.csv' using XVAL_COL:(stringcolumn(TASK_COL) eq 'raw'? column(SUM_6M_ENERGY_COL):1/0) title 'SNEE raw', \
     'exp4a-MHOSC-results.csv' using XVAL_COL:SUM_6M_ENERGY_COL title 'MHOSC'
