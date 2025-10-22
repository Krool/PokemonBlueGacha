; Inno Setup Script for Pokémon Blue Gacha
; Download Inno Setup from: https://jrsoftware.org/isdl.php
; Compile this script to create a Windows installer

#define MyAppName "Pokémon Blue Gacha"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Name"
#define MyAppURL "https://github.com/USERNAME/PokemonBlueGacha"
#define MyAppExeName "PokemonBlueGacha.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application
AppId={{8E9F2A5C-3D7B-4F1E-9A8D-2C5E7B3F6A4D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\PokemonBlueGacha
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installers
OutputBaseFilename=PokemonBlueGacha_Setup_v{#MyAppVersion}
SetupIconFile=appicon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\README"; Filename: "{app}\README.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Welcome to Pokémon Blue Gacha Setup!' + #13#10 + #13#10 + 
         'This will install the complete gacha collection game featuring all 151 Generation 1 Pokémon plus 79 classic items!' + #13#10 + #13#10 +
         'Click Next to continue.', mbInformation, MB_OK);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Installation complete!' + #13#10 + #13#10 + 
           'Your game saves will be stored in:' + #13#10 +
           ExpandConstant('{userdocs}') + '\.pokemonbluegacha' + #13#10 + #13#10 +
           'Click Finish to launch the game!', mbInformation, MB_OK);
  end;
end;

