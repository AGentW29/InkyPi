param(
    [Parameter(Mandatory=$false)]
    [string]$RemoteHost = "raspberry.local",
    [string]$RemoteUser = "pi"
)

# Path to your new plugin
$PluginPath = ".\src\plugins\message_display"
$RemotePath = "/home/$RemoteUser/InkyPi/src/plugins/"

Write-Host "Copying message_display plugin to $RemoteHost..."
scp -r $PluginPath ${RemoteUser}@${RemoteHost}:$RemotePath

Write-Host "Restarting InkyPi service..."
ssh ${RemoteUser}@${RemoteHost} "sudo systemctl restart inkypi"

Write-Host "Done! Your new plugin should now be available on your Raspberry Pi."
Write-Host "Visit http://$RemoteHost to see it in the web interface."