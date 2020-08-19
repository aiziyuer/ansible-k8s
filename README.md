项目说明
===

这里主要归档平时对kubernetes的自动化安装过程

### 协作约定

``` bash
# redhat
yum install -y gcc python36-devel openssl-devel
yum install -y sshpass openssh-clients

# ubuntu
apt install -y python3-pip
apt install -y sshpass

# 保存当前类库
# pip3 freeze > requirementes.txt

# 恢复类库
pip3 install -r requirementes.txt

# 清除所有虚环境的包 !! 危险 !!
pip3 freeze | xargs pip3 uninstall -y

# ssh_config设置样例
cat <<'EOF'>/root/.ssh/config
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
EOF

```


