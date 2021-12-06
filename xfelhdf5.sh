#!/usr/bin/bash
#SBATCH --partition=xfel-op
#SBATCH --time=02:10:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --mail-type END,FAIL                 # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user christian.grech@desy.de  # Email to which notifications will be sent

export PYTHONPATH=/beegfs/desy/group/fla/software/daq/libs/CentOS-7-x86_64
export LD_LIBRARY_PATH=/beegfs/desy/group/fla/software/daq/libs/CentOS-7-x86_64:/beegfs/desy/group/fla/software/daq/libs/CentOS-7-x86_64/extlib

python3 daqraw2hdf5.py -xml xfeldaq_sase2_test.xml -xfel -local -descr xfel_sase1_main_run1727_chan_dscr.xml

echo "Job finished - exit"
exit