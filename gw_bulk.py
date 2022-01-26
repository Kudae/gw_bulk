import requests 
import urllib3
import json
import time
import sys
import os

#remove insecure https warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# global variables 
global gwbullk
gwbulk = '/tmp/gw_bulk/gw_bulk_'
global log
log = f'{gwbulk}log.log'

# logout of existing session and end script
def end():
        logout(sid)
        sys.exit(0)

# -d or -h
def helpmenu():

    global debug
    if len(sys.argv) > 1 and sys.argv[1] == "-h": 
        print(
            '''
            [ Help Menu ]

            Purpose: 
            Run command against all gateways on a domain
            OR
            All gateways in the environment. 

            Usage: 
            ./gw_bulk OPTIONS

            Options:
            -d = Debugging
            -h = Usage 

            Notes: 
            Built for x86_64 linux systems. 

            This is a pyinstaller onefile binary
            that includes all required modules. 
            '''
        )
        end()
    elif len(sys.argv) > 1 and sys.argv[1] == "-d":
        print('\n[ Debug Mode Enabled ]\n') 
        debug = 1
    else: 
        print('\n[ Debug Mode Disabled ]\n')
        debug = 0
    
    return debug

#input validation
def question(stuff):
    while True:
        answer = input(f"\n{stuff}:\n")
        if len(answer) is not 0:
            False
            return answer 

# ask user for configuration 
def askConfig():

    print("\n[ Provide API/CMA/Domain Configuration ]\n")

    global username, password, api_ip, api_port, domain

    username = question("Username")
    password = question("Password")
    api_ip = question("API (MDM) IP Address")
    api_port = question("API Port")
    domain = question("Domain Name (in SmartConsole)")

    formatanswer = f"""username = {username}
password = {password}
API IP = {api_ip}
API Port = {api_port}
Domain Name = {domain}
"""  

    result = question(f"\n{formatanswer}\nIs this information correct? (y/n)")   
    if result == "n":
        askConfig()
    elif result == "y": 
        print("\nContinuing... \n")

# make log directory / clear old log files
def gw_mkdir():

    print(f'[ Dir: {gwbulk} ]\n')

    if os.path.isdir(gwbulk):
        print('... Exists!\n')
        print('\n[ Clearing old logs ]\n')
        os.system(f'rm -v {gwbulk}/gw_rename_*')
    else:
        print(f'... Created!\n')
        os.mkdir(gwbulk)

# sleep function
def sleeptime(timeval): 
    time.sleep(timeval)


###Debugging Functions###
# take any input to pause script
def pause_debug():
    input("\n[ DEBUG ] Press any key to continue...\n")   

def pause_script():
    input("\n[ Check and Verify ]. Press any key to continue...\n") 

###API###
# API Log
def api_debug(defname, apiurl, headers, body, result, api_post): 

    apiBugs = [
    f"\n\n[ {defname} ]\n",
    f"{defname} : URL : {apiurl} \n",
    f"{defname} : Headers : {headers} \n",
    f"{defname} : Body : {body} \n",
    f"{defname} : JSON RESPONSE : \n{result}\n",
    f"{defname} : Status Code: {api_post.status_code}\n"
    ]

    with open(log, 'a') as f:
        f.writelines(apiBugs)

# API Login
def login(): 

    print("\n[ Login to API ]\n")

    defname = f"API : Login : {domain}"
    
    api_url = f'{url}/login'
    headers = {'Content-Type' : 'application/json'}
    body = {'user' : f'{username}', 
            'password' : f'{password}',
            'domain' : f'{domain}',
            'session-timeout' : 1800}

    api_post = requests.post(api_url, data = json.dumps(body), headers=headers, verify=False)
    result = json.loads(api_post.text)

    sleeptime(1)
    api_debug(defname, api_url, headers, body, result, api_post)

    response = api_post.status_code
    if response == 200: 
        print(f'{response}... Log in Successful.\n')
    else: 
        print(f'{response}... Login Failed.\n')

