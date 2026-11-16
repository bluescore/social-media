# Gera um som no Higgsfield e baixa para audio\.
# Uso: .\gerar-audio.ps1 -Modelo mirelo_text_to_audio -Texto "..." -Duracao 13 -Saida rotor-v1 [-Extra '--force_instrumental','true']
param(
  [Parameter(Mandatory)] [string] $Modelo,
  [Parameter(Mandatory)] [string] $Texto,
  [Parameter(Mandatory)] [double] $Duracao,
  [Parameter(Mandatory)] [string] $Saida,
  [string[]] $Extra = @()
)
$ErrorActionPreference = 'Stop'
$base = $PSScriptRoot
New-Item -ItemType Directory -Force (Join-Path $base 'audio') | Out-Null
$a = @('generate', 'create', $Modelo, '--prompt', $Texto, '--duration', "$Duracao",
       '--wait', '--wait-timeout', '10m', '--wait-interval', '5s', '--json') + $Extra
$json = (& higgsfield @a) -join "`n" | ConvertFrom-Json
$job = @($json)[0]
if ($job.status -ne 'completed') { throw "Job $($job.id) terminou com status $($job.status)" }
$ext = [IO.Path]::GetExtension(([Uri]$job.result_url).AbsolutePath)
$dest = Join-Path $base "audio\$Saida$ext"
Invoke-WebRequest -Uri $job.result_url -OutFile $dest
"$Saida  job=$($job.id)  ->  $dest"
