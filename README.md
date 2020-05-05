# phaseanalysis
This script was used as part of an experiment tracking the input impedance of localized systems. A signal would be passed through an inductor and recorded with an oscilloscpe. After a secondary circuit with another inductor was introduced, another signal was passed through and again recorded. This was a tool for analyzing when a peak in voltage difference was present and how it related to coil seperation, core magnetization, and frequency. Additonally, transient behavior of a phase difference between these two signals was plotted over time with the phase function.


Usage: 

python multicoil.py (-diff | -phase | -w ) <Dualcoil> <singlecoil> 

-diff simply takes the oscilloscope data from the dual coil setup, and subtracts it from the single coil setup

-phase counts zero-crossings of the signal and approximates them to their local time domain to get an approximate phase difference between the signals. (as of 5/5/20 i don't have the finished version of the code)

-w writes diff/phase data to a csv if needed


