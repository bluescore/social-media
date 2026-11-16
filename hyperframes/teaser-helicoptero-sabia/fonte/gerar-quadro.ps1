# Gera uma imagem-chave no Higgsfield (Nano Banana Pro, 2k, 9:16) e baixa para quadros\.
# Uso: .\gerar-quadro.ps1 -Prompt prompts\q2-voo.txt -Saida q2-v1 [-Refs id1,id2]
# Refs: ids de upload ou de job do Higgsfield, ou caminhos de arquivo (a ordem importa: 1ª = ícone).
param(
  [Parameter(Mandatory)] [string] $Prompt,
  [Parameter(Mandatory)] [string] $Saida,
  [string[]] $Refs = @('05860666-4240-4ce4-b636-c589e70fa82f', '9fe6c51d-3f27-4136-ab36-6cf621686621')
)
$ErrorActionPreference = 'Stop'
$base = $PSScriptRoot
$texto = Get-Content -Raw -Encoding UTF8 (Join-Path $base $Prompt)
$args2 = @('generate', 'create', 'nano_banana_pro', '--prompt', $texto, '--aspect_ratio', '9:16', '--resolution', '2k',
           '--wait', '--wait-timeout', '10m', '--wait-interval', '5s', '--json')
foreach ($r in $Refs) { $args2 += @('--image-references', $r) }
$json = (& higgsfield @args2) -join "`n" | ConvertFrom-Json
$job = @($json)[0]
if ($job.status -ne 'completed') { throw "Job $($job.id) terminou com status $($job.status)" }
$dest = Join-Path $base "quadros\$Saida.png"
Invoke-WebRequest -Uri $job.result_url -OutFile $dest
"$Saida  job=$($job.id)  ->  $dest"
