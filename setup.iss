; https://jrsoftware.org/ishelp/index.php

#define AppName "NTON"
#define Version "2.1.1"

[Setup]
AppId={#AppName}
AppName={#AppName}
AppPublisher=rlaphoenix
AppPublisherURL=https://github.com/rlaphoenix/nton
AppReadmeFile=https://github.com/rlaphoenix/nton/blob/master/README.md
AppSupportURL=https://github.com/rlaphoenix/nton/issues
AppUpdatesURL=https://github.com/rlaphoenix/nton/blob/master/CHANGELOG.md
AppVerName={#AppName} {#Version}
AppVersion={#Version}
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
Compression=lzma2/max
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
LicenseFile=LICENSE
; Python 3.9 has dropped support for <= Windows 7/Server 2008 R2 SP1. https://jrsoftware.org/ishelp/index.php?topic=winvernotes
MinVersion=6.2
OutputBaseFilename={#AppName}-v{#Version}-setup
OutputDir=dist
OutputManifestFile={#AppName}-v{#Version}-setup-manifest.txt
PrivilegesRequiredOverridesAllowed=dialog commandline
SetupIconFile=nton/gui/resources/images/nton.ico
SolidCompression=yes
VersionInfoVersion=1.0.0
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: dist\{#AppName}\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppName}.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppName}.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppName}.exe"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
