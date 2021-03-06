# This script will cycle through a csv containing uid,employeeID and will disable or delete the users.
# Attributes to Modify for this program's functionality.
$Delete=2 #Set 0 delete all users in the CSV. 1 disable active users, delete disabled users. TODO  2 delete disabled, but backup user info.
$readOnly=1 #0 is off, 1 is on
$count=0

echo "Loading Variables"
$CSVLocation='C:\Users\user\Desktop\UATCleanup\PowershellCleanup\output.csv' #Location of the CSV

$OutputDirectoryActiveUsers='C:\Users\user\Desktop\PowershellCleanup\ActiveUsersDeleted.csv'
$OutputDirectoryDisabledUsers='C:\Users\user\Desktop\PowershellCleanup\DisabledUsersDeleted.csv'
$OutputDirectoryFailedUsers='C:\Users\user\Desktop\PowershellCleanup\FailedUsersDeleted.csv'

$csv = Import-csv -path $CSVLocation

Write-Host "Your CSV Location is at $CSVLocation"
Write-Host "Starting..."
if($Delete -eq 0) {
    $Answer = Read-Host -Prompt 'Are you sure you want to delete all users? y/n'
    if($Answer -eq 'y' -or $Answer -eq 'Y') {
        echo 'Deleting users.'
    foreach($line in $csv)
    {
        #Backup the user's attributes to the CSV
        #Backup the user's ADGroups to the CSV (Command "Get-ADPrincipalGroupMembership name")
        Write-Host "Count:$($count) - $($line.Username) is $($userEnabled). THROWING THEM OUT A WINDOW."
        Get-ADUser -Filter "EmployeeID -eq '$($line.EmployeeID)'"  -Properties * | Select-Object * | export-csv -path $OutputDirectoryDisabledUsers -NoTypeInformation -Append -Force

            #Delete the Account
        if ($readOnly -eq "0") {
            #Deleting user
            #Remove-ADUser -Identity $($line.Username) -Confirm:$false | Remove-ADObject -Recursive
            Write-Host "Deleting user with $userDN"

            Try {
                Remove-ADObject -Identity "$userDN" -Recursive -Confirm:$FALSE
            } Catch {
                Write-Host "Deleting user with $userDN failed to Delete - outputting to file."
                Get-ADUser -Filter "EmployeeID -eq '$($line.EmployeeID)'"  -Properties * | Select-Object * | export-csv -path $OutputDirectoryFailedUsers -NoTypeInformation -Append -Force
            }

        } else {
            #Read Only Mode
            echo 'Read only mode is on.'
        }
    }

    } else {
        echo 'Okay! Bye.'
    }


} elseif($Delete -eq 1) {
    echo 'Disabling all users in the csv.'
    echo 'TODO'

} elseif($Delete -eq 2) {
    echo 'Delete all disabled AD accounts and disable all active AD accounts that have been marked for deletion.'

    foreach($line in $csv)
    {
        #Write-Host "$($line.Username), whose Employee ID is $($line.EmployeeID)."
        $CurrentUser=Get-ADUser -Filter "EmployeeID -eq '$($line.EmployeeID)'"  -Properties *

        $userEnabled = $CurrentUser.enabled
        $userDN = $CurrentUser.DistinguishedName

        #Write-Host "User is $userEnabled"

        if ($userEnabled -eq $true) { #If the user is enabled
            #Backup the user's attributes to the CSV
            #Backup the user's ADGroups to the CSV (Command "Get-ADPrincipalGroupMembership name")
            Write-Host "$($line.Username) is $($userEnabled). Backing them up."
            Get-ADUser -Filter "EmployeeID -eq '$($line.EmployeeID)'"  -Properties * | Select-Object * | export-csv -path $OutputDirectoryActiveUsers -NoTypeInformation -Append -Force

        } elseif($userEnabled -eq $false) { #If the user is disabled
            #Backup the user's attributes to the CSV
            #Backup the user's ADGroups to the CSV (Command "Get-ADPrincipalGroupMembership name")
            Write-Host "Count:$($count) - $($line.Username) is $($userEnabled). THROWING THEM OUT A WINDOW."
            Get-ADUser -Filter "EmployeeID -eq '$($line.EmployeeID)'"  -Properties * | Select-Object * | export-csv -path $OutputDirectoryDisabledUsers -NoTypeInformation -Append -Force

                #Delete the Account
            if ($readOnly -eq "0") {
                #Deleting user
                #Remove-ADUser -Identity $($line.Username) -Confirm:$false | Remove-ADObject -Recursive
                Write-Host "Deleting user with $userDN"

                Try {
                    Remove-ADObject -Identity "$userDN" -Recursive -Confirm:$FALSE
                } Catch {
                    Write-Host "Deleting user with $userDN failed to Delete - outputting to file."
                    Get-ADUser -Filter "EmployeeID -eq '$($line.EmployeeID)'"  -Properties * | Select-Object * | export-csv -path $OutputDirectoryFailedUsers -NoTypeInformation -Append -Force
                }

            } else {
                #Read Only Mode
            }

        } else {
            echo "User has unknown account status."
        }

        $count = $count + 1
    }

} else {
    echo 'Unrecognized value provided in the delete field. Exiting.'
}
Write-Host "Completed!"
