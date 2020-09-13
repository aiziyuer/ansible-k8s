源码级编译(不推荐)
---

```bash
yum install -y epel-release

yum install -y git cmake gcc autoconf automake device-mapper-devel \
   sqlite-devel pcre-devel libsepol-devel libselinux-devel \
   automake autoconf gcc make glibc-devel glibc-devel.i686 kernel-devel \
   libpcap libpcap-devel numactl-devel numactl net-tools \
   fuse-devel pciutils libtool openssl-devel libpciaccess-devel CUnit-devel libaio-devel

yum install -y "kernel-devel-uname-r == $(uname -r)"

export RTE_SDK="/usr/src/dpdk"
export RTE_TARGET="x86_64-native-linuxapp-gcc"

mkdir -p ${RTE_SDK} && cd ${RTE_SDK}
curl -sSL https://fast.dpdk.org/rel/dpdk-19.11.4.tar.xz \
 | tar -xJv --strip-components=1 -C .

make config T=x86_64-native-linuxapp-gcc
make
make install T=x86_64-native-linuxapp-gcc O=x86_64-native-linuxapp-gcc

cd /usr/src/dpdk/build/kmod
modprobe uio
insmod igb_uio.ko
lsmod | grep uio

ifconfig ens192 down
cd /usr/src/dpdk/usertools/
./dpdk-devbind.py --bind=igb_uio ens192

mkdir -p /mnt/huge
mount -t hugetlbfs nodev /mnt/huge
echo 1024>/sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages

```
