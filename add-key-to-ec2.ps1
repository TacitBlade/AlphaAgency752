# PowerShell script to add SSH key to AWS EC2 instance
# Usage: .\add-key-to-ec2.ps1 -InstanceIP "your-ec2-ip" -Username "ec2-user"

param(
    [Parameter(Mandatory=$true)]
    [string]$InstanceIP,
    
    [Parameter(Mandatory=$false)]
    [string]$Username = "ec2-user",
    
    [Parameter(Mandatory=$false)]
    [string]$OldKeyPath = ".\AlphaAgency752_old.pem.backup"
)

Write-Host "Adding new SSH key to EC2 instance: $InstanceIP" -ForegroundColor Green

# Read the new public key
$PublicKey = Get-Content ".\AlphaAgency752_ed25519.pub"

if (-not $PublicKey) {
    Write-Error "Could not read public key file"
    exit 1
}

Write-Host "Public key to add: $PublicKey" -ForegroundColor Yellow

# Create the command to add the key
$AddKeyCommand = @"
mkdir -p ~/.ssh && 
chmod 700 ~/.ssh && 
echo '$PublicKey' >> ~/.ssh/authorized_keys && 
chmod 600 ~/.ssh/authorized_keys && 
echo 'SSH key added successfully!'
"@

Write-Host "`nExecuting command on EC2 instance..." -ForegroundColor Cyan
Write-Host "Command: ssh -i `"$OldKeyPath`" $Username@$InstanceIP `"$AddKeyCommand`"" -ForegroundColor Gray

# Execute the command
try {
    $result = ssh -i $OldKeyPath "$Username@$InstanceIP" $AddKeyCommand
    Write-Host $result -ForegroundColor Green
    
    Write-Host "`nTesting new key connection..." -ForegroundColor Cyan
    $testResult = ssh -i ".\AlphaAgency752_ed25519" -o ConnectTimeout=10 "$Username@$InstanceIP" "echo 'New key works!'"
    
    if ($testResult -eq "New key works!") {
        Write-Host "✅ SUCCESS: New SSH key is working!" -ForegroundColor Green
        Write-Host "You can now connect using: ssh -i AlphaAgency752_ed25519 $Username@$InstanceIP" -ForegroundColor Yellow
    } else {
        Write-Warning "New key test failed. Please check manually."
    }
} catch {
    Write-Error "Failed to add key: $_"
    Write-Host "`nTroubleshooting tips:" -ForegroundColor Yellow
    Write-Host "1. Make sure your old key file exists and has correct permissions"
    Write-Host "2. Verify the EC2 instance IP address is correct"
    Write-Host "3. Check that the instance security group allows SSH (port 22)"
    Write-Host "4. Ensure the username is correct (usually 'ec2-user' for Amazon Linux, 'ubuntu' for Ubuntu)"
}
