# TimeMarkers
Some simple Python time tracking utilities.

Known working on Python 3.11, and assumed working for all Python 3+

Dependencies: None
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
>After every X **updates** print the progress (and trigger a callback if configured)
#### time_interval | *float, default=None*:
>After every X **seconds** print the progress (and trigger a callback if configured)
#### smooth_rate | *float, default=None*:
>The time intervals between iterations are averaged if smooth_rate is > 1, with larger values leading to longer averaging
#### callback | *any callable, default=None*:
>Depending on how callback_mode is configured, the provided callback will be called during progress updates
#### callback_mode | *CallbackMode Enum, default=CallbackMode.interval*:
 - none = 0	# no callbacks will be called, the same as if callback=None
 - interval = 1 # each time the **index_interval** is reached the callback will be called
 - timed = 2 # each time the **time_interval** is reached the callback will be called
 - both = 3 # each time **either** interval is reached the callback will be called
#### twelveHour | *bool, default=True*:
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
