param(
    [switch]$Network,
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if ($Network) {
    python -m uvicorn app:app --host 0.0.0.0 --port $Port
} else {
    python -m uvicorn app:app --host 127.0.0.1 --port $Port
}
