param (
	[string]$file
)
Measure-Command { pypy $file | Write-Host }