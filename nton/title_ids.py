# Source: https://switchbrew.org/wiki/Title_list
# Last updated: 2022-11-12 08:00 UTC+0
# When updating make sure all title IDs are lowercase hex, 16 digits in length (a-z0-9{16}).
import logging
import sys
import time

import jsonpickle
import requests

from nton.constants import Files

system_modules = (
    # https://switchbrew.org/wiki/Title_list#System_Modules
    "0100000000000000",  # https://switchbrew.org/wiki/Filesystem_services
    "0100000000000001",  # https://switchbrew.org/wiki/Loader_services
    "0100000000000002",  # https://switchbrew.org/wiki/NCM_services
    "0100000000000003",  # https://switchbrew.org/wiki/Process_Manager_services
    "0100000000000004",  # https://switchbrew.org/wiki/Services_API
    "0100000000000005",  # https://switchbrew.org/wiki/Boot
    "0100000000000006",  # https://switchbrew.org/wiki/USB_services
    "0100000000000007",  # https://switchbrew.org/wiki/TMA_services
    "0100000000000008",  # https://switchbrew.org/wiki/Boot2
    "0100000000000009",  # https://switchbrew.org/wiki/Settings_services
    "010000000000000a",  # https://switchbrew.org/wiki/Bus_services
    "010000000000000b",  # https://switchbrew.org/wiki/Bluetooth_Driver_services
    "010000000000000c",  # https://switchbrew.org/wiki/BCAT_services
    "010000000000000d",  # dmnt (currently not present on retail devices)
    "010000000000000e",  # https://switchbrew.org/wiki/Friend_services
    "010000000000000f",  # https://switchbrew.org/wiki/Network_Interface_services
    "0100000000000010",  # https://switchbrew.org/wiki/PTM_services
    "0100000000000011",  # shell (currently not present on retail devices)
    "0100000000000012",  # https://switchbrew.org/wiki/Sockets_services
    "0100000000000013",  # https://switchbrew.org/wiki/HID_services
    "0100000000000014",  # https://switchbrew.org/wiki/Audio_services
    "0100000000000015",  # https://switchbrew.org/wiki/Log_services
    "0100000000000016",  # https://switchbrew.org/wiki/WLAN_services
    "0100000000000017",  # cs (currently not present on retail devices)
    "0100000000000018",  # https://switchbrew.org/wiki/LDN_services
    "0100000000000019",  # https://switchbrew.org/wiki/NV_services
    "010000000000001a",  # https://switchbrew.org/wiki/PCV_services
    "010000000000001b",  # https://switchbrew.org/wiki/PPC_services / https://switchbrew.org/wiki/Capmtp_services
    "010000000000001c",  # https://switchbrew.org/wiki/Nvnflinger_services
    "010000000000001d",  # https://switchbrew.org/wiki/PCIe_services
    "010000000000001e",  # https://switchbrew.org/wiki/Account_services
    "010000000000001f",  # https://switchbrew.org/wiki/NS_Services
    "0100000000000020",  # https://switchbrew.org/wiki/NFC_services
    "0100000000000021",  # https://switchbrew.org/wiki/PSC_services
    "0100000000000022",  # https://switchbrew.org/wiki/Capture_services
    "0100000000000023",  # https://switchbrew.org/wiki/AM_services
    "0100000000000024",  # https://switchbrew.org/wiki/SSL_services
    "0100000000000025",  # https://switchbrew.org/wiki/NIM_services
    "0100000000000026",  # cec (currently not present on retail devices)
    "0100000000000027",  # tspm (currently not present on retail devices)
    "0100000000000028",  # https://switchbrew.org/wiki/SPL_services
    "0100000000000029",  # https://switchbrew.org/wiki/Backlight_services
    "010000000000002a",  # https://switchbrew.org/wiki/BTM_services
    "010000000000002b",  # https://switchbrew.org/wiki/Error_Report_services
    "010000000000002c",  # time (currently not present on retail devices)
    "010000000000002d",  # https://switchbrew.org/wiki/Display_services
    "010000000000002e",  # https://switchbrew.org/wiki/Parental_Control_services
    "010000000000002f",  # https://switchbrew.org/wiki/NPNS_services
    "0100000000000030",  # https://switchbrew.org/wiki/Error_Upload_services
    "0100000000000031",  # arp / https://switchbrew.org/wiki/Glue_services
    "0100000000000032",  # eclct
    "0100000000000033",  # https://switchbrew.org/wiki/ETicket_services
    "0100000000000034",  # https://switchbrew.org/wiki/Fatal_services
    "0100000000000035",  # https://switchbrew.org/wiki/GRC_services
    "0100000000000036",  # https://switchbrew.org/wiki/Creport
    "0100000000000037",  # https://switchbrew.org/wiki/Loader_services#ldr:ro
    "0100000000000038",  # https://switchbrew.org/wiki/Profiler_services (currently not present on retail devices)
    "0100000000000039",  # https://switchbrew.org/wiki/Shared_Database_services
    "010000000000003a",  # https://switchbrew.org/wiki/Migration_services
    "010000000000003b",  # https://switchbrew.org/wiki/JIT_services
    "010000000000003c",  # https://switchbrew.org/wiki/Jpegdec_services
    "010000000000003d",  # https://switchbrew.org/wiki/Safemode
    "010000000000003e",  # https://switchbrew.org/wiki/OLSC_services
    "010000000000003f",  # dt (currently not present on retail devices)
    "0100000000000040",  # nd (currently not present on retail devices)
    "0100000000000041",  # https://switchbrew.org/wiki/NGCT_services
    "0100000000000042",  # https://switchbrew.org/wiki/PGL_services
    "0100000000000043",  # (currently not present on retail devices)
    "0100000000000044",  # (currently not present on retail devices)
    "0100000000000045",  # https://switchbrew.org/wiki/OMM_services
    "0100000000000046",  # https://switchbrew.org/wiki/Ethernet_services
)

