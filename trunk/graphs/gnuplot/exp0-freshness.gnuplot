load 'gnuplot/init.gnuplot'

set terminal pdf enhanced color
set out PDF_DIR.'exp0-freshness.pdf'

set auto x
set auto y
set style data linespoints
set pointsize 1.5
set xlabel "Acquisition Interval (s)"
set ylabel "Data Freshness (s)"
set key center right
set style histogram cluster gap 1
set style fill pattern border -1
set boxwidth 0.9 absolute
set yrange [0:]
set xtics
set datafile missing '?'
set datafile separator ","

plot CSV_DIR.'exp0a-MHOSC-results.csv' using 12:21 title 'MHOSC', CSV_DIR.'exp0b-INSNEE-results.csv' using 12:21 title 'SNEE', CSV_DIR.'exp0a-INSNEE-results.csv' using 12:21 title 'SNEE*'

#set term png
#set out 'exp0-freshness.png'
#plot CSV_DIR.'exp0a-MHOSC-results.csv' using 12:21 title 'MHOSC', CSV_DIR.'exp0b-INSNEE-results.csv' using 12:21 title 'SNEE', CSV_DIR.'exp0a-INSNEE-results.csv' using 12:21 title 'SNEE*'

