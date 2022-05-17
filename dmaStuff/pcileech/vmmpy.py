# vmmpy.py
#
# Provides a convenient python interface for the memory process file system
# virtual memory manager - vmm.dll / vmmpyc.pyc.
#
# Fast and convenient python access towards the native vmm.dll and in some
# cases linked pcileech.dll libraries. This wrapper also provides for code
# completion in some supported dev environments.
#
# https://github.com/ufrisk/
#
# (c) Ulf Frisk, 2018-2020
# Author: Ulf Frisk, pcileech@frizk.net
#
# Header Version: 3.2
#

import atexit
from vmmpyc import *

#------------------------------------------------------------------------------
# VmmPy CONSTANTS BELOW:
# NB! Only some unrelated contants are put here. Constants more closely related
#     to functionality is put close to the functionality itself.
#------------------------------------------------------------------------------

# NTSTATUS values. (Used/Returned by Write file plugin callbacks).
VMMPY_STATUS_SUCCESS =                  0x00000000
VMMPY_STATUS_UNSUCCESSFUL =             0xC0000001
VMMPY_STATUS_END_OF_FILE =              0xC0000011
VMMPY_STATUS_FILE_INVALID =             0xC0000098

# SYSTEM values - used to determine if a plugin is supported or not for
# the current system that is being analyzed.
VMMPY_SYSTEM_UNKNOWN_X64 =              0x0001
VMMPY_SYSTEM_WINDOWS_X64 =              0x0002
VMMPY_SYSTEM_UNKNOWN_X86 =              0x0003
VMMPY_SYSTEM_WINDOWS_X86 =              0x0004

# MEMORYMODEL values - used to determine if a plugin is supported or not
# for a specific memory model.
VMMPY_MEMORYMODEL_NA =                  0x0000
VMMPY_MEMORYMODEL_X86 =                 0x0001
VMMPY_MEMORYMODEL_X86PAE =              0x0002
VMMPY_MEMORYMODEL_X64 =                 0x0003

# EVENT values - received by the notify callback function for specific events
# occuring in the native plugin manager / vmm / memory process file system.
VMMPY_PLUGIN_EVENT_VERBOSITYCHANGE =    0x01
VMMPY_PLUGIN_EVENT_TOTALREFRESH =       0x02
VMMPY_PLUGIN_EVENT_REFRESH_PROCESS_TOTAL = 0x02
VMMPY_PLUGIN_EVENT_REFRESH_REGISTRY =   0x04

# WINDOWS REGISTRY contants below:
VMMPY_WINREG_NONE =                     0x00
VMMPY_WINREG_SZ =                       0x01
VMMPY_WINREG_EXPAND_SZ =                0x02
VMMPY_WINREG_BINARY =                   0x03
VMMPY_WINREG_DWORD =                    0x04
VMMPY_WINREG_DWORD_BIG_ENDIAN =         0x05
VMMPY_WINREG_LINK =                     0x06
VMMPY_WINREG_MULTI_SZ =                 0x07
VMMPY_WINREG_RESOURCE_LIST =            0x08
VMMPY_WINREG_FULL_RESOURCE_DESCRIPTOR = 0x09
VMMPY_WINREG_RESOURCE_REQUIREMENTS_LIST = 0x0A
VMMPY_WINREG_QWORD =                    0x0B

#------------------------------------------------------------------------------
# VmmPy INITIALIZATION FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_Close():
    """Close an initialized instance of VMM.DLL and clean up all allocated resources including plugins, linked PCILeech.dll and other memory resources.

    Keyword arguments:
    N/A
    
    Example:
    VmmPy_Close()
    """
    atexit.unregister(VmmPy_Close)
    VMMPYC_Close()



def VmmPy_Refresh():
    """Force refresh the internal state of the VMM.DLL - refreshing process listings and internal caches. NB! function may take a long time to execute!

    Keyword arguments:
    N/A
    
    Example:
    VmmPy_Refresh()
    """
    VMMPYC_Refresh(0)