system_data_archives = (
    # https://switchbrew.org/wiki/Title_list#System_Data_Archives
    "0100000000000800",  # https://switchbrew.org/wiki/SSL_services#CertStore
    "0100000000000801",  # ErrorMessage
    "0100000000000802",  # MiiModel
    "0100000000000803",  # BrowserDll
    "0100000000000804",  # Help
    "0100000000000805",  # SharedFont
    "0100000000000806",  # NgWord
    "0100000000000807",  # SsidList
    "0100000000000808",  # Dictionary
    "0100000000000809",  # SystemVersion
    "010000000000080a",  # AvatarImage
    "010000000000080b",  # LocalNews
    "010000000000080c",  # Eula (Eura)
    "010000000000080d",  # UrlBlackList
    "010000000000080e",  # TimeZoneBinary
    "010000000000080f",  # CertStoreCruiser (BrowserCertStore)
    "0100000000000810",  # FontNintendoExtension
    "0100000000000811",  # FontStandard
    "0100000000000812",  # FontKorean
    "0100000000000813",  # FontChineseTraditional
    "0100000000000814",  # FontChineseSimple
    "0100000000000815",  # FontBfcpx
    "0100000000000816",  # SystemUpdate
    "0100000000000818",  # FirmwareDebugSettings
    "0100000000000819",  # BootImagePackage
    "010000000000081a",  # BootImagePackageSafe
    "010000000000081b",  # BootImagePackageExFat
    "010000000000081c",  # BootImagePackageExFatSafe
    "010000000000081d",  # FatalMessage
    "010000000000081e",  # ControllerIcon
    "010000000000081f",  # PlatformConfigIcosa
    "0100000000000820",  # PlatformConfigCopper
    "0100000000000821",  # PlatformConfigHoag
    "0100000000000822",  # ControllerFirmware
    "0100000000000823",  # NgWord2
    "0100000000000824",  # PlatformConfigIcosaMariko
    "0100000000000825",  # ApplicationBlackList
    "0100000000000826",  # RebootlessSystemUpdateVersion
    "0100000000000827",  # ContentActionTable
    "0100000000000828",  # FunctionBlackList
    "0100000000000829",  # PlatformConfigCalcio
    "0100000000000830",  # NgWordT
    "0100000000000831",  # PlatformConfigAula
    "0100000000000832",  # Firmware binaries for Aula's dock
)

