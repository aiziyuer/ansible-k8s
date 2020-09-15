OpenVSwitch 学习
---

### 开启大页内存

``` bash
sed -i '/GRUB_CMDLINE_LINUX_DEFAULT/d' /etc/default/grub
cat<<'EOF'>>/etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
EOF
grub2-mkconfig -o /boot/grub2/grub.cfg

reboot

grep Huge /proc/meminfo

sed -i '/vm.nr_hugepages/d' /etc/sysctl.d/hugepages.conf
echo 'vm.nr_hugepages=1024' > /etc/sysctl.d/hugepages.conf
sysctl --system

grep Huge /proc/meminfo


sed -i '/hugetlbfs/d' /etc/fstab
cat <<'EOF'>>/etc/fstab
none /dev/hugepages hugetlbfs pagesize=1G 0 0
EOF
mount -a

```

### 安装DPDK

``` bash
yum install -y numactl-devel automake gcc gcc-c++ elfutils-libelf-devel kernel-devel
yum install -y "kernel-devel-uname-r == $(uname -r)"

export DPDK_DIR=/usr/src/dpdk && mkdir -p ${DPDK_DIR}
export DPDK_TARGET=x86_64-native-linuxapp-gcc
export DPDK_BUILD=$DPDK_DIR/$DPDK_TARGET
curl -ssL https://fast.dpdk.org/rel/dpdk-2.2.0.tar.xz \
  | tar xJ --strip-components=1 -C ${DPDK_DIR}

sed -i 's/^CONFIG_RTE_BUILD_COMBINE_LIBS=.*/CONFIG_RTE_BUILD_COMBINE_LIBS=y/g' ${DPDK_DIR}/config/common_linuxapp
sed -i 's/^CONFIG_RTE_LIBRTE_KNI=.*/CONFIG_RTE_LIBRTE_KNI=n/g' ${DPDK_DIR}/config/common_linuxapp
sed -i 's/^CONFIG_RTE_KNI_KMOD=.*/CONFIG_RTE_KNI_KMOD=n/g' ${DPDK_DIR}/config/common_linuxapp
cd ${DPDK_DIR} && make install -j8 T=$DPDK_TARGET DESTDIR=install
```

### 编译OVS:

```bash
# 安装依赖
yum install -y openssl-devel gcc make autoconf automake libpcap-devel libcap-ng-devel \
    python-sphinx python-devel graphviz rpm-build redhat-rpm-config libtool python-twisted-core python-zope-interface groff checkpolicy selinux-policy-devel

export OVS_DIR=/usr/src/openvswitch && mkdir -p ${OVS_DIR}
curl -ssL https://www.openvswitch.org/releases/openvswitch-2.5.10.tar.gz \
  | tar xz --strip-components=1 -C ${OVS_DIR}

cd ${OVS_DIR} && ./boot.sh
cd ${OVS_DIR} && ./configure --with-dpdk=$DPDK_BUILD CFLAGS="-g -O2 -Wno-cast-align"
cd ${OVS_DIR} && make -j 8 install CFLAGS='-O3 -march=native'

# 创建db
mkdir -p /usr/local/etc/openvswitch
mkdir -p /usr/local/var/run/openvswitch
rm -rf /usr/local/etc/openvswitch/conf.db
ovsdb-tool create /usr/local/etc/openvswitch/conf.db  \
            /usr/local/share/openvswitch/vswitch.ovsschema

ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
      --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
      --private-key=db:Open_vSwitch,SSL,private_key \
      --certificate=Open_vSwitch,SSL,certificate \
      --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert --pidfile --detach

ovs-vsctl --no-wait init


mount -t hugetlbfs -o pagesize=2MB none /dev/hugepages_2mb


# 启动ovs
ovs-vswitchd --dpdk -c 0x1 -n 4 --socket-mem 1024,0 \
   -- unix:/usr/local/var/run/openvswitch/db.sock --pidfile --detach

# 检查进程
ps -ef | grep ovs
ovs-vsctl --version
```


### FAQ
- [Open vSwitch2.3.0版本安装部署及基本操作](https://www.sdnlab.com/3166.html)
- [Ovs+Dpdk简单实践](https://www.sdnlab.com/16593.html)
- [ovs版本配套关系](https://docs.openvswitch.org/en/latest/faq/releases/)
- [ovs2.5安装指南(DPDK)](https://www.openvswitch.org/support/dist-docs-2.5/INSTALL.DPDK.md.txt)







