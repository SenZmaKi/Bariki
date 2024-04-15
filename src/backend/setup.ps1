
$PY_COMMAND = "py -3.12"
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
        WriteGreen "$toolName is already installed"
        return
      }
    WriteRed "$toolName is not installed."
    WriteGreen "Installing $toolName..."
    RunAndExitOnFailure $installCommand
    WriteGreen "Installed $toolName "

}

function CheckPythonVersion {
    CommandExists $PY_COMMAND $true
    try {

        $pythonVersion = Invoke-Expression "$PY_COMMAND --version"
        if ($LASTEXITCODE -ne 0) {
            throw
          }
        WriteGreen "Python 3.12 is already installed"
    } catch {
        WriteRed "Python 3.12 is not installed"
        WriteGreen "Installing Python 3.12..."
        RunAndExitOnFailure (MakeWingetCommand "Python.Python.3.12")
        WriteGreen "Installed Python 3.12"
    }
}


WriteGreen "Starting project setup.. ."
WriteGreen "Verifying dev tools"
CheckPythonVersion
CheckAndInstallTool "git" (MakeWingetCommand "Git.Git")
CheckAndInstallTool "docker" (MakeWingetCommand "Docker.DockerDesktop")
CheckAndInstallTool "ubuntu" (MakeWingetCommand "Canonical.Ubuntu.2204")

WriteGreen "Cloning repo"
RunAndExitOnFailure "git clone https://github.com/SenZmaKi/Bariki.git"

Set-Location Bariki


WriteGreen "Installing dependencies"
Set-Location src/backend
RunAndExitOnFailure "$PY_COMMAND -m venv .venv"
RunAndExitOnFailure "./.venv/Scripts/activate.bat"
RunAndExitOnFailure "$PY_COMMAND -m pip install -r requirements.txt"

Write-Host ""
Write-Host ""
Write-Host "If you're having issues with ubuntu or docker make sure to enable virtualization in your BIOS settings: https://support.microsoft.com/en-us/windows/enable-virtualisation-on-windows-11-pcs-c5578302-6e43-4b4b-a449-8ced115f58e1" -ForegroundColor Blue
Write-Host "If you're having issues with algokit try: https://stackoverflow.com/a/66409838/17193072" -ForegroundColor Blue
WriteGreen "Successfully setup project"