system_applets = (
    # https://switchbrew.org/wiki/Title_list#System_Applets
    "0100000000001000",  # qlaunch (SystemAppletMenu)
    "0100000000001001",  # auth (LibraryAppletAuth)
    "0100000000001002",  # cabinet (LibraryAppletCabinet)
    "0100000000001003",  # controller (LibraryAppletController)
    "0100000000001004",  # dataErase (LibraryAppletDataErase)
    "0100000000001005",  # error (LibraryAppletError)
    "0100000000001006",  # netConnect (LibraryAppletNetConnect)
    "0100000000001007",  # playerSelect (LibraryAppletPlayerSelect)
    "0100000000001008",  # swkbd (LibraryAppletSwkbd)
    "0100000000001009",  # miiEdit (LibraryAppletMiiEdit)
    "010000000000100a",  # LibAppletWeb (LibraryAppletWeb)
    "010000000000100b",  # LibAppletShop (LibraryAppletShop)
    "010000000000100c",  # overlayDisp (OverlayApplet)
    "010000000000100d",  # photoViewer (LibraryAppletPhotoViewer)
    "010000000000100e",  # set (LibraryAppletSet)
    "010000000000100f",  # LibAppletOff (LibraryAppletOfflineWeb)
    "0100000000001010",  # LibAppletLns (LibraryAppletLoginShare)
    "0100000000001011",  # LibAppletAuth (LibraryAppletWifiWebAuth)
    "0100000000001012",  # starter (DummyStarter)
    "0100000000001013",  # myPage (LibraryAppletMyPage)
    "0100000000001014",  # PlayReport
    "0100000000001015",  # maintenance (MaintenanceMenu)
    "0100000000001016",
    "0100000000001017",
    "0100000000001018",
    "0100000000001019",
    "010000000000101a",  # gift (LibraryAppletGift)
    "010000000000101b",  # DummyECApplet (LibraryAppletDummyShop)
    "010000000000101c",  # userMigration (LibraryAppletUserMigration)
    "010000000000101d",  # EncounterSys (LibraryAppletPreomiaSys)
    "010000000000101e",
    "010000000000101f",
    "0100000000001020",  # story (LibraryAppletStory)
    "0100000000001021",
    "0100000000001023",
    "0100000000001024",
    "0100000000001025",
    "0100000000001026",
    "0100000000001027",
    "0100000000001028",
    "0100000000001029",
    "010000000000102a",
    "010000000000102b",
    "010000000000102c",
    "010000000000102e",
    "010000000000102f",
    "0100000000001030",
    "0100000000001031",
    "0100000000001032",
    "0100000000001033",
    "0100000000001034",
    "0100000000001037",
    "0100000000001038",  # sample (LibraryAppletSample)
    "010000000000103c",
    "010000000000103e",
    "0100000000001fff",  # EndOceanProgramId
)