def VmmPy_Initialize(args, is_printf = True, is_verbose = False, is_verbose_extra = False, is_verbose_tlp = False, page_table_base = 0):
    """Initialize VmmPy and the Virtual Memory Manager VMM.DLL with arguments as
       in the argument list args. Important is the -device option and optionally
       -remote option as closer described in the MemProcFS and LeechCore projects.

    Keyword arguments:
    file_name -- str: memory dump file to load.
    is_printf -- bool: console output from vmm.dll is enabled.
    is_verbose -- bool: verbose level.
    is_verbose_extra -- bool: extra verbose level.
    is_verbose_tlp -- bool: show FPGA TLPs or similar - super verbose!
    page_table_base -- int: optional page directory base of the OS kernel or a x64 process.
    
    Example:
    VmmPy_Initialize(['c:\\temp\\dump.raw'])
    VmmPy_Initialize(['-device', 'dumpit','-remote', 'rpc://insecure:remote.example.com'])
    """
    if page_table_base > 0:
        args.append("-cr3")
        args.append(str(page_table_base))
    if is_printf:
        args.append("-printf")
    if is_verbose:
        args.append("-v")
    if is_verbose_extra:
        args.append("-vv")
    if is_verbose_tlp:
        args.append("-vvv")
    VMMPYC_Initialize(args)
    atexit.register(VmmPy_Close)



#------------------------------------------------------------------------------
# VmmPy CONFIGURATION FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

VMMPY_OPT_CORE_PRINTF_ENABLE                  = 0x80000001  # RW
VMMPY_OPT_CORE_VERBOSE                        = 0x80000002  # RW
VMMPY_OPT_CORE_VERBOSE_EXTRA                  = 0x80000003  # RW
VMMPY_OPT_CORE_VERBOSE_EXTRA_TLP              = 0x80000004  # RW
VMMPY_OPT_CORE_MAX_NATIVE_ADDRESS             = 0x80000005  # R
VMMPY_OPT_CORE_SYSTEM                         = 0x80000007  # R
VMMPY_OPT_CORE_MEMORYMODEL                    = 0x80000008  # R

VMMPY_OPT_CONFIG_IS_REFRESH_ENABLED           = 0x40000001  # R - 1/0
VMMPY_OPT_CONFIG_TICK_PERIOD                  = 0x40000002  # RW - base tick period in ms
VMMPY_OPT_CONFIG_READCACHE_TICKS              = 0x40000003  # RW - memory cache validity period (in ticks)
VMMPY_OPT_CONFIG_TLBCACHE_TICKS               = 0x40000004  # RW - page table (tlb) cache validity period (in ticks)
VMMPY_OPT_CONFIG_PROCCACHE_TICKS_PARTIAL      = 0x40000005  # RW - process refresh (partial) period (in ticks)
VMMPY_OPT_CONFIG_PROCCACHE_TICKS_TOTAL        = 0x40000006  # RW - process refresh (full) period (in ticks)
VMMPY_OPT_CONFIG_VMM_VERSION_MAJOR            = 0x40000007  # R
VMMPY_OPT_CONFIG_VMM_VERSION_MINOR            = 0x40000008  # R
VMMPY_OPT_CONFIG_VMM_VERSION_REVISION         = 0x40000009  # R
VMMPY_OPT_CONFIG_STATISTICS_FUNCTIONCALL      = 0x4000000A  # RW - enable function call statistics (.status/statistics_fncall file)

VMMDLL_OPT_WIN_VERSION_MAJOR                  = 0x40000101  # R
VMMDLL_OPT_WIN_VERSION_MINOR                  = 0x40000102  # R
VMMDLL_OPT_WIN_VERSION_BUILD                  = 0x40000103  # R


def VmmPy_ConfigGet(vmmpy_opt_id):
    """Retrieve a configuration setting given a VMMPY_OPT_* option.

    Keyword arguments:
    vmmpy_opt_id -- int: the configuration value to retrieve as defined by VMMPY_OPT_*.
    return -- int: configuration value. (Fail: -1).
    
    Example:
    VmmPy_ConfigGet(VMMPY_OPT_CORE_PRINTF_ENABLE) --> 1
    """
    return VMMPYC_ConfigGet(vmmpy_opt_id)



def VmmPy_ConfigSet(vmmpy_opt_id, value):
    """Set a configuration setting given a VMMPY_OPT_* option.

    Keyword arguments:
    vmmpy_opt_id -- int: the configuration value to retrieve as defined by VMMPY_OPT_*.
    value -- int: value to set.
    
    Example:
    VmmPy_ConfigSet(VMMPY_OPT_CORE_PRINTF_ENABLE, 0)
    """
    VMMPYC_ConfigSet(vmmpy_opt_id, value)



