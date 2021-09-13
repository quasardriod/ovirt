# See the License for the specific language governing permissions and
# limitations under the License.
#

# import logging
# import time
# import request
import os
import sys
import yaml
import ovirtsdk4 as sdk
import ovirtsdk4.types as types


def load_settings():
    global SETTINGS
    global OVIRT_VMS
    app_dir = os.path.dirname(os.path.realpath(__file__))
    
    if not os.path.exists("{}/config.yaml".format(app_dir)):
        sys.exit("Error! Could not find config.yaml in App directory: {}".format(app_dir))
        return False
    
    if not os.path.exists("{}/vm_list.yaml".format(app_dir)):
        sys.exit("Error! Could not find vm_list.yaml in App directory: {}".format(app_dir))
        return False
    
    with open("{}/config.yaml".format(app_dir), 'r') as stream:
        try:
            SETTINGS = yaml.safe_load(stream)
        
            if 'ovirt' not in SETTINGS:
                sys.exit("Error! ovirt variable not found in config.yaml")
            if 'ovirt_hosts' not in SETTINGS:
                sys.exit("Error! ovirt_hosts variable not found in config.yaml")
            if 'exported_vms_volume' not in SETTINGS:
                sys.exit("Error! exported_vms_volume variable not found in config.yaml")
            if 'ca_cert' not in SETTINGS:
                sys.exit("Error! ca_cert variable not found in config.yaml")
            if not os.path.exists(SETTINGS['ca_cert']):
                sys.exit("Error! CA cert is missing: {}".format(SETTINGS['ca_cert']))
        
        except yaml.YAMLError as exc:
            sys.exit("Error when parsing config.yaml: {}".format(exc))
            return False
    
    with open("{}/vm_list.yaml".format(app_dir), 'r') as stream:
        try:
            OVIRT_VMS = yaml.safe_load(stream)
        
            if 'ovirt_vms' not in OVIRT_VMS:
                sys.exit("Error! ovirt_vms variable not found in vm_list.yaml")    
            if len(OVIRT_VMS['ovirt_vms']) == 0:
                sys.exit("Error! ovirt_vms list is empty in vm_list.yaml")

        except yaml.YAMLError as exc:
            sys.exit("Error when parsing vm_list.yaml: {}".format(exc))
            return False
    
    return SETTINGS, OVIRT_VMS
    

def ovirt_vm_export():
    load_settings()

    # Ovirt host specific vars
    target_host = SETTINGS['ovirt_hosts'][0]
    host_search_str = 'name' + '=' + target_host

    print("Backup will be triggered for following vms: \n{}".format(OVIRT_VMS['ovirt_vms']))
    print("Target Ovirt host: {}".format(target_host))  
    
    sys.exit()("exit 0")
    # This example shows how to export a virtual machine as a Virtual
    # Appliance (OVA) file to a specified path on a host.
    # Create the connection to the server:
    connection = sdk.Connection(
        url=SETTINGS['ovirt']['url'],
        username=SETTINGS['ovirt']['user'],
        password=SETTINGS['ovirt']['password'],
        ca_file=SETTINGS['ca_cert'],
        debug=True,
    #    log=logging.getLogger(),
    )

    # Find the host:
    hosts_service = connection.system_service().hosts_service()
    host = hosts_service.list(search=host_search_str)[0]

    # Find the virtual machine:
    vms_service = connection.system_service().vms_service()
    for read_vm in OVIRT_VMS['ovirt_vms']:
        vm_search_str = 'name' + '=' + read_vm
        vm_info = vms_service.list(search=vm_search_str)[0]
        print(vm_info)

    
    # Export the virtual machine. Note that the 'filename' parameter is
    # optional, and only required if you want to specify a name for the
    # generated OVA file that is different from <vm_name>.ova.
    # Note that this operation is only available since version 4.2 of
    # the engine and since version 4.2 of the SDK.
    vm_service.export_to_path_on_host(
        host=types.Host(id=host.id),
        directory=SETTINGS['exported_vms_volume'],
        filename='maas-ansible-controller-9.ova''franz-ubuntu01.ova'
    )

    # Close the connection to the server:
    connection.close()

ovirt_vm_export()