development_system_applets = (
    # https://switchbrew.org/wiki/Title_list#Development_System_Applets
    "0100000000002000",  # A2BoardFunction
    "0100000000002001",  # A3Wireless
    "0100000000002002",  # C1LcdAndKey (LcdAndKey)
    "0100000000002003",  # C2UsbHpmic (UsbAndHPMicTest)
    "0100000000002004",  # C3Aging (Aging)
    "0100000000002005",  # C4SixAxis (6axisTest)
    "0100000000002006",  # C5Wireless (AssembledWireless)
    "0100000000002007",  # C7FinalCheck (FinalCheck)
    "010000000000203f",  # AutoCapture
    "0100000000002040",  # DevMenuCommandSystem
    "0100000000002041",  # recovery
    "0100000000002042",  # DevMenuSystem
    "0100000000002044",  # HB-TBIntegrationTest
    "010000000000204d",  # BackupSaveData
    "010000000000204e",  # A4BoardCalWriti (BoardCalWriting)
    "0100000000002054",  # RepairSslCertificate
    "0100000000002055",  # GameCardWriter
    "0100000000002056",  # UsbPdTestTool
    "0100000000002057",  # RepairDeletePctl
    "0100000000002058",  # RepairBackup
    "0100000000002059",  # RepairRestore
    "010000000000205a",  # RepairAccountTransfer
    "010000000000205b",  # RepairAutoNetworkUpdater
    "010000000000205c",  # RefurbishReset
    "010000000000205d",  # RepairAssistCup
    "010000000000205e",  # RepairPairingCutter
    "0100000000002064",  # DevMenu
    "0100000000002065",  # DevMenuApp
    "0100000000002066",  # GetGameCardAsicInfo
    "0100000000002068",  # NfpDebugToolSystem
    "0100000000002069",  # AlbumSynchronizer
    "0100000000002071",  # SnapShotDumper
    "0100000000002073",  # DevMenuSystemApp
    "0100000000002099",  # DevOverlayDisp
    "010000000000209a",  # NandVerifier
    "010000000000209b",  # GpuCoreDumper
    "010000000000209c",  # TestApplication (TestApplicationLauncher)
    "010000000000209e",  # HelloWorld
    "01000000000020a0",  # XcieWriter
    "01000000000020a1",  # GpuOverrunNotifier
    "01000000000020c8",  # NfpDebugTool
    "01000000000020ca",  # NoftWriter
    "01000000000020d0",  # BcatSystemDebugTool
    "01000000000020d1",  # DevSafeModeUpdater
    "01000000000020d3",  # ControllerConnectionAnalyzer
    "01000000000020d4",  # DevKitUpdater
    "01000000000020d6",  # RepairTimeReviser
    "01000000000020d7",  # RepairReinitializeFuelGauge
    "01000000000020da",  # RepairAbortMigration
    "01000000000020dc",  # RepairShowDeviceId
    "01000000000020dd",  # RepairSetCycleCountReliability
    "01000000000020e0",  # Interface
    "01000000000020e1",  # AlbumDownloader
    "01000000000020e3",  # FuelGaugeDumper
    "01000000000020e4",  # UnsafeExtract
    "01000000000020e5",  # UnsafeEngrave
    "01000000000020ee",  # BluetoothSettingTool
    "01000000000020f0",  # ApplicationInstallerRomfs (devmenuapp_installer)
    "0100000000002100",  # DevMenuLotcheckDownloader
    "0100000000002101",  # DevMenuCommand
    "0100000000002102",  # ExportPartition
    "0100000000002103",  # SystemInitializer (SystemInitializ)
    "0100000000002104",  # SystemUpdaterHostFs
    "0100000000002105",  # WriteToStorage
    "0100000000002106",  # CalWriter (CalWriterManu)
    "0100000000002107",  # SettingsManager
    "0100000000002109",  # testBuildSystemIris
    "010000000000210a",  # SystemUpdater
    "010000000000210b",  # nvnflinger_util
    "010000000000210c",  # ControllerFirmwareUpdater
    "010000000000210d",  # testBuildSystemNintendoWare (Test)
    "0100000000002110",  # TestSaveDataCreator
    "0100000000002111",  # C9LcdSpker
    "0100000000002114",  # RankTurn
    "0100000000002116",  # BleTestTool
    "010000000000211a",  # PreinstallAppWriter
    "010000000000211c",  # ControllerSerialFlashTool
    "010000000000211d",  # ControllerFlashWriter
    "010000000000211e",  # Handling
    "010000000000211f",  # Hid
    "0100000000002120",  # ControllerTestApp
    "0100000000002121",  # HidInspectionTool
    "0100000000002124",  # BatteryCyclesEditor
    "0100000000002125",  # UsbFirmwareUpdater
    "0100000000002126",  # PalmaSerialCodeTool
    "0100000000002127",  # renderdoccmd
    "0100000000002128",  # HidInspectionToolProd
    "010000000000212c",  # ExhibitionMenu
    "010000000000212f",  # ExhibitionSaveData
    "0100000000002130",  # LuciaConverter
    "0100000000002133",  # CalDumper
    "0100000000002134",  # AnalogStickEvaluationTool
    "010000000000216d",  # ExhibitionSaveDataSnapshot (Unofficial name)
    "0100000000002178",  # SecureStartupSettings (Unofficial name)
    "010000000000217d",  # CradleFirmwareUpdater
)


