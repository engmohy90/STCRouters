import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand

from routerApp.models import Port, Slot, Router, Neighbor


class Command(BaseCommand):

    def handle(self, *args, **options):
        full_path = os.path.join(settings.BASE_DIR, 'routers.conf')
        routers_dir = os.listdir(full_path)
        # loop over the 12 conf files and parse data from them
        # neighbors = []
        loading = '*'
        for file_conf in routers_dir:
            print(loading)
            print(file_conf)
            loading += '*'
            input_file = open(os.path.join(full_path, file_conf))
            raw_text_data = input_file.readlines()
            input_file.close()
            parsed_router = self.parse(raw_text_data)
            r = Router(name=file_conf.split('.conf')[0])
            r.save()
            s = []
            for slot in parsed_router['platform']:
                q = Slot(name=slot['slot'], router=r,
                         node_type=slot['node_type'], speed=slot['speed'],
                         port_count=int(slot['portNum']), state=slot['state'])
                s.append(q)
            Slot.objects.bulk_create(s)
            p = []
            for port in parsed_router['interface_brief']:
                slot_q = Slot.objects.get(name=port['slot'], router=r.id)
                q = Port(name=port['ports'], router=r,
                         slot=slot_q, ip=port['ip'], state=port['status'])
                p.append(q)
            Port.objects.bulk_create(p)
            n = []
            for neighbor in parsed_router['neighbor']:
                # if (r.name, neighbor['device_id']) in neighbors or (neighbor['device_id'], r.name,) in neighbors:
                #     continue
                # else:
                # neighbors.append((r.name, neighbor['device_id']))

                q = Neighbor(router=r, remote=neighbor['device_id'],
                             router_port=neighbor['local_port'], remote_slot=neighbor['remote_slot'],
                             remote_port=neighbor['remote_port'], router_slot=neighbor['local_slot'], )
                n.append(q)
            Neighbor.objects.bulk_create(n)
        print('successfully finished pulling data')

    @staticmethod
    def parse(raw_text_data):
        router_data = {
            'interface_brief': [],
            'neighbor': [],
            'platform': []
        }
        current_cli = ''
        append_data = False
        for line in raw_text_data:
            if line == '\n':
                append_data = False
                continue
            if re.search(r'.*show ipv4 interface brief.*', line.lower()):
                current_cli = 'interface_brief'
                append_data = False
                continue
            if re.search(r'.*show lldp neighbor.*', line.lower()):
                current_cli = 'neighbor'
                append_data = False
                continue
            if re.search(r'.*show platform.*', line.lower()):
                current_cli = 'platform'
                append_data = False
                continue

            if current_cli == 'interface_brief':
                if re.search(r'.*interface.*', line.lower()):
                    append_data = True
                    continue
                if append_data is True and re.search(r'.*/\d+/\d+/\d+', line) is not None:
                    # "Interface                      IP-Address      Status                Protocol"
                    out = re.compile(" +").split(line)
                    interface = re.compile("/").split(out[0])
                    interface_out = dict()
                    interface_out['slot'] = interface[1]
                    interface_out['ports'] = interface[3]
                    interface_out['ip'] = out[1]
                    interface_out['status'] = out[2]
                    interface_out['protocol'] = out[3]
                    router_data[current_cli].append(interface_out)

            if current_cli == 'neighbor':
                if re.search(r'.*device id.*', line.lower()):
                    append_data = True
                    continue
                if (append_data is True and
                        re.search(r'.*/\d+/\d+/\d+', line) is not None and
                        re.search(r'corencs-.*', line.lower()) is not None):
                    # Device ID       Local Intf          Hold-time  Capability     Port ID
                    z = re.compile(" +").split(line)
                    interface = re.compile("/").split(z[1])
                    remote_interface = re.compile("/").split(z[4])
                    device_id = re.compile("\.").split(z[0])
                    if re.search(r'.*/\d+/\d+/\d+.*', z[4]):
                        remote_interface = re.compile("/").split(z[4])
                    else:
                        remote_interface = re.compile("/").split(z[5])
                    x = dict()
                    x['local_slot'] = interface[1]
                    x['local_port'] = interface[3]
                    x['remote_port'] = remote_interface[3]
                    x['remote_slot'] = remote_interface[1]
                    x['device_id'] = device_id[0]
                    x['local_intf'] = z[1]
                    x['hold-time'] = z[2]
                    x['capability'] = z[3]
                    x['far_intf'] = z[4]
                    router_data[current_cli].append(x)
            if current_cli == 'platform':
                if re.search(r'.*node', line.lower()):
                    append_data = True
                    continue
                if append_data is True and re.search(r'\d+X\d+[^-]*', line) is not None:
                    # Node name         Node type             Node state        Admin state   Config state
                    # NC6-10X100G-M-K
                    z = re.compile(" +").split(line)
                    interface = re.compile("/").split(z[0])
                    node_type = re.compile("\d+X\d+[^-]*").search(z[1])
                    type_str = re.compile("X").split(node_type.group())
                    x = dict()
                    x['slot'] = interface[1]
                    x['portNum'] = type_str[0]
                    x['speed'] = type_str[1]
                    x['node_type'] = z[1]
                    x['state'] = z[2]
                    router_data[current_cli].append(x)
        return router_data
