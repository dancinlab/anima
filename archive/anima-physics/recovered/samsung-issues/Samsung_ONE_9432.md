https://github.com/Samsung/ONE/issues/9432
# Compiler FE: Support ubuntu 22.04 (jammy)

## What
Let's let ONE compiler support ubuntu 22.04.

## Why
Ubuntu 22.04 has started to be release. The number of users using ubuntu 22.04 will gradually increase. So, let's prepare to support it in advance! It may a little bit early, but there is nothing wrong with preparing in advance.

## Environment of ubuntu 22.04
### default version
- cmake: 3.22.1
- python3: 3.10.4
- gcc: 11.2.0
- libboost: 1.74

## To do
- [x] Support cmake 3.22.1
- [x] Support python3 3.10.4 (by https://github.com/Samsung/ONE/issues/9432#issuecomment-1185208025)
- [ ] Support gcc 11.2.0 (internal only)
- [ ] Create jammy docker file (no plan yet) 
- [ ] Docker build on CI (no plan yet)

## Build Target Architectures
### Build for x86_64
```bash
$ cd {one dir}
$ docker run -it --rm -v `pwd`:`pwd` -w `pwd` ubuntu:22.04 /bin/bash
apt update
apt install cmake libboost-all-dev g++ patch python3-pip python3-venv
python3 -m pip install --upgrade pip

./nncc configure
./nncc build
./nncc test
```

### Build for arm32
```bash
$ sudo apt-get install qemu qemu-user-static binfmt-support debootstrap
$ cd {one dir}
$ ROOTFS_DIR=`pwd`/tools/cross/rootfs/arm-jammy sudo -E ./tools/cross/install_rootfs.sh arm jammy --skipunmount
```
```bash
$ cd {one dir}
$ docker run -it --rm -v `pwd`:`pwd` -w `pwd` ubuntu:22.04 /bin/bash
apt update
apt install cmake libboost-all-dev g++ patch python3-pip python3-venv
python3 -m pip install --upgrade pip

apt install g++-arm-linux-gnueabihf make
ROOTFS_ARM=`pwd`/tools/cross/rootfs/arm-jammy make -f infra/nncc/Makefile.arm32 cfg
ROOTFS_ARM=`pwd`/tools/cross/rootfs/arm-jammy make -f infra/nncc/Makefile.arm32 debug
```
