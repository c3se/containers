# Building and using containers in HPC environments"
## container-based solutions to share reproducible science

   The following material is Open Source: you can redistribute it and/or modify it under the terms 
   of the GNU GPL v3.0 License. For details please see LICENSE under the project's repository.
   
   The material is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
   even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
   GNU GPL v3.0 License for more details. 
   Copyright © 2020, Soheil Soltani, Chalmers Center for Computational Science and Engineering (C3SE) 

# Background
* Containers provide:
    * encapsulation of system environment 
    * interaction mechanisms for the hosted resources 
* On a linux system, there can be many isolated containers running simultaneously 
    * gives the illusion that each one is the *only* process running on the host
* In this tutorial, we will show how to:
    * build Docker and Singularity images, and
    * use an already-built image in an HPC environment
    * use Nvidia's [HPCCM](https://github.com/NVIDIA/hpc-container-maker) tool to prepare optimized container recipes

# Docker and Singularity
* Singularity is a very popular choice for a container runtime in HPC clusters
    * the runtime system does not need superuser privileges to run an image
    * Singularity images are *flat* (in contrast to the *layered* structure of docker images)
        * makes transferring and sharing them across a cluster very easy
	* also helpful for reproducibility (changes in any of the layers may break reproducibility

* Advantages of *layered* images:
    * caching the build layers can speed up the build process
    * multi-stage builds make fine-tuning the size and the content of the final image possible


# Singularity
* Scientists require reproducibility, portability, and the means which provide the freedom to others to interact with their software. 

* Singularity aims to guarantee these goals

* Running a singularity container does not require superuser privileges 


# Running a singularity image on a single CPU
``singularity exec someImage.sif /path/to/binary/inside/container`` --> runs the binary inside the container \
``singularity run someImage.sif``  --> executes the runscript embedded inside the container \
``singularity shell someImage.sif`` --> gives an interactive shell inside the container


# Running singularity with MPI across multiple nodes
* There are four main components involved in a containerized MPI-based application:
    1. The executable MPI program (e.g. ``a.out``)
    2. The MPI library
    3. MPI runtime, e.g. `mpirun`
    4. Communication channel, e.g. SSH server

* Depending on how to containerize those elements, there are two general approaches to running a containerized application across a multi-node cluster: 
    1. Packaging the MPI program and the MPI library iside the container, but keeping the MPI runtime outside on the host
    2. Packaging the MPI runtime also inside the container leaving only the communication channel on the host

# Host-based MPI runtime
In this approach, the mpirun command runs on the host:
``mpirun singularity run myImage.sif myMPI_program``

``mpirun`` does, among other things, the following: 
* Spawns the ORTE deamon on the compute nodes
* Launches the MPI program on the nodes
* Manages the communication among the MPI ranks

This fits perfectly with the regular workflow of submitting jobs on the HPC clusters, and is, therefore, the recommended approach. There is one thing to keep in mind however: \
The MPI runtime on the host needs to be able to communicate with the MPI library inside the container; therefore, i) there must be the same implementation of the MPI standard (e.g. OpenMPI) inside the container, and, ii) the version of the two MPI libraries should be as close to one another as possible to prevent unpredicted behaviour (ideally the exact same version).

# Image-based MPI runtime
* In this approach, the MPI launcher is called from within the container; therefore, it can even run on a host system without an MPI installation (your challenge would be to find one!): \
``singularity run myImage.sif mpirun myMPI_program`` 
* Everything works well on a single node. There's a problem though: as soon as the launcher tries to spawn into the second node, the ORTED process crashes. The reason is it tries to launch the MPI runtime on the host and not inside the container.
* The solution is to have a launch agent do it inside the container. With OpenMPI, that would be: \
``singularity run myImage.sif mpirun --launch-agent 'singularity run myImage.sif orted' myMPI_program``
    
# Filesystem and singularity containers
* The ``$HOME`` directory of the host system is mounted by default
* The current directory will also be mounted
* The user can specify which file systems get binded. For instance to bind ``/tmp`` to ``/opt`` use the following flag:
``--bind /tmp:/opt someImage.sif``

# Further remarks
* To check the recipe file from which a container was build:
``Singularity inspect --deffile someImage.sif``
* To enable **GPU** support when running a containerized application that offloads to an Nvidia GPU, use ``singularity --nv ....``
* **Building** your own singularity containers requires root access. If you do not have access to a Linux machine on which you can become root, you can still use cloud-based services that take your recipe file and build your singularity image for you. Here are two ways to go about:
    1. login to <https://cloud.sylabs.io/builder> ; upload your recipe and trigger the build process
    2. You can do the same using the command-line: ``singularity build --remote``, which will ask you for an API token. From your account dashboard on the link above, click on Access Tokens to generate an API key and proceed with the build. As a general note, do NOT run this on a login node; building some images can be a very demanding process.

   
