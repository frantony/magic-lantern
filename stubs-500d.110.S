/** \file
 * Entry points into the firmware image.
 *
 * These are the functions that we can call from our tasks
 * in the Canon 1.1.0 firmware for the 500d.
 *
 * \todo Sort this file?  Generate it from the IDA map?
 */
/*
 * Copyright (C) 2010 Trammell Hudson <hudson+ml@osresearch.net>
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the
 * Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor,
 * Boston, MA  02110-1301, USA.
 */

.text

#define NSTUB(addr,name) \
	.global name; \
	name = addr

NSTUB( ROMBASEADDR, firmware_entry )

/** These must be found first for any progress to be made */
NSTUB( 0xFF010894, cstart )
NSTUB( 0xFF3EBC24, bzero32 ) // called by cstart()
NSTUB( 0xFF011DBC, init_task ) // passed as arg to create_init_task, look for dmSetup
NSTUB( 0xFF0174E0, create_init_task ) 

/** Look for the normal printf strings */
NSTUB( 0xFF066A98, DebugMsg )

/** Task dispatch hook hasn't moved in several versions */
NSTUB( 0x1934, task_dispatch_hook )

/** Find the additioanl version string in GUI_GetFirmVersion */
NSTUB( 0x1506C, additional_version )
NSTUB( 0xFF1C659C, GUI_GetFirmVersion )

// Everything below here is not needed for the first boot

/** Camera interface? */
NSTUB( 0xC0220000, camera_engine )

NSTUB( 0xFF067828, call )

/** Find the shell register commands */
NSTUB( 0xFF01C54C, register_func )

/** Debugging commands are all registered by name.  Search for the strings */
NSTUB( 0xFF066A18, dmstart )
NSTUB( 0xFF066A58, dmstop )
NSTUB( 0xFF06732C, dumpf )

/** Look in DebugMsg, near the bottom.  It calls vsnprintf()
 * with a buffer size of 0x4C.
 */
NSTUB( 0xFF1A4398, vsnprintf )

NSTUB( 0xFF069D74, msleep ) // called from EV_GETDONE_CACHE param 0x64
NSTUB( 0xFF069E2C, task_create )
NSTUB( 0xFF1962A4, FIO_Open)
NSTUB( 0xFF196358, FIO_CreateFile )
NSTUB( 0xFF196400, FIO_CloseFile )
NSTUB( 0xFF1969F4, FIO_GetFileSize )
NSTUB( 0xFF196840, FIO_WriteFile )
NSTUB( 0xFF196690, FIO_ReadFile )
NSTUB( 0xFF0699B8, give_semaphore )
NSTUB( 0xFF0698D0, take_semaphore )
NSTUB( 0xFF066D7C, dm_set_store_level ) // called by "dmstore"
NSTUB( 0xFF059868, prop_register_slave ) // called by"GUI_RegisterPropertySlave"
NSTUB( 0xFF059988, prop_request_change )
NSTUB( 0xFF0597E0, prop_deliver ) // maybe?

NSTUB( 0xFF198EE0, dispcheck )
NSTUB( 0x27D84, bmp_vram_info )
NSTUB( 0x37304, vram_info )
NSTUB( 0xFF23ABD4, vram_get_number )
NSTUB( 0xFF198100, vram_get_pos_and_size )

NSTUB( 0xFF066700, bootdisk_enable )
NSTUB( 0xFF06670C, bootdisk_disable )

NSTUB( 0xFF06ACB4, malloc )
NSTUB( 0xFF019044, free )

NSTUB( 0x2D18, dm_names )
NSTUB( 0xFF07835C, strcpy )
NSTUB( 0xFF0642D0, LoadCalendarFromRTC )
NSTUB( 0xFF072B30, task_trampoline )

NSTUB( 0xFF05993C, prop_cleanup )

NSTUB( 0xFF01F160, AE_MODE_MOVIE_OFF )
NSTUB( 0xFF01F130, AE_MODE_MOVIE_ON )
NSTUB( 0xFF203C34, EP_SetMovieManualExposureMode )
NSTUB( 0xFF206168, EP_SetDebugLogMode )
NSTUB( 0xFF206190, EP_SetLVAEDebugPort )

NSTUB( 0xFF17C218, mvrFixQScale )
NSTUB( 0xFF17BDA4, mvrSetDefQScale )

NSTUB( 0xFF056064, _audio_ic_write )
NSTUB( 0xFF056EB0, _audio_ic_read )
NSTUB( 0xFF0549E8, sounddev_task )
NSTUB( 0xFF054B8C, sounddev_active_in )
NSTUB( 0xFFFFFFFF, audio_thresholds )
NSTUB( 0x1F04, sounddev )

NSTUB( 0xFF069770, create_named_semaphore )
NSTUB( 0xFF2676E0, gui_task_create )
NSTUB( 0xFF267800, gui_task_destroy )
NSTUB( 0xFF267590, ctrlman_dispatch_event )

NSTUB( 0xFF3EBB30, memcpy )
NSTUB( 0xFF0932FC, prop_request_icu_auto_poweroff )
NSTUB( 0xFF1A7204, alloc_dma_memory )
NSTUB( 0xFF1A7238, free_dma_memory )
NSTUB( 0x23568, cf_device )
NSTUB( 0x23694, sd_device )

NSTUB( 0xFF01DCCC, hotplug_task )
NSTUB( 0x1AF4, hotplug_struct )
NSTUB( 0x1B24, hotplug_usb_buf )

#if 0
NSTUB( 0xFF012E44, cli_save )
NSTUB( 0xFF012E58, sei_restore )
NSTUB( 0xFF20C404, ptp_register_handler )
NSTUB( 0xFF11E058, gui_lock )
NSTUB( 0xFF068268, oneshot_timer )
NSTUB( 0xFFA6BE34, gui_task_destroy )
NSTUB( 0xFF022A9C, gui_main_task )
NSTUB( 0xFF023450, gui_init_end )
NSTUB( 0x3B90, gui_timer_struct )
NSTUB( 0x1C70, gui_main_struct )
NSTUB( 0xFF0694D0, msg_queue_receive )
NSTUB( 0xFF091114, gui_local_post )
NSTUB( 0xFF090C4C, gui_change_mode )
NSTUB( 0xFF0915F0, gui_other_post )
NSTUB( 0xFF091720, gui_post_10000085 )
NSTUB( 0xFF091E9C, gui_init_event )
NSTUB( 0xFF0917D4, gui_change_shoot_type_post )
NSTUB( 0xFF09186C, gui_change_lcd_state_post )
NSTUB( 0xFF08F638, gui_massive_event_loop )
NSTUB( 0xFF1A0918, gui_timer_something )
#endif