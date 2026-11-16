# Gera varios sons em sequencia a partir de prompts\<nome>.txt
# Uso: .\gerar-lote.ps1 -Nomes hall2-a,hall2-b -Duracao 8
param([Parameter(Mandatory)] [string[]] $Nomes, [Parameter(Mandatory)] [double] $Duracao)
$base = $PSScriptRoot
foreach ($n in $Nomes) {
  $t = Get-Content -Raw (Join-Path $base "prompts\$n.txt")
  & (Join-Path $base 'gerar-audio.ps1') -Modelo mirelo_text_to_audio -Texto $t -Duracao $Duracao -Saida $n
}
