import os
import csv
from ..importer.scraper import search_vuln
from ..importer.time_func import time_func
from ..models import Issues
from vulnerabilities.models import *


def read_csv(path):
    if not os.path.exists(path):
        return

    vulnerabilities = {}

    with open(path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # toss headers
        for data in reader:
            vulnerabilities[data[6]] = {
                # 'Test Result Code': data[2],
                'Vulnerability ID': data[3],
                # 'CVE ID': data[4],
                'Severity': data[5]
            }

    with open(path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # toss headers
        for data in reader:
            for key, index in [('Hosts', 0), ('Service Ports', 1)]:
                if key in vulnerabilities[data[6]] and data[index] not in vulnerabilities[data[6]][key]:
                    vulnerabilities[data[6]][key].append(data[index])
                else:
                    vulnerabilities[data[6]][key] = [data[index]]
    return vulnerabilities


@time_func
def import_rapid_seven(file: str, case):
    print(f"Importing {file}...")
    data = read_csv(file)
    count = 0
    success = True
    message = ""
    try:
        for key in data:
            #  check if the key can be found in the VulnerabilitiesImported db before doing a search.
            #  Save to model after search if it isn't
            if not VulnerabilitiesImported.objects.filter(title=key).exists():
                vulnerabilityID = data[key]['Vulnerability ID']
                dta = search_vuln(vulnerabilityID)

                # references for get_or_create:
                # https://stackoverflow.com/questions/1941212/correct-way-to-use-get-or-create
                # https://stackoverflow.com/questions/1821176/django-check-whether-an-object-already-exists-before-adding
                dbObj, _ = VulnerabilitiesImported.objects.get_or_create(title=key, description=dta['Detail'],
                                                                         solution=dta['Solution'],
                                                                         reference=dta['References'],
                                                                         severity=data['Severity'])
            else:
                dbObj = VulnerabilitiesImported.objects.filter(title=key).first()

            obj = data[key]
            issue, created = Issues.objects.get_or_create(case=case, name=dbObj.title, severity=dbObj.severity,
                                                          affected_hosts=",".join(str(x) for x in obj['Hosts']),
                                                          description=dbObj.description, solution=dbObj.solution,
                                                          reference=dbObj.reference)
            if created:
                count += 1
    except Exception as e:
        message = str(e)
        success = False

    return success, count, message
