CUR_DIR = $(shell pwd)
LLVM_BUILD := /home/jamrot/llvm-project/build
SRC_DIR := ${CURDIR}/src
SRC_BUILD := ${CURDIR}/build

NPROC := $(shell nproc)

build_src_func = \
	(mkdir -p ${2} \
		&& cd ${2} \
		&& PATH=/home/jamrot/llvm-project/build/bin:/home/jamrot/llvm-project/build/bin:/home/jamrot/gems/bin:/home/jamrot/gems/bin:/home/jamrot/gems/bin:/home/jamrot/gems/bin:/home/jamrot/.local/bin:/home/jamrot/bin:/home/jamrot/anaconda3/condabin:/home/jamrot/gems/bin:/home/jamrot/gems/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib \
			CC=clang CXX=clang++ \
			cmake ${1} \
				-DCMAKE_BUILD_TYPE=Release \
        		-DCMAKE_CXX_FLAGS_RELEASE="-std=c++14 -fno-rtti -fpic -fopenmp -O3" \
				-DLLVM_INSTALL_DIR=${LLVM_USED} \
				-DZLIB_INCLUDE_DIR=/usr/include \
				-DZLIB_LIBRARY=/usr/lib/x86_64-linux-gnu/libz.so \
		&& make -j${NPROC})

all: analyzer

analyzer:
	echo ${LLVM_BUILD}
	$(call build_src_func, ${SRC_DIR}, ${SRC_BUILD})

clean:
	rm -rf ${SRC_BUILD}