def VmmPy_GetVersion():
    """Retrieve the Version of the core functionality in the VMM.DLL.
  
    Example:
    VmmPy_GetVersion() -> 1.0.0
    """
    verMajor = VMMPYC_ConfigGet(VMMPY_OPT_CONFIG_VMM_VERSION_MAJOR)
    verMinor = VMMPYC_ConfigGet(VMMPY_OPT_CONFIG_VMM_VERSION_MINOR)
    verRevision = VMMPYC_ConfigGet(VMMPY_OPT_CONFIG_VMM_VERSION_REVISION)
    return str(verMajor) + '.' + str(verMinor) + '.' + str(verRevision)



#------------------------------------------------------------------------------
# VmmPy MEMORY ACCESS FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

VMMPY_FLAG_NOCACHE           = 0x0001      # do not use the data cache (force reading from memory acquisition device)
VMMPY_FLAG_ZEROPAD_ON_FAIL   = 0x0002      # zero pad failed physical memory reads and report success if read within range of physical memory.
VMMPY_FLAG_FORCECACHE_READ   = 0x0008      # force use of cache - fail non-cached pages - only valid for reads, invalid with VMM_FLAG_NOCACHE/VMM_FLAG_ZEROPAD_ON_FAIL.



def VmmPy_MemRead(pid, address, length, flags = 0):
    """Read memory given a pid, a (64-bit) address and length. Return result as bytes.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory. -1 when reading physical memory.
    address -- int: the address to read.
    length -- int: the number of bytes to read.
    flags -- int: optional flags as specified by VMMPY_FLAG* constants.
    return -- bytes: memory.
    
    Example:
    VmmPy_MemRead(-1, 0x1000, 4) --> b'\x00\x01\x02\x03'
    """
    return VMMPYC_MemRead(pid, address, length, flags)



def VmmPy_MemReadScatter(pid, address_list, flags = 0):
    """Read page (4kB) sized & aligned memory given a pid and a list of (64-bit) addresses. Return result in list of dict.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory. -1 when reading physical memory.
    address_list -- list: a list of page (4kB/0x1000) aligned addresses.
    flags -- int: optional flags as specified by VMMPY_FLAG* constants.
    return -- list: of dicts with the result.
    
    Example:
    VmmPy_MemReadScatter(-1, [0x1000]) --> [{'addr': 4096, 'pa': 4096, 'data': b'\x00\x01\x02\x03\x04 ... ', 'size': 4096}]
    """

    return VMMPYC_MemReadScatter(pid, address_list, flags)



def VmmPy_MemWrite(pid, address, bytes_data):
    """Write memory given a pid, a (64-bit) address and length. No return.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory. -1 when writing physical memory.
    address -- int: the address to write.
    bytes_data -- bytes: a bytes-like object.
    
    Example:
    VmmPy_MemWrite(0x666, 0x1000, b'\x00\x01\x02\x03')
    """
    VMMPYC_MemWrite(pid, address, bytes_data)



def VmmPy_MemVirt2Phys(pid, address):
    """Translate a virtual address (va) to a physical address given a pid and return the result.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    va -- int: the virtual address (va) to translate
    return -- int: the physical address (pa).
    
    Example:
    VmmPy_MemVirt2Phys(0x666, 0x00007ff74d5da000) --> 0x000000004d5da000
    """
    return VMMPYC_MemVirt2Phys(pid, address)



#------------------------------------------------------------------------------
# VmmPy GENERAL PROCESS / MEMORY MAP FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_PidList():
    """Retrieve all process identifiers (pids) in the system and return them as a list.

    Keyword arguments:
    return -- list: pids.
    
    Example:
    VmmPy_PidList() --> [4, 76, 324, 392, 576, 588, ...]
    """
    return sorted(VMMPYC_PidList())



def VmmPy_PidGetFromName(process_name):
    """Retrieve a pid from a process_name and return it.
    NB! if more processes do have the same name only one will be returned by
    this function. If important to find all then use VmmPy_PidList() instead.

    Keyword arguments:
    process_name -- str: name of a process to find.
    return -- int: pid number.
    
    Example:
    VmmPy_PidGetFromName() --> 4
    """
    return VMMPYC_PidGetFromName(process_name)



