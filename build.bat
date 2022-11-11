@ECHO OFF
setlocal enabledelayedexpansion

set name=%~1
set publisher=%~2
set drive=%~3
set npath=%~4
set id=%~5

IF [%id%]==[] (
    set n=0
    :loop
    set rand=
    set /A rand=%RANDOM%%%16+1
    set /A n=n+1
    IF !rand!==1 set rand!n!=a
    IF !rand!==2 set rand!n!=b
    IF !rand!==3 set rand!n!=c
    IF !rand!==4 set rand!n!=d
    IF !rand!==5 set rand!n!=e
    IF !rand!==6 set rand!n!=f
    IF !rand!==7 set rand!n!=1
    IF !rand!==8 set rand!n!=2
    IF !rand!==9 set rand!n!=3
    IF !rand!==10 set rand!n!=4
    IF !rand!==11 set rand!n!=5
    IF !rand!==12 set rand!n!=6
    IF !rand!==13 set rand!n!=7
    IF !rand!==14 set rand!n!=8
    IF !rand!==15 set rand!n!=9
    IF !rand!==16 set rand!n!=0
    IF !n! LSS 11 goto loop
    set id=01%rand1%%rand2%%rand3%%rand4%%rand5%%rand6%%rand7%%rand8%%rand9%%rand10%%rand11%000
)

set fullpath=%drive%:%npath%
set filename=%name% by %publisher% [%id%]

echo Building...
echo Name: %name%
echo Publisher: %publisher%
echo Path: %fullpath%
echo ID: %id%

REM Prepare folders and ensure control and romfs are clean
REM It wouldn't be good if random data were in these folders!
IF NOT EXIST "output" mkdir output
rmdir /S/Q control
mkdir control
rmdir /S/Q romfs
mkdir romfs

REM Extract the nacp from the NRO
nstool -k .\prod.keys --nacp "control/control.nacp" "%fullpath%"

REM Extract the icon from the NRO
nstool -k .\prod.keys --icon "control/icon_AmericanEnglish.dat" "%fullpath%"

REM Prepare the icon as a jpeg 256x256 with stripped metadata
REM Even extracted icons may not be up to spec for NSP icons
magick mogrify -format jpg -resize 256x256 -strip "control/icon_AmericanEnglish.dat"
del control\icon_AmericanEnglish.dat
REN "control\icon_AmericanEnglish.jpg" "icon_AmericanEnglish.dat"

REM Prepare the nextArgv and nextNroPath ROMs
echo|set /p="sdmc:%npath%"> romfs/nextArgv
echo|set /p="sdmc:%npath%"> romfs/nextNroPath

REM Build the NSP
hacbrewpack.exe --titleid %id% --titlename "%name%" --titlepublisher "%publisher%" --nspdir output -k .\prod.keys

REM Post-Cleanup
rmdir /S/Q hacbrewpack_backup
rmdir /S/Q control
rmdir /S/Q romfs

REM Rename NSP to something better
REN "output\%id%.nsp" "%filename%.nsp"

echo %filename%.nsp is ready!
