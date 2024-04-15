function CommandExists {
    param (
        [Parameter(Mandatory=$true)]
        [string]$command,
        [Parameter(Mandatory=$false)]
        [bool]$exitOnError = $false
    )

    $commandTool = $command.Split(" ", 2)[0]
    try {
        Get-Command $commandTool -ErrorAction Stop | Out-Null
        if (-not $exitOnError) {
            return $true
          }
    } catch {
        if ($exitOnError) {
            Write-Output "Command '$commandTool' does not exist. Exiting."
            exit 1
        }
        return $false
    }
}

function RunAndExitOnFailure {
    param (
        [Parameter(Mandatory=$true)]
        [string]$command
    )
    CommandExists $command $true
    Invoke-Expression $command
    if ($LASTEXITCODE -ne 0) {
        WriteRed "Command '$command' failed with exit code $LASTEXITCODE. Exiting."
        exit $LASTEXITCODE
    }
}

function MakeWingetCommand {
  param (
    [Parameter(Mandatory=$true)]
    [string]$package
  )

  return "winget install $package --silent --accept-package-agreements --accept-source-agreements"
}

function WriteGreen {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Text
    )
    Write-Host $Text -ForegroundColor Green
}

function WriteRed {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Text
    )
    Write-Host $Text -ForegroundColor Red
}

function CheckAndInstallTool {
    param (
        [Parameter(Mandatory=$true)]
        [string]$toolName,
        [Parameter(Mandatory=$true)]
        [string]$installCommand
    )

    if (CommandExists $toolName) {
        WriteGreen "$toolName is already installed."
        return
      }
    WriteRed "$toolName is not installed."
    WriteGreen "Installing $toolName..."
    RunAndExitOnFailure $installCommand
    WriteGreen "Installed $toolName "

}

function CheckPythonVersion {
    CommandExists $pyCommand $true
    try {

        $pythonVersion = Invoke-Expression "$pyCommand --version"
        if ($LASTEXITCODE -ne 0) {
            throw
          }
    } catch {
        WriteRed "Python 3.12 is not installed"
        WriteGreen "Installing Python 3.12..."
        RunAndExitOnFailure (MakeWingetCommand "Python.Python.3.12")
        WriteGreen "Installed Python 3.12"
    }
}


WriteGreen "Starting project setup.. ."

$pyCommand = "py -3.12"
WriteGreen "Verifying python version"
CheckPythonVersion


CheckAndInstallTool "git" (MakeWingetCommand "Git.Git")
WriteGreen "Cloning repo"
RunAndExitOnFailure "git clone https://github.com/SenZmaKi/Bariki.git"

Set-Location Bariki

CheckAndInstallTool "docker" (MakeWingetCommand "Docker.DockerDesktop")

CheckAndInstallTool "ubuntu" (MakeWingetCommand "Canonical.Ubuntu.2204")

WriteGreen "Installing dependencies"
Set-Location src/backend
RunAndExitOnFailure "$pyCommand -m venv .venv"
RunAndExitOnFailure "./.venv/Scripts/activate.bat"
RunAndExitOnFailure "$pyCommand -m pip install -r requirements.txt"

Write-Host "If you're having issues with ubuntu or docker make sure to enable virtualisation in your BIOS settings: https://support.microsoft.com/en-us/windows/enable-virtualization-on-windows-11-pcs-c5578302-6e43-4b4b-a449-8ced115f58e1"
Write-Host "If you're having issues with algokit try: https://stackoverflow.com/a/66409838/17193072 "
WriteGreen "Successfully setup project"