def VmmPy_ProcessGetPteMap(pid, is_identify_modules = False):
    """Retrieve the pte memory map for a specific pid.

    Keyword arguments:
    pid -- int: the process identifier (pid).
    is_identify_modules -- bool: (optional) identify module names (slow).
    return -- list: of dict of PTE memory map entries.
    
    Example:
    VmmPy_ProcessGetMemoryMap(4) --> [{'va': 140715078701056, 'size': 8192, 'pages': 2, 'wow64': False, 'tag': 'ntdll.dll', 'flags-pte': 9223372036854775812, 'flags': '-r--'}, ...]
    """
    return VMMPYC_ProcessGetPteMap(pid, is_identify_modules)

def VmmPy_ProcessGetMemoryMap(pid, is_identify_modules = False):
    """Deprecated - use VmmPy_ProcessGetPteMap instead!"""
    return VMMPYC_ProcessGetPteMap(pid, is_identify_modules)



def VmmPy_ProcessGetVadMap(pid, is_identify_modules = False):
    """Retrieve the virtual address descriptor (VAD) memory map for a specific pid.

    Keyword arguments:
    pid -- int: the process identifier (pid).
    is_identify_modules -- bool: (optional) identify module names (slow).
    return -- list: of dict of VAD memory map entries.
    
    Example:
    VmmPy_ProcessGetMemoryMap(4) --> [{'start': 140715077140480, 'end': 140715079172095, 'subsection': 18446644053817718944, 'prototype': 18446663847518789648, 'prototype-len': 3968, 'mem_commit': False, 'commit_charge': 17, 'protection': '---wxc', 'type': 'Image', 'tag': '\\Windows\\System32\\ntdll.dll'}, ...]
    """
    return VMMPYC_ProcessGetVadMap(pid, is_identify_modules)



def VmmPy_ProcessGetHeapMap(pid):
    """Retrieve information about heaps for a specific pid.

    Keyword arguments:
    pid -- int: the process identifier (pid).
    return -- list: of dict of heap entries.
    
    Example:
    VmmPy_ProcessGetHeapMap(256) --> [{'va': 296288256, 'size': 16576512, 'size-uncommitted': 13893632, 'id': 64, 'primary': False}, ...]
    """
    return VMMPYC_ProcessGetHeapMap(pid)



def VmmPy_ProcessGetThreadMap(pid):
    """Retrieve information about threads for a specific pid.

    Keyword arguments:
    pid -- int: the process identifier (pid).
    return -- list: of dict of thread entries.
    
    Example:
    VmmPy_ProcessGetThreadMap(4) --> [{'tid': 9920, 'pid': 4280, 'exitstatus': 0, 'state': 5, 'running': 0, 'priority': 9, 'basepriority': 8, 'va-ethread': 18446644053942476992, 'va-teb': 13279232, 'va-start': 140715077586608, 'va-stackbase': 50331648, 'va-stacklimit': 50274304, 'va-stackbase-kernel': 18446613807470415872, 'va-stacklimit-kernel': 18446613807470391296, 'time-create': 132162322866787797, 'time-exit': 0, 'time-create-str': '2019-10-22 15:38:06 UTC', 'time-exit-str': '                    ***'}, ...]
    """
    return VMMPYC_ProcessGetThreadMap(pid)



def VmmPy_ProcessGetHandleMap(pid):
    """Retrieve information about handles for a specific pid.

    Keyword arguments:
    pid -- int: the process identifier (pid).
    return -- list: of dict of handle entries.
    
    Example:
    VmmPy_ProcessGetHandleMap(4) --> [{'va-object': 18446644053936528592, 'handle': 12268, 'access': 1180063, 'typeindex': 37, 'pid': 4280, 'pooltag': 1701603654, 'chandle': 1, 'cpointer': 1, 'va-object-creatinfo': 18446644053883285568, 'va-securitydescriptor': 0, 'tag': '\\Users\\User\\AppData\\Local\\Microsoft\\Windows\\Explorer\\thumbcache_256.db', 'type': 'File'}, ...]
    """
    return VMMPYC_ProcessGetHandleMap(pid)



