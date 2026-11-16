# Gera uma imagem-chave no Higgsfield (Nano Banana Pro, 9:16) e baixa para quadros\.
# Uso: .\gerar-quadro.ps1 -Prompt prompts\q1-fachada.txt -Saida q1-v1 [-Refs arquivo1,arquivo2] [-Resolucao 4k]
# Refs: caminhos de arquivo ou ids de job/upload do Higgsfield (a ordem importa).
param(
  [Parameter(Mandatory)] [string] $Prompt,
  [Parameter(Mandatory)] [string] $Saida,
  [string[]] $Refs = @(),
  [string] $Resolucao = '2k',
  [string] $Proporcao = '9:16'
)
$ErrorActionPreference = 'Stop'
$base = $PSScriptRoot
$texto = Get-Content -Raw -Encoding UTF8 (Join-Path $base $Prompt)
$a = @('generate', 'create', 'nano_banana_pro', '--prompt', $texto, '--aspect_ratio', $Proporcao, '--resolution', $Resolucao,
       '--wait', '--wait-timeout', '10m', '--wait-interval', '5s', '--json')
foreach ($r in $Refs) {
  $p = Join-Path $base $r
  if (Test-Path $p) { $a += @('--image-references', $p) } else { $a += @('--image-references', $r) }
}
$json = (& higgsfield @a) -join "`n" | ConvertFrom-Json
$job = @($json)[0]
if ($job.status -ne 'completed') { throw "Job $($job.id) terminou com status $($job.status)" }
$dest = Join-Path $base "quadros\$Saida.png"
Invoke-WebRequest -Uri $job.result_url -OutFile $dest
"$Saida  job=$($job.id)  ->  $dest"
