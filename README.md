# delete-disabled-ad-accounts
Clean your disabled AD accounts safely using this process. These scripts will exclude two csv's of users to give 
you a final list of accounts that are disabled. 

## Features
1. Includes a Python3 script to exclude up to two CSV's of active accounts from all AD accounts.
2. Useful user extraction commands below.
3. A script that will extract users to be deleted as a SQL readable list. 
4. Includes a PowerShell script to delete users. This includes attribute exporting and different functions like deleting
disabled users, all users, or disabling active users and deleteing disabled ones. 


## Disclaimer
It is your responsibility to double and triple check that all users being deleted are disabled and inactive. Make sure to use due diligence.  

## Procedure
1. Extract from your data sources
    1. Get a list of all AD Accounts. There are multiple ways to do this, but if you want to get sensitive data like 
    Employee Id's this will work: 
    ```CSVDE.exe -f C:\Users\user\Desktop\UATCleanup\AllEmployeeResults.csv -s domainControllerName -d "OU=company,dc=domain,dc=com" -p subtree -r "(&(objectCategory=User))" -l "sAMAccountName,employeeId"```
    2. Get a CSV list of AD users that do not have an employee ID. The CSV should contain employee ID and samAccountName
     or CN. In our organization, these users would be considered Service accounts, so they are excluded from deletion. 
    ```Get-ADUser -Filter 'employeeid -notlike "*"' -Properties employeeid -SearchBase "OU=Putnam,DC=ENG2008,dc=com" | select sAMAccountName, EmployeeID | Export-CSV -Append "C:\Users\OIMAgentAD\Desktop\UATCleanup\ResultsNoEmpID.csv" -NoTypeInformation```
    3. Get a CSV list of users from your Identity Manager, whether it's Okta, Oracle Identity Manager, or netIQ, we 
    need to get the active user's matching Employee number and User Login. Make the CSV match accordingly. They should 
    match the users in Active Directory. 
2. extractActiveUsers.py
    1. Change the directories in extractActiveUsers.py to the CSV's you saved. Ensure that the Service accounts file and
    extracted Identity Provider CSV match accordingly. If you do not have a service account CSV, give it a blank file. 
    Note: If you want a database readable list, uncomment the comment block at the end of the file and it will output a 
    list that you can use to cross check against your Identity Provider's Database.
    2. Change the output directories to location that you want to have them placed.
    3. Run the script ```python3 extractActiveUsers.py```
3. Cross Check
    1. For the health and safety of yourself and your company, please take a few minutes to make sure output.csv DOES 
    NOT contain any active accounts. 
    2. If you chose to use the database lists, use that list to 
    ``` select usernames, status ```
    ```from your user table ```
    ```where users are active and usernames in ('this','exported','list','contains','users','that','will','get','deleted.') ```
    That sudo code will give you any users that were exported and marked for deletion. 
    3. Triple check! Usernames change, but employee numbers don't. Take the list of 
    employee ID's and run those against the database. It will look very similar to the query above. Remove any active 
    users from output.csv.
4. Handle the Inactive accounts. 
    1. At this point you should feel confident that the list of users in output.csv are all accounts that are safe for 
    deletion. Open PowerShell ISE and copy the contents of deleteAccounts.ps1 into a new project. This will prevent 
    needing to allow remote-signed scripts. 
    2. Update the $CSVLocation variables to your output.csv file.
    3. Update the output variables to a diretory where you would like your backups to be saved. These files will give you
    more to work with if something is in question. 
    4. Change $Delete to the setting you wish to work with. 
        1. Set to 0 if you want to delete all users in the output.csv. 
        2. Set to 1 if you want to disable active users and delete disabled users. As of now, this is a work in progress, 
          but the idea is that any active account will be disabled so if it is in use, you will find out after a few weeks and reenable the account.
        3. Set to 2 if you want to delete disabled accounts, but skip active accounts. This is the reccomended option if
        you wish to be cautious - any active account should merit some kind of investigation. 
    5. Ensure readOnly is set to 1, then run deleteAccounts.ps1 with the green arrow in the top bar. You will get a copy
     of the results output to each directory. Glance through the results, ensuring that they look how they are expected.
     No active users, active AD accounts are in the right file, and disabled are in theirs. 
    6. When you're satisfied, it's time to do the deed. Set readonly to 0, then run. Expect this script to take some 
    time to run.
    
    Congratulations! Your AD environment should now be cleaner. Good job. 