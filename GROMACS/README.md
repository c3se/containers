# GROMACS

Built from Nvidia NGC repository.

GROMACS is a molecular dynamics application designed to simulate Newtonian equations of motion for systems with hundreds to millions of particles. GROMACS is designed to simulate biochemical molecules like proteins, lipids, and nucleic acids that have a lot of complicated bonded interactions. More info on GROMACS can be found at <http://www.gromacs.org/>

## Running the container image 

An example using the water benchmark is given below. The benchmark can be downloaded from the NGC Examples Repository:`wget https://gitlab.com/NVHPC/ngc-examples/raw/master/gromacs/2018.2/single-node/singularity.sh`

Set the permission and run the test:
```
 chmod +x singularity.sh
 ./singularity.sh gpuCount /path/to/the/container/image 
```
where:

    `gpuCount`: the number of GPUs for GROMACS to use
    the path to the container image is `/apps/hpc-ai-containers/GROMACS/gromacs.sif`

**Note:** Do NOT run the simulation on a login node. Use an interactive job or submit the command execution to the compute nodes using a job submission script.


* For further information see: <https://ngc.nvidia.com/catalog/containers/hpc:gromacs>
