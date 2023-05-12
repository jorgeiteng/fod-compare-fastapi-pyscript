import json
import requests
import csv
import xlwt

# Fetch config from config.json
def config():
    with open('.config.json') as f:
        return json.load(f)
    # return something like this:
    # {
    #     "url": "https://api.ams.fortify.com",
    #     "username": "******",
    #     "password": "******",
    #     "tenant": "tenantname"
    # }
    
# Authenticate
def authenticate(config):
    c = config
    # can use either password or client credentials -- comment out one of the next two lines accordingly
    # with requests.post(f"{c['url']}/oauth/token", data={"grant_type":"client_credentials","scope":"api-tenant","client_id":f"{c['apikey']}","client_secret":f"{c['secret']}"}) as r:
    with requests.post(f"{c['url']}/oauth/token", data={"grant_type":"password","scope":"api-tenant","username":f"{c['tenant']}\{c['username']}","password":f"{c['password']}","security_code":""}) as r:
        return json.loads(r.text)
        
# Fetch scan summary through REST
#       Example: https://api.ams.fortify.com/api/v3/scans/6395564/summary
def scansummary(config, authentication, id):
    c = config
    a = authentication
    with requests.get(f"{c['url']}/api/v3/scans/{id}/summary", headers={"authorization":f"Bearer {a['access_token']}"}) as r:
        return json.loads(r.text)

# Fetch manifest through REST
#       Example: https://api.ams.fortify.com/api/v3/scans/6395564/manifest
def manifest(config, authentication, id):
    c = config
    a = authentication
    with requests.get(f"{c['url']}/api/v3/scans/{id}/manifest", headers={"authorization":f"Bearer {a['access_token']}"}) as r:
        return r.text.strip()

# This makes a dictionary where property values differ between runs
def differences(scansummary, prefix: str=""):
    r = {}
    x = scansummary[0]
    for k in x:
        v = []
        m = True
        l = x.get(k)
        for y in scansummary:
            z = y.get(k)
            v.append(z)
            if z!=l: m = False
        if isinstance(l, str) or not hasattr(l,'__iter__'):     # check isString or not-iterable type (primitives like int, bool, etc)
            if m==False:     # only append to results if different
                r[f"{prefix}{k}"] = v
        else: 
            z = differences(v, f"{prefix}{k}.")  # for non-string iterables recursively call this function, appending key prefix
            for w in z:
                r[w]=z.get(w)
    return r

# Makes a dictionary of all manifest files -- columns of sizes & dates for comparison
def merge(manifest):
    r = {}
    i = 0
    for y in manifest:
        for l in csv.reader(y.splitlines(), delimiter = ' ', skipinitialspace=True):
            p = l[0]
            if r.get(p) is None:
                r[p]=[None] * (len(manifest) * 2)

            r[p][i]=int(l[1])               # keep all field 1's (size?) together
            r[p][(len(manifest)+i)]=l[2]    # keep all field 2's (date) together
        i+=1
    return r

def fetchScans(ids):
    # Get config details and logon
    c = config()
    a = authenticate(c)

    # Setup a variable to hold our ScanIds and the rest outputs
    x = {"id": ids}
    s = []
    m = []
    for id in x["id"]:
        s.append(scansummary(c,a,id))
        m.append(manifest(c,a,id))
    x["data"]=s
    x["differences"]=differences(s)     # Enumerate the differences
    x["manifest"]=merge(m)              # merge the manifests

    # Spool results to JSON file
    with open(f"differences.json","w") as f:
        json.dump(x, f)

    # Spool results to XLS file
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Differences")
    ws.write(0,0,"Property")
    j = 0
    for k in x["differences"]:
        for i in range(len(x["id"])):
            if (j==0) :
                ws.write(j,i+1,f"ScanId: {x['id'][i]}")
            if (i==0) : ws.write(j+1,0,f"{k}")
            v = x["differences"][k]
            ws.write(j+1,i+1,v[i])
        j+=1
    ws = wb.add_sheet("Manifest")
    ws.write(0,0,"Path")
    j = 0
    for k in x["manifest"]:
        for i in range(len(x["id"])):
            if (j==0) :
                ws.write(j,i+1,f"Sz: {x['id'][i]}")
                ws.write(j,i+len(x["id"])+1,f"Dt: {x['id'][i]}")
            if (i==0) : ws.write(j+1,0,f"{k}")
            v = x["manifest"][k]
            ws.write(j+1,i+1,v[i])
            ws.write(j+1,i+len(x["id"])+1,v[(len(x["id"])+i)])
        j+=1
    wb.save("Differences.xls")

# Fetch comparisons of these scans
fetchScans([6395564, 6395413, 6386441])