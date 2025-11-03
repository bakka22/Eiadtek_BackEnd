# setup.ps1
# -----------------------------------
# Sets up Medico Backend on Windows:
# - Installs Rust if missing
# - Installs Python dependencies
# -----------------------------------

Write-Host ""
Write-Host "=== Starting Medico Backend Setup ==="
Write-Host ""

# Step 1: Check for Rust
Write-Host "Checking for Rust installation..."
if (-not (Get-Command rustc -ErrorAction SilentlyContinue)) {
    Write-Host "Rust not found. Installing..."
    $rustInstaller = "rustup-init.exe"
    Invoke-WebRequest -Uri "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe" -OutFile $rustInstaller
    Start-Process -FilePath ".\rustup-init.exe" -ArgumentList "-y" -NoNewWindow -Wait
    Remove-Item $rustInstaller -Force
    Write-Host "Rust installed successfully!"
} else {
    Write-Host "Rust already installed."
}

# Step 2: Ensure cargo is in PATH
$CargoPath = Join-Path $env:USERPROFILE ".cargo\bin"
$env:PATH += ";$CargoPath"
if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "Warning: Cargo not detected in PATH. You may need to restart PowerShell after setup."
}

# Step 3: Install Python dependencies
Write-Host ""
Write-Host "Installing Python dependencies..."
if (Test-Path "requirements.txt") {
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    Write-Host "Python dependencies installed successfully!"
} else {
    Write-Host "Error: requirements.txt not found in the current folder."
}

Write-Host ""
Write-Host "=== Setup complete! ==="
Write-Host "You can now run your FastAPI app using:"
Write-Host "   uvicorn main:app --reload"
Write-Host ""
