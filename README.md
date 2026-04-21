'SecMark DDoSsia Monitor' is a tool to monitor if specific URLs, TLDs or IP addresses have ended up on the NoName057(16) DDoSsia projects target list.

Created this in a few hours so will need to return to this spaghetti code later to make it pretty and add more options. 

Command line utility. 
for help:
```bash
DDoSsia_mononitor.py -h
```

   
# Email Sending Version
## Entra ID / Exchange 
1. **In Exchange Online, create a new Shared mailbox that you'll use for sending emails**
   > https://admin.cloud.microsoft/exchange#/mailboxes  
3. **In Entra ID Create a new app registration with **application** permission **Mail.Send****
   > https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade/quickStartType~/null/sourceType/Microsoft_AAD_IAM
4. **Create a secret for the application**
5. **Create application access policy to limit the access of the application**
   > https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/new-applicationaccesspolicy?view=exchange-ps
7. **Grant Admin consent for the application**
   > (If I remember correctly the minimum required role is Cloud Application Administrator)

## On Server 
Instructions to setting this up on your random linux box
1. **Make directory for the script**
   ```bash
   sudo mkdir /usr/local/bin/DDoSsiaMonitor
   ```

2. **Please the script into the folder**

3. **Modify the script by filling the missing details.**
   ```python
   from_address = ""
   to_address = ""

   credential = ClientSecretCredential(
       tenant_id="",
       client_id="",
       client_secret="")
   ```

2. **Move to the directory**
   ```bash
   cd /usr/local/bin/DDoSsiaMonitor
   ```

3. **Prepare Python venv**
   ```bash
   sudo python3 -m venv .
   ```
4. **Install Python Requirements**
   ```bash
   sudo ./bin/pip3 install msgraph-sdk
   ```
5. **Prepare targets file**
   ```bash
   sudo nano targets.txt
   ```
   Fill file with wanted targets
6. **Test Usage**
   ```bash
   ./bin/python3 DDoSsia_monitor_emailMsGraph.py -tf targets.txt
   ```
7. **Create a Cronjob**
   ```bash
   sudo crontab -e
   ```
   Insert to the File:
   ```bash
   */5 * * * * /usr/local/bin/DDoSsiaMonitor/bin/python3 /usr/local/bin/DDoSsiaMonitor/DDoSsia_monitor_emailMsGraph.py -tf /usr/local/bin/DDoSsiaMonitor/targets.txt >> /usr/local/bin/DDoSsiaMonitor/log.txt
   ```
   - Above job will run every 5 minutes, adjust however you feel would be suitable for you. Remember this is fetching data from witha.name so please don't spam them 😊
   - Also good to note that if you make this like 1 minute, and there are hits, you'll get one email every minute, there currently is no history feature.
   - log.txt is there to also create very basic logging
8. **Verify that cronjobs work by viewing the log file after X duration**
   ```bash
   cat log.txt
   ```
   - It should be appended with "[]" if there are no hits