# Building Docker images
* Docker images can be built from a recipe file the content of which can be e.g.:

```text
FROM ubuntu:latest
RUN date > /result.txt
```

which can be built using: 
`sudo docker build -t myImage:someTag -f docker/Dockerfile . `

* the Dockerfile contains the recipe
* the `-t` option specifes NAME:TAG
* the **.** at the end of the command specifies the path to use for the build, i.e. the sandbox from which the host files are accessible during the build process.
* Running the image:
    * `sudo docker run --rm -it myImage /command/to/run/inside/image`
* Inspecting the layers:
    * `sudo docker history second-image` use `--no-trunc` to list full instructions
	
# File layer deduplication
* If the same file is modified in a subsequent layer, it causes that layer to duplicate the entire file resulting in an unnecessarily increased size.
* To prevent such redundancy, the best practice is to keep all the modifying actions to the same file in the same docker instruction (using e.g. `&&` to concantenate shell commands).
    * **Note** that this prevents caching the layers, so maitain a balanced level between the two alternatives
	* If desired, do a bit of cleanup after package installation: `rm -rf /var/lib/apt/lists/*` in the same instructions as they are created


# Docker multi-stage build
* Docker images can be built recursively inheriting the result of one build stage, all in the same recipe file! Here's a template:
```text
# Start from a basic Ubuntu 16.04 image
FROM ubuntu:16.04 AS stage_1
// prepare an executable
// start with a clean container again
FROM ubuntu:16.04

// Move the binary along from the previous stage
COPY --from=stage_1 /path/to/bin/ /path/to/new/bin
```

* Further image size reduction: unnecessary material (e.g. compiler, source code, etc.) can be purged out of the final image at the end of the build if they are not going to be needed for the runtime system:
    ```text
    ``rm -rf /path/to/source.c``
    `apt-get purge -y build-essential gcc`
    `apt autoremove -y`
    ```

# HPC container maker (HPCCM)
Conceptually, HPCCM uses building blocks. For instance, openmpi is a building block that can be installed. The ``hpccm`` command line tool can parse an input python script that includes these building blocks in a possibly multi-stage build recipe. It will then generate either a docker or a singularity recipe. Example:
```text
Stage0 += baseimage(image='nvidia/cuda:9.2-devel-centos7')
Stage0 += openmpi(infiniband=False)
```
The publically available CUDA base images can be accessed here: <https://hub.docker.com/r/nvidia/cuda/>


# Building application container with HPCCM
* Adding instruction to the container recipe for handling files and compiling from source requires the use of [primitives](https://github.com/NVIDIA/hpc-container-maker/blob/master/docs/primitives.md).
    * Primitives are wrappers that translate into native container specification
    * also unify the specification irrespective of the target image type (being docker or singularity)
* Example of using primitives:
    * `Stage0 += copy(src='path/to/source/file.c', dest='path/to/dest/inside/the/image')`
    * `Stage0 += shell(commands = ['mpicc -o myAwsomeApp my_awesome_app.c'])
* After building the docker image, use the docker-daemon endpoint to build a Singularity image from the local Docker image repository:
    * `singularity build my_sing_app.sif docker-daemon://my_awesome_app:latest`

# Build your own singularity container
Singularity is compatible with Docker; therefore, the following **best practice** for building containers can be recommended: \
    1. Specify the content of the desired container with HPCCM
    2. Build the image with Docker
    3. Transform the Docker image to a Singularity one
    4. Use Singularity runtime to execute the image on the target HPC system    

* The advantage of taking the second step above is that one can tune the layers to reduce the size of the final image. If the image size is not a major concern, you can directly obtain a singularity build recipe from HPCCM and bypass step 3.

# Online resources
* Scilabs Inc. YouTube channel: <https://www.youtube.com/channel/UCsxpqAJKGJBMEFHFr-5VL2w/featured>
* Docker's library of container images: <https://hub.docker.com/>
* Singularity container registry: <https://singularity-hub.org/>
* Nvidia's NGC catalogue including an up-to-date plethora of HPC/AI/Visualization container images verified by Nvidia: <https://ngc.nvidia.com>
* Nvidia's HPC Container Maker: <https://github.com/NVIDIA/hpc-container-maker>
* Open Containers Image Specifications: <https://github.com/opencontainers/image-spec>
* Singularity user's guide: <https://sylabs.io/guides/3.2/user-guide/quick_start.html>
* Docker Docs: <https://docs.docker.com/>
* Docker multi-stage build: <https://docs.docker.com/develop/develop-images/multistage-build/>

# Summary
We hope that by now you feel more comfortable with building and running HPC containers across a compute cluster. \
We will continue adding more hands-on material to this section. If you find any errors or deprecated feaetures in the material, feel free to send us an email: <support@c3se.chalmers.se> or open a pull-request. 