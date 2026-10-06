# Owner-specified validation block (2026-10-06), with stdout of each step captured to a log.
$ErrorActionPreference = 'Stop'
Set-Location 'C:\Projects\timescape-fsigma8'
$L = 'C:\Users\Claudio\AppData\Local\Temp\claude\C--Projects-timescape-fsigma8\e40ff1c8-d399-4ad8-8662-6eb2f409e405\scratchpad\r3'
$env:PYTHONPATH = Join-Path -Path (Get-Location).Path -ChildPath 'src'
$env:OPENBLAS_NUM_THREADS = '1'
"start $(Get-Date -Format o)" | Out-File -FilePath "$L\run_summary.txt" -Encoding utf8

& './.venv/Scripts/python.exe' --version | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw 'Interprete principale non disponibile' }

& './.venv311/Scripts/python.exe' --version | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw 'Interprete 3.11 non disponibile' }

"py314 start $(Get-Date -Format o)" | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
& './.venv/Scripts/python.exe' -B -W error -m pytest -q -p no:cacheprovider | Out-File -FilePath "$L\fullsuite_314.log" -Encoding utf8
$code314 = $LASTEXITCODE
"py314 exit=$code314 end $(Get-Date -Format o)" | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
if ($code314 -ne 0) { throw 'Suite principale fallita' }

"py311 start $(Get-Date -Format o)" | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
& './.venv311/Scripts/python.exe' -B -W error -m pytest -q -p no:cacheprovider | Out-File -FilePath "$L\fullsuite_311.log" -Encoding utf8
$code311 = $LASTEXITCODE
"py311 exit=$code311 end $(Get-Date -Format o)" | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
if ($code311 -ne 0) { throw 'Suite Python 3.11 fallita' }

git diff --check | Out-File -FilePath "$L\git_diff_check.txt" -Encoding utf8
$codeCheck = $LASTEXITCODE
"git diff --check exit=$codeCheck" | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
if ($codeCheck -ne 0) { throw 'Errori nel diff' }
"ALL OK $(Get-Date -Format o)" | Out-File -FilePath "$L\run_summary.txt" -Append -Encoding utf8
