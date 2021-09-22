#!/usr/bin/env python3

# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import yaml
import ovirtsdk4 as sdk
import ovirtsdk4.types as types


if len(sys.argv[1:]) != 7:
    sys.exit(""" Error! Missing arguments. Arguments must be passed in below listed sequence.
1. oVirt API url
2. oVirt User
3. oVirt Password
4. CA Cert path
5. VM name (or comma separated list "vm1,vm2")
6. oVirt Host
7. NFS path to export VM (volume must be mounted in oVirt host)
""")

ovirt_url = sys.argv[1]
ovirt_user = sys.argv[2]
ovirt_passwd = sys.argv[3]
ca_cert = sys.argv[4]
target_vm = sys.argv[5]
ovirt_host = sys.argv[6]
exported_vms_volume = sys.argv[7]

if not os.path.exists(ca_cert):
    print("\n Error! CA cert is missing: {}".format(ca_cert))
            
# Ovirt host specific vars
host_search_str = 'name' + '=' + ovirt_host

print("\n Backup will be triggered for following vms:")
for _vm in target_vm.split(','):
    print(_vm)
    
print("\n Target Ovirt host: {}".format(ovirt_host))  
    
    # This example shows how to export a virtual machine as a Virtual
    # Appliance (OVA) file to a specified path on a host.
    # Create the connection to the server:
connection = sdk.Connection(
    url=ovirt_url,
    username=ovirt_user,
    password=ovirt_passwd,
    ca_file=ca_cert,
    debug=True,
#    log=logging.getLogger(),
)
    
# Find the host:
hosts_service = connection.system_service().hosts_service()
host = hosts_service.list(search=host_search_str)[0]
print("\n Host info: \n href: {} \n ID: {} \n Name: {}".format(host._href, host._id, host._name))

# Find the virtual machine:
vms_service = connection.system_service().vms_service()
    
for _vm in target_vm.split(','):
    vm_search_str = 'name' + '=' + _vm
    vm_info = vms_service.list(search=vm_search_str)[0]
    vm_exported_file = vm_info.name + ".ova"
    print("\n VM info: \n href: {} \n ID: {} \n Name: {}".format(vm_info._href, vm_info._id, vm_info._name))
    vm_task = vms_service.vm_service(vm_info.id)

        # Export the virtual machine. Note that the 'filename' parameter is
        # optional, and only required if you want to specify a name for the
        # generated OVA file that is different from <vm_name>.ova.
        # Note that this operation is only available since version 4.2 of
        # the engine and since version 4.2 of the SDK.
    vm_task.export_to_path_on_host(
        host=types.Host(id=host.id),
        directory=exported_vms_volume,
        filename=vm_exported_file
    )

# Close the connection to the server:
connection.close()
