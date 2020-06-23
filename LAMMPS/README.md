# LAMMPS

Built from Nvidia NGC repository.

Large-scale Atomic/Molecular Massively Parallel Simulator (LAMMPS) is a software application designed for molecular dynamics simulations. It has potentials for solid-state materials (metals, semiconductor), soft matter (biomolecules, polymers) and coarse-grained or mesoscopic systems. It can be used to model atoms or, more generically, as a parallel particle simulator at the atomic, meso, or continuum scale.

LAMMPS runs on single processors or in parallel using message-passing techniques and a spatial-decomposition of the simulation domain.

## GPU support

The NGC container supports the following NVIDIA GPU architectures:
    * Pascal(sm60)
    * Volta(sm70)
A LAMMPS executable optimized for the available architecture will be chosen automatically at runtime.

## Running the container image

The primary LAMMPS application executable is `lmp`. It is built against KOKKOS utilizing the CUDA backend and OpenMPI for multi-process and distributed execution. The executable can be launched on our cluster using the following command:

`<mpi-launcger> lmp -k on g <NUM-GPUs> -sf kk -pk kokkos gpu/direct on neigh full comm device binsize 2.8 -in <input-file.txt>` ,

where:

    `<mpi-launcger>`: MPI launch command, e.g. `mpirun` or `mpiexec`
    `lmp`: The LAMMPS executable
    `-k on g <NUM-GPUs>`: number of GPUs per node to be used by KOKKOS
    `-sf kk`: Use KOKKOS styles when available
    `-pk kokkos`: KOKKOS package option flag
        `gpu/direct on`: use GPU aware MPI
        `neigh full`: use full neighbor list
        `comm device`: perform communication packing/unpacking on GPU
        `binsize 2.8`: neighbor list bin sizing(2.8)
    -`in <input-file.txt>: input file


## Example

The following example demonstrates how to run the NGC LAMMPS container on HPC systems. The example makes use of the Leanard Jones 3D melt input file `in.lj.txt`, which can be obtained using: `wget https://lammps.sandia.gov/inputs/in.lj.txt`.

The input file `in.lj.txt` can be tuned at runtime by setting the x,y,z dimensions of the problem: `lmp -in in.lj.txt -var x 8 -var y 8 -var z 8`

### Using mpirun on the host system

The NGC LAMMPS container can be launched using the host provided `mpirun` or `mpiexec` launcher. When using the host MPI launcher there is no need to generate a hostfile or ensure rsh/ssh is setup correctly allowing for good integration with the cluster resource manager. It is however required to have OpenMPI/3.1.0 or newer. When running with the host provided mpirun tight integration with the resource manager is maintained.

Launching the job within the container using mpirun:

`mpirun --np=xx --map-by ppr:n:socket singularity run --nv -B$(pwd):/host_pwd lammps-24Oct2018.sif lmp -k on g <nGPUs> -sf kk -pk kokkos gpu/direct on neigh full comm device binsize 2.8 -var x 8 -var y 8 -var z 8 -in /host_pwd/in.lj.txt

Where:

    `--np`: sets a total of xx task count
    `--map-by ppr:n:socket`: launches n tasks per CPU socket. n should match the number of GPUs with affinity to each CPU socket
    `singularity run`: must always be used to ensure the container is properly initialized. `exec` SHOULD NOT be used
    `--nv`: expose the host GPU to the container
    -`B$(pwd):/host_pwd`: expose the current working directory in the container at `/host_pwd`
    `lammps-24Oct2018.sif`: name of the singularity image file
    `nGPUs`: sets the number of GPU's available per compute system 
    

* For further information see: <https://ngc.nvidia.com/catalog/containers/hpc:lammps>