# Anima uma imagem-chave no Higgsfield (Kling 4.0, imagem -> vídeo, 1080p, 9:16) e baixa para clipes\.
# Uso: .\gerar-clipe.ps1 -Prompt prompts\c1-decolagem.txt -Inicio <job_id> [-Fim <job_id>] -Saida c1-v1 [-Duracao 5]
param(
  [Parameter(Mandatory)] [string] $Prompt,
  [Parameter(Mandatory)] [string] $Inicio,
  [string] $Fim,
  [Parameter(Mandatory)] [string] $Saida,
  [int] $Duracao = 5
)
$ErrorActionPreference = 'Stop'
$base = $PSScriptRoot
$texto = Get-Content -Raw -Encoding UTF8 (Join-Path $base $Prompt)
$a = @('generate', 'create', 'kling4_0', '--mode', 'image-to-video', '--prompt', $texto, '--start-image', $Inicio,
       '--aspect_ratio', '9:16', '--duration', "$Duracao", '--resolution', '1080p',
       '--wait', '--wait-timeout', '25m', '--wait-interval', '10s', '--json')
if ($Fim) { $a += @('--end-image', $Fim) }
$json = (& higgsfield @a) -join "`n" | ConvertFrom-Json
$job = @($json)[0]
if ($job.status -ne 'completed') { throw "Job $($job.id) terminou com status $($job.status)" }
$dest = Join-Path $base "clipes\$Saida.mp4"
Invoke-WebRequest -Uri $job.result_url -OutFile $dest
"$Saida  job=$($job.id)  ->  $dest"
