bootstrap: docker
from: rstudio/r-base:4.0-focal

%post
    # Misc. utilities
    apt update
    apt install -y \
        make \
        pandoc \
        wget \
        vim \
        git \
        nano \
        git \
        cmake \
        gfortran \
        g++ \
        curl \
        wget \
        python \
        autoconf \
        bzip2 \
        libtool \
        libtool-bin \
        libssl-dev \
        libxml2-dev
        python-pip \
        python-dev
    apt clean
    locale-gen en_US.UTF-8
  
    # Install Tensorflow
    pip install tensorflow
  
    # Install required R packages
    R --slave -e 'install.packages("devtools", repos="https://cloud.r-project.org/")'
    R --slave -e 'devtools::install_github("rstudio/tensorflow")'
    R --slave -e 'devtools::install_github("mlverse/torch")'
    R --slave -e 'devtools::install_github("mlverse/torchvision")'

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

