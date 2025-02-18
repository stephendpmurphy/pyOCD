# pyOCD debugger
# Copyright (c) 2021 Nuvoton
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...coresight.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile

SCS_DHCSR       = 0xE000EDF0
SCS_DHCSR_S_SDE = 0x00100000
SCU_SRAMNSSET   = 0x4002F024
SCU_FNSADDR     = 0x4002F028

def flash_algo(load_address):
    return {
        'load_address' : load_address,

        # Flash algorithm as a hex string
        'instructions': [
        0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
        0x9018b09a, 0x92169117, 0x90154678, 0x90149815, 0x78c0a814, 0x280006c0, 0xe7ffd528, 0x68004860,
        0x280007c0, 0xe7ffd110, 0x2159485d, 0x21166001, 0x21886001, 0x68006001, 0x280007c0, 0xe7ffd103,
        0x90192001, 0xe7ffe0a1, 0x68014856, 0x43112204, 0x48556001, 0x43116801, 0xe7ff6001, 0x68004853,
        0x280006c0, 0xe7ffd401, 0xe027e7f8, 0x68004848, 0x280007c0, 0xe7ffd110, 0x21594845, 0x21166001,
        0x21886001, 0x68006001, 0x280007c0, 0xe7ffd103, 0x90192001, 0xe7ffe079, 0x6801483e, 0x43112204,
        0x483d6001, 0x43116801, 0xe7ff6001, 0x6800483b, 0x280006c0, 0xe7ffd401, 0xe7ffe7f8, 0x90134678,
        0x90129813, 0x78c0a812, 0x280006c0, 0xe7ffd52d, 0x90114678, 0x90109811, 0x00c09810, 0x4a354934,
        0x46082800, 0x92089109, 0xd4019007, 0x90079808, 0x68019807, 0x43112209, 0x46786001, 0x980f900f,
        0x980e900e, 0x280000c0, 0x92069809, 0xd4019005, 0x90059808, 0x68009805, 0x40089906, 0xd0032809,
        0x2001e7ff, 0xe0309019, 0x4678e02c, 0x980d900d, 0x980c900c, 0x491e00c0, 0x28004a1e, 0x91044608,
        0x90029203, 0x9803d401, 0x98029002, 0x22296801, 0x60014311, 0x900b4678, 0x900a980b, 0x00c0980a,
        0x98042800, 0x90009201, 0x9803d401, 0x98009000, 0x99016800, 0x28294008, 0xe7ffd003, 0x90192001,
        0xe7ffe003, 0x90192000, 0x9819e7ff, 0x4770b01a, 0x40000100, 0x40000200, 0x40000204, 0x40000250,
        0x50000100, 0x50000200, 0x50000204, 0x50000250, 0x5000c000, 0x4000c000, 0x9008b089, 0x4678e7ff,
        0x98079007, 0x98069006, 0x491200c0, 0x28004a12, 0x91029203, 0x9803d401, 0x98029002, 0x07c06800,
        0xd0012800, 0xe7eae7ff, 0x90054678, 0x90049805, 0x00c09804, 0x4a0a4909, 0x92012800, 0xd4019100,
        0x90009801, 0x68019800, 0x43912201, 0x20006001, 0x4770b009, 0x5000c040, 0x4000c040, 0x5000c000,
        0x4000c000, 0x902ab0ac, 0x2101982a, 0x4390070a, 0x982a902a, 0x40104a71, 0x982a902a, 0x0512220f,
        0x05494010, 0xd1074288, 0x982ae7ff, 0x1840496c, 0x2001902a, 0xe0029029, 0x90292000, 0xe7ffe7ff,
        0x90284678, 0x90279828, 0x00c09827, 0x4a664965, 0x92142800, 0xd4019113, 0x90139814, 0x68009813,
        0x280007c0, 0xe7ffd001, 0x4678e7ea, 0x98269026, 0x98259025, 0x495d00c0, 0x28004a5d, 0x91119212,
        0x9812d401, 0x98119011, 0x22406801, 0x60014311, 0x90244678, 0x90239824, 0x00c09823, 0x4a564955,
        0x92102800, 0xd401910f, 0x900f9810, 0x2122980f, 0x982a6001, 0x91224679, 0x91219922, 0x00c99921,
        0x4b4f4a4e, 0x900e2900, 0x920c930d, 0x980dd401, 0x980c900c, 0x6001990e, 0x28009829, 0xe7ffd113,
        0x90204678, 0x901f9820, 0x00c0981f, 0x4a464945, 0x920b2800, 0xd401910a, 0x900a980b, 0x2100980a,
        0x600143c9, 0x4678e011, 0x981e901e, 0x981d901d, 0x493c00c0, 0x28004a3c, 0x91089209, 0x9809d401,
        0x98089008, 0x60014939, 0x4678e7ff, 0x981c901c, 0x981b901b, 0x493600c0, 0x28004a36, 0x91069207,
        0x9807d401, 0x98069006, 0x60012101, 0x8f6ff3bf, 0x4678e7ff, 0x981a901a, 0x98199019, 0x492100c0,
        0x28004a21, 0x91049205, 0x9805d401, 0x98049004, 0x07c06800, 0xd0012800, 0xe7eae7ff, 0x90184678,
        0x90179818, 0x00c09817, 0x4a194918, 0x92032800, 0xd4019102, 0x90029803, 0x68009802, 0x28000640,
        0xe7ffd516, 0x90164678, 0x90159816, 0x00c09815, 0x4a0f490e, 0x92012800, 0xd4019100, 0x90009801,
        0x68019800, 0x43112240, 0x20016001, 0xe002902b, 0x902b2000, 0x982be7ff, 0x4770b02c, 0xfffff800,
        0xffe00000, 0x5000c040, 0x4000c040, 0x5000c000, 0x4000c000, 0x5000c00c, 0x4000c00c, 0x5000c004,
        0x4000c004, 0x5000c008, 0x4000c008, 0x0055aa03, 0x5000c010, 0x4000c010, 0x9028b0aa, 0x92269127,
        0x1cc09827, 0x43882103, 0x98289027, 0x07092101, 0x90284388, 0x4678e7ff, 0x98259025, 0x98249024,
        0x496100c0, 0x28004a61, 0x91129213, 0x9813d401, 0x98129012, 0x07c06800, 0xd0012800, 0xe7eae7ff,
        0x90234678, 0x90229823, 0x00c09822, 0x4a594958, 0x92112800, 0xd4019110, 0x90109811, 0x68019810,
        0x43112240, 0x46786001, 0x98219021, 0x98209020, 0x495100c0, 0x28004a51, 0x910e920f, 0x980fd401,
        0x980e900e, 0x60012121, 0x9827e7ff, 0xd1002800, 0x9828e083, 0x911f4679, 0x911e991f, 0x00c9991e,
        0x4b484a47, 0x900d2900, 0x920b930c, 0x980cd401, 0x980b900b, 0x6001990d, 0x68009826, 0x911d4679,
        0x911c991d, 0x00c9991c, 0x4b404a3f, 0x900a2900, 0x92089309, 0x9809d401, 0x98089008, 0x6001990a,
        0x901b4678, 0x901a981b, 0x00c0981a, 0x4a394938, 0x92072800, 0xd4019106, 0x90069807, 0x21019806,
        0xf3bf6001, 0xe7ff8f6f, 0x90194678, 0x90189819, 0x00c09818, 0x4a254924, 0x92052800, 0xd4019104,
        0x90049805, 0x68009804, 0x280007c0, 0xe7ffd001, 0x4678e7ea, 0x98179017, 0x98169016, 0x491c00c0,
        0x28004a1c, 0x91029203, 0x9803d401, 0x98029002, 0x06406800, 0xd5162800, 0x4678e7ff, 0x98159015,
        0x98149014, 0x491200c0, 0x28004a12, 0x91009201, 0x9801d401, 0x98009000, 0x22406801, 0x60014311,
        0x90292001, 0x9828e00c, 0x90281d00, 0x1d009826, 0x98279026, 0x90271f00, 0x2000e777, 0xe7ff9029,
        0xb02a9829, 0x46c04770, 0x5000c040, 0x4000c040, 0x5000c000, 0x4000c000, 0x5000c00c, 0x4000c00c,
        0x5000c004, 0x4000c004, 0x5000c008, 0x4000c008, 0x5000c010, 0x4000c010, 0x9028b0aa, 0x92269127,
        0x1cc09827, 0x43882103, 0x98289027, 0x07092101, 0x90254008, 0x43889828, 0xe7ff9028, 0x90244678,
        0x90239824, 0x00c09823, 0x4a634962, 0x92122800, 0xd4019111, 0x90119812, 0x68009811, 0x280007c0,
        0xe7ffd001, 0x4678e7ea, 0x98229022, 0x98219021, 0x495a00c0, 0x28004a5a, 0x910f9210, 0x9810d401,
        0x980f900f, 0x22406801, 0x60014311, 0x90204678, 0x901f9820, 0x00c0981f, 0x4a534952, 0x920e2800,
        0xd401910d, 0x900d980e, 0x2100980d, 0xe7ff6001, 0x28009827, 0xe087d100, 0x46799828, 0x991e911e,
        0x991d911d, 0x4a4900c9, 0x29004b49, 0x930b900c, 0xd401920a, 0x900a980b, 0x990c980a, 0x46786001,
        0x981c901c, 0x981b901b, 0x494200c0, 0x28004a42, 0x91089209, 0x9809d401, 0x98089008, 0x60012101,
        0x8f6ff3bf, 0x4678e7ff, 0x981a901a, 0x98199019, 0x493000c0, 0x28004a30, 0x91069207, 0x9807d401,
        0x98069006, 0x07c06800, 0xd0012800, 0xe7eae7ff, 0x90184678, 0x90179818, 0x00c09817, 0x4a284927,
        0x92052800, 0xd4019104, 0x90049805, 0x68009804, 0x28000640, 0xe7ffd516, 0x90164678, 0x90159816,
        0x00c09815, 0x4a1e491d, 0x92032800, 0xd4019102, 0x90029803, 0x68019802, 0x43112240, 0x20016001,
        0xe0249029, 0x90144678, 0x90139814, 0x00c09813, 0x4a1b491a, 0x92012800, 0xd4019100, 0x90009801,
        0x68009800, 0x68099926, 0xd0034288, 0x2001e7ff, 0xe00c9029, 0x1d009828, 0x98269028, 0x90261d00,
        0x1f009827, 0xe7739027, 0x90292000, 0x9829e7ff, 0x4770b02a, 0x5000c040, 0x4000c040, 0x5000c000,
        0x4000c000, 0x5000c00c, 0x4000c00c, 0x5000c004, 0x4000c004, 0x5000c010, 0x4000c010, 0x5000c008,
        0x4000c008, 0x00000000
        ],

        # Relative function addresses
        'pc_init': load_address + 0x00000021,
        'pc_unInit': load_address + 0x000001d9,
        'pc_program_page': load_address + 0x00000459,
        'pc_erase_sector': load_address + 0x00000245,
        'pc_eraseAll': 0x0,

        'static_base' : load_address + 0x00000020 + 0x00000804,
        'begin_stack' : load_address + 0x00000b00,
        'begin_data' : load_address + 0x1000,
        'page_size' : 0x800,
        'analyzer_supported' : False,
        'analyzer_address' : 0x00000000,
        'page_buffers' : [load_address + 0x00001000, load_address + 0x00001800],   # Enable double buffering
        'min_program_length' : 0x800,
    }