def VmmPy_ProcessGetModuleMap(pid):
    """Retrieve the module map for a specific pid.

    Keyword arguments:
    pid -- int: the process identifier (pid).
    return -- list: of dict of module map information entries.
    
    Example:
    VmmPy_ProcessGetModuleMap(332) --> [{'va': 140700185460736, 'va-entry': 140700186087664, 'wow64': False, 'size': 4599808, 'name': 'explorer.exe'}, ...]
    """
    return VMMPYC_ProcessGetModuleMap(pid)



def VmmPy_ProcessGetModuleFromName(pid, module_name):
    """Retrieve the module map for a specific pid and module name.

    Keyword arguments:
    pid -- int: the process identifier (pid).
    module_name -- bool: name of the module to retrieve.
    return -- dict: of module information.
    
    Example:
    VmmPy_ProcessGetModuleMap(332, "ntdll.dll") --> {'va': 140700185460736, 'va-entry': 140700186087664, 'wow64': False, 'size': 4599808, 'name': 'explorer.exe'}
    """
    return VMMPYC_ProcessGetModuleFromName(pid, module_name)



def VmmPy_ProcessGetInformation(pid):
    """Retrieve process information for a specific pid and return as dict.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    return -- dict: of process information.
    
    Example:
    VmmPy_ProcessGetInformation(332) --> {'pid': 4280, 'ppid': 4248, 'pa-dtb': 5930565632, 'pa-dtb-user': 5930561536, 'state': 0, 'tp-memorymodel': 3, 'tp-system': 2, 'usermode': True, 'name': 'explorer.exe', 'name-long': 'explorer.exe', 'path-kernel': '\\Device\\HarddiskVolume4\\Windows\\explorer.exe', 'path-user': 'C:\\Windows\\Explorer.EXE', 'cmdline': 'C:\\Windows\\Explorer.EXE', 'wow64': False, 'va-peb32': 0, 'va-eprocess': 18446644053912244352, 'va-peb': 14229504, 'id-session': 1, 'luid': 225102, 'sid': 'S-1-5-21-3317879871-105768242-2947499445-1001'}
    """
    return VMMPYC_ProcessGetInformation(pid)



def VmmPy_ProcessListInformation():
    """Retrieve process information for all pids and return as dict of dict.

    Keyword arguments:
    return -- dict: dict of process information with pid as key.
    
    Example:
    VmmPy_ProcessListInformation() --> {4: {...}, ..., 322: {'pid': 8796, 'ppid': 456, 'pa-dtb': 5798625280, 'pa-dtb-user': 6237978624, 'state': 0, 'tp-system': 2, 'usermode': True, 'name': 'cmd.exe', 'wow64': False, 'va-entry': 140700131683072, 'va-eprocess': 18446635809067693440, 'va-peb': 708313505792, 'va-peb32': 0}
    """
    pids = VmmPy_PidList()
    result = {}
    for pid in pids:
        result[pid] = VMMPYC_ProcessGetInformation(pid)
    return result



#------------------------------------------------------------------------------
# VmmPy WINDOWS SPECIFIC PROCESS FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_ProcessGetEAT(pid, module_name):
    """Retrieve the export address table (EAT) for a specific pid and module name and return as list of dict.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    module_name -- str: name of the module to retrieve.
    return -- list: of dict of EAT information.
    
    Example:
    VmmPy_ProcessGetEAT(332, "ntdll.dll") --> [{'i': 0, 'va': 140718385196671, 'offset': 585343, 'fn': 'AcquireSRWLockExclusive'}, ... ]
    """
    return VMMPYC_ProcessGetEAT(pid, module_name)



def VmmPy_ProcessGetIAT(pid, module_name):
    """Retrieve the import address table (IAT) for a specific pid and module name and return as list of dict.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    module_name -- str: name of the module to retrieve.
    return -- list: of dict of IAT information.
    
    Example:
    VmmPy_ProcessGetAT(332, "cmd.exe") --> [{'i': 0, 'va': 140718377374992, 'fn': 'setlocale', 'dll': 'msvcrt.dll'}, ... ]
    """
    return VMMPYC_ProcessGetIAT(pid, module_name)



def VmmPy_ProcessGetDirectories(pid, module_name):
    """Retrieve the data directories for a specific pid and module name and return as list of dict.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    module_name -- str: name of the module to retrieve.
    return -- list: of dict of data direcories information.
    
    Example:
    VmmPy_ProcessGetDirectories(332, "cmd.exe") --> [{'i': 0, 'size': 0, 'offset': 0, 'name': 'EXPORT'},  ... ]
    """
    return VMMPYC_ProcessGetDirectories(pid, module_name)



