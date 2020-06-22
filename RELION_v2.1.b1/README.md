# RELION

Built from Nvidia NGC repository.

RELION (REgularized LIkelihood OptimizatioN) implements an empirical Bayesian approach for analysis of electron cryo-microscopy (Cryo-EM). Specifically it provides methods of refinement of singular or multiple 3D reconstructions as well as 2D class averages. RELION is an important tool in the study of living cells.

RELION is comprised of multiple steps to cover the entire single-particle analysis workflow. Steps include beam-induced motion-correction, CTF estimation, automated particle picking, particle extraction, 2D class averaging, 3D classification, high-resolution refinement in 3D. RELION can process movies generated from direct-electron detectors, apply final map sharpening and perform local-resolution estimation.


## Performance tuning

* Systems with at least 4 GPUs are best. While the container will run on Volta GPUs, more work is needed to optimize RELION for that platform. Work on this is currently progressing.

* Make sure you use the fast local disk (TMPDIR) for the scratch space. The RELION Benchmark needs at least 100 GB of scratch space.

* Launch multiple ranks per GPU to get better GPU utilization. For example on a 2 socket Broadwell server with 32 total cores and 4 P100, set ranks per GPU to 3, Threads to 2.

## Running RELION

The primary executable is `relion_refine_mpi`. For more information and instructions on how to run the singularity image see: <https://ngc.nvidia.com/catalog/containers/hpc:relion> . **NOTE** Do NOT run the benchmarks on the login node. Instead, submit the job to the compute nodes using a jov submission script. 