class M2354KJFAE(CoreSightTarget):
    VENDOR = "Nuvoton"

    MEMORY_MAP = MemoryMap()

    def __init__(self, link):
        super(M2354KJFAE, self).__init__(link, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("M2354_v1.svd")

    def create_flash(self):
        dhcsr      = self.read32(SCS_DHCSR)
        s_sde      = 1 if (dhcsr & SCS_DHCSR_S_SDE) else 0

        fnsaddr    = self.read32(SCU_FNSADDR   if s_sde else (0x10000000+SCU_FNSADDR))
        sramnsnset = self.read32(SCU_SRAMNSSET if s_sde else (0x10000000+SCU_SRAMNSSET))
        snsaddr    = 0x20040000

        for i in range(16):
            if sramnsnset & (1 << i):
                snsaddr = 0x20000000 + (0x4000 * i)
                break

        if s_sde and (fnsaddr > 0):
            self.memory_map.add_regions(
                FlashRegion(name='aprom',      start=0x00000000,         length=fnsaddr,
                                                                         sector_size=0x0800,
                                                                         page_size=0x0800,
                                                                         is_boot_memory=True,
                                                                         algo=flash_algo(0x20000000))
                )

        if fnsaddr < 0x00100000:
            self.memory_map.add_regions(
                FlashRegion(name='aprom_ns',   start=0x10000000+fnsaddr, length=0x00100000-fnsaddr,
                                                                         sector_size=0x0800,
                                                                         page_size=0x0800,
                                                                         algo=flash_algo(0x20000000 if s_sde else (0x10000000+snsaddr)))
                )

        if s_sde:
            self.memory_map.add_regions(
                FlashRegion(name='ldrom',      start=0x00100000,         length=0x4000,
                                                                         sector_size=0x0800,
                                                                         page_size=0x0800,
                                                                         algo=flash_algo(0x20000000)),
                FlashRegion(name='data_flash', start=0x00110000,         length=0x2000,
                                                                         sector_size=0x0800,
                                                                         page_size=0x0800,
                                                                         algo=flash_algo(0x20000000))
                )

        if s_sde and (snsaddr > 0x20000000):
            self.memory_map.add_regions(
                RamRegion(  name='sram',       start=0x20000000,         length=snsaddr-0x20000000)
                )

        if snsaddr < 0x20040000:
            self.memory_map.add_regions(
                RamRegion(  name='sram_ns',    start=0x10000000+snsaddr, length=0x20040000-snsaddr)
                )

        super(M2354KJFAE, self).create_flash()