def VmmPy_ProcessGetSections(pid, module_name):
    """Retrieve the sections for a specific pid and module name and return as list of dict.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    module_name -- str: name of the module to retrieve.
    return -- list: of dict of section information.
    
    Example:
    VmmPy_ProcessGetSections(332, "cmd.exe") --> [{'i': 0, 'Characteristics': 1610612768, 'misc-PhysicalAddress': 183592, 'misc-VirtualSize': 183592, 'Name': '.text', 'NumberOfLinenumbers': 0, 'NumberOfRelocations': 0, 'PointerToLinenumbers': 0, 'PointerToRawData': 1024, 'PointerToRelocations': 0, 'SizeOfRawData': 183808, 'VirtualAddress': 4096},  ... ]
    """
    return VMMPYC_ProcessGetSections(pid, module_name)



#------------------------------------------------------------------------------
# VmmPy Windows Registry FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_WinReg_HiveList():
    """Retrieve all registry hives and and return as list of dict.

    Keyword arguments:
    return -- list: of dict of registry hive information.
    
    Example:
    VmmPy_WinReg_HiveList() --> [{'i': 0, 'va_hive': 18446631989106032640, 'va_baseblock': 18446631989106098176, 'name': '0xffff9a0f4505c000-SYSTEM-MACHINE_SYSTEM.reghive'},  ... ]
    """
    return VMMPYC_WinReg_HiveList()



def VmmPy_WinReg_HiveRead(va_hive, address, length, flags = 0):
    """Read from a registry hive raw memory space.
    Note! The BaseBlock/regf header is not included in the memory space.

    Keyword arguments:
    va_hive -- int: the virtual address of the registry hive to write to.
    address -- int: the raw registry address to read.
    length -- int: the number of bytes to read.
    flags -- int: optional flags as specified by VMMPY_FLAG* constants.
    return -- bytes: memory.
    
    Example:
    VmmPy_MemRead(0xfffff800acb0000, 0x1000, 4) --> b'hbin'
    """
    return VMMPYC_WinReg_HiveRead(va_hive, address, length, flags)



def VmmPy_WinReg_HiveWrite(va_hive, address, bytes_data):
    """Write to a registry hive raw memory space.
    Note! The BaseBlock/regf header is not included in the memory space.

    Keyword arguments:
    va_hive -- int: the virtual address of the registry hive to write to.
    address -- int: the raw registry address to write to.
    bytes_data -- bytes: a bytes-like object.
    
    Example:
    VmmPy_WinReg_HiveWrite(0xfffff800acb0000, 0x1000, b'\x00\x01\x02\x03')
    """
    VMMPYC_WinReg_HiveWrite(va_hive, address, bytes_data)



def VmmPy_WinReg_KeyList(key):
    """Retrieve sub-keys and associated values with the specified registry key.

    Keyword arguments:
    key -- str: path of registry key to list. May start with address of CMHIVE
                in 0xhexadecimal format or HKLM.
    return -- dict: of list of subkeys and list of values.
    
    Example:
    VmmPy_WinReg_KeyList('HKLM\\HARDWARE') --> {'subkeys': [{'name': 'DEVICEMAP', 'time': 131877368614156304, 'time-str': '2018-11-26 20:14:21 UTC'}, ...], 'values': [...]}
    """
    return VMMPYC_WinReg_EnumKey(key)



def VmmPy_WinReg_ValueRead(keyvalue):
    """Read a registry value.

    Keyword arguments:
    keyvalue -- str: path of registry value to read. May start with address of
                 CMHIVE in 0xhexadecimal format or HKLM.
    return -- dict: of 'type' (value type as in VMMPY_WINREG_*) and 'data' (value data).
    
    Example:
    VmmPy_WinReg_ValueRead('HKLM\\SYSTEM\\Setup\\SystemPartition') --> {'type': 1, 'data': b'\\\x00D\x00e\x00v\x00i\x00c\x00e\x00\\\x00H...'}
    """
    return VMMPYC_WinReg_QueryValue(keyvalue)



