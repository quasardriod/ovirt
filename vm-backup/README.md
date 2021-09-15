# oVirt VM backup using jenkins (Run code directly from jenkins UI)

## Setup jenkins job param

1. ovirt_vm  # Type String
2. ovirt_api_url  # Type String and set URL as default value
3. ovirt_user # Type String
4. ovirt_password # Type Password
5. ca_cert # Type String and set ca cert path as default value
6. ovirt_host # Type Choice and define list of hosts
7. exported_vms_volume # Type Choice and list NFS volumes