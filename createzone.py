import CloudFlare
import os
import sys


def main():
    cf = CloudFlare.CloudFlare(
        email='', token='')
    file = open('domains.txt').readlines()
    for domain in file:
        zone_name = domain

        # print('Create zone %s ...' % (zone_name))
        # try:
        #     zone_info = cf.zones.post(
        #         data={'jump_start': False, 'name': zone_name})
        # except CloudFlare.exceptions.CloudFlareAPIError as e:
        #     print('Бэээээ ', e)

        # zone_info = cf.zones.get(params={'name': zone_name})
        # print(zone_info)
        # zone_id = zone_info['id']
        # if 'email' in zone_info['owner']:
        #     zone_owner = zone_info['owner']['email']
        # else:
        #     zone_owner = '"' + zone_info['owner']['name'] + '"'
        # zone_plan = zone_info['plan']['name']
        # zone_status = zone_info['status']
        # print('\t%s name=%s owner=%s plan=%s status=%s\n' % (
        #     zone_id,
        #     zone_name,
        #     zone_owner,
        #     zone_plan,
        #     zone_status
        # ))

        # DNS records to create
        zone_info = cf.zones.get(params={'name': zone_name})
        for zone_id in zone_info:
            zone_id = zone_info[0]['id']
            print(zone_id)

            dns_records = [
                {'name': '@', 'type': 'A', 'content': '65.21.203.49'},
            ]
            print(dns_records)

            print('Create DNS records ...')
            for dns_record in dns_records:
                # Create DNS record
                try:
                    r = cf.zones.dns_records.post(zone_id, data=dns_record)
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    continue
                # ('/zones.dns_records.post %s %s - %d %s' %
                #  (zone_name, dns_record['name'], e, e))
                # Print respose info - they should be the same
                dns_record = r
                print('\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
                    dns_record['id'],
                    dns_record['name'],
                    dns_record['ttl'],
                    dns_record['type'],
                    dns_record['content'],
                    dns_record['proxied'],
                    dns_record['proxiable']
                ))

                # set proxied flag to false - for example
                dns_record_id = dns_record['id']

                new_dns_record = {
                    # Must have type/name/content (even if they don't change)
                    'type': dns_record['type'],
                    'name': dns_record['name'],
                    'content': dns_record['content'],
                    # now add new values you want to change
                    'proxied': True
                }

                try:
                    dns_record = cf.zones.dns_records.put(
                        zone_id, dns_record_id, data=new_dns_record)
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    exit('/zones/dns_records.put %d %s - api call failed' % (e, e))

            print('')

            # Now read back all the DNS records
            print('Read back DNS records ...')
            try:
                dns_records = cf.zones.dns_records.get(zone_id)
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                exit('/zones.dns_records.get %s - %d %s' % (zone_name, e, e))

            for dns_record in sorted(dns_records, key=lambda v: v['name']):
                print('\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
                    dns_record['id'],
                    dns_record['name'],
                    dns_record['ttl'],
                    dns_record['type'],
                    dns_record['content'],
                    dns_record['proxied'],
                    dns_record['proxiable']
                ))

            print('')


if __name__ == '__main__':
    main()
