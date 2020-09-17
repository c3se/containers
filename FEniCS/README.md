# Description

Containerized image of the FEniCS project using conda installation based on the provided requirements.

## Usage
First, pull the image:
`singularity pull shub://c3se/containers:fenics` 

and then use the container using the following command in your job script: 
`singularity exec containers_fenics.sif ...`
