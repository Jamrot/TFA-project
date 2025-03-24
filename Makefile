CUR_DIR = $(shell pwd)
LLVM_BUILD := /app/llvm-project/build
SRC_DIR := ${CURDIR}/src
SRC_BUILD := ${CURDIR}/build

NPROC := $(shell sysctl -n hw.ncpu 2>/dev/null || nproc)

build_src_func = \
	(mkdir -p ${2} \
		&& cd ${2} \
		&& PATH=${LLVM_BUILD}/bin:${PATH}\
			CC=clang CXX=clang++ \
			cmake ${1} \
				-DCMAKE_BUILD_TYPE=Release \
        		-DCMAKE_CXX_FLAGS_RELEASE="-std=c++14 -fno-rtti -fpic -fopenmp -O3" \
				-DLLVM_INSTALL_DIR=${LLVM_USED} \
				-DZLIB_INCLUDE_DIR=/usr/include \
		&& make -j${NPROC})

all: analyzer

analyzer:
	echo ${LLVM_BUILD}
	$(call build_src_func, ${SRC_DIR}, ${SRC_BUILD})

clean:
	rm -rf ${SRC_BUILD}