#------------------------------------------------------------------------------
# VmmPy NETWORK FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_WinNet_Get():
    """Retrieve networking information

    Keyword arguments:
    return -- dict with 'TcpE' list with dict for each TCP connection.
    
    Example:
    VmmPy_WinReg_HiveList() --> {'TcpE': [{'ver': 4, 'pid': 612, 'state': 4, 'va': 18446690201099026448, 'time': 131983383869225588, 'time-str': '2019-03-29 13:06:26 UTC', 'src-ip': '127.0.0.1', 'src-port': 51734, 'dst-ip': '127.0.0.1', 'dst-port': 51733}, ...]}
    """
    return VMMPYC_WinNet_Get()



#------------------------------------------------------------------------------
# VmmPy VFS (Virtual File System) FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_VfsList(path):
    """Retrieve a Virtual File System directory listing a path and return it.

    Keyword arguments:
    path -- str: the directory path.
    return -- dict: of dict of file/directory names.
    
    Example:
    VmmPy_VfsList("/") --> {'pmem' : {'size': 247078670, 'f_isdir': False}, ...}
    """
    path = path.replace('/', '\\')
    return VMMPYC_VfsList(path)



def VmmPy_VfsRead(path_file, length, offset = 0):
    """Read a Virtual File System file.

    Keyword arguments:
    path_file -- str: the file path including the file name.
    length -- int: the amount of bytes to read.
    offset -- int: start reading from this offset.
    return -- bytes: the read data.
    
    Example:
    VmmPy_VfsRead("/pmem", 0x1000, 0x10000000) --> b'000032040234023400 ...'
    """
    path_file = path_file.replace('/', '\\')
    return VMMPYC_VfsRead(path_file, length, offset)



def VmmPy_VfsWrite(path_file, bytes_data, offset = 0):
    """Write to Virtual File System file.

    Keyword arguments:
    path_file -- str: the file path including the file name.
    bytes_data -- bytes: the data to write.
    offset -- int: start writing from this offset.
    
    Example:
    VmmPy_VfsWrite("/pmem", b'000000011122', 0x2000)
    """
    path_file = path_file.replace('/', '\\')
    VmmPy_VfsWrite(path_file, bytes_data, offset)



#------------------------------------------------------------------------------
# VmmPy Windows Symbol Debugging (.pdb) FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_PdbSymbolAddress(module_name, symbol_name):
    """Retrieve a symbol address by module and symbol name.
    NB! Vmm PDB Symbol functionality is limited and there is no guarantee that
        all modules will be loaded - or that the functionality is available.
        If multiple modules with the same name exists - the symbol will be
        searched for in the 1st hit.

    Keyword arguments:
    module_name -- str: the module name or 'nt' for kernel.
    symbol_name -- str: the symbol name to lookup.
    return -- int: address of the located symbol.
    
    Example:
    VmmPy_PdbSymbolAddress('nt', 'PsInitialSystemProcess') --> 0xffff800012345600
    """
    return VMMPYC_PdbSymbolAddress(module_name, symbol_name)

def VmmPy_PdbTypeSize(module_name, type_name):
    """Retrieve a type size by by module and type name.
    NB! Vmm PDB Symbol functionality is limited and there is no guarantee that
        all modules will be loaded - or that the functionality is available.
        If multiple modules with the same name exists - the symbol will be
        searched for in the 1st hit.

    Keyword arguments:
    module_name -- str: the module name or 'nt' for kernel.
    type_name -- str: the type name to lookup.
    return -- int: size of the type.
    
    Example:
    VmmPy_PdbTypeSize('nt', '_EPROCESS') --> 1568
    """
    return VMMPYC_PdbTypeSize(module_name, type_name)

def VmmPy_PdbTypeChildOffset(module_name, type_name, type_child_name):
    """Retrieve the ofset of a type child (struct member) by by module, type and child name.
    NB! Vmm PDB Symbol functionality is limited and there is no guarantee that
        all modules will be loaded - or that the functionality is available.
        If multiple modules with the same name exists - the symbol will be
        searched for in the 1st hit.

    Keyword arguments:
    module_name -- str: the module name or 'nt' for kernel.
    type_name -- str: the type name to lookup.
    type_child_name -- str: the type child name (struct member) to lookup.
    return -- int: offset (relative to type base) of the child type name.
    
    Example:
    VmmPy_PdbTypeChildOffset('nt', '_EPROCESS', 'CreateTime') --> 768
    """
    return VMMPYC_PdbTypeChildOffset(module_name, type_name, type_child_name)



