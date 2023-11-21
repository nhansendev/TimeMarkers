# Copyright (c) 2023, Nathan Hansen
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import time
from Util import sec_to_HMS, progress_bar, to_set_len_str
from enum import Enum


class CallbackMode(Enum):
    none = 0
    interval = 1
    timed = 2
    both = 3


class Segments(Enum):
    timestamp = 0
    elapsed = 1
    end_time = 2
    sec_per_step = 3
    progress = 4
    bargraph = 5
    default = tuple(range(6))


class TimeWrap:
    # A simple context for timing code execution
    # Usage: "with TimeWrap(msg): *your code*"
    def __init__(self, msg, ljst=50, use_HMS_format=False) -> None:
        self.msg = msg
        self.ljst = ljst
        self.use_HMS_format = use_HMS_format

    def __enter__(self):
        print("> " + self.msg.ljust(self.ljst), end="", flush=True)
        self.st = time.time()

    def __exit__(self, *args):
        if self.use_HMS_format:
            print(f"Done, {sec_to_HMS(time.time()-self.st, True)} hh:mm:ss")
        else:
            print(f"Done, {time.time()-self.st:.3f} sec")


class TimeMarker:
    def __init__(
        self,
        est_iters=None,
        index_interval=None,
        time_interval=None,
        smooth_rate=10,
        callback=None,
        callback_mode=CallbackMode.interval,
        twelveHour=True,
        time_format=None,
        progress_bar=False,
        progress_bar_length=50,
        oneline=False,
        segments=Segments.default.value,
    ) -> None:
        if callback is not None and not callable(callback):
            raise TypeError("Provided callback must be callable, or <None>!")

        if callback_mode not in CallbackMode:
            raise ValueError("Unknown value for callback mode")

        if not hasattr(segments, "__iter__") or not all(
            [seg in Segments for seg in segments]
        ):
            raise ValueError("Unknown segment definition")

        self.est_iters = est_iters
        self.index_interval = index_interval
        self.time_interval = time_interval
        self.smooth_rate = smooth_rate
        self.callback = callback
        self.callback_mode = callback_mode
        self.twelveHour = twelveHour
        self.time_format = time_format
        self.progress_bar = progress_bar
        self.progress_bar_length = progress_bar_length
        self.oneline = oneline
        self.segments = segments
        self.reset()

    def reset(self) -> None:
        self._st_time = None
        self._last_time = None
        self._smooth_time = None
        self._iters = 0
        self._last_time_mod = 0

    def get_now_str(self, offset=0):
        if self.time_format is not None:
            # Allow custom formats
            return time.strftime(self.time_format, time.localtime(time.time() + offset))
        else:
            if self.twelveHour:
                # 12 Hour format
                return time.strftime(
                    "%Y-%m-%d %I:%M:%S %p", time.localtime(time.time() + offset)
                )
            else:
                # 24 Hour format
                return time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(time.time() + offset)
                )

    @property
    def total_duration(self):
        if self._st_time is not None:
            return time.time() - self._st_time
        else:
            return 0

    @property
    def elapsed(self):
        # Average time between iterations
        return self._smooth_time

    def __call__(self, *args, **kwds) -> None:
        if self._st_time is None:
            self._begin()
        else:
            self._update()

    def _begin(self) -> None:
        self._st_time = time.time()
        self._last_time = time.time()

    def _print_update(self):
        seg0 = self.get_now_str()
        seg3 = f"{self.elapsed:.3f} sec/step avg <{sec_to_HMS(self.elapsed)}>"

        if self.est_iters is not None:
            time_remaining = self.elapsed * (self.est_iters - self._iters)
            seg1 = f"{sec_to_HMS(self.total_duration)}/{sec_to_HMS(time_remaining)} elap/rem"
            seg2 = f"Est: {self.get_now_str(time_remaining)}"
            seg4 = f"{self._iters:{len(str(self.est_iters))}d}/{self.est_iters} pts ({to_set_len_str(self._iters/self.est_iters*100)}%)"
            if self.progress_bar:
                seg5 = progress_bar(
                    self._iters / self.est_iters,
                    barsize=self.progress_bar_length,
                    to_string=True,
                )
            else:
                seg5 = None
        else:
            seg1 = sec_to_HMS(self.total_duration)
            seg2 = None
            seg4 = f"{self._iters} pts"
            seg5 = None

        seg = [seg0, seg1, seg2, seg3, seg4, seg5]

        tmp = " | ".join([seg[s] for s in self.segments if seg[s] is not None])

        if self.oneline:
            print(tmp, end="\r", flush=True)
        else:
            print(tmp)

    def _update(self) -> None:
        self._iters += 1

        now = time.time()
        tmp = now - self._last_time
        self._last_time = now
        if self._smooth_time is None:
            self._smooth_time = tmp
        else:
            self._smooth_time += (tmp - self._smooth_time) / self.smooth_rate

        if self.index_interval is not None and self._iters % self.index_interval == 0:
            self._print_update()
            if self.callback is not None and (
                self.callback_mode == CallbackMode.both
                or self.callback_mode == CallbackMode.interval
            ):
                self.callback()

        if self.time_interval is not None:
            tmp = self.total_duration % self.time_interval
            if tmp < self._last_time_mod:
                self._print_update()
                if self.callback is not None and (
                    self.callback_mode == CallbackMode.both
                    or self.callback_mode == CallbackMode.timed
                ):
                    self.callback()
            self._last_time_mod = tmp


if __name__ == "__main__":
    TM = TimeMarker(
        30,
        index_interval=3,
        progress_bar=True,
        oneline=False,
        segments=(0, 4, 5, 3, 1),
    )

    for _ in range(30):
        TM()
        time.sleep(0.1)
    TM()
