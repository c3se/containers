# ambertools

## Brief usage guide

First, pull the container using the following command:
`singularity pull shub://<image-to-pull>`

then use the image in your job submission script:
`singularity exec <container>.sif YOUR-PROGRAM`

* Available images to pull: \
`c3se/containers:ambertools-v20`

## Further information

For instructions on how to run singularity container images on our HPC cluster, see the tutorial in this repository <https://github.com/c3se/containers/tree/master/Tutorial>
