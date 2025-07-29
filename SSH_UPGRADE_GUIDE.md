# SSH Protocol v2 Upgrade Guide

## Problem
SSH protocol v.1 is no longer supported due to security vulnerabilities. Your original RSA key may have compatibility issues with modern SSH implementations.

## Solution
I've generated new SSH keys that are compatible with SSH protocol v2 (the current standard):

### New Keys Generated:
1. **Ed25519 Key (RECOMMENDED)**: `AlphaAgency752_ed25519`
   - More secure and faster than RSA
   - Smaller key size but stronger security
   - Modern standard for SSH authentication

2. **RSA 4096 Key (Alternative)**: `AlphaAgency752_rsa4096`
   - Traditional RSA with 4096-bit strength
   - Compatible with older systems that don't support Ed25519

### Your Public Keys:

#### Ed25519 Public Key (Copy this to your servers):
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOtKZ56kUGeExyFqeKVeom9qQm1rebJEKuKh4VjddXtE AlphaAgency752-2025-07-29
```

#### RSA 4096 Public Key (Alternative):
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDh9zNsyPxjKisCPuDbjY1UlqFmds2V9fZFZMKsLcalIGQuTCW5XnI2fcqIqxeFYNbDsmksW9d7rdthe9HGzJdUOZ/SGFOo3qmzJUQYVMQ+UcD3FMDuJTUDdFJYIdHd4gEef2ycERdc8ug4Wsb/XaHqqfMjOnsMLdX7t5Vso9VR6C5zq4bfDFdt8+7uw9fZOKg0+bnXa2mTpQ5lzSlBSRfBelehaCKA0LkbvIwgimcIm8McReu3/MFHzgtMj6/sHJ7x9yTzGsHyDCuFEmkOSDoRaJOpp4S3K0v4rfxqT8JD2HP4lwuVcoo7tsg07p1xYfOvt63jE0GfvFLSQ/dNiiFioJQZQZzw95K+lElSPOZicGHYsEmQ8RC55sXqxZFlkR0iWSdMpORRsOwfHu3rq+lyx/7K6+L8ZaztWdNMQJ/wU4u6lzYHL0roh3NT4xJ2Ox/uQRvsm6vTtLoZuLD4g/iAHSzHzIQvNCed/scKaF5CB80vpyfrRcqkI27wA4rszDEdAFQIjNLqQ0esrUUHDbNxIF+94e/8LYmjXt957mQ2fZMn1RHU/LXZ4qFvmYA7GVpMJ5ADUb3lFQRZPn8yUEMFW60yvEr9vVJ+GRSgwpTwWVAQSblxWyCKcapTupQw2GtiR3awpbrs5S53Aa3dbJSd+iO3PxbvrVW+Vs2TrUqaLTotQ== AlphaAgency752-2025-07-29
```

## Steps to Update Your SSH Access:

### 1. For GitHub/GitLab/Bitbucket:
- Go to your account settings → SSH Keys
- Add the new Ed25519 public key (recommended)
- Test the connection: `ssh -T git@github.com`

### 2. For AWS EC2 Instances:

#### Method 1: Add to existing running instance (Recommended)
If you can currently access your EC2 instance:

1. **Connect to your instance** using your current key:
   ```bash
   ssh -i AlphaAgency752_old.pem.backup ec2-user@your-instance-ip
   ```

2. **Add the new public key** to authorized_keys:
   ```bash
   # Create .ssh directory if it doesn't exist
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   
   # Add your new Ed25519 public key (recommended)
   echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOtKZ56kUGeExyFqeKVeom9qQm1rebJEKuKh4VjddXtE AlphaAgency752-2025-07-29" >> ~/.ssh/authorized_keys
   
   # Set correct permissions
   chmod 600 ~/.ssh/authorized_keys
   ```

3. **Test the new key** (from your local machine):
   ```bash
   ssh -i AlphaAgency752_ed25519 ec2-user@your-instance-ip
   ```

#### Method 2: Using AWS Systems Manager (if SSM is enabled)
If you have AWS Systems Manager Session Manager enabled:

1. **Connect via AWS Console** → EC2 → Instance → Connect → Session Manager
2. **Run the same commands** as Method 1 to add your public key

#### Method 3: Using EC2 User Data (for new instances)
For new instances, add this to User Data script:
```bash
#!/bin/bash
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOtKZ56kUGeExyFqeKVeom9qQm1rebJEKuKh4VjddXtE AlphaAgency752-2025-07-29" >> /home/ec2-user/.ssh/authorized_keys
```

#### Method 4: Create new Key Pair in AWS (Alternative)
1. **AWS Console** → EC2 → Key Pairs → Import Key Pair
2. **Name**: AlphaAgency752-Ed25519
3. **Paste your Ed25519 public key** from above
4. **Use this key pair** when launching new instances

### 3. For Other Servers/Cloud Instances:
- Add the public key to `~/.ssh/authorized_keys` on your servers
- Use the new private key when connecting:
  ```bash
  ssh -i AlphaAgency752_ed25519 user@server.com
  ```

### 4. Update SSH Config for AWS EC2:
Create/update `~/.ssh/config` (or `C:\Users\{username}\.ssh\config` on Windows):
```
# AWS EC2 Instance
Host aws-alpha
    HostName your-ec2-instance-ip-or-dns
    User ec2-user
    IdentityFile ~/path/to/AlphaAgency752_ed25519
    Protocol 2

# Alternative with RSA key
Host aws-alpha-rsa
    HostName your-ec2-instance-ip-or-dns
    User ec2-user
    IdentityFile ~/path/to/AlphaAgency752_rsa4096
    Protocol 2
```

Then connect simply with:
```bash
ssh aws-alpha
```

### 5. Test Your New Keys:
```bash
# Test Ed25519 key
ssh-keygen -l -f AlphaAgency752_ed25519

# Test RSA key
ssh-keygen -l -f AlphaAgency752_rsa4096
```

## Security Notes:
- Your original key has been backed up as `AlphaAgency752_old.pem.backup`
- Ed25519 keys are recommended for new deployments
- Both new keys use SSH protocol v2 exclusively
- Keep your private keys secure and never share them

## File Permissions (Important):
Make sure your private keys have correct permissions:
```bash
chmod 600 AlphaAgency752_ed25519
chmod 600 AlphaAgency752_rsa4096
```

Generated on: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
