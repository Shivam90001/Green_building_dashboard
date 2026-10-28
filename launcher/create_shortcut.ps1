$DesktopPath = "C:\Users\abc\Desktop"
$ShortcutPath = Join-Path $DesktopPath "Green Building Dashboard.lnk"
$LauncherPath = "C:\Users\abc\.gemini\antigravity\scratch\green_building_dashboard\launcher\start_dashboard.bat"
$WorkingDir = "C:\Users\abc\.gemini\antigravity\scratch\green_building_dashboard\launcher"
$IconPath = "C:\Users\abc\.gemini\antigravity\scratch\green_building_dashboard\launcher\icon.ico"

Write-Host "Creating Desktop shortcut..."
Write-Host "Shortcut Path: $ShortcutPath"
Write-Host "Target Launcher: $LauncherPath"

try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $LauncherPath
    $Shortcut.WorkingDirectory = $WorkingDir
    $Shortcut.IconLocation = $IconPath
    $Shortcut.Description = "Launch Green Building Performance Dashboard"
    $Shortcut.Save()
    Write-Host "Desktop shortcut created successfully!"
} catch {
    Write-Error "Failed to create desktop shortcut: $_"
}