debug_system_modules = (
    # https://switchbrew.org/wiki/Title_list#Debug_System_Modules
    "0100000000003002",  # DummyProcess
    "0100000000003003",  # DebugMonitor0
    "0100000000003004",  # SystemHelloWorld
)


development_system_modules = (
    # https://switchbrew.org/wiki/Title_list#Development_System_Modules
    "010000000000b120",  # nvdbgsvc
    "010000000000b123",  # acc:CORNX
    "010000000000b14a",  # manu
    "010000000000b14b",  # ManuUsbLoopBack
    "010000000000b1b8",  # DevFwdbgHbPackage
    "010000000000b1b9",  # DevFwdbgUsbPackage
    "010000000000b1ba",  # ProdFwdbgPackage
    "010000000000b22a",  # scs
    "010000000000b22b",  # ControllerFirmwareDebug
    "010000000000b240",  # htc
)


bdk_system_modules = (
    # https://switchbrew.org/wiki/Title_list#Bdk_System_Modules
    "010000000000c600",  # BdkSample01
    "010000000000c601",  # BdkSample02
    "010000000000c602",  # BdkSample03
    "010000000000c603",  # BdkSample04
)


micro_system_modules = (
    # https://switchbrew.org/wiki/Title_list#Micro_System_Modules
    "010000000000d609",  # dmnt.gen2
    "010000000000d60a",
    "010000000000d60b",
    "010000000000d60c",
    "010000000000d60d",
    "010000000000d60e",
    "010000000000d610",
    "010000000000d611",
    "010000000000d612",
    "010000000000d613",
    "010000000000d614",
    "010000000000d615",
    "010000000000d616",
    "010000000000d617",
    "010000000000d619",
    "010000000000d623",  # DevServer
    "010000000000d633",
)


system_applications = (
    # https://switchbrew.org/wiki/Title_list#System_Applications
    "01008bb00013c000",  # flog (NES emulator)
    "0100069000078000",  # RetailInteractiveDisplayMenu (DevQuestMenu)
    "010000b003486000",  # AudioUsbMicDebugTool
    "0100458001e04000",  # BcatTestApp01
    "0100f910020f8000",  # BcatTestApp02
    "0100b7d0020fc000",  # BcatTestApp03
    "0100132002100000",  # BcatTestApp04
    "0100935002116000",  # BcatTestApp05
    "0100da4002130000",  # BcatTestApp06
    "0100b0f002104000",  # BcatTestApp07
    "010051e002132000",  # BcatTestApp08
    "01004cb0015c8000",  # BcatTestApp09
    "01009720015ca000",  # BcatTestApp10
    "01002f20015c6000",  # BcatTestApp11
    "0100204001f90000",  # BcatTestApp12
    "0100060001f92000",  # BcatTestApp13
    "0100c26001f94000",  # BcatTestApp14
    "0100462001f96000",  # BcatTestApp15
    "01005c6001f98000",  # BcatTestApp16
    "010070000e3c0000",  # EncounterUsr (LibraryAppletPreomiaUsr)
    "010086000e49c000",  # EncounterUsrDummy (LibraryAppletPreomiaUsrDummy)
    "0100810002d5a000",  # ShopMonitaringTool
    "010023d002b98000",  # DeltaStress
    "010099f00d810000",
)


pre_release_system_applets = (
    # https://switchbrew.org/wiki/Title_list#Pre-release_System_Applets
    "1000000000000001",  # SystemInitializer (SystemInitializ)
    "1000000000000004",  # CalWriter (CalWriterManu)
    "1000000000000005",  # DevMenuCommand
    "1000000000000006",  # SettingsManager
    "1000000000000007",  # DevMenu (debug) / TestApplication (factory)
    "100000000000000b",  # SnapShotDumper
    "100000000000000c",  # SystemUpdater
    "100000000000000e",  # ControllerFirmwareUpdater
)


