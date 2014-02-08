#     Copyright (C) 2014  airv
# 
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.#

import weechat
import time

SCRIPT_NAME    = "countdown"
SCRIPT_AUTHOR  = "AirV"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "countdown"

settings = {
	"channel"            : 'server, channel',  # print a new timestamp every X minutes if there is activity
}

current_time = 0
go = -1
bufferChannel = ""
currentTotalTime = 0


def command_timestamp(buffer, timestamp):
    weechat.command(buffer, time.strftime("%H:%M:%S",time.gmtime(timestamp)))

def timer_cb(data, remaining_calls):
	global go
	global bufferChannel
	if (go != -1):
		if (go == 0):
			weechat.command(bufferChannel, "go!")
		else:
			weechat.command(bufferChannel, str(go))
	go -= 1
	return weechat.WEECHAT_RC_OK

def timer_time(data, remaining_calls):
	global currentTotalTime
	command_timestamp(bufferChannel, currentTotalTime + (4 - int(remaining_calls)) * 5)
	return weechat.WEECHAT_RC_OK
	
def print_cb(data, buffer, date, tags, displayed, highlight, prefix, message):
	global go
	global bufferChannel
	global current_time
	global currentTotalTime
	if message == "!og":
		go=5
		bufferChannel = buffer
		weechat.hook_timer(1000, 0, 6, 'timer_cb', '')
	else:
		if message == "go!":
			current_time = int(date)
		else:
			if message == "!time":
				bufferChannel = weechat.info_get("irc_buffer", str(weechat.config_get_plugin("channel"))) 
				currentTotalTime = int(date) - current_time
				command_timestamp(bufferChannel,currentTotalTime)
				weechat.hook_timer(5000, 0, 4, 'timer_time', '')
	return weechat.WEECHAT_RC_OK

if __name__ == "__main__":
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
                        SCRIPT_DESC, "", ""):
        # Set default settings
        for option, default_value in settings.iteritems():
            if not weechat.config_is_set_plugin(option):
                weechat.config_set_plugin(option, default_value)
	weechat.hook_print('', '', '', 0, 'print_cb', '')
