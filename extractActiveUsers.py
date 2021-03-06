# Find Unused Disabled accounts
# The bottom line is that we are going to take the full list of AD users and remove the okta Active users and ADServiceAccounts.
# At the end, we will have a list of accounts that are not active and can be deleted.
import csv

# Files
oktaActiveUsers = r'C:\Users\user\Desktop\Projects\UATCleanup\oktaUserExportUAT.csv'

# Service accounts are pulled based on the fact they uaually don't have an employee ID.
ADServiceAccounts = r'C:\Users\user\Desktop\Projects\UATCleanup\UATServiceAccounts.csv'
AllUATAccounts = r'C:\Users\user\Desktop\Projects\UATCleanup\AllADAccountsUAT.csv'
outputDirectory = r'C:\Users\user\Desktop\Projects\UATCleanup\outputDirectory'

# Lets get all data into arrays
# Two paralell lists per CSV to hold the csv data.
oktaActiveUserNames = []
oktaActiveEmpIds = []
oktaUserNum = 0
with open(oktaActiveUsers, 'r') as csv_file:
    reader = csv.reader(csv_file)

    counter = 0
    for row in reader:
        counter = counter + 1
        oktaActiveUserNames.append(row[0])
        oktaActiveEmpIds.append(row[1])
oktaUserNum = counter
print(oktaActiveUserNames)
print("All active okta Accounts imported. There are " + str(oktaUserNum) + " accounts.")

# AD Service Accounts
ADServiceUserNames = []
ADServiceEmpIds = []
serviceAccountUserNum = 0
with open(ADServiceAccounts, 'r') as csv_file:
    reader = csv.reader(csv_file)

    counter = 0
    for row in reader:
        counter = counter + 1
        ADServiceUserNames.append(row[0])

serviceAccountUserNum = counter
print(ADServiceUserNames)
print("All AD Service Accounts imported. There are " + str(serviceAccountUserNum) + " accounts.")

# All AD Accounts
AllADAccountUserNames = []
AllADAccountEmpIds = []

with open(AllUATAccounts, 'r') as csv_file:
    reader = csv.reader(csv_file)

    counter = 0
    for row in reader:
        counter = counter + 1
        AllADAccountUserNames.append(row[0])
        AllADAccountEmpIds.append(row[1])

print(AllADAccountUserNames)
print("All AD Accounts imported. There are " + str(counter) + " accounts.")

# for account in AllADAccountUserNames:
#     print(account + " "+ str(type(account)))


# Remove Service Accounts from ADDisabledAccountUserNames and ADDisabledAccountEmpIds
counter = 0
oktaCounter = 0
serviceCounter = 0
RemovedoktaAccountUserNames = []
RemovedServiceAccountUserNames = []
# Create the final list of disabled users. We will be modifying the new list, not the original list.
ADDisabledAccountUserNames = AllADAccountUserNames.copy()
ADDisabledAccountEmpIds = AllADAccountEmpIds.copy()

# for count, account in enumerate(AllADAccountUserNames):
while counter < len(AllADAccountUserNames):
    found = 0
    remove = 0
    print(AllADAccountUserNames[counter] + " " + str(counter))
    # Remove Service Account: if this account is in the service account list, delete it.
    if AllADAccountUserNames[counter] in ADServiceUserNames:
        remove = ADDisabledAccountUserNames.index(AllADAccountUserNames[counter])
        # print("Will remove Service Account " + ADDisabledAccountUserNames[remove] + " at index: " + str(remove))
        ADDisabledAccountUserNames.pop(remove)
        ADDisabledAccountEmpIds.pop(remove)
        serviceCounter = serviceCounter + 1
        RemovedServiceAccountUserNames.append(AllADAccountUserNames[counter])
        found = 1
        print("Removed Service account: " + AllADAccountUserNames[counter] + " which has counter " + str(counter))

    # Remove okta Account: if this account is in the okta account list, delete it. If the account was removed in the previous function, it should already be deleted.
    if AllADAccountUserNames[counter] in oktaActiveUserNames and found != 1:
        remove = ADDisabledAccountUserNames.index(AllADAccountUserNames[counter])
        # print("Will remove okta User " + ADDisabledAccountUserNames[remove] + " at index: " + str(remove))
        ADDisabledAccountUserNames.pop(remove)
        ADDisabledAccountEmpIds.pop(remove)
        oktaCounter = oktaCounter + 1
        RemovedoktaAccountUserNames.append(AllADAccountUserNames[counter])
        found = 1
        print("Removed active okta account: " + AllADAccountUserNames[counter] + " which has counter " + str(counter))

    if AllADAccountUserNames[counter] in oktaActiveUserNames and AllADAccountUserNames[counter] in ADServiceUserNames:
        print("Found " + AllADAccountUserNames[counter] + " that is both a service account and okta user.")

    #     if (found == 0):
    #         print( AllADAccountUserNames[counter] + " belongs to a user that needs to be removed which has counter " + str(counter))

    counter = counter + 1

