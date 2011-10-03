#ifndef _propvalues_h_
#define _propvalues_h_

extern int lv; // former lv_drawn(); TRUE when LiveView is active.
extern int lv_dispsize; // 1 / 5 / A
extern int expsim;
extern int shooting_mode;
extern int shooting_type;
extern int efic_temp;
extern int gui_state;
extern int max_auto_iso;
extern int pic_quality;
//~ extern int burst_count;
extern int avail_shot;
extern int recording;
extern int af_mode;
extern int dofpreview;
extern int display_sensor;
extern int shutter_count;
extern int liveview_actuations;
extern int ae_mode_movie;
extern int ext_monitor_hdmi;
extern int ext_monitor_rca;
extern int alo;
extern int file_number;
extern int folder_number;
extern int file_number_also;
extern int tft_status;
extern int drive_mode;
extern int strobo_firing;
extern int lvaf_mode;
extern int image_review_time;
extern int lv_disp_mode;
extern int mirror_down;
extern int hdmi_code;
extern int backlight_level;
extern int video_mode_crop;
extern int video_mode_fps;
extern int video_mode_resolution; // 0 if full hd, 1 if 720p, 2 if 480p
extern int beep_enabled;
extern int lv_movie_select;
extern int sensor_cleaning;

#define EXT_MONITOR_CONNECTED (ext_monitor_hdmi | ext_monitor_rca)

extern struct bmp_ov_loc_size os;

#endif