pre_release_system_modules = (
    # https://switchbrew.org/wiki/Title_list#Pre-release_System_Modules
    "1000000000000201",  # usb
    "1000000000000202",  # tma
    "1000000000000203",  # boot2
    "1000000000000204",  # settings
    "1000000000000205",  # Bus
    "1000000000000206",  # bluetooth
    "1000000000000208",  # DebugMonitor0
    "1000000000000209",  # dmnt
    "100000000000020b",  # nifm
    "100000000000020c",  # ptm
    "100000000000020e",  # bsdsocket
    "100000000000020f",  # hid
    "1000000000000210",  # audio
    "1000000000000212",  # LogManager
    "1000000000000213",  # wlan
    "1000000000000214",  # cs
    "1000000000000215",  # ldn
    "1000000000000216",  # nvservices
    "1000000000000217",  # pcv
    "1000000000000218",  # ppc
    "100000000000021a",  # lbl0
    "100000000000021b",  # nvnflinger
    "100000000000021c",  # pcie
    "100000000000021d",  # account
    "100000000000021e",  # ns
    "100000000000021f",  # nfc
    "1000000000000220",  # psc
    "1000000000000221",  # capsrv
    "1000000000000222",  # am
    "1000000000000223",  # ssl
    "1000000000000224",  # nim
)


# The following are unofficial title IDs I have pre-defined to be used for specific homebrew
# This is to keep a specific title ID throughout each release's bundled prebuilt NSPs
unofficial = {
    "hbmenu": "010d6fd3b35cd000",              # https://github.com/switchbrew/nx-hbmenu
    "aio-switch-updater": "016454da0e765000",  # https://github.com/HamletDuFromage/aio-switch-updater
}


def get_game_title_ids() -> dict:
    """Get a mapping of Game Title IDs -> Game Names from Tinfoil's API."""
    res = requests.get(
        url="https://tinfoil.media/Title/ApiJson/",
        params={
            # is this actually returning a full list?
            "rating_content": "",
            "language": "",
            "category": "",
            "region": "ar,at,au,be,bg,br,ca,ch,cl,cn,co,cy,cz,de,dk,ee,es,fi,fr,gb,gr,hk,hr,hu,"
                      "ie,it,jp,kr,lt,lu,lv,mt,mx,nl,no,nz,pe,pl,pt,ro,ru,se,si,sk,us,xx,za,zh",
            "rating": "",
            "_": str(time.time_ns() // 1000000)
        },
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Origin": "https://tinfoil.io",
            "Referer": "https://tinfoil.io/"
        }
    )

    if not res.ok:
        raise requests.ConnectionError(
            f"Failed to get a list of Game Title IDs from Tinfoil's API, [{res.status_code}]")

    title_ids = {
        title["id"].lower(): title["name"].removeprefix("<a>").removesuffix("</a>")
        for title in res.json()["data"]
    }

    return title_ids


if not Files.game_title_ids.exists():
    print("[ERROR]: The Game Title ID registry is missing! Please re-add `/assets/game_title_ids.json`!")
    sys.exit(1)
if Files.game_title_ids.stat().st_mtime + (60 * 24 * 30) < time.time():
    log = logging.getLogger()
    log.warning("Game Title ID registry is quite old, I recommend updating it with `nton update-game-ids`")
game_title_ids = jsonpickle.loads(Files.game_title_ids.read_text("utf8"))


ALL_SYSTEM = (
    *system_modules,
    *system_data_archives,
    *system_applets,
    *development_system_applets,
    *debug_system_modules,
    *development_system_modules,
    *bdk_system_modules,
    *micro_system_modules,
    *system_applications,
    *pre_release_system_applets,
    *pre_release_system_modules
)

ALL = (
    *ALL_SYSTEM,
    *list(game_title_ids),
    *list(unofficial.values())
)
