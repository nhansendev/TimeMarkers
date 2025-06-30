# TimeMarkers
Some simple Python time tracking utilities.

Known working on Python 3.11, and assumed working for all Python 3+

Dependencies: None

# Installation
From within the TimeMarkers folder:

```
pip install .
```

To uninstall:

```
pip uninstall TimeMarkers
```

# Classes
## TimeWrap
A context manager class which times the bulk execution of code within its context.

### Configuration:
#### msg | *str, default=""*:
>An optional label
#### just | *int, default=50*:
>The number of characters to justify the "Done" by, for cleanliness. The default is probably fine unless you have long messages, or a narrow window
#### use_HMS_format | *bool, default=False*:
>Print duration in seconds, or hours:minutes:seconds
	
### Usage Example:
    from TimeMarkers import TimeWrap
    
    with TimeWrap("Processing..."):
    	*your code*
	with TimeWrap("Step 2...", use_HMS_format=True):
		*more code*

### Result:
	> Processing...                                     Done, 1.151 sec
	> Step 2...                                         Done, 00:00:8.223 hh:mm:ss
	
## TimeMarker
A configurable timer class for tracking time in long-running processes

### Configuration:
#### est_iters | *int, default=None*:
>The expected total number of iterations. Required to estimate completion time
#### index_interval | *int, default=None*:
>After every X **iterations** print the progress (and trigger a callback if configured)
#### time_interval | *float, default=None*:
>After every X **seconds** print the progress (and trigger a callback if configured)
>Note: can't trigger faster than the iterations are called
#### smooth_rate | *float, default=None*:
>The time intervals between iterations are averaged if smooth_rate is > 1, with larger values leading to longer averaging
#### callback | *any callable, default=None*:
>Depending on how callback_mode is configured, the provided callback will be called during progress updates
#### callback_mode | *CallbackMode Enum, default=CallbackMode.interval*:
 - none = 0	# no callbacks will be called, the same as if callback=None
 - interval = 1 # each time the **index_interval** is reached the callback will be called
 - timed = 2 # each time the **time_interval** is reached the callback will be called
 - both = 3 # each time **either** interval is reached the callback will be called
#### twelve_hour | *bool, default=True*:
>Displays time in 12 hour or 24 hour format
#### time_format | *str, default=None*:
>Overrides time formatting to something custom
#### progress_bar_length | *int, default=50*:
>If a progress bar is displayed this is the total length in characters
#### oneline | *bool, default=False*:
>Repeatedly update the same line when printing
#### segments | *Segments Enum, default=Segments.default.value*:
>The displayed information can be customized by providing a list/tuple of segment IDs.
 - timestamp  =  0 # the current time when the progress update was triggered
 - elapsed  =  1 # how much time has elapsed since the beginning, and a remaining time estimate if est_iters was defined
 - end_time  =  2 # the approximate completion time timestamp if est_iters was defined
 - sec_per_step  =  3 # the average seconds per step
 - progress  =  4 # the completed iterations, and the remaining iterations if est_iters was defined
 - bargraph  =  5 # a bar graph showing progress if est_iters was defined
 - default  =  tuple(range(6)) # each of the above


### Usage Example:
    from TimeMarkers import TimeMarker
    
    TM = TimeMarker(100, 10)

	for _ in range(100):
		TM() # Should be placed before code execution in loop
		*do something*	
	TM() # Should be called one final time afterwards to show 100%

### Result:
Default config:

