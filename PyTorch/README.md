# PyTorch

Built from Nvidia NGC repository.

PyTorch is a GPU accelerated tensor computational framework with a Python front end. Functionality can be easily extended with common Python libraries such as NumPy, SciPy, and Cython. Automatic differentiation is done with a tape-based system at both a functional and neural network layer level. This functionality brings a high level of flexibility and speed as a deep learning framework and provides accelerated NumPy-like functionality.


## Brief usage guide

First, pull the container using the following command:
`singularity pull shub://<image-to-pull>`

then use the image in your job submission script:
`singularity exec PyTorch_vXXX.sif python YOUR-PROGRAM.py`

* Available images to pull: \
`c3se/containers:pytorch-v1.7.0-py3` \
`c3se/containers:pytorch-v1.6.0-py3` \
`c3se/containers:pytorch-v1.5.0-py3`

* Running: PyTorch can be imported as a python module:
    ```
    import torch
    print(torch.__version__)
    ```
    
* See `/workspace/README.md` inside the container for information on customizing your PyTorch image.

* For further information see: <https://ngc.nvidia.com/catalog/containers/nvidia:pytorch>
   

## Further information

For instructions on how to run singularity container images on our HPC cluster, see the tutorial in this repository <https://github.com/c3se/containers/tree/master/Tutorial>
