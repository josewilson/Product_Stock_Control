param(
    [switch]$App,
    [switch]$Tests
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

function Get-PythonCommand {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @("python")
    }

    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @("py", "-3")
    }

    $fallback = Join-Path $env:LOCALAPPDATA "Programs\Python\Python313\python.exe"
    if (Test-Path $fallback) {
        return @($fallback)
    }

    throw "Python nao encontrado. Instale o Python ou ajuste o PATH antes de executar este script."
}

if (-not $App -and -not $Tests) {
    $App = $true
}

$pythonCmd = @(Get-PythonCommand)
$pythonExe = $pythonCmd[0]
$pythonBaseArgs = @()
if ($pythonCmd.Count -gt 1) {
    $pythonBaseArgs = $pythonCmd[1..($pythonCmd.Count - 1)]
}

if ($Tests) {
    & $pythonExe @pythonBaseArgs -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

if ($App) {
    & $pythonExe @pythonBaseArgs -m src.main
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

