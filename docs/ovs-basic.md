## openvswitch 学习

# CentOS7 开启

现在的 CentOS7(7.8.2003)都是内核态自带了`openvswitch.ko`, 可以通过如下命令`modinfo openvswitch`, 我这里:

```
filename:       /lib/modules/3.10.0-1127.el7.x86_64/kernel/net/openvswitch/openvswitch.ko.xz
alias:          net-pf-16-proto-16-family-ovs_packet
alias:          net-pf-16-proto-16-family-ovs_flow
alias:          net-pf-16-proto-16-family-ovs_vport
alias:          net-pf-16-proto-16-family-ovs_datapath
license:        GPL
description:    Open vSwitch switching datapath
retpoline:      Y
rhelversion:    7.8
srcversion:     A0E0E36B77DC28BC8DE7469
depends:        nf_conntrack,nf_nat,libcrc32c,nf_nat_ipv6,nf_nat_ipv4,nf_defrag_ipv6
intree:         Y
vermagic:       3.10.0-1127.el7.x86_64 SMP mod_unload modversions 
signer:         CentOS Linux kernel signing key
sig_key:        69:0E:8A:48:2F:E7:6B:FB:F2:31:D8:60:F0:C6:62:D8:F1:17:3D:57
sig_hashalgo:   sha256
```

安装dpdk的组件`yum install -y dpdk-tools dpdk`, `dpdk-devbind --status`查看当前网卡绑定状态:

```
Network devices using kernel driver
===================================
0000:0b:00.0 'VMXNET3 Ethernet Controller 07b0' if=ens192 drv=vmxnet3 unused= *Active*
0000:13:00.0 '82574L Gigabit Network Connection 10d3' if=ens224 drv=e1000e unused= *Active*

No 'Crypto' devices detected
============================

No 'Eventdev' devices detected
==============================

No 'Mempool' devices detected
=============================

No 'Compress' devices detected
==============================
```


下面只需要安装必要的外围工具即可:

```bash

# 安装用户态的工具
curl -o /etc/yum.repos.d/leifmadsen-ovs-master-epel-7.repo \
      https://copr.fedorainfracloud.org/coprs/leifmadsen/ovs-master/repo/epel-7/leifmadsen-ovs-master-epel-7.repo
yum install -y openvswitch

# 创建db
ovsdb-tool create /etc/openvswitch/conf.db

# 初始化db
ovsdb-server -v --remote=punix:/var/run/openvswitch/db.sock --remote=db:Open_vSwitch,Open_vSwitch,manager_options --private-key=db:Open_vSwitch,SSL,private_key --certificate=db:Open_vSwitch,SSL,certificate --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert --pidfile --detach
ovs-vsctl --no-wait init

# 启动ovs
ovs-vswitchd --pidfile --detach

# 检查进程
ps -ef | grep ovs
ovs-vsctl --version

```




## FAQ
[Open vSwitch2.3.0版本安装部署及基本操作](https://www.sdnlab.com/3166.html)