Note: the progress bar characters don't render correctly on GitHub.

	2023-11-21 12:57:09 AM | 00:00:01/00:00:22 elap/rem | Est: 2023-11-21 12:57:32 AM | 0.250 sec/step avg <00:00:00> |  10/100 pts ( 10.0%) | |▒▒▒▒▒    .         .         .         .         .|
	2023-11-21 12:57:11 AM | 00:00:04/00:00:17 elap/rem | Est: 2023-11-21 12:57:29 AM | 0.222 sec/step avg <00:00:00> |  20/100 pts ( 20.0%) | |▒▒▒▒▒▒▒▒▒▒         .         .         .         .|
	2023-11-21 12:57:14 AM | 00:00:06/00:00:14 elap/rem | Est: 2023-11-21 12:57:28 AM | 0.213 sec/step avg <00:00:00> |  30/100 pts ( 30.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .         .         .         .|
	2023-11-21 12:57:16 AM | 00:00:08/00:00:12 elap/rem | Est: 2023-11-21 12:57:29 AM | 0.216 sec/step avg <00:00:00> |  40/100 pts ( 40.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         .         .         .|
	2023-11-21 12:57:17 AM | 00:00:09/00:00:08 elap/rem | Est: 2023-11-21 12:57:26 AM | 0.178 sec/step avg <00:00:00> |  50/100 pts ( 50.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .         .         .|
	2023-11-21 12:57:20 AM | 00:00:12/00:00:10 elap/rem | Est: 2023-11-21 12:57:30 AM | 0.253 sec/step avg <00:00:00> |  60/100 pts ( 60.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         .         .|
	2023-11-21 12:57:22 AM | 00:00:14/00:00:06 elap/rem | Est: 2023-11-21 12:57:28 AM | 0.210 sec/step avg <00:00:00> |  70/100 pts ( 70.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .         .|
	2023-11-21 12:57:24 AM | 00:00:17/00:00:04 elap/rem | Est: 2023-11-21 12:57:29 AM | 0.215 sec/step avg <00:00:00> |  80/100 pts ( 80.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         .|
	2023-11-21 12:57:26 AM | 00:00:19/00:00:02 elap/rem | Est: 2023-11-21 12:57:29 AM | 0.213 sec/step avg <00:00:00> |  90/100 pts ( 90.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .|
	2023-11-21 12:57:28 AM | 00:00:21/00:00:00 elap/rem | Est: 2023-11-21 12:57:28 AM | 0.210 sec/step avg <00:00:00> | 100/100 pts (100.0%) | |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒|

 Default result without defining est_iter:
 
	2023-11-21 01:09:47 AM | 00:00:02 | 0.180 sec/step avg <00:00:00> | 10 pts
	2023-11-21 01:09:48 AM | 00:00:03 | 0.176 sec/step avg <00:00:00> | 20 pts
	2023-11-21 01:09:50 AM | 00:00:05 | 0.183 sec/step avg <00:00:00> | 30 pts
	2023-11-21 01:09:52 AM | 00:00:06 | 0.151 sec/step avg <00:00:00> | 40 pts
	2023-11-21 01:09:53 AM | 00:00:08 | 0.171 sec/step avg <00:00:00> | 50 pts
	2023-11-21 01:09:55 AM | 00:00:10 | 0.194 sec/step avg <00:00:00> | 60 pts
	2023-11-21 01:09:57 AM | 00:00:12 | 0.165 sec/step avg <00:00:00> | 70 pts
	2023-11-21 01:09:59 AM | 00:00:14 | 0.216 sec/step avg <00:00:00> | 80 pts
	2023-11-21 01:10:01 AM | 00:00:16 | 0.176 sec/step avg <00:00:00> | 90 pts
	2023-11-21 01:10:03 AM | 00:00:18 | 0.181 sec/step avg <00:00:00> | 100 pts

 Result with custom segment definition (segments=(Segments.bargraph, Segments.progress, Segments.end_time)):

	|▒▒▒▒▒    .         .         .         .         .| |  10/100 pts ( 10.0%) | Est: 2023-11-21 01:20:42 AM
	|▒▒▒▒▒▒▒▒▒▒         .         .         .         .| |  20/100 pts ( 20.0%) | Est: 2023-11-21 01:20:46 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .         .         .         .| |  30/100 pts ( 30.0%) | Est: 2023-11-21 01:20:50 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         .         .         .| |  40/100 pts ( 40.0%) | Est: 2023-11-21 01:20:47 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .         .         .| |  50/100 pts ( 50.0%) | Est: 2023-11-21 01:20:45 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         .         .| |  60/100 pts ( 60.0%) | Est: 2023-11-21 01:20:46 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .         .| |  70/100 pts ( 70.0%) | Est: 2023-11-21 01:20:46 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         .| |  80/100 pts ( 80.0%) | Est: 2023-11-21 01:20:46 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    .| |  90/100 pts ( 90.0%) | Est: 2023-11-21 01:20:45 AM
	|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒| | 100/100 pts (100.0%) | Est: 2023-11-21 01:20:45 AM



# License
Copyright (c) 2023, Nathan Hansen

All rights reserved.

This source code is licensed under the BSD-style license found in the

LICENSE file in the root directory of this source tree.
