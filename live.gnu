set datafile separator ','
# '1' represents x-axis (time) & '26' represents the y-axis (currently x gravity)
plot "properties.csv" using 1:26 with lines
set yrange[-1.5:1.5]
if (GPVAL_DATA_X_MAX > 10) set xrange[GPVAL_DATA_X_MAX-10:GPVAL_DATA_X_MAX+1]; 
pause 1
reread