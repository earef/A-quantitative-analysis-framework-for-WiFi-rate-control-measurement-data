
import subprocess
import argparse





# Take input from the user for label, start_index, and end_index
dataset = input("Enter the path of the trace file: ")
label = input("Enter the label name for plots: ")
start_index = int(input("Enter star index from trace file: "))
end_index = int(input("Enter end index from trace file: "))

# Run cleaning.py
subprocess.run(["python", "cleaning.py", "--dataset", dataset ,"--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
# subprocess.run(["python", "process.py"])
subprocess.run(["python", "attemptmap.py", "--dataset", dataset , "--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "heatmap-p.py", "--dataset", dataset , "--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "heatmap.py",  "--dataset", dataset ,"--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "coldmap-p.py", "--dataset", dataset , "--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "coldmap.py", "--dataset", dataset , "--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
# subprocess.run(["python", "Invert-map.py",  "--dataset", dataset ,"--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "airtime_probability.py",  "--dataset", dataset ,"--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "channel-update-adjustmenet-overlap.py",  "--dataset", dataset ,"--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "MCSIndexVSTime-probabilitycoldmap.py",  "--dataset", dataset ,"--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
subprocess.run(["python", "MCSIndexVSTime-probabilityheatmap.py",  "--dataset", dataset ,"--label", label, "--start_index", str(start_index), "--end_index", str(end_index)])
