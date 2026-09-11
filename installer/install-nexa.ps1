$ErrorActionPreference = "Stop"

Write-Host "Nexa Installer"
Write-Host "==============="

$extension = ".nexa"
$fileType = "Nexa.SourceFile"
$iconPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\nexa-file.ico"))

# .nexa -> Nexa.SourceFile
New-Item -Path "HKCU:\Software\Classes\$extension" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Classes\$extension" -Name "(Default)" -Value $fileType

# Nexa-Dateityp
New-Item -Path "HKCU:\Software\Classes\$fileType" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Classes\$fileType" -Name "(Default)" -Value "Nexa Source File"

# Nexa-Icon
$iconKey = "HKCU:\Software\Classes\$fileType\DefaultIcon"
New-Item -Path $iconKey -Force | Out-Null
Set-ItemProperty -Path $iconKey -Name "(Default)" -Value $iconPath

# ?ffnen mit VS Code
$commandKey = "HKCU:\Software\Classes\$fileType\shell\open\command"
New-Item -Path $commandKey -Force | Out-Null
Set-ItemProperty -Path $commandKey -Name "(Default)" -Value 'code "%1"'

# Explorer aktualisieren
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class ExplorerRefresh {
    [DllImport("shell32.dll")]
    public static extern void SHChangeNotify(
        uint wEventId,
        uint uFlags,
        IntPtr dwItem1,
        IntPtr dwItem2);
}
"@

[ExplorerRefresh]::SHChangeNotify(0x08000000, 0x0000, [IntPtr]::Zero, [IntPtr]::Zero)

Write-Host ""
Write-Host "Nexa wurde erfolgreich registriert!"
Write-Host "Dateiendung: .nexa"
Write-Host "Icon: $iconPath"
Write-Host "?ffnen: VS Code"
