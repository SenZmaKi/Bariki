echo "Verifying python version"
$pythonVersion = python --version
$pythonVersion = $pythonVersion.Replace("Python ", "")
$majorVersion = $pythonVersion.Split(".")[0]
$minorVersion = $pythonVersion.Split(".")[1]

New-Item -ItemType Directory -Force -Path Bariki/src/backend

if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 11)) {
    Write-Output "You need python 3.11 or greater"
    exit 1
}
echo "Installing git"
winget install git
echo "Cloning repo"
git clone https://github.com/SenZmaKi/Bariki.git

echo "Installing docker"
winget install Docker.DockerDesktop
echo "Installing ubuntu"
winget install Canonical.Ubuntu.2204 

echo "Installing dependencies"
cd src/backend
python -m venv .venv
./.venv/Scripts/activate.bat
pip install -r requirements.txt
