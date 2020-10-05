# TensorFlow

### Built from Nvidia NGC repository.

TensorFlow is an open-source software library for numerical computation using data flow graphs. This flexible architecture lets you deploy computation to one or more CPUs or GPUs in a desktop, server, or mobile device without rewriting code.

TensorFlow was originally developed by researchers and engineers working on the Google Brain team within Google's Machine Intelligence research organization for the purposes of conducting machine learning and deep neural networks research. The system is general enough to be applicable in a wide variety of other domains, as well.

## Brief usage guide

First, pull the container using the following command:
`singularity pull shub://<image-to-pull>`

then use the image in your job submission script:
`singularity exec TensorFlow_vXXX.sif python YOUR-PROGRAM.py`

* Available images to pull: \
`c3se/containers:tensorflow-v2.3.1-tf2-py3-gpu-jupyter` \
`c3se/containers:tensorflow-v2.2.0-tf2-py3-ngc-r20.08` \
`c3se/containers:tensorflow-v2.1.0-tf2-py3-ngc-r20.03`

* Running TensorFlow: TensorFlow can be imported as a python module:
    ```
    import tensorflow
    print(tensorflow.__version__)
    ```
    * See `/workspace/README.md` inside the container for information on customizing your TensorFlow image
    * TensorFlow tutorials: <https://www.tensorflow.org/tutorials>
    * For further information see: <https://ngc.nvidia.com/catalog/containers/nvidia:tensorflow>

## Further information

For instructions on how to run singularity container images on our HPC cluster, see the tutorial in this repository <https://github.com/c3se/containers/tree/master/Tutorial>