# API Publish 
def publish(): 

    print("\n[ Publish Changes ]\n")
    defname = f"API : Publish : {domain}"

    api_url = f'{url}/publish'
    x = sid["sid"]
    headers = {'Content-Type' : 'application/json',
                'X-chkp-sid' : f'{x}'} 
    body = {}

    api_post = requests.post(api_url, data=json.dumps(body), headers=headers, verify=False)
    result = api_post.json() 

    sleeptime(1)
    api_debug(defname, api_url, headers, body, result, api_post)

    response = api_post.status_code
    if response == 200: 
        print(f'{response}... Publish Successful.\n')
    else: 
        print(f'{response}... Publish Failed.\n')

# API Logout
def logout(): 

    print("\n[ Log out of session ]\n")

    defname = f"API : Logout : {sid['sid']}"

    api_url = f'{url}/logout'
    x = sid["sid"]
    headers = {'Content-Type' : 'application/json',
                'X-chkp-sid' : f'{x}'} 
    body = {}
    api_post = requests.post(api_url, data=json.dumps(body), headers=headers, verify=False)
    result = api_post.json()

    sleeptime(1)
    api_debug(defname, api_url, headers, body, result, api_post)

    response = api_post.status_code
    if response == 200: 
        print(f'{response}... Logged out\n')
    else: 
        print(f'{response}... Logout failed\n')


###List Gateways, Clusters, Cluster Members###
def show_simple(config, body):

    print(f"\n[ API : Generate {config} Object List : {domain}]\n")
    defname = f"API : Show Simple {config} : {domain}"
    
    api_url = f'{url}/show-simple-{config}'
    x = sid["sid"]
    headers = {'Content-Type' : 'application/json',
                'X-chkp-sid' : f'{x}'} 
    body = {}

    api_post = requests.post(api_url, data=json.dumps(body), headers=headers, verify=False)
    result = api_post.json()

    sleeptime(1)
    api_debug(defname, api_url, headers, body, result, api_post)

    if config == 'gateways':
        global gatewaylist
        gatewaylist = [] 
        for gw in result['objects']:
            gatewaylist.append(gw['name'])
        
        print(f"[ API: GATEWAY LIST ]\n{gatewaylist}\n")

    if config == 'clusters':
        global clusterlist
        clusterlist = [] 
        for i in result['objects']:
            clusterlist.append(i['name'])
        print(f"[ API: CLUSTER OBJECT LIST ]\n{clusterlist}\n")

    if config == 'members':
        global memberlist
        memberlist = [] 
        for i in result['cluster-members']:
            memberlist.append(i['name'])
        print(f"[ API: CLUSTER MEMBER LIST ]\n{memberlist}\n")
    

### Collect script from user ###
def runscript(): 

    print(f"\n[ API: Run-Script : {domain}]\n")
    defname = f"API : Run-Script : {domain}"

    global cmd
    cmd = question("Paste entire command below to run on gateways")
    
    api_url = f'{url}/run-script'
    x = sid["sid"]
    headers = {'Content-Type' : 'application/json',
                'X-chkp-sid' : f'{x}'} 
    body = {'script-name' : f'{defname}',
    'script' : f'{cmd}',
    'targets' : f'{targets}',
    'comments' : f'{cmd}'}

    api_post = requests.post(api_url, data=json.dumps(body), headers=headers, verify=False)
    result = api_post.json()

    sleeptime(1)
    api_debug(defname, api_url, headers, body, result, api_post)


def main():

    helpmenu()

    global sid 
    sid = login()

    global url
    url = f'https://{api_ip}:{api_port}/web_api'

    # get gateways and cluster lists from domain / API
    show_simple('gateways', body = {})
    show_simple('clusters', body = {})

    global completemembers
    completemembers = [] 

    for c in clusterlist:
        show_simple('members', body = {'name' : f'{c}'})
        completemembers.append(memberlist)
    print(f"[ API: COMPLETE MEMBER LIST ]\n{completemembers}\n")
    
    global targets
    targets = gatewaylist + completemembers

    runscript()


if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"[ Error ]\n{e}\n")
    finally:
        end()
