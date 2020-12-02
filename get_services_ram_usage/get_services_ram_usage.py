#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('service_file')
    args = argp.parse_args()
    service_file = args.service_file
    with open(service_file) as f:
        services = f.readlines()

    usages = []
    for service in services:
        service = service.split(',', 1)[0]
        service = service.strip()
        if not service:
            continue

        try:
            out = subprocess.check_output(['systemctl', '-p', 'ExecMainPID', 'show', service])
        except subprocess.CalledProcessError as e:
            print('get pid of service "%s" failed, err=%s' % (service, e))
            usages.append('{},{}\n'.format(service, 0.0))
            continue

        try:
            _, pid = out.split('=')
            pid = int(pid)
        except ValueError:
            print('get pid of service "%s" failed' % service)
            usages.append('{},{}\n'.format(service, 0.0))
            continue

        if not pid:
            print('get pid of service "%s" failed, pid=0' % service)
            usages.append('{},{}\n'.format(service, 0.0))
            continue

        # print('{}, pid={}'.format(service, pid))
        try:
            out = subprocess.check_output("ps -lax | grep %s | grep -v grep | awk '{sum+=$8}END{print sum}'" % pid, shell=True)
            ram_usage_kb = int(out)
            ram_usage_mb = ram_usage_kb / 1024.0
        except subprocess.CalledProcessError as e:
            print('get service "%s"(pid=%s) ram usage failed, err=%s' % (service, pid, e))
            usages.append('{},{}\n'.format(service, 0.0))
            continue

        usages.append('{},{:.3f}\n'.format(service, ram_usage_mb))

    with open(service_file, 'w') as f:
        f.writelines(usages)


if __name__ == '__main__':
    main()
