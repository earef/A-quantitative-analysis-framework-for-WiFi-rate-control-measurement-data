# scnx-plot-analysis


## How to run the code

1- Create a new-folder in the "scnx-plot-analysis" path and name it "plot" to save exported plots. <br />
2- Run ```sh python3 run_all.py ``` <br />
3- Follow the steps and answer the questions:<br />

Example:<br />
"Enter the path of the trace file:"  dataset/tracefile.csv <br />
"Enter the label name for plots: " Test-Plots<br />
"Enter star index from trace file: " 1000<br />
"Enter end index from trace file: " 1500<br />

-The start and end of index can be empty if you want to analyse the whole dataset.<br />
-In the "run_all.py" comment out any type of the plots you don't want to use.<br />
-Rolling Time window been set to "100ms" it is adjustable.(To Do: ask the rolling windows size before running the code)<br />

## What does it plot

**attemptmap**: plot (success+fail) attempt counts per rate. X= Modulation-Coding Y= Rate-BW-GI-NSS<br />

**heatmap**: plot the success counts per rate. X= Modulation-Coding Y= Rate-BW-GI-NSS<br />
**heatmap-probability**: plot the success probability per rate. X= Modulation-Coding Y= Rate-BW-GI-NSS<br />

**coldmap**: plot the fail counts per rate. X= Modulation-Coding Y= Rate-BW-GI-NSS.<br />
**coldmap-probability**: plot the fail counts per rate. X= Modulation-Coding Y= Rate-BW-GI-NSS.<br />

**MCS.vs.Time-coldprobabilitymap**: plot fail probability. X= Time (Rolling windows of 100ms) Y= Rate-Modulation-Coding-BW-GI-NSS.<br />
**MCS.vs.Time-heatprobabilitymap**: plot success probability. X= Time (Rolling windows of 100ms) Y= Rate-Modulation-Coding-BW-GI-NSS.<br />

**airtime_probability**: plot X= airtime(ns) hex notion Y= Success probability.<br />

*Details of each plot can be find in The Thesis.[Thesis Files](https://drive.google.com/drive/folders/1M3FYC0_m9GNfRadza3TwTa0jy-BChPb1?usp=sharing)

##  Note

Analysis of **TXS** lines are parsing undermentioned txs header.<br />

**TXS_Columns** = ["radio","timestamp","txs","macaddr","num_frames","num_acked","probe",
                "rate0","count0","rate1","count1","rate2","count2","rate3","count3"]
