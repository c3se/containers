BootStrap: debootstrap
OSVersion: xenial
MirrorURL: http://archive.ubuntu.com/ubuntu/

%post
    sed -i 's/main/main restricted universe/g' /etc/apt/sources.list
    apt-get update
  
    # Install R, Python, misc. utilities
    apt-get install -y libopenblas-dev r-base-core libcurl4-openssl-dev libopenmpi-dev openmpi-bin openmpi-common openmpi-doc openssh-client openssh-server libssh-dev wget vim git nano git cmake  gfortran g++ curl wget python autoconf bzip2 libtool libtool-bin python-pip python-dev
    apt-get clean
    locale-gen en_US.UTF-8
  
    # Install Tensorflow
    pip install tensorflow
  
    # Install required R packages
    R --slave -e 'install.packages("devtools", repos="https://cloud.r-project.org/")'
    R --slave -e 'devtools::install_github("rstudio/tensorflow")'

    # Make image writable with overlays
    chmod a+rwX -fR /boot /bin /sbin /lib /lib32 /lib64 /usr /etc /var /opt || :


%test
  #!/bin/sh
  exec R --slave -e "library(tensorflow); \
                     sess  <- tensorflow::tf\$Session(); \
                     hello <- tensorflow::tf\$constant('Hello, TensorFlow!'); \
                     sess\$run(hello)"


%runscript
  #!/bin/bash
  Rscript --slave "main.R"