print("Usernames:" + str(len(ADDisabledAccountUserNames)) + ", Employee ID:" + str(len(ADDisabledAccountEmpIds)))
print(str(serviceCounter) + " Service Accounts removed from total AD List out of " + str(
    serviceAccountUserNum) + " Service Accounts")
print(str(oktaCounter) + " okta Accounts removed from total AD List out of " + str(oktaUserNum) + " okta users.")
print("Removed all active and service account. There are " + str(
    len(ADDisabledAccountUserNames)) + " accounts remaining.")

####### WRITE FILES ###########
outputFile = ""
with open(outputDirectory + '\output.csv', 'a') as f:
    counter = 0
    for account in ADDisabledAccountUserNames:
        outputFile = (outputFile + ADDisabledAccountUserNames[counter] + "," + ADDisabledAccountEmpIds[counter] + "\n")
        counter = counter + 1
    f.write(outputFile)
print("Successfully created output file: output.csv")

outputFile = ""
with open(outputDirectory + '\outputRemovedoktaUsers.csv', 'a') as f:
    counter = 0
    for account in RemovedoktaAccountUserNames:
        outputFile = (outputFile + RemovedoktaAccountUserNames[counter] + "\n")
        counter = counter + 1
    f.write(outputFile)
print("Successfully created output file: outputRemovedoktaUsers.csv")

outputFile = ""
with open(outputDirectory + '\outputRemovedServiceUsers.csv', 'a') as f:
    counter = 0
    for account in RemovedServiceAccountUserNames:
        outputFile = (outputFile + RemovedServiceAccountUserNames[counter] + "\n")
        counter = counter + 1
    f.write(outputFile)
print("Successfully created output file: outputRemovedServiceUsers.csv")

####Make Database Batches####
# Uncomment this section if you want to extract all remaining users in a ('user1','user2') format.
# This is useful for SQL Queries if you want to double check for active users against a database.
'''
counter = 0
set1 = "("
while counter < 999:
    set1 = set1 + "\'" + ADDisabledAccountUserNames[counter] + "\',"
    counter = counter + 1
set1 = set1[:-1] + ")"
print(set1)

set2 = "("
while counter < 1998:
    set2 = set2 + "\'" + ADDisabledAccountUserNames[counter] + "\',"
    counter = counter + 1
set2 = set2[:-1] + ")"
print(set2)

set3 = "("
while counter < len(ADDisabledAccountUserNames):
    set3 = set3 + "\'" + ADDisabledAccountUserNames[counter] + "\',"
    counter = counter + 1
set3 = set3[:-1] + ")"
print(set3)

###Get another list of employee ID's###
counter = 0
set1 = "("
while counter < 999:
    set1 = set1 + "\'" + ADDisabledAccountEmpIds[counter] + "\',"
    counter = counter + 1
set1 = set1[:-1] + ")"
print(set1)

set2 = "("
while counter < 1998:
    set2 = set2 + "\'" + ADDisabledAccountEmpIds[counter] + "\',"
    counter = counter + 1
set2 = set2[:-1] + ")"
print(set2)

set3 = "("
while counter < len(ADDisabledAccountEmpIds):
    set3 = set3 + "\'" + ADDisabledAccountEmpIds[counter] + "\',"
    counter = counter + 1
set3 = set3[:-1] + ")"
print(set3)
'''