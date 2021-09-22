FROM centos
RUN dnf install http://resources.ovirt.org/pub/yum-repo/ovirt-release44.rpm -y 
RUN dnf install python3-ovirt-engine-sdk4 -y 
RUN dnf -y install gcc libxml2-devel python3-devel python3-pyyaml vim && dnf clean all
WORKDIR /root
COPY config.yaml /root/
COPY export_VM_to_OVA.py export_VM_to_OVA-jenkins-args.py /root/
COPY vm_list.yaml /root/