#------------------------------------------------------------------------------
# VmmPy WINDOWS ONLY FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_GetUsers():
    """Retrieve information about the non well known logged on users in the system.

    Keyword arguments:
    return -- list: of dict of handle entries.
    
    Example:
    VmmPy_GetUsers() --> [{'va-reghive': 18446663847596163072, 'sid': 'S-1-5-21-3317879871-105768242-2947499445-1001', 'name': 'User'}, ...]
    """
    return VMMPYC_GetUsers()



def VmmPy_MapGetPhysMem():
    """Retrieve information about the physical memory map

    Keyword arguments:
    return -- list: of list with memory ranges where each range is [base_physical_region, size_physical_region].
    
    Example:
    VmmPy_MapGetPhysMem() --> [[4096, 638976], [1048576, 8192], [1060864, 2902675456], [4294967296, 13931380736], ...]
    """
    return VMMPYC_MapGetPhysMem()



def VmmPy_MapGetPfns(pfns):
    """Retrieve information about page frame numbers (PFNs).

    Keyword arguments:
    pfns -- list of int: the page frame numbers to retrieve information for.
    return -- dict of dict: a dict with info for each retrieved page frame number.
    
    Example:
    VmmPy_MapGetPfns([1, 0x123456, 0x58f4c]) -> {
            1: {'pfn': 1, 'pid': 0, 'va': 18446734944756600832, 'va-pte': 18446607716437721160, 'tp': 'Active', 'tpex': '-'},
            1193046: {'pfn': 1193046, 'pid': 0, 'va': 0, 'va-pte': 18446669339889095480, 'tp': 'Standby', 'tpex': 'File'},
            364364: {'pfn': 364364, 'pid': 10744, 'va': 1977593008128, 'va-pte': 18446607188374379848, 'tp': 'Active', 'tpex': 'ProcPriv'}
        }
        
    """
    return VMMPYC_MapGetPfns(pfns)



def VmmPy_WinGetThunkInfoEAT(pid, module_name, exported_function):
    """Retrieve information about a single export address table (EAT) entry. This may be useful for hooking.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    module_name -- str: name of the module to retrieve.
    exported_function -- str: name of the exported function to retrieve.
    return -- dict: information about the EAT entry.

    Example:
    VmmPy_WinGetThunkInfoEAT(4, 'ntoskrnl.exe', 'KeGetCurrentIrql') --> {'vaFunction': 18446735288139539584, 'valueThunk': 1479808, 'vaNameFunction': 18446735288147899428, 'vaThunk': 18446735288147849312}
    """
    return VMMPYC_WinGetThunkInfoEAT(pid, module_name, exported_function)



def VmmPy_WinGetThunkInfoIAT(pid, module_name, imported_module_name, imported_module_function):
    """Retrieve information about a single import address table (IAT) entry. This may be useful for hooking.

    Keyword arguments:
    pid -- int: the process identifier (pid) when reading process virtual memory.
    module_name -- str: name of the module to retrieve.
    imported_module_name -- str: name of the imported module to retrieve.
    imported_module_function -- str: name of the imported function to retrieve.
    return -- dict: information about the IAT entry.

    Example:
    VmmPy_WinGetThunkInfoIAT(4, 'ntoskrnl.exe', 'hal.dll', 'HalSendNMI') --> {'32': False, 'vaFunction': 18446735288149190896, 'vaNameFunction': 18446735288143568050, 'vaNameModule': 18446735288143568362, 'vaThunk': 18446735288143561136}
    """
    return VMMPYC_WinGetThunkInfoIAT(pid, module_name, imported_module_name, imported_module_function)



#------------------------------------------------------------------------------
# VmmPy UTIL FUNCTIONALITY BELOW:
#------------------------------------------------------------------------------

def VmmPy_UtilFillHexAscii(data_bytes, cb_initial_offset = 0):
    """Fill a human readable hex ascii memory dump string given a bytes object.

    Keyword arguments:
    data_bytes -- bytes: binary data to convert.
    cb_initial_offset -- int: offset, must be max 0x1000 and multiple of 0x10.
    return -- str: human readable dump-data.
    """
    return VMMPYC_UtilFillHexAscii(data_bytes, cb_initial_offset)


