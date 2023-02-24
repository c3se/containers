Build instructions:

PMIx:

```bash
cd $HOME/rpmbuild/SOURCES
wget pmix-3.2.2.tar.bz2 # From github
apptainer exec /apps/containers/rpm-builds/build-pmix-rocky86.sif rpmbuild --define 'build_all_in_one_rpm 0' --define 'configure_options --with-munge --disable-per-user-config-files' -tb pmix-3.2.2.tar.bz2
```

Slurm:
```bash
# Make sure the newly built pmix and pmix-devel are available in the c3se-repo before recreating the build-slurm-... container
cd $HOME/rpmbuild/SOURCES
wget slurm-21.08.8.tar.bz2 # From github
apptainer exec /apps/containers/rpm-builds/build-slurm-rocky86.sif rpmbuild --with hwloc --with lua --with mysql --with numa --with pmix -tb slurm-21.08.8.tar.bz2
```
