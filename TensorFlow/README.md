# TensorFlow

Built from Nvidia NGC repository.

TensorFlow is an open-source software library for numerical computation using data flow graphs. Nodes in the graph represent mathematical operations, while the graph edges represent the multidimensional data arrays (tensors) that flow between them. This flexible architecture lets you deploy computation to one or more CPUs or GPUs in a desktop, server, or mobile device without rewriting code.

TensorFlow was originally developed by researchers and engineers working on the Google Brain team within Google's Machine Intelligence research organization for the purposes of conducting machine learning and deep neural networks research. The system is general enough to be applicable in a wide variety of other domains, as well.

* Running TensorFlow
    TensorFlow can be imported as a python module:
    ```
    import tensorflow
    print(tensorflow.__version__)
    ```
    * For instructions on how to run singularity container images on an HPC cluster, see <https://github.com/c3se/containers/blob/master/README.md>
    * TensorFlow tutorials: <https://www.tensorflow.org/tutorials>
    
* See `/workspace/README.md` inside the container for information on customizing your TensorFlow image.

* For further information see: <https://ngc.nvidia.com/catalog/containers/nvidia:tensorflow>