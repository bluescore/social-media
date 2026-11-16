# Cadastro da chave da OpenAI neste computador
# ---------------------------------------------
# O que faz:
#   1. Pede a chave (o que você digita/cola fica escondido na tela).
#   2. Testa a chave na OpenAI sem gastar nada (só lista os modelos liberados).
#   3. Guarda a chave na variável de ambiente OPENAI_API_KEY do seu usuário do Windows.
#   4. Escolhe sozinho o melhor modelo de imagem que a sua conta tem e anota em config.json.
#
# Como rodar (no terminal, dentro de C:\social-media):
#   powershell -ExecutionPolicy Bypass -File .\ferramentas\openai\cadastrar-chave.ps1
#
# A chave nunca é escrita em arquivo do projeto nem mostrada na tela.

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$pasta = Split-Path -Parent $MyInvocation.MyCommand.Path
$configPath = Join-Path $pasta 'config.json'

Write-Host ''
Write-Host '=== Cadastro da chave da OpenAI ===' -ForegroundColor Cyan
$atual = [Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'User')
if ($atual) {
  $fim = $atual.Substring([Math]::Max(0, $atual.Length - 4))
  Write-Host "Já existe uma chave cadastrada (termina em ...$fim). A nova vai substituir a antiga."
}
Write-Host 'Cole a chave (começa com sk-) e aperte Enter. Nada vai aparecer enquanto você cola; é normal.'
$seguro = Read-Host -AsSecureString 'Chave'
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($seguro)
try { $chave = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
$chave = ($chave -replace '\s', '')

if (-not $chave.StartsWith('sk-')) {
  Write-Host 'Isso não parece uma chave da OpenAI (deveria começar com sk-). Nada foi salvo.' -ForegroundColor Red
  exit 1
}

Write-Host 'Testando a chave na OpenAI (não gasta crédito)...'
try {
  $resp = Invoke-RestMethod -Uri 'https://api.openai.com/v1/models' -Headers @{ Authorization = "Bearer $chave" } -Method Get -TimeoutSec 30
} catch {
  $codigo = $null
  try { $codigo = [int]$_.Exception.Response.StatusCode } catch {}
  if ($codigo -eq 401) { Write-Host 'A OpenAI recusou a chave (401). Confira se copiou inteira e se ela está ativa. Nada foi salvo.' -ForegroundColor Red }
  else { Write-Host "Não consegui falar com a OpenAI: $($_.Exception.Message). Nada foi salvo." -ForegroundColor Red }
  exit 1
}

$ids = @($resp.data | ForEach-Object { $_.id })
$imagem = @($ids | Where-Object { $_ -like 'gpt-image*' } | Sort-Object)
$sora = @($ids | Where-Object { $_ -like 'sora*' } | Sort-Object)

[Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $chave, 'User')
$env:OPENAI_API_KEY = $chave
Write-Host 'Chave válida e salva no seu usuário do Windows (OPENAI_API_KEY).' -ForegroundColor Green

# Ordem de preferência: o melhor primeiro. "sunburst" = mais precisão; "flare" = mais rápido e barato.
$preferFinal = @('gpt-image-2.6-sunburst', 'gpt-image-2.5-sunburst', 'gpt-image-2.6-flare', 'gpt-image-2.5-flare', 'gpt-image-2')
# Rascunho: o 2.5 flare em qualidade baixa gasta ~4x menos que o 2.6 (pesquisa de 2026-11-11).
$preferRascunho = @('gpt-image-2.5-flare', 'gpt-image-2.6-flare', 'gpt-image-2.5-sunburst', 'gpt-image-2.6-sunburst', 'gpt-image-2')
$final = $preferFinal | Where-Object { $imagem -contains $_ } | Select-Object -First 1
$rascunho = $preferRascunho | Where-Object { $imagem -contains $_ } | Select-Object -First 1

if (-not $final) {
  Write-Host ''
  Write-Host 'Atenção: a chave funciona, mas a sua conta ainda não tem modelo de imagem liberado.' -ForegroundColor Yellow
  Write-Host 'Normalmente é a "verificação da organização" da OpenAI: platform.openai.com > Settings > Organization > General > Verify Organization.'
  Write-Host 'Depois de verificar, rode este cadastro de novo.'
  if ($imagem.Count -gt 0) { Write-Host "Modelos de imagem vistos: $($imagem -join ', ')" }
} else {
  $config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
  $config.modelo_final = $final
  $config.modelo_rascunho = $rascunho
  $config.modelos_disponiveis = $imagem
  $config.sora_disponivel = ($sora.Count -gt 0)
  $config.verificado_em = (Get-Date -Format 'yyyy-MM-dd HH:mm')
  $json = $config | ConvertTo-Json -Depth 5
  [IO.File]::WriteAllText($configPath, $json, (New-Object System.Text.UTF8Encoding $false))
  Write-Host "Modelo para imagens finais: $final"
  Write-Host "Modelo para rascunhos: $rascunho"
  if ($sora.Count -gt 0) { Write-Host "Vídeo (Sora) também liberado nesta conta: $($sora -join ', ')" }
}
Write-Host ''
Write-Host 'Pronto. Pode voltar para o Claude e avisar que cadastrou.' -ForegroundColor Cyan
