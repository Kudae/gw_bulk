[ Description ] 

Run BASH commands across all gateways on given domain on MDM.  



[ Instructions ] 

1. Enter relevant API/Domain Information


2. Allow the script to get all gateways/cluster members from the domain. 


3. Enter the command you wish to run on the system 


4. Decide how long it will take to run said command. 

From my Lab: 

Example: 

fw stat ~ taking around 10 seconds to complete task on gateway 
hostname ~ took around 1 second
ioc_feeds commands ~ may take around 20 - 30 seconds per gateway


5. Monitor the task output. 


[ API Log ] 

Located in /tmp/gw_bulk/
