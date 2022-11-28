param (
	[string]$file
)
Measure-Command { python $file | Write-Host }