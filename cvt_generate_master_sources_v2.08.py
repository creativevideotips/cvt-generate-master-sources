#!/usr/bin/env python3
#
# Generate All Clips Timeline PRO - part of ResolveConformTools
# Copyright (C) 2026 Maris Polis - marispolis.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# ---------------------------------------------------------------------------
# cvt_generate_master_sources_v2.08
#
# Modified version of "Generate All Clips Timeline PRO" v2.9 by Maris Polis,
# from https://github.com/polisvfx/ResolveConformTools . All credit for the
# tool goes to him. Some of the idea for the script also originated with
# Thatcher Freeman. Changes after v1.00 are by Chadwick, Creative Video Tips
# (https://creativevideotips.com), 2026, and are listed below.
#
# Like the original, this is free software under the GNU GPL v3 or later
# (see the notice above): you may use, change and share it, and any copy you
# pass on must keep this notice and stay under the same licence.
#
# What it does:
#   1. Create: builds one timeline holding every source clip used across the
#      approved edits you pick, with handles, joining close segments, and
#      marks duplicates, retimes, freeze frames, speed ramps and reversed
#      clips, including the frames transitions use. Still images get a
#      Purple clip color. Each segment sits on the video track it came from,
#      and segments that were composited together in an edit are stacked
#      (L1, L2 ...) at the same spot, so they read as one shot. The tracks
#      are named L1, L2 ... Every shot starts at frame 1001.
#   2. Shot Namer: names the shots on the open timeline (sh010, sh020 ...),
#      giving a stack of composited layers one shot name, continuing after
#      the highest number already used and leaving named shots alone. It
#      writes the source file name into each clip's Comments, an optional
#      client code (e.g. cfa) into its Shot field for Deliver's %{Shot}
#      token, sets a clip color and names the tracks L1, L2 ...
#   3. Update: re-reads the approved edits you pick (the approved bin, or a
#      Media Pool selection) and brings the open Master Sources timeline up
#      to date, marking every shot it changed. Shots only ever get longer:
#      frames already sent out for work are never cut. New shots and longer
#      copies go at the end of the timeline on their own track (no new
#      tracks), and a shot that gained head frames gets a green marker with
#      its new start frame (10 frames more = 991).
#   4. Shows a log of what it did, which can be copied for a producer or
#      exported as a CSV file.
#
# v1.00: Maris Polis's v2.9, unchanged apart from this header and the
#        version stamp (2.9-cvt1.00) written onto the timelines it builds.
# v1.01: renamed from cvt_generate_all_clips_timeline_pro to
#        cvt_generate_master_sources ("Generate Master Sources" in the window
#        title, which now also shows the version); new timelines are called
#        Master_Sources. Timelines made by v1.00 or the original still update.
# v1.02: the windows get the CVT look: charcoal and teal, opening in the middle
#        of the screen, options grouped into numbered sections, and Cancel
#        beside a teal Create / Update / Dry Run button in the lower right.
# v1.03: new "Source Timecode" choice under Sort clips by: the new timeline
#        is laid out in the order the shots were recorded, by each shot's
#        first source timecode, across every clip and camera.
# v1.04: the note about the timeline an update would change only shows when
#        Mode is set to update a timeline.
# v1.05: the Update sources choice in section 2 only shows when Mode is set
#        to update a timeline.
# v1.06: section 6, Update safety, only shows when Mode is set to update a
#        timeline.
# v1.07: the New timeline section only shows when Mode is set to create a
#        timeline; the sections are numbered 1-5 in either mode.
# v1.08: in Update mode, Update sources comes first and Select timelines by
#        only shows when the sources include the current selection (the
#        timeline being updated is always the open one). A timeline with no
#        record of its sources starts on Current selection. "Colour" is
#        spelled "color" everywhere in the window and the console.
# v1.09: Update never shortens a shot in the master timeline, only lengthens
#        it. When the edit now uses fewer frames, the shot keeps its full
#        length and the update plan lists it as kept.
# v1.10: Update reads the timelines you pick, the same way Create does: the
#        Update sources choice is gone. "Select timelines by" is now "Pick
#        them from", with Current bin first. Update mode shows what the
#        timeline was last built from, and the window remembers your choices.
# v1.11: always video only and always uses the XML for precise retime
#        detection, so neither has a checkbox any more. The connection
#        threshold defaults to 24 frames, Preserve source track layout leaves
#        48 frames between source-timeline blocks, and the duplicate marker
#        option now reads "Mark duplicate sources with colored markers".
# v1.12: clip names are always copied from the edit timelines (no checkbox),
#        and empty color versions are no longer copied with them. Disabled
#        clips, and clips on disabled tracks, are never included; the Include
#        disabled clips checkbox is gone.
# v1.13: section 4 is now Sources, with one setting, "Join gaps up to [24]
#        frames" (was Connection threshold), explained in a note and a
#        tooltip; a gap of exactly that many frames is now joined too. A file
#        imported twice is always treated as one source, so that checkbox is
#        gone. The window is shorter to fit, and long tooltips wrap.
# v1.14: the two modes are tabs, Create Sources Timeline and Update Sources
#        Timeline, instead of a Mode drop-down. The edit timelines are called
#        approved edits everywhere (section 1 is Approved edits), and a
#        stretch of a source in the master is a segment.
# v1.15: section 2 of the Create tab is now New master sources timeline. A
#        note under Pick them from says what will be read (Current bin skips
#        the bins inside it). The window is shorter.
# v1.16: handles. Each segment gets extra source frames before and after it
#        (10 by default, set under New master sources timeline), so Deliver's
#        Individual clips export includes them. Handles stop at the start and
#        end of the media, and overlapping ones join into one segment. Update
#        keeps the handle length the master was built with. Fixes v1.12-v1.15
#        skipping every track of an approved edit that was not the open
#        timeline (Resolve only reports track on/off for the open one).
# v1.17: no more false "slip unfixable" error for a segment that runs to the
#        end of its media: reaching the last frame counts as placed. The
#        Update tab no longer shows a stray "frames each side".
# v1.18: a log window opens after every run (Create, Update and Dry run)
#        with a summary and every clip that was added, lengthened, put on the
#        update track, marked no longer used or left for a manual update, and
#        a Copy to clipboard button for pasting the report into a chat.
# v1.19: the windows stay in front of Resolve, so the log no longer drops
#        behind it when clicked (Copy to clipboard could not be reached).
# v1.20: Copy to clipboard works from inside Resolve: it checks the copy
#        landed and falls back to Fusion's own clipboard, and says in the
#        console what it did.
# v1.21: the log window stays open until you close it; it used to close by
#        itself a few seconds after appearing.
# v1.22: really fixes the log closing by itself: an event from the progress
#        window crashed the log's event loop (KeyError 'On'), ending the
#        script. Copy to clipboard can now be used.
# v1.23: a dry run's log has an Apply update button: it runs the real update
#        with the same settings and shows what was done in a new log. The
#        log's summary lists only what happened ("1 longer copy on ...").
# v1.24: the track an update adds is named with just the date and the time,
#        rounded to the nearest 10 minutes, e.g. 2026-10-23_1310. An update
#        only changes the timeline the window named: if a different timeline
#        is open when it runs (e.g. Apply update after switching timelines),
#        it stops and changes nothing.
# v1.26: Create and Update finish by reopening the master and removing the
#        empty subtitle and audio tracks Resolve adds when clips are placed
#        (one audio track stays). Reopening first draws their headers;
#        deleting them without that crashed Resolve (v1.25, withdrawn).
# v1.27: still images (JPEG, PNG, TIFF and the like) come into the master
#        with a Purple clip color, so they stand out from the footage.
# v1.28: the Preserve source track layout option is gone: it placed segments
#        on top of each other, cutting shots short or losing them. Create now
#        keeps each segment on the video track it came from (V2, V3 ... for
#        composited elements; the lowest one when a source was used on more
#        than one), still laid out one after another in the Sort order.
#        Masters built with the old option still update.
# v1.29: Sort clips by has two choices, Source Name and Source Timecode (the
#        others are gone). Still images always go at the end of a new master,
#        after the footage, whichever sort is chosen. The log window now opens
#        even when a run stops with an error, and the error is shown in it.
# v1.30: the log window no longer opens and then vanishes at the end of a
#        run: the script waits for Resolve to finish redrawing the timeline
#        (the reopen that lets empty tracks be removed) before showing the
#        log, and the log stays open until you close it.
# v1.31: a shot that plays forward and then runs backward (a speed curve
#        that turns around) now gets every frame it reaches, not just the
#        frames between where it starts and ends. Dissolves and other
#        transitions now get the extra source frames they use on each side
#        of the cut, before the handles are added.
# v1.32: the log window closes as soon as you click Close (or its close
#        button), instead of after a delay.
# v1.33: really fixes the slow Close: the progress window's events kept
#        interrupting the log (KeyError 'On' over and over in the console),
#        so a click had to wait its turn. All the windows now share one
#        event handler.
# v1.34: handles are the same length at both ends: every segment used to get
#        one extra frame at its tail (11 instead of 10), because Resolve
#        21.1.2 reports a placed clip's end differently from earlier builds.
# v1.35: handles are exactly the length you set on every shot. Resolve
#        reports some edit clips one frame wider than the frames they really
#        use (C012: 212-252 for 213-251), which gave those shots 11-frame
#        handles. The frames a shot uses are now read exactly.
# v1.36: a segment can now reach the very last frame of its file. The last
#        frame was always left out, so a shot cut or dissolving near the end
#        of a short clip (C127) came up one frame short.
# v1.37: Update leaves still images that are already in the master alone.
#        It used to "lengthen" them: a still has no frames to add, but the
#        handles made it look longer in the edit than in the master. New
#        stills are still added, and stills no edit uses are still marked.
# v2.00: Shot Namer is built in, as the middle tab (Create, Shot Namer,
#        Update): it names the shots on the master, one name per stack of
#        composited layers, continuing after the highest number and leaving
#        named shots alone; always writes the source file name into
#        Comments; writes a client code into the Shot field for %{Shot};
#        names the tracks L1, L2 ... Create stacks segments that were
#        composited together in an edit and names its tracks L1, L2 ...
#        Update no longer adds a dated track: new shots and longer copies go
#        at the end of the timeline on the track they belong on. Every
#        segment has a green Start frame marker: 1001 on its first run,
#        lower when an update adds head frames (10 more = 991). Replaces
#        cvt_shot_namer_v1.06.lua.
# v2.01: the green Start frame marker only appears when an update has added
#        head frames and the shot no longer starts at 1001; new shots get
#        none. The log has Export CSV, and the Shot Namer's log lists each
#        clip's track layer and Shot field and says how many Shot fields it
#        filled. Shot Namer: the clip color starts on Keep current color, the
#        client code hint is "e.g. cfa" (Chick-fil-A), and the Name Shots
#        button is no longer cut off. The window is shorter.
# v2.02: one green marker per updated shot: the update's own marker now
#        carries the new start frame ("Start frame 991", on the shot's first
#        frame) instead of a second green marker beside it. The window fits
#        each tab's options, so it is much shorter, and the note under Pick
#        them from is no longer cut off. The Shot Namer tab drops its
#        "Always: ..." note.
# v2.03: after Create, the window opens again on the Shot Namer tab, so the
#        new master can be named straight away. Update gives its new shots
#        the same Shot field (client code) as the rest of the master. The
#        window is about half as tall: each tab is its own page, so no empty
#        rows from the other tabs, and the lines between sections have the
#        same space above and below them. The Shot Namer's dry run has its
#        own section, 3. Check first.
# v2.04: new Sort clips by choice, Edit Order (single timeline): the shots
#        are laid out in the order they first appear in the edit (stills
#        still last), for a master built from one timeline. The Update tab
#        says at the top that new shots, and longer copies of changed ones,
#        are added after the last shot.
# v2.05: clearer note beside Join gaps up to: "frames (pull close cuts of a
#        clip as one)".
# v2.06: the note beside Join gaps up to now reads "frames (merges nearby
#        segments into one clip)".
# v2.07: the section with Join gaps up to is called Segment merging (was
#        Sources) on the Create and Update tabs.
# v2.08: credits Thatcher Freeman, who also originated some of the idea for
#        the script, in this header. Nothing else changed.
#
# Install location: Fusion/Scripts/Utility  (run via Workspace > Scripts)
# ---------------------------------------------------------------------------
"""
cvt_generate_master_sources_v2.08

Generate Master Sources
Based on Generate All Clips Timeline PRO v2.9 by Maris Polis

Three tabs: Create, Shot Namer and Update, in the order they are used.

CREATE: builds a master timeline from the selected timelines, collecting all
unique source clips, merging overlapping source ranges, and placing them on a
new timeline. Detects and marks:
- Duplicate clips (colored markers)
- Retimed clips (red markers with speed info)
- Frame holds / freeze frames
- Non-linear retimes / speed ramps (via XML analysis)
- Reversed clips (normalized to forward-playing)

UPDATE: re-reads the source timelines and reconciles an existing Master Sources
timeline against them — lengthening shots to the newest state (never
shortening them: frames already sent out for work stay in the master),
appending genuinely new shots at the end of the timeline, and marking every shot it
touched with a timestamped changelog. The source timelines and the settings used
are stamped onto the timeline so a later run can find them again.

Update mode only rebuilds clips whose source range actually moved, because
Resolve has no trim and no move: changing a clip's range means deleting and
re-appending it. Its name, clip color, flags, enabled state and markers are
restored afterwards, but ITS GRADE AND FUSION COMPS CANNOT BE — there is no API
to read a grade back out. Clips carrying that work are skipped by default, and
dry run exists because Resolve's undo stack is not scriptable.

SHOT NAMER: names the shots on the open timeline from a pattern (sh###). The
layers stacked over one another (a composite) are one shot and share a name.
Shots that already have a name matching the pattern keep it, and new shots
continue after the highest number. Each clip's source file name goes into the
Comments of its media pool clip, and a client code into its Shot field (both
are media pool metadata, shared by every segment of one file).

START FRAMES: every segment starts at 1001 on its first run, with no marker.
When an update adds head frames, the update's green clip marker for that
segment becomes "Start frame N": 1001 minus the frames added. Clip markers sit
in source-frame space, and the marker's customData records which source frame
was 1001, so later
updates count from the same frame and anything keyed against the original
1001 still lines up. A segment without the marker still starts at 1001 from
its current first frame.
"""

from __future__ import annotations

import csv
import json
import math
import os
import subprocess
import tempfile
import textwrap
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Optional

# Constants
# Keep in step with the "Version:" line in the module docstring above — the repo
# convention is that the docstring is authoritative, this is what gets recorded
# into the manifest so an old timeline says which build last touched it.
TOOL_VERSION = "2.9-cvt2.08"
SCRIPT_TITLE = "Generate Master Sources"
VERSION = "2.08"
BRAND = "Creative Video Tips"

# CVT window colors: charcoal with teal accents. Every window gets
# "StyleSheet": WINDOW_STYLE; the button with "Default": True is drawn teal.
WINDOW_STYLE = """
QWidget { background-color: rgb(46, 58, 66); color: rgb(233, 239, 242); }
QLineEdit, QTextEdit, QComboBox {
    background-color: rgb(31, 40, 46); border: 1px solid rgb(76, 95, 107);
    border-radius: 3px; padding: 2px 4px; }
QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid rgb(34, 184, 174); }
QComboBox QAbstractItemView { background-color: rgb(31, 40, 46);
    selection-background-color: rgb(26, 140, 132); }
QPushButton { background-color: rgb(59, 73, 82); border: 1px solid rgb(76, 95, 107);
    border-radius: 4px; padding: 4px 14px; }
QPushButton:hover { background-color: rgb(70, 86, 96); }
QPushButton:pressed { background-color: rgb(50, 62, 70); }
QPushButton:default { background-color: rgb(34, 184, 174); border: 1px solid rgb(34, 184, 174);
    color: rgb(255, 255, 255); }
QPushButton:default:hover { background-color: rgb(46, 204, 193); }
QWidget:disabled { color: rgb(105, 120, 130); }
QLineEdit:disabled, QComboBox:disabled { background-color: rgb(40, 50, 57);
    border: 1px solid rgb(58, 72, 81); }
QTreeWidget { background-color: rgb(31, 40, 46); border: 1px solid rgb(76, 95, 107);
    alternate-background-color: rgb(38, 49, 56); }
QHeaderView::section { background-color: rgb(59, 73, 82); color: rgb(95, 224, 212);
    border: none; border-right: 1px solid rgb(46, 58, 66); padding: 4px; font-weight: bold; }
QTabBar::tab { background-color: rgb(59, 73, 82); color: rgb(190, 202, 208);
    border: 1px solid rgb(76, 95, 107); border-top-left-radius: 4px;
    border-top-right-radius: 4px; padding: 6px 16px; margin-right: 3px; }
QTabBar::tab:hover:!selected { background-color: rgb(70, 86, 96); }
QTabBar::tab:selected { background-color: rgb(34, 184, 174);
    border: 1px solid rgb(34, 184, 174); color: rgb(255, 255, 255); }
"""
HEADING_STYLE = "color: rgb(95, 224, 212); font-size: 11px; font-weight: bold;"
# The line between sections, drawn as the top border of the next heading:
# the margin is the space above the line, the padding the space below it (the
# heading's text adds about 2 more, and the row spacing 4 more above).
SECTION_LINE_STYLE = (" border-top: 1px solid rgb(76, 95, 107);"
                      " margin-top: 6px; padding-top: 8px;")
# Gaps either side of the line above the buttons.
SECTION_GAP_ABOVE = 4
SECTION_GAP_BELOW = 4
LABEL_W = 150
# Keeps the windows in front of Resolve: without it a click could drop the log
# behind Resolve's main window, out of reach, with its loop still running.
ON_TOP_FLAGS = {"Window": True, "WindowStaysOnTopHint": True}
DIVIDER_STYLE = "min-height: 1px; max-height: 1px; background-color: rgb(76, 95, 107);"
HINT_STYLE = "color: rgb(150, 165, 174);"
WARNING_STYLE = "color: rgb(230, 170, 60);"
MIN_FRAME_DIFF = 3
MIN_PERCENT_DIFF = 3.0
# Above this speed a clip is a whip or a ramp rather than a plain speed change,
# and the percentage stops carrying information — the marker reports the source
# span instead. Measured across three real commercial conform timelines: an
# ordinary slow/fast shot lands at 200-300%, while genuine whips came back at
# 800%, 1018%, 2020%, 3066% and 4616%. 400% sits in the empty gap between them.
EXTREME_RETIME_PERCENT = 400.0
DEFAULT_CONNECTION_THRESHOLD = 24
DEFAULT_HANDLES = 10  # source frames added before and after every segment
INTER_TIMELINE_GAP = 48  # frames left between an update's groups of new shots
# AppendToTimeline can place clips with a small source-frame slip relative to
# what we requested (observed: -1/0 on start, 0/-1 on end depending on whether
# the request hits a media-end clamp or an auto pre-roll handle). The post-
# processing matchers (duplicate/retime markers, clip-name import) use this
# tolerance when correlating placed timeline items back to their ClipInfo.
SLIP_TOLERANCE = 2
# Max attempts to compensate for AppendToTimeline source-frame slip before
# accepting whatever Resolve produced and logging a warning.
SLIP_RETRY_LIMIT = 2

# Diagnostics
# If XML retime expansion would grow a clip's source range by more than this
# factor, skip the expansion and keep the API range. Catches the "full length
# inclusion" case caused by Time Remap keyframes referencing the entire source.
XML_EXPANSION_MAX_GROWTH = 5.0
# In the end-of-run Range Audit, flag any clip whose final source range on the
# new timeline is >= this many times the original API-reported range.
RANGE_AUDIT_GROWTH_THRESHOLD = 2.0

# Still images are given this clip color in the master so they stand out from
# the footage. A clip is a still when Resolve's Type property says so, or, as a
# fallback, when its file has one of these extensions and is not an image
# sequence (a sequence's File Path holds a [first-last] frame range).
STILL_CLIP_COLOR = "Purple"
STILL_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".gif", ".heic",
    ".heif", ".webp", ".psd", ".tga",
}

DUPLICATE_MARKER_COLORS = [
    "Yellow", "Green", "Cyan", "Blue", "Purple", "Pink",
    "Fuchsia", "Lavender", "Rose", "Cocoa", "Sand", "Sky", "Mint", "Lemon",
]

# Update-mode manifest. Stamped onto an All Clips timeline so a later run knows
# which source timelines it was built from and with which settings — neither is
# recoverable by looking at the output. Everything else (which clips are on the
# timeline, where, and over what source range) is deliberately NOT stored: it is
# re-scanned every run so edits made in between are respected rather than
# overwritten from a stale cache.
MANIFEST_SCHEMA = 1
MANIFEST_KEY = "RCT_AllClipsManifest"
MANIFEST_MARKER_PREFIX = "RCT_AllClipsManifest_v1:"
MANIFEST_MARKER_COLOR = "Cream"  # the one color no other pass in this file uses
MANIFEST_MARKER_NAME = "Master Sources Manifest"
MANIFEST_MAX_RUNS = 20
# The customData size limit is undocumented. A 16,000-character payload was
# verified to round-trip intact on 21.0.4.5, so this cap is conservative on
# purpose — the oldest run records are dropped first if it is ever reached.
MANIFEST_MARKER_MAX_CHARS = 8000

# customData prefix on the per-clip update marker. Carries the desired range the
# clip was last reconciled against, which is what stops a clip whose target is
# physically unreachable from being rebuilt on every run forever.
UPDATE_MARKER_PREFIX = "RCT_UPD:"
# A source range must GROW by more than this many frames before the update
# rebuilds the clip. Must stay >= SLIP_TOLERANCE so last run's own placement slip
# never reads as a change; 3 also matches MIN_FRAME_DIFF, the "difference that
# matters" threshold the retime detector already uses.
UPDATE_CHANGE_TOLERANCE = 3
# ...and by more than this many frames before a clip is SHORTENED. The two are
# deliberately asymmetric: missing frames break a pull, surplus frames do not.
# Rebuilding to remove a few frames of handle costs that clip its grade and its
# Fusion comps and leaves a gap, which is a bad trade for frames nobody minds.
# Observed in practice: an All Clips timeline built by an earlier version of this
# script carried a reversed clip with 5 frames of extra handle — real, harmless,
# and not worth a rebuild. 12 frames is about half a second at 24/25 fps, well
# clear of handle and rounding differences but far below a genuine edit change.
UPDATE_SHRINK_TOLERANCE = 12
# Free space after the last clip on a track: there is always more timeline.
FREE_SPACE_UNBOUNDED = 1 << 30
# Spare frames to reserve on each side when deciding whether a grown clip may
# also use the append helper's +/-1 widening fallback. Without it, widening
# collides with the neighbour and the append fails.
REBUILD_FIT_SLACK = 1

# Per-clip update markers. Colors are Resolve marker names; the overlap with
# DUPLICATE_MARKER_COLORS is harmless — different frame, name and customData.
UPDATE_MARKER_COLORS = {
    "extended": "Green",
    "shortened": "Yellow",
    "both": "Sand",
    "new": "Mint",
    "superseded": "Purple",
    "dropped": "Rose",
    "manual": "Fuchsia",
}

# Start frame marker: the frame number to render the shot from. The first run
# of a segment starts at 1001 whatever its handles, and has no marker (v2.01);
# frames added to the head later count down from there (10 more = 991), and
# only then is the marker added, so anything keyed against the original 1001
# stays where it was. customData keeps the source frame that was 1001, which
# an update carries to the rebuilt clip.
START_MARKER_PREFIX = "CVT_START:"
START_MARKER_COLOR = "Green"
FIRST_START_FRAME = 1001
START_NOTE_LEAD = "Render this shot with its first frame numbered"
# Video tracks are named L1, L2 ... (layer 1, layer 2) by Create, Update and
# the Shot Namer.
TRACK_NAME_PREFIX = "L"

# Shot Namer: Resolve's clip colors, in the order of its Clip Color menu.
CLIP_COLORS = [
    "Orange", "Apricot", "Yellow", "Lime", "Olive", "Green", "Teal", "Navy",
    "Blue", "Purple", "Violet", "Pink", "Tan", "Beige", "Brown", "Chocolate",
]
KEEP_COLOR = "Keep current color"
CLEAR_COLOR = "Clear color"
# The media pool metadata field the client code goes in; Deliver's %{Shot}.
SHOT_CODE_FIELD = "Shot"
# Fraction of the clip the update marker sits at. The duplicate pass uses 0.25
# and the retime pass 0.5, so 0.75 keeps all three apart on all but tiny clips —
# and pick_marker_frame() steps off a collision even then.
UPDATE_MARKER_FRACTION = 0.75
RUN_MARKER_PREFIX = "RCT_RUN:"
RUN_MARKER_COLOR = "Sky"
# Changelog lines kept in a clip's update marker note before the tail is folded
# into a "... (N earlier changes)" summary line.
CHANGELOG_MAX_LINES = 8
CHANGELOG_TRUNCATION_MARK = "... ("
# Marker text stays ASCII: it round-trips through the scripting bridge and back
# out through GetMarkers on every subsequent run.
CHANGELOG_SEPARATOR = " | "

# UI mode labels, and the update-source options mapped to the internal names
# run_update_workflow expects.
MODE_CREATE = "Create New Timeline"
MODE_UPDATE = "Update Existing Timeline"
MODE_NAMER = "Shot Namer"
# Upstream's choice of which sources an update re-reads. The window no longer
# offers it (v1.10): Update always reads the picked timelines ("Selection").
SOURCE_MODES = [
    ("Recorded in timeline", "Recorded"),
    ("Current selection", "Selection"),
    ("Recorded + current selection", "Union"),
]
# Tab labels, in tab order; the mode values above stay as stored in settings
MODE_TABS = [(MODE_CREATE, "Create Sources Timeline"),
             (MODE_NAMER, "Shot Namer"),
             (MODE_UPDATE, "Update Sources Timeline")]
# "Pick them from" choices: (label in the window, value resolve_source_timelines expects)
PICK_FROM = [
    ("Current bin", "Current Bin"),
    ("Media Pool selection", "Current Selection"),
]
# What an update does to the timeline, at the top of the Update tab
UPDATE_NOTE = ("New shots, and longer copies of changed ones, are added after "
               "the last shot.")
# The note under the tabs on the Create tab (the others name the open timeline)
CREATE_LABEL = "Builds a new master sources timeline from the approved edits."
# The note under "Pick them from", per choice
PICK_FROM_HINTS = {
    "Current bin": "Reads every timeline in the open bin. Bins inside it are "
                   "skipped, so move old versions into one.",
    "Media Pool selection": "Reads only the timelines you have selected in the "
                            "Media Pool.",
}


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ClipInfo:
    """Source clip frame range for timeline assembly.

    All frame ranges are normalized: start_frame <= end_frame.
    Metadata fields track the original clip's editorial state.
    """
    media_pool_item: object
    start_frame: int
    end_frame: int
    timeline_inpoint: int = 0
    timeline_endpoint: int = 0
    source_track_index: int = 1
    source_timeline_name: str = ""
    is_reversed: bool = False
    is_retimed: bool = False
    is_frame_hold: bool = False
    is_non_linear_retime: bool = False
    retime_percentage: Optional[float] = None
    xml_source_min: Optional[int] = None
    xml_source_max: Optional[int] = None
    source_name: Optional[str] = None
    # Populated by find_duplicate_groups after merging. None = not a duplicate.
    duplicate_set_index: Optional[int] = None
    duplicate_position: Optional[int] = None
    duplicate_set_size: Optional[int] = None
    # Raw API-reported source range, captured BEFORE XML expansion and merging.
    # Used by the end-of-run Range Audit to detect ranges that grew unexpectedly.
    api_source_start: Optional[int] = None
    api_source_end: Optional[int] = None
    # Every place in the approved edits this segment is used:
    # (edit name, video track, record start, record end exclusive). Merging
    # joins the lists; find_composite_groups() reads them.
    uses: list = field(default_factory=list)
    # Segments composited together in an edit share a group number.
    composite_group: Optional[int] = None


@dataclass
class TimelineClipData:
    """Wrapper for timeline items used in duplicate detection and marker placement."""
    clip: object
    media_pool_item: object
    start_frame: int
    name: str
    track_index: int
    retime_percentage: Optional[float] = None
    is_non_linear_retime: bool = False


@dataclass
class RetimeKeyframe:
    """A single keyframe from the FCP XML Time Remap effect."""
    when: int
    value: int


@dataclass
class PlacedClip:
    """A clip found on an existing All Clips timeline during an update scan.

    record_end is EXCLUSIVE and is computed as GetStart() + GetDuration() rather
    than from GetEnd(). Verified on 21.0.4.5 that GetEnd() is itself exclusive
    (start 90100 + duration 79 = end 90179), so the two agree — but duration is
    unambiguous by definition, so the arithmetic here does not rest on that.
    """
    item: object
    identity: str
    source_start: int          # inclusive, normalised so start <= end
    source_end: int            # inclusive
    record_start: int          # absolute timeline frame
    record_end: int            # exclusive
    track_index: int
    name: str = ""
    # Desired range this clip was last reconciled against, read back from its own
    # update marker. None when the clip has never been through an update.
    accepted_start: Optional[int] = None
    accepted_end: Optional[int] = None
    linked_item_count: int = 0


@dataclass
class ItemState:
    """Everything about a TimelineItem that survives a delete + re-append.

    Grades and Fusion comps are absent because they cannot be carried across:
    CopyGrades copies FROM a live source item, and SetCDL has no getter. Their
    presence is recorded so a clip that would lose them can be reported, and
    optionally left alone.
    """
    name: Optional[str] = None
    clip_color: Optional[str] = None
    flags: list = field(default_factory=list)
    markers: dict = field(default_factory=dict)
    enabled: Optional[bool] = None
    fusion_comp_count: int = 0
    version_names: list = field(default_factory=list)
    linked_item_count: int = 0
    track_index: int = 1
    record_start: int = 0
    duration: int = 0
    source_start: int = 0
    source_end: int = 0


@dataclass
class ClipDiff:
    """One reconciliation decision: what to do about one shot."""
    identity: str
    kind: str                          # unchanged|extended|shortened|both|new|dropped
    clip_info: Optional[ClipInfo] = None   # None for "dropped"
    placed: Optional[PlacedClip] = None    # None for "new"
    head_delta: int = 0                # desired_start - placed_start; <0 grows
    tail_delta: int = 0                # desired_end - placed_end;    >0 grows
    # The edit now uses fewer frames than the master holds; the master keeps them.
    kept_frames: bool = False


def window_title(suffix=""):
    """'Generate Master Sources - v2.08  |  Creative Video Tips' (suffix after the name)."""
    name = f"{SCRIPT_TITLE} - {suffix}" if suffix else SCRIPT_TITLE
    return f"{name} - v{VERSION}  |  {BRAND}"


NAMER_LOG_COLUMNS = [("Shot name", 200), ("What happened", 250), ("Frames", 80),
                     ("Source file", 230), ("Track layer", 100),
                     (f"{SHOT_CODE_FIELD} field", 200)]
LOG_COLUMNS = [("Clip", 220), ("What happened", 260), ("Frames", 150),
               ("Source frames", 170), ("Note", 340)]


@dataclass
class RunReport:
    """What a run did, for the log window and the clipboard."""
    title: str = ""
    summary: str = ""
    rows: list = field(default_factory=list)  # (clip, what, frames, source, note)
    can_apply: bool = False  # a dry run that found changes to make
    columns: Optional[list] = None  # [(title, width)]; LOG_COLUMNS when None

    def add(self, *values) -> None:
        self.rows.append(tuple(str(v) for v in values))

    def headings(self) -> list:
        return [title for title, _width in (self.columns or LOG_COLUMNS)]

    def write_csv(self, path: str) -> None:
        """The log's table as a CSV file (UTF-8 with a BOM, so Excel reads it)."""
        width = len(self.headings())
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(self.headings())
            for row in self.rows:
                writer.writerow((list(row) + [""] * width)[:width])

    def as_text(self) -> str:
        """Plain text for pasting into a chat."""
        lines = [line for line in (self.title, self.summary) if line]
        if self.rows:
            lines.append("")
            for row in self.rows:
                lines.append("- " + " | ".join(part for part in row if part))
        return "\n".join(lines)


# Filled in by the run, shown by main() once it finishes.
REPORT = RunReport()
# The main window's UI Manager and dispatcher, reused by the log window.
UI_HANDLES: dict = {}
WINDOW_COUNTER = [0]  # gives each progress/log window its own ID


def count_phrase(count: int, one: str, many: str) -> str:
    """'1 new shot' / '3 new shots'."""
    return f"{count} {one if count == 1 else many}"


def update_summary(tally: dict, edits: list) -> str:
    """One sentence for the log, leaving out the kinds that did not happen."""
    lengthened = tally.get("extended", 0) + tally.get("shortened", 0) + tally.get("both", 0)
    parts = [phrase for count, phrase in (
        (lengthened, count_phrase(lengthened, "shot lengthened in place",
                                  "shots lengthened in place")),
        (tally.get("superseded", 0), count_phrase(tally.get("superseded", 0),
                                                  "longer copy at the end of the timeline",
                                                  "longer copies at the end of the timeline")),
        (tally.get("new", 0), count_phrase(tally.get("new", 0), "new shot", "new shots")),
        (tally.get("dropped", 0), count_phrase(tally.get("dropped", 0),
                                               "shot no longer used", "shots no longer used")),
        (tally.get("skipped", 0), count_phrase(tally.get("skipped", 0),
                                               "shot needs a manual update",
                                               "shots need a manual update")),
        (tally.get("failed", 0), count_phrase(tally.get("failed", 0), "failed", "failed")),
    ) if count]
    done = ", ".join(parts) if parts else "No changes"
    return f"{done}. Approved edits: {', '.join(edits)}."


def frames_change(head_delta: int, tail_delta: int) -> str:
    """'head +12, tail +5' from desired-minus-placed deltas (head grows when negative)."""
    parts = []
    if -head_delta:
        parts.append(f"head {-head_delta:+d}")
    if tail_delta:
        parts.append(f"tail {tail_delta:+d}")
    return ", ".join(parts)


def wrap_tip(text: str, width: int = 70) -> str:
    """Tooltip text with line breaks: Resolve's tooltips do not wrap on their own."""
    return "\n\n".join(textwrap.fill(part, width) for part in text.split("\n\n"))


def summarise_names(names: list, limit: int = 6) -> str:
    """'A, B, C' for a few names, 'A, B ... and 4 more' for many."""
    names = [n for n in names if n] or ["(none recorded)"]
    if len(names) <= limit:
        return ", ".join(names)
    return f"{', '.join(names[:limit])} and {len(names) - limit} more"


# ---------------------------------------------------------------------------
# Remembered settings (unversioned file, so they carry over between versions)
# ---------------------------------------------------------------------------

SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".cvt",
                             "generate_master_sources.json")


def default_settings() -> dict:
    return {
        "mode": MODE_CREATE,
        "pick_from": PICK_FROM[0][0],
        "timeline_name": "Master_Sources",
        "sorting_method": "Source Name",
        "connection_threshold": DEFAULT_CONNECTION_THRESHOLD,
        "mark_duplicates": True,
        "mark_retimed_clips": True,
        "handles": DEFAULT_HANDLES,
        "protect_graded_clips": True,
        # Shot Namer tab
        "namer_pattern": "sh###",
        "namer_start": 10,
        "namer_increment": 10,
        "namer_from_playhead": False,
        "namer_keep_names": True,
        "namer_append_source": False,
        "namer_clip_color": KEEP_COLOR,
        "namer_code": "",
    }


def load_settings() -> dict:
    """Saved choices over the defaults; anything missing or unrecognised falls back."""
    settings = default_settings()
    try:
        with open(SETTINGS_PATH) as f:
            saved = json.load(f)
    except (OSError, ValueError):
        return settings
    if not isinstance(saved, dict):
        return settings
    if saved.get("settings_version", 1) < 2 and saved.get("connection_threshold") == 25:
        saved["connection_threshold"] = DEFAULT_CONNECTION_THRESHOLD  # old default
    if saved.get("settings_version", 1) < 3 and saved.get("namer_clip_color") == "Teal":
        saved["namer_clip_color"] = KEEP_COLOR  # v2.00's default
    choices = {"mode": (MODE_CREATE, MODE_NAMER, MODE_UPDATE),
               "namer_clip_color": [KEEP_COLOR] + CLIP_COLORS + [CLEAR_COLOR],
               "pick_from": [label for label, _value in PICK_FROM],
               "sorting_method": list(SORT_METHODS)}
    for key, default in settings.items():
        value = saved.get(key)
        if key in choices:
            if value in choices[key]:
                settings[key] = value
        elif isinstance(default, bool):
            if isinstance(value, bool):
                settings[key] = value
        elif isinstance(default, int):
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                settings[key] = value
        elif isinstance(value, str) and value.strip():
            settings[key] = value.strip()
    return settings


# 2: connection threshold default went from 25 to 24 (v1.11)
# 3: the Shot Namer's clip color default went from Teal to Keep current color (v2.01)
SETTINGS_VERSION = 3


def save_settings(settings: dict) -> None:
    try:
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, "w") as f:
            json.dump(dict(settings, settings_version=SETTINGS_VERSION), f, indent=2)
    except OSError as e:
        print(f"{SCRIPT_TITLE}: could not save settings: {e}")


def screen_area():
    """(left, top, width, height) of the screen Resolve is on, minus the menu bar, in points, or None."""
    script = ("ObjC.import('AppKit'); var p = $.NSScreen.screens.objectAtIndex(0).frame; "
              "var v = $.NSScreen.mainScreen.visibleFrame; "
              "[p.size.height, v.origin.x, v.origin.y, v.size.width, v.size.height].join(',')")
    try:
        proc = subprocess.run(["osascript", "-l", "JavaScript", "-e", script],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
        primary_h, vx, vy, vw, vh = (float(v) for v in proc.stdout.decode().strip().split(","))
    except (OSError, ValueError, subprocess.SubprocessError):
        return None
    return int(vx), int(primary_h - vy - vh), int(vw), int(vh)  # flip y to count from the top


def centered_geometry(width, height):
    """UI Manager Geometry [x, y, w, h] that centres a window on the screen."""
    area = screen_area()
    if not area:
        return [300, 200, width, height]
    left, top, screen_w, screen_h = area
    width, height = min(width, screen_w - 40), min(height, screen_h - 40)
    return [left + (screen_w - width) // 2, top + (screen_h - height) // 2, width, height]


# ---------------------------------------------------------------------------
# XML Retime Analysis
# ---------------------------------------------------------------------------


def export_timeline_to_xml(timeline) -> Optional[str]:
    """Export a timeline to FCP 7 XML in a temp file. Returns the file path or None."""
    try:
        fd, temp_path = tempfile.mkstemp(suffix=".xml", prefix="resolve_export_")
        os.close(fd)
        success = timeline.Export(temp_path, resolve.EXPORT_FCP_7_XML)  # noqa: F821
        if success:
            print(f"  Exported timeline XML to: {temp_path}")
            return temp_path
        else:
            print("  Warning: XML export failed (may require Resolve Studio)")
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            return None
    except Exception as e:
        print(f"  Warning: XML export error: {e}")
        return None


def parse_time_remap_keyframes(clip_element: ET.Element) -> list[RetimeKeyframe]:
    """Extract Time Remap keyframes from a <clipitem> element.

    Looks for <effect><name>Time Remap</name> with <parameter> containing
    <keyframe> entries with <when> and <value>. Resolve puts them under the
    "graphdict" parameter.

    Values are FRACTIONAL and must be parsed as floats. Measured on 21.0.4.5,
    a hand-authored speed ramp exports as:

        when=0     value=0
        when=2226  value=7781.12
        when=5094  value=3819.31
        when=7009  value=8750.2
        when=9264  value=3122.6

    int("7781.12") raises ValueError, and the except below used to swallow it,
    so every keyframe but an all-integer one was silently dropped. That left
    most curves looking like a single keyframe: compute_source_range_from_
    keyframes() then saw fewer than three and never reported a speed ramp, so
    the XML pass reported nothing and expanded nothing. Rounding to whole
    frames is right — a source frame is what gets pulled.
    """
    keyframes = []
    for effect in clip_element.findall(".//effect"):
        name_el = effect.find("name")
        if name_el is None or name_el.text != "Time Remap":
            continue
        for param in effect.findall("parameter"):
            for kf in param.findall("keyframe"):
                when_el = kf.find("when")
                value_el = kf.find("value")
                if when_el is not None and value_el is not None:
                    try:
                        keyframes.append(RetimeKeyframe(
                            when=int(round(float(when_el.text))),
                            value=int(round(float(value_el.text))),
                        ))
                    except (ValueError, TypeError):
                        continue
    return keyframes


def curve_value_at(keyframes: list[RetimeKeyframe], when: float) -> float:
    """The retime curve's source frame at output frame `when`, interpolated.

    The curve is piecewise linear between keyframes and flat outside them.
    """
    points = sorted(keyframes, key=lambda kf: kf.when)
    if when <= points[0].when:
        return float(points[0].value)
    if when >= points[-1].when:
        return float(points[-1].value)
    for first, second in zip(points, points[1:]):
        if first.when <= when <= second.when:
            if second.when == first.when:
                return float(second.value)
            progress = (when - first.when) / (second.when - first.when)
            return first.value + progress * (second.value - first.value)
    return float(points[-1].value)


def compute_source_range_from_keyframes(
    keyframes: list[RetimeKeyframe],
    when_start: Optional[int] = None,
    when_end: Optional[int] = None,
) -> tuple[int, int, bool]:
    """From retime keyframes, compute (min_source_frame, max_source_frame, is_non_linear).

    is_non_linear is True if the speed varies between keyframe segments.

    `when_start`/`when_end` scope the answer to one timeline instance, and are
    the clipitem's own <in>/<out>. Resolve writes ONE curve per source clip,
    covering the whole file, and each instance is a window into it -- so
    min/max over every keyframe describes the entire media, not this shot.
    Measured across three real conform timelines: unscoped, 76 of 82 ramped
    clips came back spanning >500 source frames (their whole file), while
    scoping reproduced the API's own range exactly on 74 of 82.

    Within the window the extremes are taken over the endpoints AND every
    keyframe inside it, which is what catches an overshoot: a curve that runs
    past its out-point and reverses back turns around at an interior keyframe,
    so its furthest frame is never at either end.
    """
    if not keyframes:
        return (0, 0, False)

    if when_start is None or when_end is None:
        values = [kf.value for kf in keyframes]
        scoped = list(keyframes)
    else:
        low, high = min(when_start, when_end), max(when_start, when_end)
        values = [curve_value_at(keyframes, low), curve_value_at(keyframes, high)]
        scoped = [kf for kf in keyframes if low < kf.when < high]
        values.extend(kf.value for kf in scoped)
        # Endpoints act as the segment bounds for the linearity test below.
        scoped = ([RetimeKeyframe(when=low, value=round(values[0]))]
                  + scoped
                  + [RetimeKeyframe(when=high, value=round(values[1]))])

    src_min = int(round(min(values)))
    src_max = int(round(max(values)))

    # Check for non-linear speed: compare speed ratios between consecutive segments
    is_non_linear = False
    if len(scoped) >= 3:
        speeds = []
        for i in range(len(scoped) - 1):
            dt = scoped[i + 1].when - scoped[i].when
            dv = scoped[i + 1].value - scoped[i].value
            if dt != 0:
                speeds.append(dv / dt)
        if speeds:
            ref_speed = speeds[0]
            for s in speeds[1:]:
                if abs(s - ref_speed) > 0.01:
                    is_non_linear = True
                    break

    return (src_min, src_max, is_non_linear)


def transition_overlap(clip_start: int, clip_end: int, transitions: list) -> tuple:
    """(head, tail) timeline frames that transitions reach past a clip's cut points.

    `transitions` are (start, end) timeline frames, end exclusive like
    GetEnd(). A centred dissolve on the cut at the clip's start begins before
    it: those frames need source before the clip's in point (head). One on the
    cut at its end runs past it: source after the out point (tail).
    """
    head = tail = 0
    for t_start, t_end in transitions:
        if t_start < clip_start <= t_end:
            head = max(head, clip_start - t_start)
        if t_start <= clip_end < t_end:
            tail = max(tail, t_end - clip_end)
    return head, tail


def build_xml_clip_lookup(xml_path: str) -> dict[str, list[dict]]:
    """Parse FCP 7 XML and build a lookup from clip name to retime data.

    Returns: {clip_file_name: [{source_min, source_max, is_non_linear}, ...]}
    """
    lookup: dict[str, list[dict]] = {}
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"  Warning: XML parse error: {e}")
        return lookup

    # A <file> is written in full once and referenced by id after that, so
    # map ids to file names first.
    file_names: dict = {}
    for file_el in root.iter("file"):
        file_id, file_name = file_el.get("id"), file_el.findtext("name")
        if file_id and file_name:
            file_names[file_id] = file_name

    for clip_item in root.iter("clipitem"):
        keyframes = parse_time_remap_keyframes(clip_item)
        if not keyframes:
            continue

        # Key the entry by the clip's <name> AND its file's name: a clip
        # renamed in the edit ("C094") has a different <name> from the file
        # ("A001_08201510_C094.braw"), and the timeline may report either.
        names = []
        clip_name = clip_item.findtext("name")
        if clip_name:
            names.append(clip_name)
        file_el = clip_item.find("file")
        if file_el is not None:
            file_name = file_el.findtext("name") or file_names.get(file_el.get("id"))
            if file_name and file_name not in names:
                names.append(file_name)
        if not names:
            continue

        # <in>/<out> are this instance's window into the clip's retime curve,
        # in the same frame domain as the keyframes' <when>. Without them the
        # range below is the whole media (see compute_source_range_from_
        # keyframes) and every expansion it proposes is refused by the growth
        # cap, which is why the XML pass used to change nothing.
        when_start = when_end = None
        try:
            in_el, out_el = clip_item.find("in"), clip_item.find("out")
            if in_el is not None and out_el is not None:
                when_start = int(round(float(in_el.text)))
                when_end = int(round(float(out_el.text)))
        except (TypeError, ValueError):
            when_start = when_end = None

        src_min, src_max, is_non_linear = compute_source_range_from_keyframes(
            keyframes, when_start, when_end)
        entry = {
            "source_min": src_min,
            "source_max": src_max,
            "is_non_linear": is_non_linear,
        }
        for name in names:
            lookup.setdefault(name, []).append(entry)

    return lookup


def match_xml_retime_to_clip(
    clip_name,
    clip_source_start: int,
    clip_source_end: int,
    xml_lookup: dict[str, list[dict]],
) -> Optional[dict]:
    """Match a Resolve timeline clip to its XML counterpart by name and overlapping range.

    clip_name may be one name or a list of names to try (timeline item name,
    media pool name); the first entry whose range overlaps wins.
    """
    names = [clip_name] if isinstance(clip_name, str) else list(clip_name)
    entries = []
    for name in names:
        for entry in xml_lookup.get(name) or []:
            if entry not in entries:
                entries.append(entry)
    if not entries:
        return None
    for entry in entries:
        # Check for overlapping source range
        if entry["source_max"] >= clip_source_start and entry["source_min"] <= clip_source_end:
            return entry
    # No overlap found — don't guess; returning a wrong entry would expand ranges incorrectly
    return None


# ---------------------------------------------------------------------------
# Sorting Functions
# ---------------------------------------------------------------------------

def sort_by_start_frame(clip_infos: list[ClipInfo]) -> None:
    clip_infos.sort(key=lambda c: c.start_frame)


def sort_by_source_name(clip_infos: list[ClipInfo]) -> None:
    clip_infos.sort(key=lambda c: (c.media_pool_item.GetName(), c.timeline_inpoint))


def parse_timecode(tc: str) -> Optional[tuple]:
    """'09:25:54:15' or '09:25:54;15' -> (h, m, s, f, is_drop_frame), or None."""
    parts = (tc or "").strip().replace(";", ":").replace(".", ":").split(":")
    if len(parts) != 4:
        return None
    try:
        h, m, s, f = (int(p) for p in parts)
    except ValueError:
        return None
    return h, m, s, f, ";" in tc or "." in tc


def timecode_to_frames(h: int, m: int, s: int, f: int, nominal: int, drop: bool) -> int:
    """Frame count of a timecode label at a whole-number rate (30 for 29.97)."""
    frames = (h * 3600 + m * 60 + s) * nominal + f
    if drop:
        dropped = 2 * nominal // 30          # 2 at 29.97, 4 at 59.94
        minutes = h * 60 + m
        frames -= dropped * (minutes - minutes // 10)
    return frames


def frames_to_timecode(frames: int, nominal: int, drop: bool) -> tuple:
    """(h, m, s, f) label for a frame count; the inverse of timecode_to_frames."""
    if drop:
        dropped = 2 * nominal // 30
        per_ten = nominal * 600 - 9 * dropped
        per_minute = nominal * 60 - dropped
        tens, rest = divmod(frames, per_ten)
        frames += 9 * dropped * tens
        if rest > dropped:
            frames += dropped * ((rest - dropped) // per_minute)
    s_total, f = divmod(frames, nominal)
    h, rest = divmod(s_total, 3600)
    m, s = divmod(rest, 60)
    return h, m, s, f


def source_timecode_seconds(start_tc: str, fps, offset_frames: int,
                            drop_flag=None) -> Optional[float]:
    """Seconds on the timecode clock of the frame offset_frames into a clip.

    Counted as the label reads (hh:mm:ss + ff / rate), so clips at different
    frame rates still sort the way their timecode reads. None if the clip has
    no usable Start TC or frame rate.
    """
    parsed = parse_timecode(start_tc)
    try:
        nominal = int(round(float(fps)))
    except (TypeError, ValueError):
        return None
    if parsed is None or nominal <= 0:
        return None
    h, m, s, f, drop = parsed
    drop = (drop or str(drop_flag) == "1") and nominal % 30 == 0
    total = timecode_to_frames(h, m, s, f, nominal, drop) + int(offset_frames)
    h, m, s, f = frames_to_timecode(max(total, 0), nominal, drop)
    return h * 3600 + m * 60 + s + f / nominal


def sort_by_source_timecode(clip_infos: list[ClipInfo]) -> None:
    """Order clips by the source timecode of their first frame, across all clips.

    Clips without a usable Start TC go last, by source name.
    """
    properties: dict = {}

    def tc_key(c: ClipInfo):
        item = c.media_pool_item
        key = id(item)
        if key not in properties:
            try:
                properties[key] = item.GetClipProperty() or {}
            except Exception:
                properties[key] = {}
        props = properties[key]
        name = item.GetName() or ""
        seconds = source_timecode_seconds(props.get("Start TC"), props.get("FPS"),
                                          c.start_frame, props.get("Drop frame"))
        if seconds is None:
            return (1, 0.0, name, c.start_frame)
        return (0, seconds, name, c.start_frame)

    clip_infos.sort(key=tc_key)


def sort_by_edit_order(clip_infos: list[ClipInfo], edit_rank: Optional[dict] = None) -> None:
    """Order clips by where they are first used in the edit (record order).

    Meant for a master built from one timeline. With several edits, each clip
    goes by its earliest use in the first edit that uses it, in the order the
    edits were read (edit_rank: edit name -> position).
    """
    edit_rank = edit_rank or {}

    def first_use(c: ClipInfo):
        uses = [(edit_rank.get(edit, len(edit_rank)), start)
                for edit, _track, start, _end in (c.uses or [])]
        return (min(uses) if uses else (len(edit_rank) + 1, c.timeline_inpoint),
                c.media_pool_item.GetName() or "")

    clip_infos.sort(key=first_use)


EDIT_ORDER = "Edit Order (single timeline)"
SORT_METHODS = {
    "Source Name": sort_by_source_name,
    "Source Timecode": sort_by_source_timecode,
    EDIT_ORDER: sort_by_edit_order,
}


# ---------------------------------------------------------------------------
# Clip Merging Functions
# ---------------------------------------------------------------------------

def check_overlap(a: ClipInfo, b: ClipInfo, threshold: int) -> bool:
    """Whether two normalized ClipInfos overlap, or leave a gap of at most
    `threshold` missing frames between them (the "Join gaps up to" setting).

    Frames 100-200 and 225-300 leave 24 frames out (201-224): joined at 24.
    """
    return not (a.end_frame < b.start_frame - threshold - 1 or
                b.end_frame < a.start_frame - threshold - 1)


def merge_two(a: ClipInfo, b: ClipInfo) -> ClipInfo:
    """Merge two overlapping ClipInfos into one spanning both ranges."""
    merged_min = min(a.start_frame, b.start_frame)
    merged_max = max(a.end_frame, b.end_frame)

    print(f"Merging clips with frames:")
    print(f"  A: {a.start_frame} to {a.end_frame}")
    print(f"  B: {b.start_frame} to {b.end_frame}")
    print(f"  Merged: {merged_min} to {merged_max}")

    # Merge XML source ranges if available
    xml_min = None
    xml_max = None
    if a.xml_source_min is not None and b.xml_source_min is not None:
        xml_min = min(a.xml_source_min, b.xml_source_min)
    else:
        xml_min = a.xml_source_min if a.xml_source_min is not None else b.xml_source_min
    if a.xml_source_max is not None and b.xml_source_max is not None:
        xml_max = max(a.xml_source_max, b.xml_source_max)
    else:
        xml_max = a.xml_source_max if a.xml_source_max is not None else b.xml_source_max

    # Carry the API-reported source range through the merge as the span of
    # constituent API ranges. Range Audit compares final start/end_frame to
    # this span — any growth past 1.0x means XML expansion was applied to
    # at least one constituent.
    api_min: Optional[int] = None
    api_max: Optional[int] = None
    if a.api_source_start is not None and b.api_source_start is not None:
        api_min = min(a.api_source_start, b.api_source_start)
    else:
        api_min = a.api_source_start if a.api_source_start is not None else b.api_source_start
    if a.api_source_end is not None and b.api_source_end is not None:
        api_max = max(a.api_source_end, b.api_source_end)
    else:
        api_max = a.api_source_end if a.api_source_end is not None else b.api_source_end

    return ClipInfo(
        media_pool_item=a.media_pool_item,
        start_frame=merged_min,
        end_frame=merged_max,
        timeline_inpoint=min(a.timeline_inpoint, b.timeline_inpoint),
        timeline_endpoint=max(a.timeline_endpoint, b.timeline_endpoint),
        source_track_index=min(a.source_track_index, b.source_track_index),
        source_timeline_name=a.source_timeline_name,
        is_reversed=a.is_reversed or b.is_reversed,
        is_retimed=a.is_retimed or b.is_retimed,
        is_frame_hold=a.is_frame_hold and b.is_frame_hold,
        is_non_linear_retime=a.is_non_linear_retime or b.is_non_linear_retime,
        retime_percentage=a.retime_percentage if a.retime_percentage is not None else b.retime_percentage,
        xml_source_min=xml_min,
        xml_source_max=xml_max,
        source_name=a.source_name if a.source_name is not None else b.source_name,
        api_source_start=api_min,
        api_source_end=api_max,
        uses=list(a.uses) + list(b.uses),
        composite_group=a.composite_group if a.composite_group is not None else b.composite_group,
    )


def add_handles(start: int, end: int, handles: int, media_frames: Optional[int]) -> tuple:
    """(start, end) grown by `handles` source frames each side, kept inside the media.

    The last usable frame is media_frames - 1 (see below); with no known length
    the end is not capped.
    """
    if handles <= 0:
        return start, end
    new_start = max(0, start - handles)
    new_end = end + handles
    if media_frames:
        # Measured on 21.1.2 (v1.36): startFrame=0, endFrame=54 on a 54-frame
        # clip places all 54 frames, 0-53, so N-1 is the last usable frame.
        # The N-2 used before came from GetSourceEndFrame, which reads 53
        # there whether 53 or 54 frames were placed.
        new_end = min(new_end, max(end, media_frames - 1))
    return new_start, new_end


def merge_all_overlapping(clip_infos: list[ClipInfo], threshold: int) -> list[ClipInfo]:
    """Iteratively merge all overlapping clips for the same media pool item."""
    sort_by_start_frame(clip_infos)
    i = 0
    while i < len(clip_infos):
        j = i + 1
        merged = False
        while j < len(clip_infos):
            if check_overlap(clip_infos[i], clip_infos[j], threshold):
                print(f"Merging clips: {clip_infos[i].media_pool_item.GetName()}")
                clip_infos[i] = merge_two(clip_infos[i], clip_infos[j])
                clip_infos.pop(j)
                merged = True
            else:
                j += 1
        if not merged:
            i += 1
    return clip_infos


# ---------------------------------------------------------------------------
# Composites, start frames and shot names (no Resolve dependency)
# ---------------------------------------------------------------------------

def find_composite_groups(clip_infos: list) -> int:
    """Number the segments that were composited together in an approved edit.

    Two segments belong together when one of their uses sits on a different
    video track of the same edit, at the same time (their record ranges
    overlap). Groups chain: a V3 element over a V2 element over a V1 plate is
    one group. Sets composite_group (None for a segment on its own) and returns
    how many groups there are.
    """
    parent = list(range(len(clip_infos)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    uses = []  # (edit, start, end, track, segment index)
    for index, ci in enumerate(clip_infos):
        for edit, track, start, end in ci.uses or ():
            uses.append((edit, start, end, track, index))
    uses.sort()
    # Sweep each edit in record order; only uses still running can overlap.
    running: list = []
    current_edit = None
    for edit, start, end, track, index in uses:
        if edit != current_edit:
            current_edit, running = edit, []
        running = [u for u in running if u[0] > start]
        for other_end, other_track, other_index in running:
            if other_track != track and other_index != index:
                parent[find(index)] = find(other_index)
        running.append((end, track, index))

    members: dict = {}
    for index in range(len(clip_infos)):
        members.setdefault(find(index), []).append(index)
    group_no = 0
    for ci in clip_infos:
        ci.composite_group = None
    for root in sorted(members, key=lambda r: min(members[r])):
        group = members[root]
        if len(group) < 2:
            continue
        for index in group:
            clip_infos[index].composite_group = group_no
        group_no += 1
    return group_no


def composite_blocks(clip_infos: list) -> list:
    """The segments as blocks to lay out: a composite group is one block, in
    the place of its first segment in the list; any other segment is a block
    of its own. Inside a block the segments are ordered by track, then by
    where they are first used in the edit."""
    blocks, by_group = [], {}
    for ci in clip_infos:
        group = ci.composite_group
        if group is None:
            blocks.append([ci])
        elif group in by_group:
            by_group[group].append(ci)
        else:
            by_group[group] = [ci]
            blocks.append(by_group[group])

    def order(ci):
        first_use = min(((u[0], u[2]) for u in ci.uses), default=("", 0))
        return (max(1, ci.source_track_index or 1), first_use)

    for block in blocks:
        block.sort(key=order)
    return blocks


def read_start_reference(markers: dict) -> Optional[tuple]:
    """(source frame, start frame it was given) off a clip's update marker
    (the newest run's), or off a v2.00/v2.01 start frame marker; None when the
    clip has neither, i.e. it still starts at 1001 from its first frame."""
    best_run, best, legacy = None, None, None
    for frame in sorted(markers):
        custom = (markers[frame] or {}).get("customData") or ""
        if not isinstance(custom, str):
            continue
        try:
            if custom.startswith(UPDATE_MARKER_PREFIX):
                data = json.loads(custom[len(UPDATE_MARKER_PREFIX):])
                if not isinstance(data, dict) or "rs" not in data:
                    continue
                run = data.get("run") if isinstance(data.get("run"), int) else -1
                if best_run is None or run >= best_run:
                    best_run, best = run, (int(data["rs"]), int(data["rf"]))
            elif custom.startswith(START_MARKER_PREFIX) and legacy is None:
                data = json.loads(custom[len(START_MARKER_PREFIX):])
                legacy = (int(data["src"]), int(data["start"]))
        except (ValueError, TypeError, KeyError):
            continue
    return best or legacy


def start_frame_for(first_source_frame: int, reference: Optional[tuple]) -> int:
    """The frame to render a segment from, given its first source frame now.

    The reference source frame keeps its number, so 10 more frames at the
    head give 1001 - 10 = 991; with no reference the segment starts at 1001.
    """
    if reference is None:
        return FIRST_START_FRAME
    reference_source, reference_start = reference
    return reference_start - (reference_source - int(first_source_frame))


def start_marker_text(start_frame: int, was: Optional[int] = None) -> tuple:
    """(name, note) of a start frame marker."""
    name = f"Start frame {start_frame}"
    note = f"{START_NOTE_LEAD} {start_frame}."
    if was is not None and was != start_frame:
        note += (f" It was {was}: {was - start_frame} frame(s) were added at the "
                 f"head, so frames keyed against {was} have not moved.")
    return name, note


def parse_shot_pattern(pattern: str) -> Optional[tuple]:
    """(prefix, digits) from a pattern like 'sh###', or None without a '#'."""
    pattern = (pattern or "").strip()
    if "#" not in pattern:
        return None
    prefix = pattern[:pattern.index("#")]
    rest = pattern[len(prefix):]
    digits = len(rest) - len(rest.lstrip("#"))
    return prefix, digits


def shot_number_in(name: str, prefix: str, digits: int) -> Optional[int]:
    """The number in a shot name made from the pattern ('sh040' or
    'sh040_A001C003' -> 40), or None when the name isn't one."""
    name = name or ""
    if not name.startswith(prefix):
        return None
    rest = name[len(prefix):]
    number = ""
    for char in rest:
        if not char.isdigit():
            break
        number += char
    if len(number) < max(1, digits):
        return None
    tail = rest[len(number):]
    if tail and not tail.startswith("_"):
        return None
    return int(number)


def format_shot_name(prefix: str, digits: int, number: int,
                     source_name: str = "") -> str:
    """'sh010', or 'sh010_A001C003' with a source name."""
    base = f"{prefix}{number:0{digits}d}"
    return f"{base}_{source_name}" if source_name else base


def group_stacks(entries: list) -> list:
    """Shots on a timeline: entries are (start, end exclusive, track, payload);
    clips that overlap in time on any tracks are one shot. Returns the shots
    in timeline order, each a list of entries sorted by track then start."""
    shots, current, current_end = [], [], None
    for entry in sorted(entries, key=lambda e: (e[0], e[2])):
        if current and entry[0] < current_end:
            current.append(entry)
            current_end = max(current_end, entry[1])
        else:
            if current:
                shots.append(current)
            current, current_end = [entry], entry[1]
    if current:
        shots.append(current)
    for shot in shots:
        shot.sort(key=lambda e: (e[2], e[0]))
    return shots


def plan_shot_numbers(shots_existing: list, start: int, increment: int,
                      keep_names: bool) -> list:
    """Number for each shot. shots_existing[i] is the number already in shot
    i's names (None if it has none). Kept numbers stay; the others continue
    after the highest number used (or from `start`), going up by
    `increment`."""
    increment = max(1, increment)
    if keep_names:
        used = [n for n in shots_existing if n is not None]
        next_number = max(start, max(used) + increment) if used else start
    else:
        next_number = start
    numbers = []
    for existing in shots_existing:
        if keep_names and existing is not None:
            numbers.append(existing)
        else:
            numbers.append(next_number)
            next_number += increment
    return numbers


def add_source_line(comments: str, file_name: str) -> Optional[str]:
    """Comments with 'Source: <file>' added below what is there, or None when
    it is already there (or there is no file name)."""
    if not file_name:
        return None
    line = f"Source: {file_name}"
    comments = comments or ""
    if line in comments:
        return None
    return line if not comments.strip() else f"{comments}\n{line}"


# ---------------------------------------------------------------------------
# Clip Identity
# ---------------------------------------------------------------------------

def is_still_image(clip_type, file_path) -> bool:
    """True for a single still image, from a clip's Type and File Path properties."""
    if "still" in str(clip_type or "").lower():
        return True
    path = str(file_path or "")
    if not path or "[" in path:
        return False
    return os.path.splitext(path)[1].lower() in STILL_EXTENSIONS


def is_still_item(media_pool_item) -> bool:
    """True when a MediaPoolItem is a single still image (see is_still_image)."""
    try:
        return is_still_image(media_pool_item.GetClipProperty("Type"),
                              media_pool_item.GetClipProperty("File Path"))
    except Exception:
        return False


def exact_source_range(item) -> Optional[tuple]:
    """(first, last) source frames a 100%-speed timeline item really uses, or None.

    Measured on 21.1.2: GetSourceStartFrame/GetSourceEndFrame report some
    plain cuts one frame wider at one or both ends (C012 reads 212-252 for a
    39-frame shot whose frames are 213-251), while GetLeftOffset() plus the
    duration matches the FCP XML <in>/<out> on every clip. On a retimed clip
    the offset is in curve time, not source frames, so those return None and
    keep the old reading.
    """
    try:
        speed = item.GetSpeed()  # Resolve 21+
        speed = speed.get("Percentage") if isinstance(speed, dict) else speed
        if speed is None or abs(float(speed) - 100.0) > 0.01:
            return None
        first = int(item.GetLeftOffset())
        duration = int(item.GetDuration() or 0)
    except Exception:
        return None
    if first < 0 or duration <= 1:  # a still or a one-frame hold: keep the old reading
        return None
    return first, first + duration - 1


def clip_identity_key(media_pool_item, merge_by_source_file: bool) -> Optional[str]:
    """Bucket identity for a MediaPoolItem.

    - merge_by_source_file=True: key by File Path so two MediaPoolItems pointing
      at the same source file (the dual-import scenario from round-tripped
      conform timelines) land in the same bucket and get merged. Falls back to
      the MediaId when File Path is empty.
    - merge_by_source_file=False: key by MediaId (legacy behaviour).

    Returns None when neither is available; the caller skips the clip.

    Both the collection pass and the update pass's timeline scan go through this
    so a clip already on an All Clips timeline is recognised as the same shot the
    collector just produced. The track never enters the identity: a source used
    on different tracks is still one shot.
    """
    media_id = None
    try:
        media_id = media_pool_item.GetMediaId()
    except Exception:
        media_id = None

    if merge_by_source_file:
        try:
            file_path = media_pool_item.GetClipProperty("File Path") or ""
        except Exception:
            file_path = ""
        if file_path:
            return f"FP:{file_path}"

    return media_id or None


# ---------------------------------------------------------------------------
# Duplicate Detection & Marking
# ---------------------------------------------------------------------------

def find_duplicate_groups(all_clip_infos: list[ClipInfo]) -> int:
    """Identify duplicate ClipInfo groups (same media pool item, 2+ entries
    after merging) and stamp duplicate_set_index / duplicate_position /
    duplicate_set_size onto each member. Returns the number of duplicate sets.
    """
    by_mid: dict[str, list[ClipInfo]] = {}
    for ci in all_clip_infos:
        try:
            mid = ci.media_pool_item.GetMediaId()
        except Exception:
            mid = None
        if not mid:
            continue
        by_mid.setdefault(mid, []).append(ci)

    set_index = 0
    for group in by_mid.values():
        if len(group) < 2:
            continue
        group.sort(key=lambda c: (c.timeline_inpoint, c.source_track_index))
        size = len(group)
        for position, ci in enumerate(group):
            ci.duplicate_set_index = set_index
            ci.duplicate_position = position
            ci.duplicate_set_size = size
        set_index += 1

    return set_index


def get_all_timeline_clips(timeline) -> list[TimelineClipData]:
    """Extract all video clips from all tracks of a timeline."""
    clip_list = []
    if not timeline:
        return clip_list

    tracks_count = timeline.GetTrackCount("video")
    print(f"Found {tracks_count} video tracks")

    for track_index in range(1, tracks_count + 1):
        clips = timeline.GetItemListInTrack("video", track_index)
        if not clips:
            print(f"No clips found in track {track_index}")
            continue

        print(f"Track {track_index}: Found {len(clips)} clips")
        for clip_index, clip in enumerate(clips):
            try:
                media_pool_item = clip.GetMediaPoolItem()
            except Exception:
                media_pool_item = None

            if media_pool_item:
                file_path = media_pool_item.GetClipProperty("File Path") or "N/A"
                clip_name = clip.GetName()
                print(f"Clip {clip_index + 1} on track {track_index}: {clip_name}")
                print(f"  File Path: {file_path}")
                clip_list.append(TimelineClipData(
                    clip=clip,
                    media_pool_item=media_pool_item,
                    start_frame=clip.GetStart(),
                    name=clip_name,
                    track_index=track_index,
                ))
            else:
                print(f"Clip {clip_index + 1} on track {track_index} has no media pool item")

    print(f"Total clips found: {len(clip_list)}")
    return clip_list


# ---------------------------------------------------------------------------
# Retime Detection
# ---------------------------------------------------------------------------

def check_retime_properties(clip: TimelineClipData) -> tuple[bool, Optional[float], bool]:
    """Check clip properties for retime indicators.

    Returns: (is_retimed, retime_percentage, is_non_linear)

    DEAD ON 21.0.4.5, and probably on every build. GetClipProperty is a
    MediaPoolItem method; TimelineItem does not have it, and the scripting
    bridge resolves the unknown attribute to None, so every call below raises
    "'NoneType' object is not callable" and is swallowed by its own except.
    Measured on 21.0.4.5: TimelineItem exposes GetProperty/SetProperty instead
    (GetProperty("ZoomX") -> 0.5), and GetProperty("Speed") returns None — the
    retime speed is not on that surface either.

    So is_clip_retimed()'s duration comparison is in practice the only thing
    that detects a linear retime, and the XML pass the only thing that detects a
    speed ramp: the "Retime Curve" branch here has never fired. Left in place
    rather than deleted because it is harmless and a future build may add the
    method, but do not read it as working detection.
    """
    # Check Speed property
    speed = None
    try:
        speed = float(clip.clip.GetClipProperty("Speed"))
    except (ValueError, TypeError, Exception):
        pass

    if speed is not None and speed != 100.0:
        print(f"Detected retimed clip via property: {clip.name} with speed: {speed}%")
        return (True, speed, False)

    # Check for non-linear retime (speed curve/ramp)
    retime_curve = None
    try:
        retime_curve = clip.clip.GetClipProperty("Retime Curve")
    except Exception:
        pass
    if retime_curve and retime_curve != "" and retime_curve != "None":
        print(f"Detected non-linear retimed clip via Retime Curve: {clip.name} ({retime_curve})")
        return (True, None, True)

    # Check other retiming attributes
    for attr in ("Retime Process", "Motion Estimation", "Frame Interpolation"):
        value = None
        try:
            value = clip.clip.GetClipProperty(attr)
        except Exception:
            pass
        if value and value != "" and value != "None":
            print(f"Detected retimed clip via property: {clip.name} with {attr}: {value}")
            return (True, None, False)

    return (False, None, False)


def is_clip_retimed(clip: TimelineClipData) -> tuple[bool, Optional[float], bool]:
    """Comprehensive retime detection: duration comparison + property check.

    Returns: (is_retimed, retime_percentage, is_non_linear)
    """
    if not clip or not clip.clip:
        print("Warning: Invalid clip object in is_clip_retimed")
        return (False, None, False)

    # Safely get durations
    try:
        timeline_duration = clip.clip.GetEnd() - clip.clip.GetStart()
        source_duration = clip.clip.GetSourceEndFrame() - clip.clip.GetSourceStartFrame()
    except Exception:
        print(f"Warning: Could not calculate durations for clip: {clip.name}")
        return check_retime_properties(clip)

    # Guard against division by zero (frame holds have sourceDuration of 0 or 1)
    if source_duration <= 0:
        print(f"Warning: Source duration is {source_duration} for clip: {clip.name} (likely frame hold)")
        return (True, 0.0, False)
    if timeline_duration <= 0:
        print(f"Warning: Timeline duration is {timeline_duration} for clip: {clip.name}")
        return check_retime_properties(clip)

    # Calculate differences. Speed is source frames over timeline frames, which
    # is the convention Resolve's own "Speed" clip property uses and therefore
    # what check_retime_properties() returns from the other detection path: a
    # clip at 50% occupies twice as many timeline frames as it has source
    # frames. Dividing the other way round reported that clip as 200%.
    frame_diff = abs(timeline_duration - source_duration)
    retime_percentage = (source_duration / timeline_duration) * 100
    percent_diff = abs(retime_percentage - 100)

    if frame_diff > MIN_FRAME_DIFF and percent_diff > MIN_PERCENT_DIFF:
        print(f"Detected retimed clip: {clip.name} with speed: {retime_percentage:.1f}%")
        return (True, retime_percentage, False)

    # Fall back to property checks
    return check_retime_properties(clip)


# ---------------------------------------------------------------------------
# API Helper
# ---------------------------------------------------------------------------

def sanitize_for_api(clip_info: ClipInfo) -> dict:
    """Create a clean dict with only API-recognized fields for AppendToTimeline.

    AppendToTimeline's endFrame is EXCLUSIVE: requesting endFrame=E places source
    frames start..E-1. ClipInfo ranges are inclusive (they come from a source
    clip's GetSourceStartFrame/GetSourceEndFrame, where the last frame is
    included), so the request has to be end + 1.

    Measured on 21.0.4.5 against a 158-frame clip:

        bare append, whole clip          duration 158   (ground truth)
        startFrame=0, endFrame=157       duration 157   one frame short
        startFrame=0, endFrame=158       duration 158   correct
        startFrame=10, endFrame=19       duration 9     covers 10..18
        startFrame=10, endFrame=10       REFUSED        zero-length

    Without the +1 every generated clip lost the last frame of its range, and a
    frame hold - where start == end - asked for a zero-length clip, which Resolve
    refuses outright, so freeze frames silently never appeared on the timeline.
    """
    return {
        "mediaPoolItem": clip_info.media_pool_item,
        "startFrame": clip_info.start_frame,
        "endFrame": clip_info.end_frame + 1,
    }


# ---------------------------------------------------------------------------
# Timeline Resolution
# ---------------------------------------------------------------------------

def get_timeline_for_media_pool_item(media_pool_item):
    """Return the Timeline a timeline-type MediaPoolItem points at, or None.

    MediaPoolItem.GetTimeline() arrived in DaVinci Resolve 21.0.4 and resolves the
    item exactly, with no dependence on timeline names being unique. Older builds
    resolve the unknown attribute to None instead of raising AttributeError, so
    probe with getattr + callable() and let the caller fall back to a name lookup.

    The 21.0.4 docs label the return type "TimelineItem" while the prose says
    "timeline object". Verified on 21.0.4.5: it is a real Timeline — GetTrackCount
    and GetItemListInTrack work, GetLeftOffset and GetSourceStartFrame are absent.
    The duck-type check keeps that verification honest: anything that does not
    behave like a Timeline falls through to the name lookup, so a future API
    surprise degrades to the old behaviour instead of crashing.
    """
    getter = getattr(media_pool_item, "GetTimeline", None)
    if not callable(getter):
        return None
    try:
        timeline = getter()
    except Exception:
        return None
    if timeline is None:
        return None
    if not callable(getattr(timeline, "GetTrackCount", None)):
        return None
    return timeline


# ---------------------------------------------------------------------------
# Update Manifest
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    """Current UTC time as 2026-08-06T12:22:33Z — the manifest's machine clock."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_settings_record(*, connection_threshold, merge_by_source_file,
                          video_only, use_xml_retime,
                          import_clip_names, mark_duplicates,
                          mark_retimed_clips,
                          preserve_track_layout=False, handles=0) -> dict:
    """The generation settings a manifest records.

    One shape for both workflows: create stamps what it built with, update
    compares against it and warns about the ones that reshape merged ranges.
    They have to agree key for key or every first update would report settings
    that "changed" only because the two lists were written separately.
    """
    return {
        "connection_threshold": connection_threshold,
        "merge_by_source_file": merge_by_source_file,
        "video_only": video_only,
        "use_xml_retime": use_xml_retime,
        "import_clip_names": import_clip_names,
        "mark_duplicates": mark_duplicates,
        "mark_retimed_clips": mark_retimed_clips,
        "preserve_track_layout": preserve_track_layout,
        "handles": handles,
    }


def build_manifest(timeline_uid, timeline_name, sources, settings, now_iso,
                   tool_version) -> dict:
    """A fresh manifest for an All Clips timeline.

    `sources` is [{"uid": ..., "name": ...}] for the timelines it was built from;
    the uid is exact and survives renames, the name is the only thing a human can
    act on once a uid stops resolving. `settings` is the generation settings that
    shaped the merged ranges — re-running with a different connection threshold
    reshapes nearly every clip, so the previous value has to be recoverable.
    """
    return {
        "schema": MANIFEST_SCHEMA,
        "tool": SCRIPT_TITLE,
        "tool_version": tool_version,
        "timeline_uid": timeline_uid or "",
        "timeline_name": timeline_name or "",
        "created_utc": now_iso,
        "last_run_utc": now_iso,
        "run_counter": 0,
        "adopted": False,
        "sources": list(sources or []),
        "settings": dict(settings or {}),
        "runs": [],
    }


def manifest_add_run(manifest: dict, run_record: dict,
                     max_runs: int = MANIFEST_MAX_RUNS) -> dict:
    """Append a run record, bump the counters, cap the history. Returns a copy."""
    updated = dict(manifest)
    runs = list(manifest.get("runs") or [])
    runs.append(dict(run_record))
    if max_runs >= 0:
        runs = runs[-max_runs:] if max_runs else []
    updated["runs"] = runs
    updated["run_counter"] = run_record.get("n", manifest.get("run_counter", 0) + 1)
    if run_record.get("utc"):
        updated["last_run_utc"] = run_record["utc"]
    return updated


def encode_manifest(manifest: dict) -> str:
    """Compact, key-sorted JSON so the same manifest always encodes identically."""
    return json.dumps(manifest, sort_keys=True, separators=(",", ":"))


def decode_manifest(text) -> Optional[dict]:
    """Parse a manifest payload, with or without the marker prefix.

    Returns None for anything unusable — absent, junk, not an object, or written
    by a schema this build does not understand. A newer schema is reported loudly
    rather than half-read, because acting on a manifest we only partly understand
    is how an update deletes the wrong clips.
    """
    if not text:
        return None
    if isinstance(text, dict):
        # GetThirdPartyMetadata can hand back {key: value} instead of the value.
        text = text.get(MANIFEST_KEY) or ""
    if not isinstance(text, str):
        return None
    payload = text.strip()
    if payload.startswith(MANIFEST_MARKER_PREFIX):
        payload = payload[len(MANIFEST_MARKER_PREFIX):]
    if not payload:
        return None
    try:
        data = json.loads(payload)
    except (ValueError, TypeError):
        return None
    if not isinstance(data, dict):
        return None
    schema = data.get("schema")
    if schema != MANIFEST_SCHEMA:
        if schema is not None:
            print(f"  NOTE: ignoring manifest with unsupported schema {schema!r} "
                  f"(this build understands {MANIFEST_SCHEMA}).")
        return None
    return data


def trim_manifest_for_marker(manifest: dict,
                             max_chars: int = MANIFEST_MARKER_MAX_CHARS) -> dict:
    """Drop the oldest run records until the encoded manifest fits `max_chars`.

    Never drops sources or settings — those are the parts that cannot be
    re-derived. If it still does not fit with no runs left, the manifest is
    returned as-is and the caller writes what it can.
    """
    trimmed = dict(manifest)
    runs = list(manifest.get("runs") or [])
    while runs and len(MANIFEST_MARKER_PREFIX) + len(
            encode_manifest({**trimmed, "runs": runs})) > max_chars:
        runs = runs[1:]
    trimmed["runs"] = runs
    return trimmed


def normalised_markers(obj) -> dict:
    """GetMarkers() as {int frame: info}. Resolve returns float keys (96.0)."""
    getter = getattr(obj, "GetMarkers", None)
    if not callable(getter):
        return {}
    try:
        raw = getter()
    except Exception:
        return {}
    if not raw:
        return {}
    markers = {}
    try:
        for frame, info in raw.items():
            try:
                markers[int(frame)] = info
            except (TypeError, ValueError):
                continue
    except AttributeError:
        return {}
    return markers


def first_free_frame(existing_frames, preferred: int,
                     lower: Optional[int] = None,
                     upper: Optional[int] = None) -> int:
    """First frame free of `existing_frames` at or after `preferred`.

    Falls back to searching backwards towards `lower` when the forward range is
    exhausted. Returns -1 when every frame in [lower, upper] is taken. Resolve
    permits only one marker per frame, so any code adding a marker near a
    fraction of a clip has to be able to step off a collision.
    """
    taken = {int(f) for f in existing_frames}
    if upper is None:
        upper = preferred + len(taken) + 1
    start = preferred if lower is None else max(preferred, lower)
    for frame in range(start, upper + 1):
        if frame not in taken:
            return frame
    if lower is not None:
        for frame in range(min(preferred, upper), lower - 1, -1):
            if frame not in taken:
                return frame
    return -1


def find_manifest_marker_frame(markers: dict) -> Optional[int]:
    """Frame of the manifest marker in a normalised markers dict, or None.

    Scans for the customData prefix rather than using GetMarkerByCustomData,
    which matches the whole string exactly and so cannot find a payload whose
    tail changes on every run.
    """
    for frame in sorted(markers):
        info = markers[frame] or {}
        custom = info.get("customData") or ""
        if isinstance(custom, str) and custom.startswith(MANIFEST_MARKER_PREFIX):
            return frame
    return None


def read_manifest(timeline) -> tuple:
    """Read the manifest off a timeline. Returns (manifest, source).

    source is "metadata", "marker" or "none". Both stores are written on every
    update; whichever answers first wins. Third-party metadata is the primary
    because it is invisible. It was verified to round-trip on a timeline's
    MediaPoolItem on 21.0.4.5 — which was not a given, since third-party metadata
    is a camera/sidecar concept and a timeline has no media file — but survival
    across a project save and reload has not been checked, and the visible marker
    is the badge that tells a human this timeline is managed. Keep both.
    """
    getter = getattr(timeline, "GetMediaPoolItem", None)
    if callable(getter):
        try:
            mpi = getter()
        except Exception:
            mpi = None
        if mpi is not None:
            reader = getattr(mpi, "GetThirdPartyMetadata", None)
            if callable(reader):
                try:
                    raw = reader(MANIFEST_KEY)
                except Exception:
                    raw = None
                manifest = decode_manifest(raw)
                if manifest is not None:
                    return manifest, "metadata"

    markers = normalised_markers(timeline)
    frame = find_manifest_marker_frame(markers)
    if frame is not None:
        manifest = decode_manifest((markers[frame] or {}).get("customData"))
        if manifest is not None:
            return manifest, "marker"

    return None, "none"


def write_manifest(timeline, manifest: dict) -> dict:
    """Write the manifest to both stores. Returns {"metadata": ok, "marker": ok}."""
    result = {"metadata": False, "marker": False}
    encoded = encode_manifest(manifest)

    getter = getattr(timeline, "GetMediaPoolItem", None)
    if callable(getter):
        try:
            mpi = getter()
        except Exception:
            mpi = None
        if mpi is not None:
            writer = getattr(mpi, "SetThirdPartyMetadata", None)
            if callable(writer):
                try:
                    result["metadata"] = bool(writer(MANIFEST_KEY, encoded))
                except Exception:
                    result["metadata"] = False

    markers = normalised_markers(timeline)
    existing = find_manifest_marker_frame(markers)
    if existing is not None:
        try:
            timeline.DeleteMarkerAtFrame(existing)
        except Exception:
            pass
        markers.pop(existing, None)

    trimmed = trim_manifest_for_marker(manifest)
    dropped = len(manifest.get("runs") or []) - len(trimmed.get("runs") or [])
    if dropped > 0:
        print(f"  NOTE: manifest marker trimmed by {dropped} old run record(s) "
              f"to stay under {MANIFEST_MARKER_MAX_CHARS} characters.")

    frame = existing if existing is not None else first_free_frame(markers, 0, lower=0)
    if frame < 0:
        print("  WARNING: no free frame for the manifest marker.")
        return result

    note = (f"Managed by {SCRIPT_TITLE}.\n"
            f"Run {manifest.get('run_counter', 0)} · "
            f"{manifest.get('last_run_utc', '')}\n"
            f"Sources: "
            + ", ".join(s.get("name", "?") for s in manifest.get("sources") or []))
    try:
        result["marker"] = bool(timeline.AddMarker(
            frame, MANIFEST_MARKER_COLOR, MANIFEST_MARKER_NAME, note, 1,
            MANIFEST_MARKER_PREFIX + encode_manifest(trimmed),
        ))
    except Exception:
        result["marker"] = False

    if not result["metadata"] and not result["marker"]:
        print("  WARNING: could not persist the manifest — this timeline will "
              "not be recognised as a Master Sources timeline on the next run.")
    return result


# ---------------------------------------------------------------------------
# Source Timeline Resolution
# ---------------------------------------------------------------------------

def resolve_source_timelines(media_pool, selection_method: str,
                             project_timelines: dict, progress_cb=None) -> list:
    """Resolve the user's Media Pool selection into [(name, Timeline), ...].

    Non-timeline items are reported and skipped. Returns an empty list when
    nothing usable was selected — the caller decides what to say about that.
    """

    def _p(stage: str, current: int = 0, total: int = 0) -> None:
        if progress_cb is not None:
            progress_cb(stage, current, total)

    # Get selected clips
    selected_clips = []
    if selection_method == "Current Bin":
        selected_bin = media_pool.GetCurrentFolder()
        if selected_bin:
            bin_clips = selected_bin.GetClipList()
            if bin_clips:
                selected_clips = bin_clips
    elif selection_method == "Current Selection":
        sel_clips = media_pool.GetSelectedClips()
        if sel_clips:
            selected_clips = sel_clips
    else:
        print("Unknown selection method.")
        return []

    if not selected_clips:
        print("No approved edits found: select them in the Media Pool, or open the "
              "bin that holds them.")
        return []

    print("Processing selected clips...")

    resolved = []
    total_selected = len(selected_clips)
    _p("Resolving timelines...", 0, total_selected)

    for sel_idx, media_pool_item in enumerate(selected_clips, start=1):
        if media_pool_item is None:
            continue

        # Check if it's a timeline
        clip_type = ""
        try:
            clip_type = media_pool_item.GetClipProperty("Type")
        except Exception:
            pass

        if clip_type != "Timeline":
            print(f"Skipping '{media_pool_item.GetName()}': not a timeline.")
            _p(f"Skipping non-timeline item ({sel_idx}/{total_selected})",
               sel_idx, total_selected)
            continue

        timeline_name = media_pool_item.GetName()
        _p(f"Resolving: {timeline_name} ({sel_idx}/{total_selected})",
           sel_idx, total_selected)

        # Ask the item for its own timeline (Resolve 21.0.4+). The name lookup
        # silently picks the wrong timeline when two timelines in the project share
        # a name, which Resolve permits across different bins.
        curr_timeline = get_timeline_for_media_pool_item(media_pool_item)
        if curr_timeline is None:
            curr_timeline = project_timelines.get(timeline_name)
        if not curr_timeline:
            print(f"Timeline not found in project: {timeline_name}")
            continue

        resolved.append((timeline_name, curr_timeline))

    return resolved


# ---------------------------------------------------------------------------
# Clip Collection
# ---------------------------------------------------------------------------

def video_track_states(project, timeline) -> list:
    """[enabled?] for each video track of `timeline`, index 0 = track 1.

    Measured on 21.1.2: GetIsTrackEnabled answers False for every track of a
    timeline that is not the current one, so the timeline is made current to
    ask. The caller puts the user's own timeline back afterwards.
    """
    count = timeline.GetTrackCount("video") or 0
    if project is not None:
        try:
            current = project.GetCurrentTimeline()
            if current is None or current.GetUniqueId() != timeline.GetUniqueId():
                project.SetCurrentTimeline(timeline)
        except Exception:
            pass
    states = []
    for index in range(1, count + 1):
        try:
            states.append(timeline.GetIsTrackEnabled("video", index) is not False)
        except Exception:
            states.append(True)
    return states


def collect_desired_clips(
    source_timelines: list,
    *,
    connection_threshold: int,
    mark_duplicates: bool,
    mark_retimed_clips: bool,
    use_xml_retime: bool,
    import_clip_names: bool,
    merge_by_source_file: bool,
    sorting_method: str,
    handles: int = 0,
    progress_cb=None,
) -> tuple:
    """Walk the source timelines and produce the desired clip set.

    Returns (all_clip_infos, timeline_block_markers, duplicate_set_count).

    This is the whole "what belongs on the output timeline" computation: track
    walk, retime and XML analysis, identity bucketing, overlap merging, the
    optional per-source-timeline layout, duplicate stamping and sorting. The
    create and update workflows both run it and differ only in what they do with
    the result.
    """

    def _p(stage: str, current: int = 0, total: int = 0) -> None:
        if progress_cb is not None:
            progress_cb(stage, current, total)

    # Collect clips from all selected timelines
    clips: dict[str, list[ClipInfo]] = {}
    total_selected = len(source_timelines)
    _p("Reading clips...", 0, total_selected)

    # Reading track states opens each approved edit in turn; reopen the user's.
    try:
        project = resolve.GetProjectManager().GetCurrentProject()  # noqa: F821
        users_timeline = project.GetCurrentTimeline() if project else None
    except Exception:
        project, users_timeline = None, None
    track_states = {}
    for timeline_name, curr_timeline in source_timelines:
        track_states[timeline_name] = video_track_states(project, curr_timeline)
    if project is not None and users_timeline is not None:
        try:
            project.SetCurrentTimeline(users_timeline)
        except Exception:
            pass

    for sel_idx, (timeline_name, curr_timeline) in enumerate(source_timelines, start=1):
        print(f"Reading approved edit: {timeline_name}")
        _p(f"Reading: {timeline_name} ({sel_idx}/{total_selected})",
           sel_idx, total_selected)

        # XML retime analysis for this timeline
        xml_lookup = {}
        xml_temp_path = None
        if use_xml_retime:
            xml_temp_path = export_timeline_to_xml(curr_timeline)
            if xml_temp_path:
                xml_lookup = build_xml_clip_lookup(xml_temp_path)
                print(f"  XML lookup built with {len(xml_lookup)} clip entries")

        # Walk video tracks
        num_tracks = curr_timeline.GetTrackCount("video")
        for track_idx in range(1, num_tracks + 1):
            # A disabled track is not part of the cut, so nothing on it is pulled.
            states = track_states.get(timeline_name) or []
            track_enabled = states[track_idx - 1] if track_idx <= len(states) else True
            if not track_enabled:
                print(f"Skipping disabled video track {track_idx}")
                continue
            track_items = curr_timeline.GetItemListInTrack("video", track_idx)
            if not track_items:
                print(f"No items in track {track_idx}")
                continue

            # Transitions (dissolves, wipes) are items with no media of their
            # own. Items on one track never overlap, so one that crosses a
            # clip's edge is a transition into or out of that clip.
            transitions = []
            for other in track_items:
                try:
                    if other is not None and other.GetMediaPoolItem() is None:
                        transitions.append((int(other.GetStart()), int(other.GetEnd())))
                except Exception:
                    pass

            for item_index, track_item in enumerate(track_items):
                if track_item is None:
                    print(f"Track item #{item_index + 1} is nil")
                    continue

                # Get name
                item_name = "Unknown"
                try:
                    item_name = track_item.GetName()
                except Exception:
                    pass
                print(f"Processing item #{item_index + 1}: {item_name}")

                # Check enabled state
                is_enabled = True
                try:
                    is_enabled = track_item.GetClipEnabled()
                except Exception:
                    pass

                if not is_enabled:
                    print(f"  Skipping disabled clip: {item_name}")
                    continue

                # Get media pool item and media ID
                try:
                    media_item = track_item.GetMediaPoolItem()
                except Exception:
                    media_item = None
                if not media_item:
                    print(f"  Could not retrieve media item for clip: {item_name}")
                    continue

                try:
                    media_id = media_item.GetMediaId()
                except Exception:
                    media_id = None
                if not media_id:
                    print(f"  Could not retrieve media ID for clip: {item_name}")
                    continue

                # Get raw source frames
                try:
                    raw_start = track_item.GetSourceStartFrame()
                    raw_end = track_item.GetSourceEndFrame()
                except Exception:
                    print(f"  Could not retrieve frame range for clip: {item_name}")
                    continue

                if raw_start is None or raw_end is None:
                    print(f"  Could not retrieve frame range for clip: {item_name}")
                    continue

                exact = exact_source_range(track_item) if raw_start <= raw_end else None
                if exact and exact != (raw_start, raw_end):
                    print(f"  Exact source range {exact[0]}-{exact[1]} "
                          f"(Resolve reported {raw_start}-{raw_end})")
                    raw_start, raw_end = exact

                # Detect frame hold
                raw_source_duration = abs(raw_end - raw_start)
                is_frame_hold = raw_source_duration <= 1

                if is_frame_hold:
                    print(f"  FOUND FRAME HOLD CLIP: {item_name}")
                    print(f"  Source frames (raw): {raw_start} to {raw_end}")

                # Detect reversed
                is_reversed = raw_start > raw_end

                if is_reversed:
                    print(f"  FOUND REVERSED CLIP: {item_name}")
                    print(f"  Source frames (raw): {raw_start} to {raw_end}")

                # Normalize: always start <= end
                norm_start = min(raw_start, raw_end)
                norm_end = max(raw_start, raw_end)

                # GetSourceEndFrame() on a source clip is the inclusive last
                # frame, so norm_end is inclusive and passes through unchanged.
                # AppendToTimeline.endFrame is EXCLUSIVE, which is not the same
                # convention — sanitize_for_api() does that conversion, once, at
                # the point of the API call. (is_frame_hold is still used
                # downstream for marker text.)

                # Capture the raw API-reported range BEFORE any XML expansion
                # or merging — used by the Range Audit at the end of the run.
                api_source_start = norm_start
                api_source_end = norm_end

                # Retime detection
                is_retimed = False
                is_non_linear = False
                retime_pct = None
                xml_min = None
                xml_max = None

                if is_frame_hold:
                    is_retimed = True
                    retime_pct = 0.0
                    print(f"  Frame hold marked as retimed (0% speed)")
                elif mark_retimed_clips:
                    temp_clip = TimelineClipData(
                        clip=track_item,
                        media_pool_item=media_item,
                        name=item_name,
                        start_frame=track_item.GetStart(),
                        track_index=track_idx,
                    )
                    is_retimed, retime_pct, is_non_linear = is_clip_retimed(temp_clip)
                    if is_retimed:
                        print(f"  FOUND RETIMED CLIP: {item_name}")
                        if retime_pct is not None:
                            print(f"  Speed: {retime_pct}%")
                        if is_non_linear:
                            print(f"  Non-linear retime (speed curve) detected")

                # XML override if available
                if use_xml_retime and xml_lookup:
                    xml_data = match_xml_retime_to_clip(
                        [item_name, media_item.GetName() or ""],
                        norm_start, norm_end, xml_lookup,
                    )
                    if xml_data:
                        xml_min = xml_data["source_min"]
                        xml_max = xml_data["source_max"]
                        is_non_lin = xml_data["is_non_linear"]
                        print(f"  XML matched: keyframe range {xml_min}-{xml_max}, "
                              f"non_linear={is_non_lin}")
                        if is_non_lin:
                            is_non_linear = True
                            is_retimed = True
                        # Union with the API range, for every clip the XML
                        # matched rather than only the ones that read as
                        # non-linear. The range is now scoped to this instance's
                        # own window into the curve, so it agrees with the API
                        # to within a frame or two on an ordinary retime and
                        # only widens where the curve genuinely reaches further.
                        #
                        # Widening is the safe direction: surplus frames are
                        # handle, missing frames break a pull. Gating this on
                        # is_non_linear meant a ramp Resolve exports with two
                        # keyframes -- most of them -- was never checked at all.
                        if not is_frame_hold:
                            proposed_start = min(norm_start, xml_min)
                            proposed_end = max(norm_end, xml_max)
                            old_duration = max(1, norm_end - norm_start + 1)
                            new_duration = max(1, proposed_end - proposed_start + 1)
                            # Measure growth against the shot's length in the
                            # edit as well: a shot that goes forward and back
                            # reports only its net move (6 frames for a 60-frame
                            # shot), so the true range looks like huge growth.
                            try:
                                edit_frames = int(track_item.GetDuration() or 0)
                            except Exception:
                                edit_frames = 0
                            growth = new_duration / max(old_duration, edit_frames)
                            if (proposed_start, proposed_end) == (norm_start, norm_end):
                                pass  # XML didn't actually expand
                            elif growth > XML_EXPANSION_MAX_GROWTH:
                                print(f"  XML EXPANSION SKIPPED: would grow "
                                      f"{old_duration}f -> {new_duration}f "
                                      f"({growth:.1f}x, cap is "
                                      f"{XML_EXPANSION_MAX_GROWTH:.0f}x). "
                                      f"Keeping API range {norm_start}-{norm_end}.")
                            else:
                                added = new_duration - old_duration
                                print(f"  XML EXPANDED range: "
                                      f"{norm_start}-{norm_end} ({old_duration}f) -> "
                                      f"{proposed_start}-{proposed_end} "
                                      f"({new_duration}f, +{added}f, {growth:.2f}x)")
                                norm_start = proposed_start
                                norm_end = proposed_end

                # Transitions: add the source frames a dissolve uses beyond the
                # cut, converted to source frames at the clip's speed (at least
                # 1:1 on a speed ramp, whose speed at the cut is unknown).
                if transitions and not is_frame_hold:
                    try:
                        head_tl, tail_tl = transition_overlap(
                            int(track_item.GetStart()), int(track_item.GetEnd()),
                            transitions)
                    except Exception:
                        head_tl = tail_tl = 0
                    if head_tl or tail_tl:
                        factor = 1.0
                        speed = retime_pct
                        try:
                            got = track_item.GetSpeed()  # Resolve 21+
                            got = got.get("Percentage") if isinstance(got, dict) else got
                            if got is not None:
                                speed = float(got)
                        except Exception:
                            pass
                        if speed:
                            factor = abs(float(speed)) / 100.0
                        if is_non_linear:
                            factor = max(factor, 1.0)
                        head_src = int(math.ceil(head_tl * factor))
                        tail_src = int(math.ceil(tail_tl * factor))
                        if is_reversed:  # the edit's head is the source's end
                            head_src, tail_src = tail_src, head_src
                        try:
                            last = int(media_item.GetClipProperty("Frames") or 0) - 1
                        except (TypeError, ValueError, Exception):
                            last = 0
                        new_start = max(0, norm_start - head_src)
                        new_end = norm_end + tail_src
                        if last > 0:
                            new_end = min(new_end, max(norm_end, last))
                        print(f"  Transition: {head_tl}f before / {tail_tl}f after "
                              f"the cut -> source {norm_start}-{norm_end} becomes "
                              f"{new_start}-{new_end}")
                        norm_start, norm_end = new_start, new_end

                # The clip's name on the edit timeline, copied onto the master
                source_clip_name: Optional[str] = None
                if import_clip_names:
                    try:
                        source_clip_name = track_item.GetName()
                    except Exception:
                        pass

                # Get timeline endpoint for layout post-processing
                try:
                    track_item_endpoint = track_item.GetEnd()
                except Exception:
                    track_item_endpoint = track_item.GetStart() + 1

                # Create ClipInfo
                clip_info = ClipInfo(
                    media_pool_item=media_item,
                    start_frame=norm_start,
                    end_frame=norm_end,
                    timeline_inpoint=track_item.GetStart(),
                    timeline_endpoint=track_item_endpoint,
                    source_track_index=track_idx,
                    source_timeline_name=timeline_name,
                    is_reversed=is_reversed,
                    is_retimed=is_retimed,
                    is_frame_hold=is_frame_hold,
                    is_non_linear_retime=is_non_linear,
                    retime_percentage=retime_pct,
                    xml_source_min=xml_min,
                    xml_source_max=xml_max,
                    source_name=source_clip_name,
                    api_source_start=api_source_start,
                    api_source_end=api_source_end,
                    uses=[(timeline_name, track_idx, int(track_item.GetStart()),
                           int(track_item_endpoint))],
                )
                # Bucket key: see clip_identity_key(). Uses on different tracks
                # share a bucket; the merged segment keeps the lowest track.
                clips_key = clip_identity_key(media_item, merge_by_source_file) or media_id
                clips.setdefault(clips_key, []).append(clip_info)
                print(f"  Added clip to processing list: {item_name} "
                      f"(Start: {norm_start}, End: {norm_end}, Track: {track_idx})")

        # Clean up XML temp file
        if xml_temp_path:
            try:
                os.unlink(xml_temp_path)
                print(f"  Cleaned up temp XML: {xml_temp_path}")
            except OSError:
                pass

    if not clips:
        print("No valid clips found to process.")
        return [], [], 0

    # Cross-bucket scan: files appearing under multiple bucket keys. With
    # merge-by-file-path ON this should be empty (or only flag clips with
    # missing File Path); with it OFF this is the classic "two MediaPoolItems,
    # one source file" warning that explains unmerged subset/superset clips.
    path_to_buckets: dict[str, list[tuple[str, ClipInfo]]] = {}
    for bucket_key, bucket_clips in clips.items():
        for ci in bucket_clips:
            try:
                fp = ci.media_pool_item.GetClipProperty("File Path") or ""
            except Exception:
                fp = ""
            if not fp:
                continue
            path_to_buckets.setdefault(fp, []).append((bucket_key, ci))

    cross_bucket = []
    for fp, entries in path_to_buckets.items():
        distinct_keys = {bk for bk, _ in entries}
        if len(distinct_keys) > 1:
            cross_bucket.append((fp, entries, distinct_keys))

    if cross_bucket and not merge_by_source_file:
        print("")
        print(f"=== Pre-Merge Warning: {len(cross_bucket)} source file(s) "
              f"appear under multiple MediaPoolItems ===")
        print("(These won't merge across buckets — different MediaIds, often "
              "sub-clip vs full clip or the same file imported twice. Enable "
              "'Merge clips by source file path' to merge them.)")
        for fp, entries, distinct_keys in cross_bucket:
            print(f"  File: {fp}")
            print(f"  -> {len(distinct_keys)} distinct bucket(s):")
            for bk, ci in entries:
                try:
                    mid = ci.media_pool_item.GetMediaId() or "?"
                except Exception:
                    mid = "?"
                print(f"       bucket='{bk}'  MediaPoolItem='{ci.media_pool_item.GetName()}'  "
                      f"MediaId={mid}  range={ci.start_frame}-{ci.end_frame}  "
                      f"(from '{ci.source_timeline_name}')")
        print("")
    elif cross_bucket and merge_by_source_file:
        # Should be rare — only files with missing File Path can land here.
        print(f"NOTE: {len(cross_bucket)} file(s) still in multiple buckets despite "
              f"merge-by-file-path being on (likely missing File Path).")

    # Canonicalize MediaPoolItem per bucket: when merge-by-file-path is on, a
    # single bucket may contain clips from multiple MediaPoolItems pointing at
    # the same file. Pick the one with the widest source range (most Frames)
    # as the canonical item for the merged ClipInfo so AppendToTimeline can
    # place the merged range without hitting sub-clip range restrictions.
    if merge_by_source_file:
        def _item_frames(item) -> int:
            try:
                val = item.GetClipProperty("Frames")
                return int(val) if val else 0
            except (ValueError, TypeError, Exception):
                return 0

        canonicalized_buckets = 0
        for bucket_key, bucket_clips in clips.items():
            distinct_items: dict = {}
            for ci in bucket_clips:
                try:
                    mid = ci.media_pool_item.GetMediaId() or ""
                except Exception:
                    mid = ""
                if mid and mid not in distinct_items:
                    distinct_items[mid] = ci.media_pool_item
            if len(distinct_items) <= 1:
                continue
            canonical = max(distinct_items.values(), key=_item_frames)
            canonical_name = canonical.GetName()
            canonical_frames = _item_frames(canonical)
            try:
                canonical_path = canonical.GetClipProperty("File Path") or ""
            except Exception:
                canonical_path = ""
            print(f"INFO: Merging {len(distinct_items)} MediaPoolItems for "
                  f"'{canonical_path or canonical_name}'. Canonical: "
                  f"{canonical_name} ({canonical_frames}f)")
            for ci in bucket_clips:
                ci.media_pool_item = canonical
            canonicalized_buckets += 1
        if canonicalized_buckets:
            print(f"=== File-Path Merge: canonicalized {canonicalized_buckets} "
                  f"bucket(s) across multiple MediaPoolItems ===")
            print("")

    # Handles: widen every use by the same number of source frames each side,
    # before merging, so handles that overlap or come close join into one
    # segment instead of exporting the same frames twice. The API range is
    # widened too, so the Range Audit still only reports XML growth.
    if handles > 0:
        media_lengths: dict = {}
        for bucket_clips in clips.values():
            for ci in bucket_clips:
                item = ci.media_pool_item
                if id(item) not in media_lengths:
                    try:
                        media_lengths[id(item)] = int(item.GetClipProperty("Frames") or 0)
                    except (TypeError, ValueError, Exception):
                        media_lengths[id(item)] = 0
                frames = media_lengths[id(item)]
                ci.start_frame, ci.end_frame = add_handles(
                    ci.start_frame, ci.end_frame, handles, frames)
                if ci.api_source_start is not None and ci.api_source_end is not None:
                    ci.api_source_start, ci.api_source_end = add_handles(
                        ci.api_source_start, ci.api_source_end, handles, frames)
        print(f"Handles: {handles} frame(s) added each side of every segment "
              f"(stopping at the start and end of the media).")

    # Merge overlapping clips for each media ID
    _p("Merging overlapping ranges...", 0, 0)
    for media_id in clips:
        clips[media_id] = merge_all_overlapping(clips[media_id], connection_threshold)

    print("Merged Clips — creating flat list for sorting...")

    # Flatten into sorted list
    all_clip_infos: list[ClipInfo] = []
    for clip_infos in clips.values():
        all_clip_infos.extend(clip_infos)

    # Segments composited together in an edit (overlapping on different
    # tracks) are stacked together in the master.
    composite_count = find_composite_groups(all_clip_infos)
    if composite_count:
        print(f"{composite_count} composite(s) found: their layers are stacked "
              f"together in the master.")

    timeline_markers: list[dict] = []

    # Detect duplicate sets on the merged ClipInfo list (before timeline creation)
    if mark_duplicates:
        _p("Detecting duplicates...", 0, 0)
        dup_set_count = find_duplicate_groups(all_clip_infos)
        print(f"Detected {dup_set_count} duplicate set(s) across {len(all_clip_infos)} clips")
    else:
        dup_set_count = 0

    # Apply sorting
    print(f"Sorting using method: {sorting_method}")
    sort_fn = SORT_METHODS.get(sorting_method)
    if sort_fn is sort_by_edit_order:
        sort_by_edit_order(all_clip_infos, {name: rank for rank, (name, _tl)
                                            in enumerate(source_timelines)})
    elif sort_fn:
        sort_fn(all_clip_infos)
    else:
        print(f"Unknown sorting method '{sorting_method}', using default (Source Name)")
        sort_by_source_name(all_clip_infos)

    # Still images go after all the footage, by name. A still's timecode is
    # usually 00:00:00:00, which would otherwise put it first.
    still_ids = {id(ci) for ci in all_clip_infos if is_still_item(ci.media_pool_item)}
    if still_ids:
        footage = [ci for ci in all_clip_infos if id(ci) not in still_ids]
        stills = [ci for ci in all_clip_infos if id(ci) in still_ids]
        sort_by_source_name(stills)
        all_clip_infos = footage + stills
        print(f"{len(stills)} still image segment(s) placed after the footage")

    return all_clip_infos, timeline_markers, dup_set_count


# ---------------------------------------------------------------------------
# Append Helper
# ---------------------------------------------------------------------------

def append_clip_with_slip_compensation(media_pool, timeline, clip_info: ClipInfo,
                                       **kwargs) -> tuple:
    """Place one ClipInfo (see _append_clip_placed) and color it Purple if it is a still.

    A rebuilt clip's own color is put back afterwards by restore_item_state, so
    a color the user chose wins over this one.
    """
    result = _append_clip_placed(media_pool, timeline, clip_info, **kwargs)
    item = result[0]
    if item is not None:
        mpi = clip_info.media_pool_item
        if is_still_item(mpi):
            try:
                item.SetClipColor(STILL_CLIP_COLOR)
            except Exception:
                print(f"  WARN: could not color still '{mpi.GetName()}' {STILL_CLIP_COLOR}")
    return result


def _append_clip_placed(
    media_pool,
    timeline,
    clip_info: ClipInfo,
    *,
    video_only: bool,
    track_index: Optional[int] = None,
    record_frame: Optional[int] = None,
    timeline_fps: Optional[float] = None,
    allow_widening: bool = True,
) -> tuple:
    """Append one ClipInfo, compensating for AppendToTimeline source-frame slip.

    `timeline` must already be the project's current timeline — AppendToTimeline
    always targets the current one.

    Resolve sometimes places clips with their source in/out shifted by ±1 frame
    (codec/internal anchor quirks). We re-query the placed clip; if it differs
    from the target, delete it and retry with startFrame/endFrame adjusted by the
    inverse of the observed slip. Capped at SLIP_RETRY_LIMIT retries; if still
    off, fall back to widening the request by ±1 so the target range is fully
    contained in the placed range (extra handle frames are acceptable, missing
    frames are not). Pass allow_widening=False when the clip is going into a
    tight gap where that extra frame has nowhere to go.

    Returns (item, status, placed_source_start, placed_source_end). status is one
    of "exact", "corrected", "widened", "unfixed", "unknown" or "error";
    "unknown" covers an append that raised nothing but gave back no single
    usable item to verify.
    """
    mpi = clip_info.media_pool_item
    clip_name = mpi.GetName()

    # Quiet FPS-mismatch check (loud warning only when triggered).
    try:
        _clip_fps_raw = mpi.GetClipProperty("FPS")
        _clip_fps_val = float(_clip_fps_raw) if _clip_fps_raw not in (None, "") else None
    except (TypeError, ValueError, Exception):
        _clip_fps_val = None
    if (timeline_fps is not None and _clip_fps_val is not None
            and abs(timeline_fps - _clip_fps_val) > 0.01):
        print(
            f"  WARN: FPS mismatch on '{clip_name}' "
            f"(clip={_clip_fps_val}, timeline={timeline_fps})"
        )

    api_dict = sanitize_for_api(clip_info)
    # Audio filtering: mediaType=1 is the documented way to import video only and
    # works across all Resolve versions. importVideo/importAudio are kept as a
    # belt-and-suspenders hint for newer API builds.
    if video_only:
        api_dict["mediaType"] = 1  # 1 = video, 2 = audio
    api_dict["importVideo"] = True
    api_dict["importAudio"] = not video_only
    if track_index is not None:
        api_dict["trackIndex"] = track_index
    if record_frame is not None:
        api_dict["recordFrame"] = record_frame

    target_start = api_dict["startFrame"]
    target_end = api_dict["endFrame"]

    # The media's length in frames: endFrame can be at most this. A segment
    # asked to run past it can never match exactly; reaching it counts as placed.
    try:
        media_frames = int(mpi.GetClipProperty("Frames") or 0)
    except (TypeError, ValueError, Exception):
        media_frames = 0
    media_frames = media_frames if media_frames > 1 else None

    def _placed_span(item) -> tuple:
        """(start, end) a placed item covers, end EXCLUSIVE like endFrame.

        Worked out from the duration: GetSourceEndFrame() on an appended clip is
        the exclusive end on 21.0.4 but the inclusive last frame on 21.1.2, and
        reading the latter as the former made every clip look one frame short,
        so the retry below added a frame to every tail. Clips are placed at
        100% speed, so the duration is the source span on any build.
        """
        exact = exact_source_range(item)
        if exact:
            return exact[0], exact[1] + 1
        start = item.GetSourceStartFrame()
        try:
            duration = int(item.GetDuration() or 0)
        except Exception:
            duration = 0
        if start is None:
            return None, None
        if duration > 0:
            return start, start + duration
        end = item.GetSourceEndFrame()
        return start, (None if end is None else end + 1)

    def _reaches_end(placed_end) -> bool:
        return (placed_end == target_end
                or (media_frames is not None and target_end > media_frames
                    and placed_end >= media_frames))

    try:
        placed_items = media_pool.AppendToTimeline([api_dict])
    except Exception:
        print(f"  ERROR: Failed to add clip: {clip_name}")
        print(f"  Frame range attempted: {api_dict['startFrame']} to {api_dict['endFrame']}")
        return None, "error", None, None

    if record_frame is not None:
        print(f"  Placed on track {track_index} at frame {record_frame}")

    last_item = None
    retry_count = 0
    while placed_items and retry_count <= SLIP_RETRY_LIMIT:
        if len(placed_items) != 1:
            break  # unexpected multi-item return; don't try to fix
        placed = placed_items[0]
        last_item = placed
        try:
            actual_start, actual_end = _placed_span(placed)
        except Exception:
            actual_start = None
            actual_end = None
        if actual_start is None or actual_end is None:
            break
        start_delta = actual_start - target_start
        end_delta = actual_end - target_end
        if start_delta == 0 and _reaches_end(actual_end):
            return (placed, "corrected" if retry_count > 0 else "exact",
                    actual_start, actual_end)
        if retry_count >= SLIP_RETRY_LIMIT:
            if not allow_widening:
                print(
                    f"  WARN: '{clip_name}' slip unfixable (target "
                    f"{target_start}-{target_end}, placed "
                    f"{actual_start}-{actual_end}); no room to widen here"
                )
                return placed, "unfixed", actual_start, actual_end
            # Widening fallback — extra frames are acceptable.
            try:
                timeline.DeleteClips([placed], False)
            except Exception:
                print(
                    f"  ERROR: '{clip_name}' slip unfixable and DeleteClips "
                    f"failed before widening; clip left at "
                    f"{actual_start}-{actual_end} "
                    f"(target {target_start}-{target_end})"
                )
                return placed, "unfixed", actual_start, actual_end
            wide_start = max(0, target_start - 1)
            wide_end = target_end + 1
            try:
                _media_end_raw = mpi.GetClipProperty("End")
                _media_end = int(_media_end_raw) if _media_end_raw not in (None, "") else None
            except (TypeError, ValueError, Exception):
                _media_end = None
            if _media_end is not None:
                # GetClipProperty("End") is the inclusive last frame of the
                # media; endFrame is exclusive, so the largest legal request is
                # one past it.
                wide_end = min(wide_end, _media_end + 1)
            api_dict["startFrame"] = wide_start
            api_dict["endFrame"] = wide_end
            try:
                wide_items = media_pool.AppendToTimeline([api_dict])
            except Exception:
                print(
                    f"  ERROR: '{clip_name}' widening append raised; clip is "
                    f"no longer on the timeline (target "
                    f"{target_start}-{target_end})"
                )
                return None, "unfixed", None, None
            covers = False
            w_start = w_end = None
            wide_item = None
            if wide_items and len(wide_items) == 1:
                wide_item = wide_items[0]
                try:
                    w_start, w_end = _placed_span(wide_item)
                except Exception:
                    pass
                if w_start is not None and w_end is not None:
                    covers = (w_start <= target_start
                              and (w_end >= target_end or _reaches_end(w_end)))
            if covers:
                print(
                    f"  WARN: '{clip_name}' slip unfixable "
                    f"(target {target_start}-{target_end}); "
                    f"widened to {w_start}-{w_end} — "
                    f"target frames preserved with handles"
                )
                return wide_item, "widened", w_start, w_end
            print(
                f"  ERROR: '{clip_name}' slip unfixable; "
                f"widened to {w_start}-{w_end} but target "
                f"{target_start}-{target_end} NOT covered "
                f"(frames missing)"
            )
            return wide_item, "unfixed", w_start, w_end
        # Silent retry with inverse-of-observed-slip compensation.
        try:
            timeline.DeleteClips([placed], False)
        except Exception:
            print(
                f"  ERROR: '{clip_name}' DeleteClips failed during "
                f"retry; leaving slipped clip at "
                f"{actual_start}-{actual_end} "
                f"(target {target_start}-{target_end})"
            )
            return placed, "unfixed", actual_start, actual_end
        api_dict["startFrame"] = target_start - start_delta
        api_dict["endFrame"] = target_end - end_delta
        try:
            placed_items = media_pool.AppendToTimeline([api_dict])
        except Exception:
            print(
                f"  ERROR: '{clip_name}' retry append raised; clip is no "
                f"longer on the timeline (target {target_start}-{target_end})"
            )
            return None, "unfixed", None, None
        last_item = None
        retry_count += 1

    return last_item, "unknown", None, None


# ---------------------------------------------------------------------------
# Marker Text
# ---------------------------------------------------------------------------

def build_duplicate_marker_text(clip_info: ClipInfo) -> tuple:
    """(color, name, note) for a duplicate-set marker."""
    set_idx = clip_info.duplicate_set_index
    color = DUPLICATE_MARKER_COLORS[set_idx % len(DUPLICATE_MARKER_COLORS)]
    marker_text = (f"Dup Set #{set_idx + 1} "
                   f"({clip_info.duplicate_position + 1}/{clip_info.duplicate_set_size})")
    return color, marker_text, "Duplicate clip detected"


def build_retime_marker_text(clip_info: ClipInfo) -> tuple:
    """(name, note) for a retime marker. The color is always Red."""
    if clip_info.is_frame_hold:
        marker_text = "Frame Hold"
        marker_note = ("Source clip used a frame hold (freeze frame). "
                       "Manual check recommended.")
    elif clip_info.is_non_linear_retime:
        marker_text = "Non-Linear Retime"
        marker_note = ("Speed curve/ramp detected. Source range may not "
                       "cover all frames used. Manual check recommended.")
        if clip_info.is_reversed:
            marker_note += " (originally reversed)"
    elif (clip_info.retime_percentage is not None
            and clip_info.retime_percentage >= EXTREME_RETIME_PERCENT):
        # Past this speed the percentage stops being useful: a whip reads as
        # "4616%", which tells a human nothing. Say what the clip actually
        # spans instead, which is the number worth checking by eye.
        span = clip_info.end_frame - clip_info.start_frame + 1
        marker_text = "Extreme Retime"
        # ASCII only: marker text round-trips through the scripting bridge and
        # back out through GetMarkers on every subsequent run.
        marker_note = (
            f"Whip or speed ramp - check by hand. {span} source frames "
            f"({clip_info.start_frame}-{clip_info.end_frame}) played over "
            f"roughly {max(1, round(span * 100 / clip_info.retime_percentage))} "
            f"timeline frames."
        )
        if clip_info.is_reversed:
            marker_note += " (originally reversed)"
    else:
        speed_value = clip_info.retime_percentage
        speed_str = f"{speed_value:.1f}" if speed_value is not None else "Unknown"
        marker_text = "Retimed Clip"
        marker_note = f"Manual check recommended. Speed: {speed_str}%"
        if clip_info.is_reversed:
            marker_note += " (originally reversed)"
    return marker_text, marker_note


# ---------------------------------------------------------------------------
# Update Diff
# ---------------------------------------------------------------------------

def read_accepted_range(markers: dict) -> tuple:
    """(accepted_start, accepted_end) from a clip's own update marker.

    Returns (None, None) when the clip has never been through an update. If more
    than one update marker survives, the highest run number wins.
    """
    best_run = None
    best = (None, None)
    for frame in sorted(markers):
        info = markers[frame] or {}
        custom = info.get("customData") or ""
        if not isinstance(custom, str) or not custom.startswith(UPDATE_MARKER_PREFIX):
            continue
        try:
            data = json.loads(custom[len(UPDATE_MARKER_PREFIX):])
        except (ValueError, TypeError):
            continue
        if not isinstance(data, dict):
            continue
        start, end = data.get("ds"), data.get("de")
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        run = data.get("run")
        run = run if isinstance(run, int) else -1
        if best_run is None or run >= best_run:
            best_run = run
            best = (start, end)
    return best


def diff_ranges(desired_ranges: list, placed_ranges: list) -> tuple:
    """Greedy maximum-overlap matching between two lists of inclusive ranges.

    Returns (pairs, unmatched_desired, unmatched_placed) where pairs is
    [(desired_index, placed_index), ...].

    Merging legitimately leaves several disjoint ranges for one source file, so
    both sides are lists. Pairing them by index breaks the moment one range is
    deleted or a new one lands in the middle, hence the overlap match. Ties are
    broken by total endpoint distance and then by index, so the result is
    deterministic for a given input.
    """
    candidates = []
    for di, (d_start, d_end) in enumerate(desired_ranges):
        for pi, (p_start, p_end) in enumerate(placed_ranges):
            overlap = min(d_end, p_end) - max(d_start, p_start) + 1
            if overlap <= 0:
                continue
            distance = abs(d_start - p_start) + abs(d_end - p_end)
            candidates.append((-overlap, distance, di, pi))
    candidates.sort()

    pairs = []
    used_desired = set()
    used_placed = set()
    for _overlap, _distance, di, pi in candidates:
        if di in used_desired or pi in used_placed:
            continue
        used_desired.add(di)
        used_placed.add(pi)
        pairs.append((di, pi))
    pairs.sort()

    unmatched_desired = [i for i in range(len(desired_ranges)) if i not in used_desired]
    unmatched_placed = [i for i in range(len(placed_ranges)) if i not in used_placed]
    return pairs, unmatched_desired, unmatched_placed


def classify_change(desired: tuple, placed: tuple, accepted=None,
                    tolerance: int = UPDATE_CHANGE_TOLERANCE,
                    shrink_tolerance: int = UPDATE_SHRINK_TOLERANCE) -> str:
    """'unchanged' | 'extended' | 'shortened' | 'both' for one matched pair.

    Each end is tested against a threshold chosen by DIRECTION, not by size:
    growth beyond `tolerance` counts, shrink only beyond `shrink_tolerance`.
    Missing frames break a pull; surplus frames are just handle, and rebuilding
    to remove them costs the clip its grade for nothing.

    That asymmetry also hardens the anti-churn guarantee. The append helper's
    widening fallback can place a clip WIDER than requested, which reads as a
    shrink on both ends — now measured against the larger threshold, so a
    widened clip stays unchanged by an even wider margin.

    `accepted` is the desired range this clip was last reconciled against, and is
    compared with the tight tolerance because it asks a different question: has
    the target itself moved? When it has not, the clip is unchanged no matter
    where it actually landed — the escape hatch for a target that is physically
    unreachable (media clamp, unfixable slip, sub-clip range limit), which would
    otherwise be retried forever.
    """
    desired_start, desired_end = desired
    if accepted is not None:
        accepted_start, accepted_end = accepted
        if (accepted_start is not None and accepted_end is not None
                and abs(desired_start - accepted_start) <= tolerance
                and abs(desired_end - accepted_end) <= tolerance):
            return "unchanged"

    placed_start, placed_end = placed
    head_delta = desired_start - placed_start
    tail_delta = desired_end - placed_end

    # head_delta < 0 reaches further back (growth); > 0 pulls the head in.
    # tail_delta > 0 reaches further on (growth); < 0 pulls the tail in.
    head_grows = head_delta < 0 and -head_delta > tolerance
    head_shrinks = head_delta > 0 and head_delta > shrink_tolerance
    tail_grows = tail_delta > 0 and tail_delta > tolerance
    tail_shrinks = tail_delta < 0 and -tail_delta > shrink_tolerance

    grows = head_grows or tail_grows
    shrinks = head_shrinks or tail_shrinks

    if not grows and not shrinks:
        return "unchanged"
    if grows and shrinks:
        return "both"
    return "extended" if grows else "shortened"


def plan_rebuild_placement(record_start: int, old_src: tuple,
                           new_src: tuple) -> tuple:
    """(new_record, new_duration, head_need, tail_need) for a rebuilt clip.

    Anchored on the source frame, not the record frame: every source frame the
    clip keeps stays at the same timeline position. A head trim therefore opens
    the gap at the head instead of sliding the whole clip left, so anything the
    user lined up against it on another track stays lined up.
    """
    old_start, old_end = old_src
    new_start, new_end = new_src
    old_duration = max(1, old_end - old_start + 1)
    new_duration = max(1, new_end - new_start + 1)
    new_record = record_start + (new_start - old_start)
    head_need = max(0, record_start - new_record)
    tail_need = max(0, (new_record + new_duration) - (record_start + old_duration))
    return new_record, new_duration, head_need, tail_need


def compute_free_space(bounds: list, index: int, timeline_start: int = 0) -> tuple:
    """(free_before, free_after) around bounds[index] on a single track.

    `bounds` is [(start, end_exclusive), ...] for one track, sorted by start.
    The last clip on a track has unbounded room after it.
    """
    start, end = bounds[index]
    if index == 0:
        free_before = max(0, start - timeline_start)
    else:
        free_before = max(0, start - bounds[index - 1][1])
    if index >= len(bounds) - 1:
        free_after = FREE_SPACE_UNBOUNDED
    else:
        free_after = max(0, bounds[index + 1][0] - end)
    return free_before, free_after


def fits_in_place(free_before: int, free_after: int, head_need: int,
                  tail_need: int, slack: int = 0) -> bool:
    """Whether a rebuilt clip's growth fits the gaps around it.

    Head and tail are independent: a clip can grow left into a gap while having
    no room at all on the right. Call once with slack=0 to ask "does it fit",
    then again with slack=REBUILD_FIT_SLACK to ask "and may it also widen".
    Widening pushes out both ends at once, so it needs a spare frame on each
    side even when only one end grew.
    """
    return (head_need + slack <= free_before
            and tail_need + slack <= free_after)


def group_desired_by_identity(clip_infos: list, merge_by_source_file: bool) -> dict:
    """identity -> [ClipInfo] sorted by source start, for the diff."""
    grouped: dict = {}
    for clip_info in clip_infos:
        identity = clip_identity_key(clip_info.media_pool_item, merge_by_source_file)
        if not identity:
            continue
        grouped.setdefault(identity, []).append(clip_info)
    for entries in grouped.values():
        entries.sort(key=lambda ci: ci.start_frame)
    return grouped


def scan_timeline_placements(timeline, merge_by_source_file: bool) -> tuple:
    """(placed_by_identity, unmanaged_items) for an existing All Clips timeline.

    The timeline is the authority on what is currently placed — nothing is read
    from the manifest here, so any reordering, retracking or deletion the user
    did between runs is simply what we see.

    Items with no MediaPoolItem (titles, generators, compound and Fusion clips)
    cannot be identified as a shot and are returned separately so the caller can
    report them. They are never touched.
    """
    placed_by_identity: dict = {}
    unmanaged = []

    try:
        track_count = timeline.GetTrackCount("video")
    except Exception:
        track_count = 0

    for track_index in range(1, (track_count or 0) + 1):
        try:
            items = timeline.GetItemListInTrack("video", track_index)
        except Exception:
            items = None
        if not items:
            continue

        for item in items:
            if item is None:
                continue
            try:
                media_pool_item = item.GetMediaPoolItem()
            except Exception:
                media_pool_item = None
            if not media_pool_item:
                unmanaged.append(item)
                continue

            identity = clip_identity_key(media_pool_item, merge_by_source_file)
            if not identity:
                unmanaged.append(item)
                continue

            try:
                raw_start = item.GetSourceStartFrame()
                raw_end = item.GetSourceEndFrame()
                record_start = item.GetStart()
                duration = item.GetDuration()
            except Exception:
                unmanaged.append(item)
                continue
            if None in (raw_start, raw_end, record_start, duration):
                unmanaged.append(item)
                continue

            # A clip the user reversed by hand would otherwise scan backwards.
            source_start = min(raw_start, raw_end)
            source_end = max(raw_start, raw_end)

            # GetSourceEndFrame() does not answer with one convention. On a clip
            # a human cut it is the inclusive last frame, so end - start + 1 ==
            # duration. On a clip AppendToTimeline placed from an explicit range
            # it mirrors back the EXCLUSIVE endFrame that was requested, so
            # end - start + 1 == duration + 1. Duration is the reliable one, so
            # use it to spot the exclusive form and bring it back to inclusive —
            # otherwise every clip this tool placed reads one frame longer than
            # the conform clip it was pulled from.
            #
            # Only an exact one-frame overhang is corrected. A retimed clip has a
            # timeline duration unrelated to its source span and must not be
            # touched here.
            if source_end - source_start + 1 - duration == 1:
                source_end -= 1
            exact = exact_source_range(item) if raw_start <= raw_end else None
            if exact:
                source_start, source_end = exact

            accepted_start, accepted_end = read_accepted_range(normalised_markers(item))

            linked_count = 0
            linked_getter = getattr(item, "GetLinkedItems", None)
            if callable(linked_getter):
                try:
                    linked = linked_getter() or []
                    # An item lists itself among its linked items on some builds.
                    linked_count = max(0, len(linked) - 1)
                except Exception:
                    linked_count = 0

            name = ""
            try:
                name = item.GetName() or ""
            except Exception:
                name = ""

            placed_by_identity.setdefault(identity, []).append(PlacedClip(
                item=item,
                identity=identity,
                source_start=source_start,
                source_end=source_end,
                record_start=record_start,
                record_end=record_start + duration,
                track_index=track_index,
                name=name,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                linked_item_count=linked_count,
            ))

    for entries in placed_by_identity.values():
        entries.sort(key=lambda pc: pc.source_start)

    return placed_by_identity, unmanaged


def widen_to_placed(desired: tuple, placed: tuple) -> tuple:
    """The desired range grown to cover the placed one, so a shot never loses frames.

    Once a master timeline exists its shots go out for work, so an update may
    only add frames. Returns (start, end) spanning both ranges.
    """
    return min(desired[0], placed[0]), max(desired[1], placed[1])


def diff_desired_vs_placed(desired_by_identity: dict, placed_by_identity: dict,
                           tolerance: int = UPDATE_CHANGE_TOLERANCE,
                           shrink_tolerance: int = UPDATE_SHRINK_TOLERANCE) -> list:
    """Reconcile desired against placed. Returns [ClipDiff] in identity order.

    Shots are never shortened: each desired range is first widened to cover the
    placed one, so a matched shot comes out 'unchanged' or 'extended' only.
    """
    diffs = []
    identities = sorted(set(desired_by_identity) | set(placed_by_identity))

    for identity in identities:
        desired = desired_by_identity.get(identity) or []
        placed = placed_by_identity.get(identity) or []
        # A still has no frame range to grow: once it is in the master it has
        # everything an edit can use, however long the edit holds it. Comparing
        # ranges would read the handles added to its one frame as new frames.
        if desired and placed and is_still_item(desired[0].media_pool_item):
            for placed_clip in placed:
                diffs.append(ClipDiff(identity=identity, kind="unchanged",
                                      clip_info=desired[0], placed=placed_clip,
                                      head_delta=0, tail_delta=0))
            continue

        desired_ranges = [(ci.start_frame, ci.end_frame) for ci in desired]
        placed_ranges = [(pc.source_start, pc.source_end) for pc in placed]

        pairs, only_desired, only_placed = diff_ranges(desired_ranges, placed_ranges)

        for desired_index, placed_index in pairs:
            clip_info = desired[desired_index]
            placed_clip = placed[placed_index]
            wanted = desired_ranges[desired_index]
            placed_range = placed_ranges[placed_index]
            widened = widen_to_placed(wanted, placed_range)
            # Worth a mention only when the edit really pulled in, not handle noise.
            kept_frames = (wanted[0] - placed_range[0] > shrink_tolerance
                           or placed_range[1] - wanted[1] > shrink_tolerance)
            if widened != wanted:
                clip_info = replace(clip_info, start_frame=widened[0],
                                    end_frame=widened[1])
            kind = classify_change(
                widened, placed_range,
                (placed_clip.accepted_start, placed_clip.accepted_end),
                tolerance, shrink_tolerance,
            )
            diffs.append(ClipDiff(
                identity=identity,
                kind=kind,
                clip_info=clip_info,
                placed=placed_clip,
                head_delta=clip_info.start_frame - placed_clip.source_start,
                tail_delta=clip_info.end_frame - placed_clip.source_end,
                kept_frames=kept_frames,
            ))

        for desired_index in only_desired:
            diffs.append(ClipDiff(identity=identity, kind="new",
                                  clip_info=desired[desired_index]))

        for placed_index in only_placed:
            diffs.append(ClipDiff(identity=identity, kind="dropped",
                                  placed=placed[placed_index]))

    return diffs


def summarise_diffs(diffs: list) -> dict:
    """Counts per change kind, for logging and the manifest run record."""
    counts = {"unchanged": 0, "extended": 0, "shortened": 0, "both": 0,
              "new": 0, "dropped": 0}
    for diff in diffs:
        counts[diff.kind] = counts.get(diff.kind, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Main Workflow
# ---------------------------------------------------------------------------

def run_workflow(
    dst_timeline_name: str,
    selection_method: str,
    sorting_method: str,
    connection_threshold: int,
    video_only: bool,
    mark_duplicates: bool,
    mark_retimed_clips: bool,
    use_xml_retime: bool,
    import_clip_names: bool,
    merge_by_source_file: bool = True,
    handles: int = DEFAULT_HANDLES,
    progress: Optional["ProgressUI"] = None,
) -> None:
    """Execute the complete timeline generation workflow."""

    def _p(stage: str, current: int = 0, total: int = 0) -> None:
        if progress is not None:
            progress.set(stage, current, total)

    # Get project context — resolve is a pre-injected global in Resolve's scripting environment
    project_manager = resolve.GetProjectManager()  # noqa: F821
    project = project_manager.GetCurrentProject()
    media_pool = project.GetMediaPool()
    num_timelines = project.GetTimelineCount()

    # Build timeline name lookup. Kept eager because it has a second consumer —
    # destination-timeline name deduplication further down — which runs on every
    # invocation. As a way of resolving a source timeline it is superseded by
    # get_timeline_for_media_pool_item() and only used as the pre-21.0.4
    # fallback. (The Lua variant builds this lazily; it has no second consumer.)
    project_timelines = {}
    for timeline_idx in range(1, num_timelines + 1):
        tl = project.GetTimelineByIndex(timeline_idx)
        if tl is not None:
            project_timelines[tl.GetName()] = tl

    source_timelines = resolve_source_timelines(
        media_pool, selection_method, project_timelines, progress_cb=_p,
    )
    if not source_timelines:
        REPORT.summary = ("No approved edits found: select them in the Media Pool, "
                          "or open the bin that holds them. Nothing was created.")
        return

    all_clip_infos, timeline_markers, dup_set_count = collect_desired_clips(
        source_timelines,
        connection_threshold=connection_threshold,
        mark_duplicates=mark_duplicates,
        mark_retimed_clips=mark_retimed_clips,
        use_xml_retime=use_xml_retime,
        import_clip_names=import_clip_names,
        merge_by_source_file=merge_by_source_file,
        sorting_method=sorting_method,
        handles=handles,
        progress_cb=_p,
    )
    if not all_clip_infos:
        REPORT.summary = "The approved edits have no video clips to pull. Nothing was created."
        return

    # Create new timeline — dedupe name against existing project timelines.
    # If "Master_Sources" exists, try "Master_Sources_01", "Master_Sources_02", …
    if dst_timeline_name in project_timelines:
        counter = 1
        while True:
            candidate = f"{dst_timeline_name}_{counter:02d}"
            if candidate not in project_timelines:
                print(f"Timeline name '{dst_timeline_name}' already exists, "
                      f"using '{candidate}' instead")
                dst_timeline_name = candidate
                break
            counter += 1

    print("Adding all clips to new timeline...")
    new_timeline = media_pool.CreateEmptyTimeline(dst_timeline_name)
    # Not an assert: `python -O` strips those, and AppendToTimeline always
    # targets the current timeline, so failing to switch would append every
    # clip onto whatever the user happened to have open.
    if new_timeline is None:
        print(f"ERROR: could not create the timeline '{dst_timeline_name}'. "
              f"Nothing was changed.")
        REPORT.summary = (f"Could not create the timeline '{dst_timeline_name}'. "
                          f"Nothing was changed.")
        return
    if not project.SetCurrentTimeline(new_timeline):
        print(f"ERROR: created '{dst_timeline_name}' but could not make it "
              f"current. Aborting rather than appending to the wrong timeline.")
        return

    # Capture timeline FPS so per-clip code can warn on FPS mismatches.
    _timeline_fps_str = ""
    try:
        _timeline_fps_str = new_timeline.GetSetting("timelineFrameRate") or ""
    except Exception:
        _timeline_fps_str = ""
    if not _timeline_fps_str:
        try:
            _timeline_fps_str = project.GetSetting("timelineFrameRate") or ""
        except Exception:
            _timeline_fps_str = ""
    try:
        _timeline_fps = float(_timeline_fps_str) if _timeline_fps_str else None
    except (TypeError, ValueError):
        _timeline_fps = None
    print(f"Timeline FPS: {_timeline_fps_str or '<unknown>'}")

    # AppendToTimeline's recordFrame is ABSOLUTE - the same space as
    # TimelineItem.GetStart() - while the layout cursor below is a zero-based
    # offset. A new timeline normally starts at
    # 01:00:00:00, so passing the raw cursor puts every clip an hour before the
    # timeline's own start: verified on 21.0.4.5, recordFrame=0 on a timeline
    # starting at 90000 places the clip at absolute frame 0, GetEndFrame() does
    # not even count it, and the block marker meant to label it lands 90000
    # frames away. Rebase the cursor onto the timeline start so clips and
    # markers agree.
    _timeline_start = 0
    _start_getter = getattr(new_timeline, "GetStartFrame", None)
    if callable(_start_getter):
        try:
            _timeline_start = int(_start_getter() or 0)
        except Exception:
            _timeline_start = 0

    # Pre-create video tracks to cover the highest source_track_index
    if all_clip_infos:
        max_track = max(ci.source_track_index for ci in all_clip_infos)
        cur = new_timeline.GetTrackCount("video")
        while cur < max_track:
            new_timeline.AddTrack("video")
            cur += 1
            print(f"Pre-created video track {cur}")
    name_video_tracks(new_timeline)

    # Add clips — single code path for all clip types
    append_success_count = 0
    append_error_count = 0
    # Slip-compensation telemetry (summarised at the end of the append phase).
    slip_corrected_count = 0  # clips that landed on target after retry
    slip_widened_count = 0    # clips that needed the ±1 widening fallback
    slip_unfixed_count = 0    # clips where even widening didn't cover target
    total_to_append = len(all_clip_infos)
    # One cursor for all tracks: each segment goes on the track it came from,
    # starting where the previous block (on any track) ended, so nothing
    # overlaps and the Sort order reads left to right. A composite is one
    # block: each of its tracks starts at the block's start, so its layers
    # sit stacked; segments of the block on one track follow one another.
    blocks = composite_blocks(all_clip_infos)
    placement_order = [ci for block in blocks for ci in block]
    block_of = {id(ci): number for number, block in enumerate(blocks) for ci in block}
    layout_cursor = 0
    current_block, block_start, track_cursor = -1, 0, {}

    for i, clip_info in enumerate(placement_order):
        if block_of[id(clip_info)] != current_block:
            current_block = block_of[id(clip_info)]
            block_start, track_cursor = layout_cursor, {}
        track = max(1, clip_info.source_track_index or 1)
        record_offset = track_cursor.get(track, block_start)
        clip_name = clip_info.media_pool_item.GetName()
        _p(f"Appending clip: {clip_name}", i + 1, total_to_append)
        print(f"Adding clip #{i + 1} to timeline:")
        print(f"  Clip name: {clip_name}")
        print(f"  Frame range: {clip_info.start_frame} to {clip_info.end_frame}")

        # Log original clip status
        status_parts = []
        if clip_info.is_reversed:
            status_parts.append("REVERSED")
        if clip_info.is_frame_hold:
            status_parts.append("FRAME HOLD")
        if clip_info.is_non_linear_retime:
            status_parts.append("NON-LINEAR RETIME")
        if clip_info.is_retimed:
            status_parts.append("RETIMED")
        if status_parts:
            print(f"  Original clip status: {', '.join(status_parts)}")
            print("  (Adding normalized forward-playing version)")

        _item, _status, _s, _e = append_clip_with_slip_compensation(
            media_pool, new_timeline, clip_info,
            video_only=video_only,
            track_index=track,
            record_frame=_timeline_start + record_offset,
            timeline_fps=_timeline_fps,
        )
        placed_end = None
        if _item is not None:
            try:
                placed_end = int(_item.GetEnd()) - _timeline_start
            except Exception:
                placed_end = None
        if placed_end is None or placed_end <= record_offset:
            placed_end = record_offset + (clip_info.end_frame - clip_info.start_frame + 1)
        track_cursor[track] = placed_end
        layout_cursor = max(layout_cursor, placed_end)
        # "unknown" is an append that raised nothing but gave back no usable
        # item, which means nothing was placed — a failure, not a success.
        if _status in ("error", "unknown"):
            append_error_count += 1
        else:
            append_success_count += 1
        notes = []
        if clip_info.is_frame_hold:
            notes.append("freeze frame")
        elif clip_info.is_non_linear_retime:
            notes.append("speed ramp")
        elif clip_info.is_retimed and clip_info.retime_percentage is not None:
            notes.append(f"retimed {clip_info.retime_percentage:.0f}%")
        if clip_info.is_reversed:
            notes.append("reversed in the edit")
        if clip_info.duplicate_set_index is not None:
            notes.append(f"duplicate set #{clip_info.duplicate_set_index + 1}")
        if clip_info.composite_group is not None:
            notes.append(f"composite #{clip_info.composite_group + 1}, "
                         f"{TRACK_NAME_PREFIX}{track}")
        REPORT.add(clip_info.source_name or clip_info.media_pool_item.GetName(),
                   ("Failed - see the console" if _status in ("error", "unknown")
                    else "Added"),
                   clip_info.end_frame - clip_info.start_frame + 1,
                   f"{clip_info.start_frame}-{clip_info.end_frame}", ", ".join(notes))
        if _status == "corrected":
            slip_corrected_count += 1
        elif _status == "widened":
            slip_widened_count += 1
        elif _status == "unfixed":
            slip_unfixed_count += 1

    print(f"Clip addition summary: {append_success_count} succeeded, "
          f"{append_error_count} failed")
    if (slip_corrected_count or slip_widened_count or slip_unfixed_count):
        print(
            f"Slip compensation: {slip_corrected_count} corrected via retry, "
            f"{slip_widened_count} widened with handles, "
            f"{slip_unfixed_count} unfixable"
        )
    print(f"New timeline created: {dst_timeline_name}")

    # Post-processing: one walk of the new timeline for all three passes.
    #
    # These used to be three separate loops, each calling
    # get_all_timeline_clips() again (three full track walks, each re-printing
    # every clip's name and file path) and each re-querying
    # GetSourceStartFrame/GetSourceEndFrame/GetName on the SAME timeline item
    # once per candidate ClipInfo -- none of which depend on the candidate. On a
    # 500-clip timeline that is on the order of 10^5 redundant bridge calls per
    # pass. Now the timeline is walked once, the per-item values are read once,
    # and candidates are looked up by source name instead of scanned linearly.
    if mark_duplicates or mark_retimed_clips or import_clip_names:
        _p("Marking clips...", 0, 0)
        clip_list = get_all_timeline_clips(new_timeline)
        total_clips = len(clip_list)

        # Candidates bucketed by source name: the first half of the match test
        # is an equality on it, so only same-named ClipInfos can ever match.
        by_source_name: dict[str, list[ClipInfo]] = {}
        for clip_info in all_clip_infos:
            try:
                key = clip_info.media_pool_item.GetName()
            except Exception:
                continue
            by_source_name.setdefault(key, []).append(clip_info)

        dup_marker_count = dup_success_count = 0
        retime_marker_count = retime_success_count = 0
        name_apply_count = 0

        for ci_idx, timeline_clip in enumerate(clip_list, start=1):
            _p(f"Marking: {timeline_clip.name}", ci_idx, total_clips)

            # Read once per placed clip, not once per candidate.
            try:
                item_name = timeline_clip.media_pool_item.GetName()
                source_start = timeline_clip.clip.GetSourceStartFrame()
                source_end = timeline_clip.clip.GetSourceEndFrame()
                clip_duration = timeline_clip.clip.GetDuration()
            except Exception:
                continue
            if None in (source_start, source_end, clip_duration):
                continue

            match = None
            for clip_info in by_source_name.get(item_name, ()):
                if (source_start >= clip_info.start_frame - SLIP_TOLERANCE
                        and source_end <= clip_info.end_frame + SLIP_TOLERANCE):
                    match = clip_info
                    break
            if match is None:
                continue

            if mark_duplicates and match.duplicate_set_index is not None:
                color, marker_text, marker_note = build_duplicate_marker_text(match)
                position = source_start + math.floor(clip_duration * 0.25)
                try:
                    success = timeline_clip.clip.AddMarker(
                        position, color, marker_text, marker_note, 1, "")
                except Exception:
                    success = False
                dup_marker_count += 1
                if success:
                    dup_success_count += 1
                    print(f"  Added duplicate marker to: {timeline_clip.name}")
                else:
                    print(f"  Failed to add duplicate marker to: {timeline_clip.name}")

            if mark_retimed_clips and match.is_retimed:
                marker_text, marker_note = build_retime_marker_text(match)
                position = source_start + math.floor(clip_duration * 0.5)
                try:
                    success = timeline_clip.clip.AddMarker(
                        position, "Red", marker_text, marker_note, 1, "")
                except Exception:
                    success = False
                retime_marker_count += 1
                if success:
                    retime_success_count += 1
                    print(f"  Added retime marker to clip: {timeline_clip.name}")
                else:
                    print(f"  Failed to add retime marker to clip: {timeline_clip.name}")

            if import_clip_names:
                if match.source_name:
                    ok = False
                    try:
                        ok = timeline_clip.clip.SetName(match.source_name)
                    except Exception:
                        pass
                    if ok:
                        print(f"  Renamed clip to: {match.source_name}")
                        name_apply_count += 1
                    else:
                        print(f"  WARNING: SetName failed for: {timeline_clip.name}")

        if mark_duplicates:
            if dup_set_count > 0:
                print(f"Successfully added {dup_success_count} duplicate markers "
                      f"out of {dup_marker_count} attempts.")
            else:
                print("No duplicate clips were found.")
        if mark_retimed_clips:
            print(f"Successfully added {retime_success_count} retime markers out "
                  f"of {retime_marker_count} attempts.")
        if import_clip_names:
            print(f"Clip names applied to {name_apply_count} clips.")


    # Range Audit: flag any clip whose final source range on the new timeline
    # grew significantly versus the raw API-reported range. The only thing in
    # the pipeline that can cause growth past 1.0x is XML retime expansion of
    # a constituent — so this is the primary diagnostic when clips end up
    # longer than expected.
    audit_rows = []
    for ci in all_clip_infos:
        if ci.api_source_start is None or ci.api_source_end is None:
            continue
        api_dur = max(1, ci.api_source_end - ci.api_source_start + 1)
        final_dur = max(1, ci.end_frame - ci.start_frame + 1)
        if final_dur >= api_dur * RANGE_AUDIT_GROWTH_THRESHOLD:
            audit_rows.append((
                final_dur / api_dur,
                ci.media_pool_item.GetName(),
                ci.source_timeline_name,
                ci.api_source_start, ci.api_source_end, api_dur,
                ci.start_frame, ci.end_frame, final_dur,
                ci.is_non_linear_retime,
            ))

    if audit_rows:
        audit_rows.sort(reverse=True)
        print("")
        print(f"=== Range Audit: {len(audit_rows)} clip(s) grew "
              f">={RANGE_AUDIT_GROWTH_THRESHOLD:.1f}x vs raw API range ===")
        print("(Cause: XML retime expansion. Disable 'Use XML for Precise "
              "Retime Detection' to keep raw API ranges.)")
        for (growth, name, tl, api_s, api_e, api_d,
             fin_s, fin_e, fin_d, non_lin) in audit_rows:
            tag = " [non-linear]" if non_lin else ""
            print(f"  [{growth:5.1f}x]{tag} {name}  (from '{tl}')")
            print(f"           API: {api_s}-{api_e} ({api_d}f)  "
                  f"->  Final: {fin_s}-{fin_e} ({fin_d}f)")
        print("")
    elif use_xml_retime:
        print("Range Audit: no clips grew significantly beyond API range.")

    # Stamp the manifest. Which source timelines this was built from and with
    # which settings is not recoverable by looking at the result, so without
    # this an update on the timeline we just made has nothing to re-read and
    # has to be adopted by hand. run_counter stays 0 and adopted stays False:
    # it has had no update runs, and it was not taken over from anyone.
    _p("Recording sources...", 0, 0)
    new_timeline_uid = ""
    _uid_getter = getattr(new_timeline, "GetUniqueId", None)
    if callable(_uid_getter):
        try:
            new_timeline_uid = _uid_getter() or ""
        except Exception:
            new_timeline_uid = ""

    manifest = build_manifest(
        new_timeline_uid,
        dst_timeline_name,
        [timeline_source_record(name, tl) for name, tl in source_timelines],
        build_settings_record(
            connection_threshold=connection_threshold,
            merge_by_source_file=merge_by_source_file,
            video_only=video_only,
            use_xml_retime=use_xml_retime,
            import_clip_names=import_clip_names,
            mark_duplicates=mark_duplicates,
            mark_retimed_clips=mark_retimed_clips,
            handles=handles,
        ),
        utc_now_iso(),
        TOOL_VERSION,
    )
    remove_empty_tracks(project, new_timeline)
    stored = write_manifest(new_timeline, manifest)
    if stored["metadata"] or stored["marker"]:
        print(f"Recorded {len(source_timelines)} approved edit(s) on "
              f"'{dst_timeline_name}', so an update can show what changed.")

    _composites = len({ci.composite_group for ci in all_clip_infos
                       if ci.composite_group is not None})
    REPORT.title = (f"{SCRIPT_TITLE}: created '{dst_timeline_name}' - "
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    REPORT.summary = (
        f"{append_success_count} segment(s) from {len(source_timelines)} approved "
        f"edit(s): {', '.join(name for name, _tl in source_timelines)}. "
        f"Handles: {handles} frame(s) each side."
        + (f" {_composites} composite(s) stacked on their layers." if _composites else "")
        + (f" {append_error_count} failed - see the console." if append_error_count else ""))

    _p("Done!", 1, 1)
    print("Done!")


# ---------------------------------------------------------------------------
# Update Execution Helpers
# ---------------------------------------------------------------------------

def local_now_str() -> str:
    """Local wall clock as 2026-08-06 14:22, for human-readable changelogs."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def format_change_line(now_str: str, run_no: int, head_delta: int,
                       tail_delta: int, old_range: tuple,
                       new_range: tuple) -> str:
    """One changelog line. head_delta/tail_delta are desired minus placed.

    Reported from the clip's point of view: "head +12f" means twelve more frames
    at the head, which is a head_delta of -12.
    """
    parts = []
    head_grow = -head_delta
    if head_grow:
        parts.append(f"head {head_grow:+d}f")
    if tail_delta:
        parts.append(f"tail {tail_delta:+d}f")
    change = ", ".join(parts) if parts else "no range change"
    return CHANGELOG_SEPARATOR.join([
        now_str,
        f"run {run_no}",
        change,
        f"{old_range[0]}-{old_range[1]} -> {new_range[0]}-{new_range[1]}",
    ])


def merge_changelog(previous_note, new_line: str,
                    max_lines: int = CHANGELOG_MAX_LINES) -> str:
    """Prepend a change line to a marker note, keeping a bounded history.

    The previous note has to be read off the old marker before the clip is
    deleted — a rebuilt clip has no markers of its own until they are restored.
    Any earlier truncation count is folded in rather than lost.
    """
    earlier = 0
    kept = []
    for line in (previous_note or "").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(CHANGELOG_TRUNCATION_MARK):
            digits = "".join(ch for ch in stripped if ch.isdigit())
            if digits:
                earlier += int(digits)
            continue
        kept.append(stripped)

    room = max(0, max_lines - 1)
    lines = [new_line] + kept[:room]
    dropped = max(0, len(kept) - room) + earlier
    if dropped > 0:
        lines.append(f"{CHANGELOG_TRUNCATION_MARK}{dropped} earlier "
                     f"change{'s' if dropped != 1 else ''})")
    return "\n".join(lines)


def pick_marker_frame(source_start: int, duration: int, existing_frames,
                      fraction: float) -> int:
    """Frame for a clip marker at `fraction` through it, stepping off collisions.

    Resolve permits one marker per frame, and this file already puts markers at
    0.25 (duplicates) and 0.5 (retimes), so on a short clip the preferred frame
    is often taken. Returns -1 when every frame of the clip has a marker.
    """
    duration = max(1, duration)
    upper = source_start + duration - 1
    preferred = source_start + int(math.floor(duration * fraction))
    preferred = min(max(preferred, source_start), upper)
    return first_free_frame(existing_frames, preferred,
                            lower=source_start, upper=upper)


def build_update_customdata(run_no: int, kind: str, desired_start,
                            desired_end, start_reference=None) -> str:
    """customData for a per-clip update marker.

    ds/de are the desired range the clip was reconciled against — the accepted
    range classify_change() reads back to stop an unreachable target being
    retried on every run.
    """
    payload = {"v": 1, "run": run_no, "kind": kind}
    if desired_start is not None and desired_end is not None:
        payload["ds"] = int(desired_start)
        payload["de"] = int(desired_end)
    if start_reference is not None:
        # rs/rf: source frame rs is numbered rf (1001) - see start_frame_for().
        payload["rs"] = int(start_reference[0])
        payload["rf"] = int(start_reference[1])
    return UPDATE_MARKER_PREFIX + json.dumps(payload, sort_keys=True,
                                             separators=(",", ":"))


def timeline_marker_offset(timeline, absolute_frame: int) -> int:
    """Timeline marker frames are offsets from GetStartFrame(), not absolutes.

    Verified on 21.0.4.5: AddMarker(0, ...) on a timeline starting at frame
    90000 comes back from GetMarkers() keyed 0.

    Note that AppendToTimeline's recordFrame is the opposite — it is absolute,
    in the same space as TimelineItem.GetStart() (asked for 90100, landed on
    90100). Marker frames and record frames are therefore NOT interchangeable
    on a timeline that does not start at zero, which is why every marker frame
    in the update path goes through this function.
    """
    start = 0
    getter = getattr(timeline, "GetStartFrame", None)
    if callable(getter):
        try:
            start = getter() or 0
        except Exception:
            start = 0
    return max(0, int(absolute_frame) - int(start))


def capture_item_state(item, track_index: int) -> ItemState:
    """Read back everything about a TimelineItem worth restoring after a rebuild."""
    state = ItemState(track_index=track_index)

    def _try(getter_name, default=None):
        getter = getattr(item, getter_name, None)
        if not callable(getter):
            return default
        try:
            value = getter()
        except Exception:
            return default
        return default if value is None else value

    state.name = _try("GetName")
    state.clip_color = _try("GetClipColor")
    state.flags = list(_try("GetFlagList", []) or [])
    state.enabled = _try("GetClipEnabled")
    state.markers = normalised_markers(item)
    state.fusion_comp_count = int(_try("GetFusionCompCount", 0) or 0)
    state.record_start = int(_try("GetStart", 0) or 0)
    state.duration = int(_try("GetDuration", 0) or 0)

    raw_start = _try("GetSourceStartFrame", 0) or 0
    raw_end = _try("GetSourceEndFrame", 0) or 0
    state.source_start = min(raw_start, raw_end)
    state.source_end = max(raw_start, raw_end)

    versions = getattr(item, "GetVersionNameList", None)
    if callable(versions):
        try:
            state.version_names = list(versions(0) or [])
        except Exception:
            state.version_names = []

    linked = getattr(item, "GetLinkedItems", None)
    if callable(linked):
        try:
            state.linked_item_count = max(0, len(linked() or []) - 1)
        except Exception:
            state.linked_item_count = 0

    return state


def restore_item_state(item, state: ItemState, new_source_start: int,
                       new_source_end: int,
                       skip_customdata_prefix=None) -> dict:
    """Put a rebuilt clip's name, color, flags and markers back.

    TimelineItem marker frames are in source/media frame space — verified on
    21.0.4.5: a marker added at GetSourceStartFrame() + 5 on a clip starting at
    source frame 100 reads back keyed 105. So a restored marker lands on the same
    picture even when the clip's head has moved, which is the whole reason the
    frames are reused unchanged.

    Markers whose frame falls outside the new source range are dropped rather
    than clamped: that picture is no longer in the clip, so a marker there would
    point at something else.
    """
    result = {"name": False, "color": False, "flags": 0, "markers": 0,
              "markers_dropped": 0, "enabled": False}

    if state.name:
        setter = getattr(item, "SetName", None)
        if callable(setter):
            try:
                result["name"] = bool(setter(state.name))
            except Exception:
                result["name"] = False

    if state.clip_color:
        setter = getattr(item, "SetClipColor", None)
        if callable(setter):
            try:
                result["color"] = bool(setter(state.clip_color))
            except Exception:
                result["color"] = False

    adder = getattr(item, "AddFlag", None)
    if callable(adder):
        for flag in state.flags:
            try:
                if adder(flag):
                    result["flags"] += 1
            except Exception:
                pass

    if state.enabled is False:
        setter = getattr(item, "SetClipEnabled", None)
        if callable(setter):
            try:
                result["enabled"] = bool(setter(False))
            except Exception:
                result["enabled"] = False

    marker_adder = getattr(item, "AddMarker", None)
    if callable(marker_adder):
        for frame in sorted(state.markers):
            info = state.markers[frame] or {}
            custom = info.get("customData") or ""
            if (skip_customdata_prefix and isinstance(custom, str)
                    and custom.startswith(skip_customdata_prefix)):
                continue
            if frame < new_source_start or frame > new_source_end:
                result["markers_dropped"] += 1
                continue
            try:
                ok = marker_adder(
                    frame, info.get("color") or "Blue", info.get("name") or "",
                    info.get("note") or "", int(info.get("duration") or 1),
                    custom if isinstance(custom, str) else "",
                )
            except Exception:
                ok = False
            if ok:
                result["markers"] += 1

    return result


def let_resolve_settle(seconds: float) -> None:
    """Wait while letting Resolve handle its pending UI events.

    A timeline switch is drawn after SetCurrentTimeline returns; a plain sleep
    only postpones that, so the redraw then lands on whatever window opens next.
    """
    try:
        fusion = bmd.scriptapp("Fusion")  # noqa: F821
    except Exception:
        fusion = None
    end = time.time() + seconds
    while time.time() < end:
        if fusion is not None:
            try:
                fusion.Wait(0)
            except Exception:
                fusion = None
        time.sleep(0.1)


def reopen_timeline(project, timeline) -> bool:
    """Switch to another timeline and back, so Resolve draws every track header.

    Measured on 21.1.2: tracks that AppendToTimeline adds to the open timeline
    (a subtitle track and audio tracks up to 4, for any clip) get no headers
    until the timeline is reopened, and removing a track in that state - by
    script or by hand - crashes Resolve. Returns True once it is open again.
    """
    try:
        uid = timeline.GetUniqueId()
        other = None
        for index in range(1, (project.GetTimelineCount() or 0) + 1):
            candidate = project.GetTimelineByIndex(index)
            if candidate is not None and candidate.GetUniqueId() != uid:
                other = candidate
                break
        if other is None:
            return False
        project.SetCurrentTimeline(other)
        let_resolve_settle(1)  # let Resolve's display catch up before switching back
        project.SetCurrentTimeline(timeline)
        let_resolve_settle(1)
        current = project.GetCurrentTimeline()
        return current is not None and current.GetUniqueId() == uid
    except Exception:
        return False


def remove_empty_tracks(project, timeline) -> dict:
    """Reopen a picture-only timeline, then delete its empty subtitle tracks and
    its empty audio tracks from the top down, keeping one audio track.

    Nothing is deleted unless the reopen worked: deleting a track whose header
    is not drawn crashes Resolve. A track with any item on it stays.
    Returns {"subtitle": n, "audio": n} deleted.
    """
    deleted = {"subtitle": 0, "audio": 0}
    if not reopen_timeline(project, timeline):
        print("Left the empty audio and subtitle tracks in place (could not reopen "
              "the timeline first, and deleting them without that is unsafe).")
        return deleted
    for kind, keep in (("subtitle", 0), ("audio", 1)):
        try:
            count = int(timeline.GetTrackCount(kind) or 0)
        except Exception:
            continue
        for index in range(count, 0, -1):
            if count - deleted[kind] <= keep:
                break
            try:
                if timeline.GetItemListInTrack(kind, index):
                    continue
                if timeline.DeleteTrack(kind, index):
                    deleted[kind] += 1
            except Exception:
                pass
    if deleted["subtitle"] or deleted["audio"]:
        print(f"Removed {deleted['audio']} empty audio and {deleted['subtitle']} "
              f"empty subtitle track(s).")
    # Let the track removals redraw too, before the log window opens.
    let_resolve_settle(1.5)
    return deleted


def add_update_track(timeline, track_name: str) -> Optional[int]:
    """Append a video track and name it. Returns its index, or None on failure.

    Deliberately never passes {"index": n}: that INSERTS a track and renumbers
    every track above it, which would invalidate every track index held by the
    run in flight.
    """
    try:
        before = timeline.GetTrackCount("video")
    except Exception:
        return None
    try:
        if not timeline.AddTrack("video"):
            return None
    except Exception:
        return None
    try:
        after = timeline.GetTrackCount("video")
    except Exception:
        return None
    if after <= before:
        return None

    setter = getattr(timeline, "SetTrackName", None)
    if callable(setter):
        try:
            setter("video", after, track_name)
        except Exception:
            pass
    print(f"  Added video track {after} '{track_name}'")
    return after


def build_track_occupancy(timeline) -> dict:
    """track index -> sorted [[start, end_exclusive], ...] for every video item.

    Includes items the diff cannot identify (titles, generators, compound clips):
    they still occupy the track, so a rebuilt clip must not be planned on top of
    them. Maintained in memory for the rest of the run — we are the only writer,
    and re-querying per clip would be O(n^2) bridge calls.
    """
    occupancy: dict = {}
    try:
        track_count = timeline.GetTrackCount("video")
    except Exception:
        return occupancy

    for track_index in range(1, (track_count or 0) + 1):
        bounds = []
        try:
            items = timeline.GetItemListInTrack("video", track_index)
        except Exception:
            items = None
        for item in items or []:
            if item is None:
                continue
            try:
                start = item.GetStart()
                duration = item.GetDuration()
            except Exception:
                continue
            if start is None or duration is None:
                continue
            bounds.append([int(start), int(start) + int(duration)])
        bounds.sort()
        occupancy[track_index] = bounds
    return occupancy


def occupancy_index(bounds: list, record_start: int) -> int:
    """Index of the entry starting at `record_start`, or -1."""
    for index, (start, _end) in enumerate(bounds):
        if start == record_start:
            return index
    return -1


def insert_occupancy(bounds: list, start: int, end: int) -> None:
    """Insert [start, end) keeping the track's bounds sorted."""
    position = len(bounds)
    for index, (existing_start, _existing_end) in enumerate(bounds):
        if existing_start > start:
            position = index
            break
    bounds.insert(position, [int(start), int(end)])


def resolve_timelines_by_source_record(project, sources: list) -> tuple:
    """Resolve manifest source records to timelines. Returns (resolved, missing).

    Matches on GetUniqueId() first — it survives renames — and falls back to the
    recorded name, which is the only thing a human can act on when a uid stops
    resolving.
    """
    by_uid = {}
    by_name = {}
    try:
        count = project.GetTimelineCount()
    except Exception:
        count = 0
    for index in range(1, (count or 0) + 1):
        try:
            timeline = project.GetTimelineByIndex(index)
        except Exception:
            timeline = None
        if timeline is None:
            continue
        try:
            name = timeline.GetName()
        except Exception:
            continue
        uid = None
        getter = getattr(timeline, "GetUniqueId", None)
        if callable(getter):
            try:
                uid = getter()
            except Exception:
                uid = None
        if uid:
            by_uid[uid] = (name, timeline)
        by_name.setdefault(name, (name, timeline))

    resolved = []
    missing = []
    for source in sources or []:
        uid = source.get("uid")
        name = source.get("name")
        hit = by_uid.get(uid) if uid else None
        if hit is None and name:
            hit = by_name.get(name)
            if hit is not None and uid:
                print(f"  NOTE: source '{name}' matched by name — its unique id "
                      f"changed since the last run.")
        if hit is None:
            missing.append(name or uid or "?")
        else:
            resolved.append(hit)
    return resolved, missing


def timeline_source_record(name: str, timeline) -> dict:
    """{"uid": ..., "name": ...} for the manifest's source list."""
    uid = ""
    getter = getattr(timeline, "GetUniqueId", None)
    if callable(getter):
        try:
            uid = getter() or ""
        except Exception:
            uid = ""
    return {"uid": uid, "name": name}


def clamp_desired_to_media(clip_info: ClipInfo) -> tuple:
    """(start, end) clamped to the media's own extents.

    Asking for frames past the end of the file produces a placement that can
    never match the request, which without clamping reads as a change forever.
    Update-path only — create mode's behaviour is deliberately untouched.
    """
    start = max(0, clip_info.start_frame)
    end = clip_info.end_frame
    try:
        raw = clip_info.media_pool_item.GetClipProperty("End")
        media_end = int(raw) if raw not in (None, "") else None
    except (TypeError, ValueError, Exception):
        media_end = None
    if media_end is not None:
        end = min(end, media_end)
    if end < start:
        end = start
    return start, end


def write_update_marker(item, kind: str, run_no: int, note: str,
                        marker_name: str, desired_range=None, start_frame=None,
                        start_reference=None, was=None) -> bool:
    """Add this run's marker to a clip, stepping off any frame already taken.

    When the shot no longer starts at 1001 (start_frame), the marker is the
    green 'Start frame N' marker on the shot's first frame, and its
    customData keeps start_reference for the next update.
    """
    moved = start_frame is not None and start_frame != FIRST_START_FRAME
    adder = getattr(item, "AddMarker", None)
    if not callable(adder):
        return False
    try:
        source_start = item.GetSourceStartFrame()
        duration = item.GetDuration()
    except Exception:
        return False
    if source_start is None or duration is None:
        return False

    existing = normalised_markers(item)
    if moved:
        frame = first_free_frame(existing, int(source_start), lower=int(source_start),
                                 upper=int(source_start) + max(1, int(duration)) - 1)
        marker_name, start_note = start_marker_text(start_frame, was)
        note = f"{start_note}\n{note}" if note else start_note
    else:
        frame = pick_marker_frame(int(source_start), int(duration), existing,
                                  UPDATE_MARKER_FRACTION)
    if frame < 0:
        print(f"  WARNING: no free frame for an update marker on "
              f"'{marker_name}'.")
        return False

    custom = build_update_customdata(
        run_no, kind,
        desired_range[0] if desired_range else None,
        desired_range[1] if desired_range else None,
        start_reference if moved else None,
    )
    color = START_MARKER_COLOR if moved else UPDATE_MARKER_COLORS.get(kind, "Blue")
    try:
        return bool(adder(frame, color, marker_name, note, 1, custom))
    except Exception:
        return False


def most_common_value(values) -> str:
    """The value given most often, ignoring empty ones ('' when none)."""
    counts: dict = {}
    for value in values:
        if value:
            counts[value] = counts.get(value, 0) + 1
    return max(counts, key=lambda v: (counts[v], v)) if counts else ""


def master_shot_code(timeline) -> str:
    """The client code the Shot Namer gave this master: the Shot field most of
    its clips have ('' when none has one)."""
    values, seen = [], set()
    try:
        track_count = int(timeline.GetTrackCount("video") or 0)
    except Exception:
        return ""
    for track in range(1, track_count + 1):
        for item in timeline.GetItemListInTrack("video", track) or []:
            try:
                media = item.GetMediaPoolItem()
                if media is None or id(media) in seen:
                    continue
                seen.add(id(media))
                values.append(media.GetMetadata(SHOT_CODE_FIELD) or "")
            except Exception:
                continue
    return most_common_value(values)


def name_video_tracks(timeline) -> int:
    """Name every video track L1, L2 ... Returns how many were renamed."""
    setter = getattr(timeline, "SetTrackName", None)
    if not callable(setter):
        return 0
    try:
        count = int(timeline.GetTrackCount("video") or 0)
    except Exception:
        return 0
    renamed = 0
    for index in range(1, count + 1):
        wanted = f"{TRACK_NAME_PREFIX}{index}"
        try:
            if timeline.GetTrackName("video", index) == wanted:
                continue
        except Exception:
            pass
        try:
            if setter("video", index, wanted):
                renamed += 1
        except Exception:
            pass
    return renamed


# ---------------------------------------------------------------------------
# Update Workflow
# ---------------------------------------------------------------------------

def previous_update_note(markers: dict) -> str:
    """The note off a clip's own update marker, so the changelog can accumulate."""
    for frame in sorted(markers, reverse=True):
        info = markers[frame] or {}
        custom = info.get("customData") or ""
        if isinstance(custom, str) and custom.startswith(UPDATE_MARKER_PREFIX):
            # The start frame sentence heads the note; it is written afresh.
            return "\n".join(line for line in (info.get("note") or "").splitlines()
                             if not line.startswith(START_NOTE_LEAD))
    return ""


def previous_update_kind(markers: dict) -> Optional[str]:
    """The kind recorded by a clip's own update marker, or None.

    Used to avoid stacking a fresh "no longer used" marker onto a clip on every
    subsequent run — it stays unused, and one marker saying so is enough.
    """
    for frame in sorted(markers, reverse=True):
        info = markers[frame] or {}
        custom = info.get("customData") or ""
        if not isinstance(custom, str) or not custom.startswith(UPDATE_MARKER_PREFIX):
            continue
        try:
            data = json.loads(custom[len(UPDATE_MARKER_PREFIX):])
        except (ValueError, TypeError):
            continue
        if isinstance(data, dict) and isinstance(data.get("kind"), str):
            return data["kind"]
    return None


def run_update_workflow(
    source_selection_mode: str,
    selection_method: str,
    connection_threshold: int,
    video_only: bool,
    mark_duplicates: bool,
    mark_retimed_clips: bool,
    use_xml_retime: bool,
    import_clip_names: bool,
    merge_by_source_file: bool,
    protect_graded_clips: bool,
    dry_run: bool,
    handles: int = DEFAULT_HANDLES,
    expected_target_uid: str = "",
    progress: Optional["ProgressUI"] = None,
) -> None:
    """Reconcile the current All Clips timeline against its source timelines.

    Minimal disturbance: only clips whose source range actually moved are
    rebuilt, because Resolve has no trim or move and a rebuild costs that clip
    its grade and Fusion comps. Everything else is left exactly as it is.
    """

    def _p(stage: str, current: int = 0, total: int = 0) -> None:
        if progress is not None:
            progress.set(stage, current, total)

    project_manager = resolve.GetProjectManager()  # noqa: F821
    project = project_manager.GetCurrentProject()
    if project is None:
        print("No project is open.")
        return
    media_pool = project.GetMediaPool()

    target = project.GetCurrentTimeline()
    if target is None:
        print("No current timeline. Open the Master Sources timeline you want to update.")
        REPORT.summary = "No timeline is open. Open the Master Sources timeline to update."
        return

    target_name = target.GetName()
    target_uid = ""
    uid_getter = getattr(target, "GetUniqueId", None)
    if callable(uid_getter):
        try:
            target_uid = uid_getter() or ""
        except Exception:
            target_uid = ""
    print(f"Update target: '{target_name}' (uid {target_uid or '<unavailable>'})")
    # Only ever change the timeline the window named. An update acts on the
    # open timeline, so if that changed since the window opened (or since the
    # dry run that Apply update repeats), stop rather than change another one.
    if expected_target_uid and target_uid and target_uid != expected_target_uid:
        print(f"STOPPED: the open timeline is now '{target_name}', not the one the "
              f"window named. Nothing was changed.")
        REPORT.title = f"{SCRIPT_TITLE}: update stopped - {local_now_str()}"
        REPORT.summary = (f"Stopped: the open timeline is now '{target_name}', not the "
                          f"timeline this update was set up for. Nothing was changed. "
                          f"Open the right timeline and run the update again.")
        return

    manifest, store = read_manifest(target)
    adopted = manifest is None
    forked = False

    # Handles are fixed when the master is built: an update keeps that length so
    # its segments stay comparable. A master from before handles has 0; a
    # timeline being adopted takes the length from the window.
    if manifest is not None:
        handles = int(((manifest.get("settings") or {}).get("handles")) or 0)
    print(f"Handles: {handles} frame(s) each side.")

    # Preserve Source Track Layout is a create-time layout, so update mode has
    # no value of its own to record: carry the recorded one forward rather than
    # stamping this run's False over it and losing the note it drives below.
    current_settings = build_settings_record(
        connection_threshold=connection_threshold,
        merge_by_source_file=merge_by_source_file,
        video_only=video_only,
        use_xml_retime=use_xml_retime,
        import_clip_names=import_clip_names,
        mark_duplicates=mark_duplicates,
        mark_retimed_clips=mark_retimed_clips,
        preserve_track_layout=bool(
            ((manifest or {}).get("settings") or {}).get("preserve_track_layout")),
        handles=handles,
    )

    if manifest is None:
        print("This timeline carries no Master Sources manifest.")
        if source_selection_mode == "Recorded":
            print("  Nothing records where its clips came from, so there is nothing "
                  "to re-read. Pick the approved edits to adopt this timeline, "
                  "or use the Create Sources Timeline tab instead.")
            REPORT.summary = ("This timeline has no record of its approved edits. "
                              "Nothing was changed.")
            return
        print("  ADOPTING this timeline — it is updated from the approved edits you picked.")
    else:
        print(f"Manifest found via {store}: run {manifest.get('run_counter', 0)}, "
              f"last {manifest.get('last_run_utc', '?')}, "
              f"{len(manifest.get('sources') or [])} recorded approved edit(s)")
        recorded = manifest.get("settings") or {}
        for key in ("connection_threshold", "merge_by_source_file",
                    "use_xml_retime"):
            if key in recorded and recorded[key] != current_settings[key]:
                print(f"  WARNING: {key} changed since the last run "
                      f"({recorded[key]!r} -> {current_settings[key]!r}). Merged "
                      f"ranges will differ and many clips may read as changed.")
        if recorded.get("preserve_track_layout"):
            print("  NOTE: this timeline was built with Preserve Source Track "
                  "Layout. Update mode reconciles by clip identity only — block "
                  "boundaries are not re-derived.")
        if target_uid and manifest.get("timeline_uid") \
                and manifest["timeline_uid"] != target_uid:
            print("  NOTE: this is a copy of the timeline the manifest was written "
                  "for. Taking it over; the history is kept.")
            forked = True

    # Build the pre-21.0.4 name fallback map once, for resolve_source_timelines.
    project_timelines = {}
    try:
        timeline_count = project.GetTimelineCount()
    except Exception:
        timeline_count = 0
    for index in range(1, (timeline_count or 0) + 1):
        try:
            tl = project.GetTimelineByIndex(index)
        except Exception:
            tl = None
        if tl is not None:
            project_timelines[tl.GetName()] = tl

    # ---- source timelines -------------------------------------------------
    sources = []
    if manifest is not None and source_selection_mode in ("Recorded", "Union"):
        recorded_sources, missing = resolve_timelines_by_source_record(
            project, manifest.get("sources") or [])
        sources.extend(recorded_sources)
        if missing:
            print(f"  WARNING: {len(missing)} recorded approved edit(s) no longer "
                  f"resolve: {', '.join(missing)}")
            print("  Every shot that came only from them will be reported as no "
                  "longer used. Cancel now if that is not what you meant.")

    if manifest is None or source_selection_mode in ("Selection", "Union"):
        sources.extend(resolve_source_timelines(
            media_pool, selection_method, project_timelines, progress_cb=_p))

    unique_sources = []
    seen_keys = set()
    for name, timeline in sources:
        record = timeline_source_record(name, timeline)
        if target_uid and record["uid"] == target_uid:
            print(f"  Skipping '{name}': that is the timeline being updated.")
            continue
        key = record["uid"] or f"name:{name}"
        if key in seen_keys:
            continue
        seen_keys.add(key)
        unique_sources.append((name, timeline))

    if not unique_sources:
        print("No approved edits to read. Nothing to do.")
        REPORT.summary = ("No approved edits found: select them in the Media Pool, "
                          "or open the bin that holds them. Nothing was changed.")
        return
    print(f"Reading {len(unique_sources)} approved edit(s): "
          f"{', '.join(name for name, _tl in unique_sources)}")

    # Compare this run's source set against the recorded one. In "Current
    # selection" mode the recorded list is not otherwise consulted, so dropping a
    # source by forgetting to select it would silently mark every shot that came
    # only from it as no longer used. Edit changes usually arrive as a new
    # version of a timeline rather than an edit to the old one, so replacing the
    # source set is the normal path — and quietly losing an unrelated source
    # along with it is the accident worth catching.
    recorded_records = (manifest.get("sources") or []) if manifest else []
    if recorded_records:
        recorded_names = {}
        for record in recorded_records:
            key = record.get("uid") or f"name:{record.get('name', '')}"
            recorded_names[key] = record.get("name") or "?"
        current_names = {}
        for name, timeline in unique_sources:
            record = timeline_source_record(name, timeline)
            current_names[record["uid"] or f"name:{name}"] = name

        kept = [n for k, n in recorded_names.items() if k in current_names]
        dropped = [n for k, n in recorded_names.items() if k not in current_names]
        added = [n for k, n in current_names.items() if k not in recorded_names]

        print(f"Approved edits: {len(kept)} kept, {len(added)} added, "
              f"{len(dropped)} dropped")
        if added:
            print(f"  added:   {', '.join(added)}")
        if dropped:
            print(f"  DROPPED: {', '.join(dropped)}")
            print("  WARNING: those approved edits were used last time and are not part of this "
                  "run. Every shot that came only from them will be reported as "
                  "no longer used. If you meant to replace one version of an edit "
                  "with another, that is expected — if you simply forgot to "
                  "pick one, cancel and include it.")

    # ---- desired state ----------------------------------------------------
    all_clip_infos, _blocks, _dup_count = collect_desired_clips(
        unique_sources,
        connection_threshold=connection_threshold,
        mark_duplicates=mark_duplicates,
        mark_retimed_clips=mark_retimed_clips,
        use_xml_retime=use_xml_retime,
        import_clip_names=import_clip_names,
        merge_by_source_file=merge_by_source_file,
        sorting_method="Source Name",
        handles=handles,
        progress_cb=_p,
    )
    if not all_clip_infos:
        return

    for clip_info in all_clip_infos:
        clip_info.start_frame, clip_info.end_frame = clamp_desired_to_media(clip_info)

    # ---- current state ----------------------------------------------------
    _p("Scanning the timeline...", 0, 0)
    placed_by_identity, unmanaged = scan_timeline_placements(
        target, merge_by_source_file)
    placed_total = sum(len(v) for v in placed_by_identity.values())
    print(f"Scanned {placed_total} placed clip(s) on '{target_name}'")
    if unmanaged:
        print(f"NOTE: {len(unmanaged)} timeline item(s) have no source clip "
              f"(titles, generators, compound or Fusion clips). Left untouched.")

    desired_by_identity = group_desired_by_identity(
        all_clip_infos, merge_by_source_file)
    diffs = diff_desired_vs_placed(desired_by_identity, placed_by_identity)
    counts = summarise_diffs(diffs)

    run_no = (manifest.get("run_counter", 0) if manifest else 0) + 1
    now_local = local_now_str()
    now_utc = utc_now_iso()

    # Shrinking frees space a later grow can use, so range changes are applied
    # by net duration change ascending: every shortening before any lengthening.
    def _net_change(diff):
        old = diff.placed.source_end - diff.placed.source_start
        new = diff.clip_info.end_frame - diff.clip_info.start_frame
        return new - old

    changed = sorted(
        [d for d in diffs if d.kind in ("extended", "shortened", "both")],
        key=_net_change)
    added = [d for d in diffs if d.kind == "new"]

    # A shot that dropped out stays dropped. Once it carries a marker saying so,
    # it is not actionable again — otherwise every later run would report it and
    # stack another marker on it.
    removed = []
    already_flagged = 0
    for diff in diffs:
        if diff.kind != "dropped":
            continue
        if previous_update_kind(normalised_markers(diff.placed.item)) in (
                "dropped", "superseded"):
            already_flagged += 1
        else:
            removed.append(diff)

    print("")
    print(f"=== Update plan for '{target_name}' (run {run_no}) ===")
    print(f"  acting on growth over {UPDATE_CHANGE_TOLERANCE}f; shots are never "
          f"shortened")
    print(f"  unchanged      {counts.get('unchanged', 0)}")
    print(f"  extended       {counts.get('extended', 0)}")
    print(f"  shortened      {counts.get('shortened', 0)}")
    print(f"  both ends      {counts.get('both', 0)}")
    print(f"  new            {len(added)}")
    kept = [d for d in diffs if d.kept_frames]
    print(f"  kept long      {len(kept)}  (the edit uses fewer frames; the master "
          f"keeps them)")
    print(f"  no longer used {len(removed)}")
    if already_flagged:
        print(f"  ({already_flagged} already flagged as unused by an earlier run)")
    for diff in diffs:
        if diff.kind == "unchanged" and not diff.kept_frames:
            continue
        if diff.kind == "unchanged":
            print(f"  = kept      {diff.placed.name or diff.identity} "
                  f"{diff.placed.source_start}-{diff.placed.source_end} "
                  f"(edit now uses fewer frames)")
        elif diff.kind == "new":
            print(f"  + new       {diff.clip_info.media_pool_item.GetName()} "
                  f"{diff.clip_info.start_frame}-{diff.clip_info.end_frame}")
        elif diff.kind == "dropped":
            print(f"  - unused    {diff.placed.name or diff.identity} "
                  f"{diff.placed.source_start}-{diff.placed.source_end}")
        else:
            print(f"  ~ {diff.kind:<9} {diff.placed.name or diff.identity} "
                  f"{diff.placed.source_start}-{diff.placed.source_end} -> "
                  f"{diff.clip_info.start_frame}-{diff.clip_info.end_frame} "
                  f"(head {-diff.head_delta:+d}f, tail {diff.tail_delta:+d}f)")
    print("")

    source_records = [timeline_source_record(n, t) for n, t in unique_sources]

    def _save_manifest(run_record) -> None:
        """Write the manifest back. run_record=None records no run.

        A run that changed nothing still refreshes the sources, settings and
        timestamp — that is what makes adopting an already-matching timeline
        useful — but it does not bump the run counter or add to the history,
        which would fill the log with no-ops.
        """
        nonlocal manifest
        if manifest is None:
            manifest = build_manifest(target_uid, target_name, source_records,
                                      current_settings, now_utc, TOOL_VERSION)
            manifest["adopted"] = True
        else:
            manifest = dict(manifest)
            manifest["timeline_uid"] = target_uid
            manifest["timeline_name"] = target_name
            manifest["sources"] = source_records
            manifest["settings"] = current_settings
            manifest["tool_version"] = TOOL_VERSION
        if run_record is None:
            manifest["last_run_utc"] = now_utc
        else:
            manifest = manifest_add_run(manifest, run_record)
        write_manifest(target, manifest)

    REPORT.title = (f"{SCRIPT_TITLE}: update of '{target_name}' (run {run_no}) - "
                    f"{now_local}")

    def _plan_rows() -> None:
        for diff in changed:
            reference = (read_start_reference(normalised_markers(diff.placed.item))
                         or (diff.placed.source_start, FIRST_START_FRAME))
            before = start_frame_for(diff.placed.source_start, reference)
            after = start_frame_for(min(diff.placed.source_start,
                                        diff.clip_info.start_frame), reference)
            REPORT.add(diff.placed.name or diff.identity, "Would be lengthened",
                       frames_change(diff.head_delta, diff.tail_delta),
                       f"{diff.placed.source_start}-{diff.placed.source_end} -> "
                       f"{diff.clip_info.start_frame}-{diff.clip_info.end_frame}",
                       (f"start frame {before} -> {after}" if after != before
                        else ""))
        code = master_shot_code(target) if added else ""
        for diff in added:
            REPORT.add(diff.clip_info.source_name
                       or diff.clip_info.media_pool_item.GetName(),
                       "Would be added (new shot)",
                       diff.clip_info.end_frame - diff.clip_info.start_frame + 1,
                       f"{diff.clip_info.start_frame}-{diff.clip_info.end_frame}",
                       f"{SHOT_CODE_FIELD} field {code}" if code else "")
        for diff in removed:
            REPORT.add(diff.placed.name or diff.identity,
                       "Would be marked no longer used", "",
                       f"{diff.placed.source_start}-{diff.placed.source_end}",
                       "not in any approved edit; kept on the timeline")

    def _kept_rows() -> None:
        for diff in diffs:
            if diff.kept_frames and diff.kind == "unchanged":
                REPORT.add(diff.placed.name or diff.identity, "Kept full length", "",
                           f"{diff.placed.source_start}-{diff.placed.source_end}",
                           "the edit now uses fewer frames; shots are never shortened")

    actionable = changed + added + removed
    if not actionable:
        print("Nothing to do — the timeline already matches its sources.")
        if not dry_run:
            _save_manifest(None)
        if dry_run:
            REPORT.title = REPORT.title.replace(": update of", ": dry run of")
        REPORT.summary = ("Nothing to change: the timeline already matches its "
                          "approved edits.")
        _kept_rows()
        _p("Done!", 1, 1)
        return

    if dry_run:
        print("DRY RUN — nothing was changed. Untick 'Dry run' to apply this plan.")
        REPORT.title = REPORT.title.replace(": update of", ": dry run of")
        REPORT.summary = (f"Dry run - nothing was changed. The update would lengthen "
                          f"{len(changed)}, add {len(added)} new and mark "
                          f"{len(removed)} as no longer used.")
        _plan_rows()
        _kept_rows()
        REPORT.can_apply = True
        _p("Done!", 1, 1)
        return

    # ---- execute ----------------------------------------------------------
    if not project.SetCurrentTimeline(target):
        print("ERROR: could not make the target timeline current. AppendToTimeline "
              "always targets the current timeline, so this run would edit the "
              "wrong one. Aborting without changes.")
        return

    timeline_fps = None
    for getter, name in ((target, "timelineFrameRate"), (project, "timelineFrameRate")):
        try:
            raw = getter.GetSetting(name)
        except Exception:
            raw = None
        if raw:
            try:
                timeline_fps = float(raw)
            except (TypeError, ValueError):
                timeline_fps = None
            break

    timeline_start = 0
    start_getter = getattr(target, "GetStartFrame", None)
    if callable(start_getter):
        try:
            timeline_start = int(start_getter() or 0)
        except Exception:
            timeline_start = 0

    occupancy = build_track_occupancy(target)

    # Anchor the run's cursor on where the video content actually ends, not on
    # GetEndFrame(). They agree on a normally built timeline, but a timeline
    # whose clips sit before its declared start - which is what preserve-layout
    # produced before the recordFrame rebase - reports an end frame that does not
    # account for its own content, and new clips would land an hour past it.
    content_end = None
    for bounds in occupancy.values():
        for _start, bound_end in bounds:
            content_end = bound_end if content_end is None else max(content_end,
                                                                   bound_end)
    if content_end is None:
        content_end = timeline_start
        end_getter = getattr(target, "GetEndFrame", None)
        if callable(end_getter):
            try:
                content_end = int(end_getter() or timeline_start)
            except Exception:
                content_end = timeline_start
    end_frame = content_end

    # New shots and longer copies go after the end of the timeline, on the
    # track their segment belongs on (v2.00; before, a dated track was added).
    state_box = {
        "tracks_added": [],
        "cursor": end_frame + INTER_TIMELINE_GAP,
        "warned_record": False,
        "first_new_record": None,
    }
    tally = {"extended": 0, "shortened": 0, "both": 0, "new": 0, "superseded": 0,
             "dropped": 0, "skipped": 0, "failed": 0}

    def _track_for(clip_info):
        """The segment's own video track, added (named L<n>) if the master
        has fewer tracks than that."""
        track = max(1, clip_info.source_track_index or 1)
        try:
            count = int(target.GetTrackCount("video") or 0)
        except Exception:
            return None
        while count < track:
            index = add_update_track(target, f"{TRACK_NAME_PREFIX}{count + 1}")
            if index is None:
                print(f"ERROR: could not add video track {count + 1}.")
                return None
            count = index
            state_box["tracks_added"].append(index)
        occupancy.setdefault(track, [])
        return track

    def _record_placement(item, track_index, requested_record):
        """Book a placed item into the occupancy map. Returns its duration.

        recordFrame was verified to be absolute, in the same space as GetStart(),
        on 21.0.4.5. The check below stays as a guard: it is undocumented, and a
        silent frame-space change would otherwise scatter clips across the
        timeline with nothing in the log to explain it.
        """
        try:
            actual_start = int(item.GetStart())
            duration = int(item.GetDuration())
        except Exception:
            actual_start, duration = requested_record, 1
        if actual_start != requested_record and not state_box["warned_record"]:
            print(f"  WARNING: asked for record frame {requested_record} but the "
                  f"clip landed at {actual_start}. recordFrame and GetStart() "
                  f"appear to use different frame spaces on this build; "
                  f"placement may be off by {actual_start - requested_record} "
                  f"frames for the rest of this run.")
            state_box["warned_record"] = True
        insert_occupancy(occupancy.setdefault(track_index, []),
                         actual_start, actual_start + max(1, duration))
        return duration

    def _accepted_for(clip_info, achieved_start, achieved_end):
        """The desired range, but only when the placement could not reach it."""
        if achieved_start is None or achieved_end is None:
            return (clip_info.start_frame, clip_info.end_frame)
        if (abs(achieved_start - clip_info.start_frame) > UPDATE_CHANGE_TOLERANCE
                or abs(achieved_end - clip_info.end_frame) > UPDATE_CHANGE_TOLERANCE):
            return (clip_info.start_frame, clip_info.end_frame)
        return None

    def _annotate_new(item, clip_info):
        """Duplicate/retime markers and imported names for a clip we just placed."""
        try:
            source_start = int(item.GetSourceStartFrame())
            duration = int(item.GetDuration())
        except Exception:
            return
        if mark_duplicates and clip_info.duplicate_set_index is not None:
            color, text, note = build_duplicate_marker_text(clip_info)
            frame = pick_marker_frame(source_start, duration,
                                      normalised_markers(item), 0.25)
            if frame >= 0:
                try:
                    item.AddMarker(frame, color, text, note, 1, "")
                except Exception:
                    pass
        if mark_retimed_clips and clip_info.is_retimed:
            text, note = build_retime_marker_text(clip_info)
            frame = pick_marker_frame(source_start, duration,
                                      normalised_markers(item), 0.5)
            if frame >= 0:
                try:
                    item.AddMarker(frame, "Red", text, note, 1, "")
                except Exception:
                    pass
        if import_clip_names and clip_info.source_name:
            try:
                item.SetName(clip_info.source_name)
            except Exception:
                pass

    def _place_at_end(clip_info, kind, marker_name, note, record=None,
                      start_reference=None, was=None):
        """Place a segment after the end of the timeline on its own track.

        With `record` it goes there and the run's cursor is left alone (a
        composite's layers share one start); without, it goes at the cursor,
        which then moves past it. start_reference carries a superseded shot's
        1001 over to its longer copy; without one the segment starts at 1001.
        Returns (item, start frame, end of the placed segment), item None on
        failure.
        """
        track = _track_for(clip_info)
        if track is None:
            return None, None, None
        requested = state_box["cursor"] if record is None else record
        item, status, achieved_start, achieved_end = \
            append_clip_with_slip_compensation(
                media_pool, target, clip_info, video_only=video_only,
                track_index=track, record_frame=requested,
                timeline_fps=timeline_fps)
        if item is None:
            print(f"  ERROR: could not place '{clip_info.media_pool_item.GetName()}' "
                  f"at the end of {TRACK_NAME_PREFIX}{track} (status {status}).")
            return None, None, None
        duration = _record_placement(item, track, requested)
        if state_box["first_new_record"] is None:
            state_box["first_new_record"] = requested
        if record is None:
            state_box["cursor"] = requested + max(1, duration) + INTER_TIMELINE_GAP
        _annotate_new(item, clip_info)
        start_frame = FIRST_START_FRAME
        if start_reference is not None:
            try:
                first = int(item.GetSourceStartFrame())
            except Exception:
                first = clip_info.start_frame
            start_frame = start_frame_for(first, start_reference)
        if start_frame != FIRST_START_FRAME:
            note = merge_changelog(note, f"start frame {start_frame}")
        if not write_update_marker(item, kind, run_no, note, marker_name,
                                   _accepted_for(clip_info, achieved_start, achieved_end),
                                   start_frame, start_reference, was):
            start_frame = None
        return item, start_frame, requested + max(1, duration)

    def _mark_in_place(placed, kind, marker_name, note):
        write_update_marker(placed.item, kind, run_no, note, marker_name)

    skip_reasons: dict = {}
    start_frames: dict = {}  # id(diff) -> the shot's start frame after the update

    def _rebuild(diff) -> str:
        placed = diff.placed
        clip_info = diff.clip_info
        state = capture_item_state(placed.item, placed.track_index)
        label = state.name or placed.name or clip_info.media_pool_item.GetName()
        old_src = (placed.source_start, placed.source_end)
        new_src = (clip_info.start_frame, clip_info.end_frame)
        line = format_change_line(now_local, run_no, diff.head_delta,
                                  diff.tail_delta, old_src, new_src)
        history = merge_changelog(previous_update_note(state.markers), line)

        if state.linked_item_count > 0:
            print(f"  SKIP '{label}': it has linked audio. Deleting the video item "
                  f"would orphan it, and re-appending gives no control over the "
                  f"audio track. Update it by hand.")
            skip_reasons[id(diff)] = "has linked audio; lengthen it by hand"
            _mark_in_place(placed, "manual", f"Needs manual update (run {run_no})",
                           history)
            return "skipped"

        loses_work = state.fusion_comp_count > 0 or len(state.version_names) > 1
        if loses_work and protect_graded_clips:
            print(f"  SKIP '{label}': rebuilding would lose "
                  f"{state.fusion_comp_count} Fusion comp(s) and "
                  f"{len(state.version_names)} color version(s). Untick "
                  f"'Skip clips with Fusion comps or extra color versions' "
                  f"to rebuild it anyway.")
            skip_reasons[id(diff)] = (f"has {state.fusion_comp_count} Fusion comp(s) "
                                      f"and {len(state.version_names)} color "
                                      f"version(s); lengthen it by hand")
            _mark_in_place(placed, "manual", f"Needs manual update (run {run_no})",
                           history)
            return "skipped"
        if loses_work:
            print(f"  WARNING: '{label}' loses {state.fusion_comp_count} Fusion "
                  f"comp(s) and {len(state.version_names)} color version(s) — "
                  f"they cannot survive a delete and re-append.")

        new_record, new_duration, head_need, tail_need = plan_rebuild_placement(
            placed.record_start, old_src, new_src)

        bounds = occupancy.setdefault(placed.track_index, [])
        index = occupancy_index(bounds, placed.record_start)
        if index < 0:
            free_before = free_after = 0
        else:
            free_before, free_after = compute_free_space(bounds, index,
                                                         timeline_start)
        fits = fits_in_place(free_before, free_after, head_need, tail_need)
        may_widen = fits_in_place(free_before, free_after, head_need, tail_need,
                                  REBUILD_FIT_SLACK)

        reference = (read_start_reference(state.markers)
                     or (old_src[0], FIRST_START_FRAME))
        old_start_frame = start_frame_for(old_src[0], reference)

        if not fits:
            end_track = f"{TRACK_NAME_PREFIX}{max(1, clip_info.source_track_index or 1)}"
            print(f"  '{label}' needs {head_need}f before and {tail_need}f after "
                  f"but has {free_before}f/{free_after}f — placing the updated "
                  f"version at the end of {end_track} instead.")
            new_item, start_frame, _end = _place_at_end(
                clip_info, diff.kind, f"Updated (moved, run {run_no})", history,
                start_reference=reference, was=old_start_frame)
            if new_item is None:
                return "failed"
            start_frames[id(diff)] = start_frame
            _mark_in_place(placed, "superseded", f"Superseded (run {run_no})",
                           merge_changelog(
                               previous_update_note(state.markers),
                               f"{now_local}{CHANGELOG_SEPARATOR}run {run_no}"
                               f"{CHANGELOG_SEPARATOR}superseded by the updated "
                               f"copy at the end of {end_track}"))
            return "superseded"

        original_mpi = None
        try:
            original_mpi = placed.item.GetMediaPoolItem()
        except Exception:
            original_mpi = None

        if index >= 0:
            bounds.pop(index)
        try:
            deleted = target.DeleteClips([placed.item], False)
        except Exception:
            deleted = False
        if not deleted:
            print(f"  ERROR: DeleteClips failed for '{label}'; leaving it alone.")
            if index >= 0:
                insert_occupancy(bounds, placed.record_start, placed.record_end)
            return "failed"

        item, status, achieved_start, achieved_end = \
            append_clip_with_slip_compensation(
                media_pool, target, clip_info, video_only=video_only,
                track_index=placed.track_index, record_frame=new_record,
                timeline_fps=timeline_fps, allow_widening=may_widen)

        if item is None:
            print(f"  ERROR: re-append failed for '{label}' (status {status}); "
                  f"restoring the previous version.")
            rollback = ClipInfo(media_pool_item=original_mpi or clip_info.media_pool_item,
                                start_frame=old_src[0], end_frame=old_src[1])
            back, back_status, _bs, _be = append_clip_with_slip_compensation(
                media_pool, target, rollback, video_only=video_only,
                track_index=placed.track_index, record_frame=placed.record_start,
                timeline_fps=timeline_fps)
            if back is None:
                print(f"  ERROR: rollback ALSO failed for '{label}'. The clip is "
                      f"gone from the timeline. Re-add "
                      f"{old_src[0]}-{old_src[1]} on track "
                      f"{placed.track_index} at frame {placed.record_start}.")
            else:
                _record_placement(back, placed.track_index, placed.record_start)
                restore_item_state(back, state, old_src[0], old_src[1],
                                   UPDATE_MARKER_PREFIX)
            return "failed"

        _record_placement(item, placed.track_index, new_record)
        # The old start frame marker is left behind: a new one replaces it.
        restored = restore_item_state(item, state, new_src[0], new_src[1],
                                      (UPDATE_MARKER_PREFIX, START_MARKER_PREFIX))
        if restored["markers_dropped"]:
            print(f"  {restored['markers_dropped']} marker(s) on '{label}' fell "
                  f"outside the new range and were not restored.")
        _annotate_new(item, clip_info)
        try:
            first = int(item.GetSourceStartFrame())
        except Exception:
            first = new_src[0]
        start_frame = start_frame_for(first, reference)
        if start_frame != old_start_frame:
            history = merge_changelog(
                history, f"start frame {old_start_frame} -> {start_frame}")
        if write_update_marker(item, diff.kind, run_no, history,
                               f"Updated ({diff.kind}, run {run_no})",
                               _accepted_for(clip_info, achieved_start, achieved_end),
                               start_frame, reference, old_start_frame):
            start_frames[id(diff)] = start_frame
        return diff.kind

    total_steps = len(changed) + len(added) + len(removed)
    step = 0

    print(f"Applying {len(changed)} range change(s)...")
    for diff in changed:
        step += 1
        _p(f"Updating: {diff.placed.name or diff.identity}", step, total_steps)
        outcome = _rebuild(diff)
        tally[outcome] = tally.get(outcome, 0) + 1
        end_track = f"{TRACK_NAME_PREFIX}{max(1, diff.clip_info.source_track_index or 1)}"
        what = {"superseded": f"Longer copy added at the end of {end_track}",
                "skipped": "Needs manual update",
                "failed": "Failed - see the console"}.get(outcome, "Lengthened in place")
        note = skip_reasons.get(id(diff), "")
        if outcome == "superseded":
            note = "the original is marked Superseded"
        if start_frames.get(id(diff)) not in (None, FIRST_START_FRAME):
            note = ", ".join(part for part in (
                note, f"start frame {start_frames[id(diff)]}") if part)
        REPORT.add(diff.placed.name or diff.identity, what,
                   frames_change(diff.head_delta, diff.tail_delta),
                   f"{diff.placed.source_start}-{diff.placed.source_end} -> "
                   f"{diff.clip_info.start_frame}-{diff.clip_info.end_frame}", note)

    # New shots go at the end in blocks: the layers of a new composite are
    # stacked at one start, like Create does it. They get the master's client
    # code in their Shot field, like the shots the Shot Namer already did.
    shot_code = master_shot_code(target) if added else ""
    print(f"Adding {len(added)} new shot(s)...")
    diff_of = {id(diff.clip_info): diff for diff in added}
    group_members: dict = {}
    for ci in all_clip_infos:
        if ci.composite_group is not None:
            group_members.setdefault(ci.composite_group, []).append(ci)
    for block in composite_blocks([diff.clip_info for diff in added]):
        block_start, track_cursor = state_box["cursor"], {}
        for clip_info in block:
            diff = diff_of[id(clip_info)]
            step += 1
            name = clip_info.media_pool_item.GetName()
            _p(f"Adding: {name}", step, total_steps)
            track = max(1, clip_info.source_track_index or 1)
            record = track_cursor.get(track, block_start)
            note = (f"{now_local}{CHANGELOG_SEPARATOR}run {run_no}"
                    f"{CHANGELOG_SEPARATOR}new shot"
                    f"{CHANGELOG_SEPARATOR}"
                    f"{clip_info.start_frame}-{clip_info.end_frame}")
            item, start_frame, placed_end = _place_at_end(
                clip_info, "new", f"New (run {run_no})", note, record=record)
            if item is not None:
                track_cursor[track] = placed_end
            tally["new" if item is not None else "failed"] += 1
            notes = ["new shot"]
            if item is not None and shot_code:
                media = clip_info.media_pool_item
                try:
                    if (media.GetMetadata(SHOT_CODE_FIELD) or "") == shot_code or \
                            media.SetMetadata({SHOT_CODE_FIELD: shot_code}):
                        notes.append(f"{SHOT_CODE_FIELD} field {shot_code}")
                        tally["coded"] = tally.get("coded", 0) + 1
                except Exception:
                    pass
            if clip_info.composite_group is not None:
                # Layers already in the master can't move to stack with it.
                others = [ci.source_name or ci.media_pool_item.GetName()
                          for ci in group_members.get(clip_info.composite_group, [])
                          if id(ci) not in diff_of]
                if others:
                    notes.append("composited in the edit with "
                                 + summarise_names(others, 3) + " (already in the master)")
            REPORT.add(clip_info.source_name or name,
                       (f"Added at the end of {TRACK_NAME_PREFIX}{track}"
                        if item is not None else "Failed - see the console"),
                       clip_info.end_frame - clip_info.start_frame + 1,
                       f"{clip_info.start_frame}-{clip_info.end_frame}",
                       ", ".join(notes))
        if track_cursor:
            state_box["cursor"] = max(track_cursor.values()) + INTER_TIMELINE_GAP

    print(f"Marking {len(removed)} shot(s) that are no longer used...")
    for diff in removed:
        step += 1
        _p(f"Marking unused: {diff.placed.name or diff.identity}", step, total_steps)
        markers = normalised_markers(diff.placed.item)
        note = merge_changelog(
            previous_update_note(markers),
            f"{now_local}{CHANGELOG_SEPARATOR}run {run_no}"
            f"{CHANGELOG_SEPARATOR}no longer used in any approved edit")
        if write_update_marker(diff.placed.item, "dropped", run_no, note,
                               f"No longer used (run {run_no})"):
            tally["dropped"] += 1
        REPORT.add(diff.placed.name or diff.identity, "Marked no longer used", "",
                   f"{diff.placed.source_start}-{diff.placed.source_end}",
                   "not in any approved edit; kept on the timeline")
    _kept_rows()

    # ---- record the run ---------------------------------------------------
    run_record = {
        "n": run_no,
        "utc": now_utc,
        "tracks_added": state_box["tracks_added"],
        "unchanged": counts.get("unchanged", 0),
        "extended": tally.get("extended", 0),
        "shortened": tally.get("shortened", 0),
        "both": tally.get("both", 0),
        "new": tally.get("new", 0),
        "superseded": tally.get("superseded", 0),
        "dropped": tally.get("dropped", 0),
        "skipped": tally.get("skipped", 0),
        "failed": tally.get("failed", 0),
        "sources": [timeline_source_record(n, t)["uid"] for n, t in unique_sources],
    }
    if forked:
        run_record["forked"] = True
    _save_manifest(run_record)
    remove_empty_tracks(project, target)

    # Sit the run marker at the start of what this run added, so the ruler reads
    # as a changelog. Offset 0 is the manifest badge, hence lower=1.
    preferred_run_frame = 1
    if state_box["first_new_record"] is not None:
        preferred_run_frame = max(
            1, timeline_marker_offset(target, state_box["first_new_record"]))
    run_marker_frame = first_free_frame(normalised_markers(target),
                                        preferred_run_frame, lower=1)
    if run_marker_frame >= 0:
        try:
            target.AddMarker(
                run_marker_frame, RUN_MARKER_COLOR,
                f"Update run {run_no} - {now_local}",
                (f"{tally.get('extended', 0)} extended, "
                 f"{tally.get('shortened', 0)} shortened, "
                 f"{tally.get('both', 0)} both ends, "
                 f"{tally.get('new', 0)} new, "
                 f"{tally.get('superseded', 0)} superseded, "
                 f"{tally.get('dropped', 0)} no longer used, "
                 f"{tally.get('skipped', 0)} skipped, "
                 f"{tally.get('failed', 0)} failed.\nSources: "
                 + ", ".join(n for n, _t in unique_sources)),
                1, RUN_MARKER_PREFIX + json.dumps(
                    {"v": 1, "run": run_no, "utc": now_utc},
                    sort_keys=True, separators=(",", ":")),
            )
        except Exception:
            pass

    REPORT.summary = update_summary(tally,
                                    [n for n, _t in unique_sources])
    if tally.get("coded"):
        REPORT.summary += (f" {count_phrase(tally['coded'], 'new shot', 'new shots')} "
                           f"given the {SHOT_CODE_FIELD} field '{shot_code}'.")

    print("")
    print(f"=== Update run {run_no} complete ===")
    for key in ("extended", "shortened", "both", "new", "superseded", "dropped",
                "skipped", "failed"):
        print(f"  {key:<11} {tally.get(key, 0)}")
    if tally.get("failed"):
        print("  Check the log above for the clips that failed.")
    _p("Done!", 1, 1)
    print("Done!")


# ---------------------------------------------------------------------------
# Shot Namer
# ---------------------------------------------------------------------------

def file_stem(file_name: str) -> str:
    """'A001C003.mov' -> 'A001C003'."""
    stem, _ext = os.path.splitext(file_name or "")
    return stem or (file_name or "")


def run_shot_namer(pattern: str, start_number: int, increment: int,
                   from_playhead: bool, keep_names: bool, append_source: bool,
                   clip_color: str, shot_code: str, dry_run: bool,
                   expected_target_uid: str = "",
                   progress: Optional["ProgressUI"] = None) -> None:
    """Name the shots on the open timeline and fill in their metadata.

    A shot is every clip that overlaps in time on any video track, so the
    layers of a composite share one name. Shots whose names already match the
    pattern keep them (unless keep_names is off), and new ones continue after
    the highest number. Every clip's source file name goes into its media pool
    clip's Comments and the client code into its Shot field; the tracks are
    named L1, L2 ..., and a segment with no start frame marker gets 1001.
    """

    def _p(stage: str, current: int = 0, total: int = 0) -> None:
        if progress is not None:
            progress.set(stage, current, total)

    REPORT.title = (f"{SCRIPT_TITLE}: Shot Namer{' dry run' if dry_run else ''} - "
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    parsed = parse_shot_pattern(pattern)
    if parsed is None:
        REPORT.summary = (f"The shot pattern '{pattern}' has no # for the number "
                          f"(e.g. sh###). Nothing was changed.")
        return
    prefix, digits = parsed
    project = resolve.GetProjectManager().GetCurrentProject()  # noqa: F821
    timeline = project.GetCurrentTimeline() if project else None
    if timeline is None:
        REPORT.summary = ("No timeline is open. Open the timeline whose shots you "
                          "want to name.")
        return
    if expected_target_uid:
        try:
            uid = timeline.GetUniqueId() or ""
        except Exception:
            uid = ""
        if uid and uid != expected_target_uid:
            REPORT.summary = (f"Stopped: the open timeline is now '{timeline.GetName()}', "
                              f"not the one this window named. Nothing was changed.")
            return

    # Every clip with media on every video track (titles, generators and
    # transitions have no media pool clip and are left out), disabled ones too
    # only if they are switched on.
    _p("Reading the timeline...", 0, 0)
    entries = []
    try:
        track_count = int(timeline.GetTrackCount("video") or 0)
    except Exception:
        track_count = 0
    for track in range(1, track_count + 1):
        for item in timeline.GetItemListInTrack("video", track) or []:
            try:
                media = item.GetMediaPoolItem()
                if media is None:
                    continue
                enabled = getattr(item, "GetClipEnabled", None)
                if callable(enabled) and enabled() is False:
                    continue
                start = int(item.GetStart())
                end = start + int(item.GetDuration())
            except Exception:
                continue
            entries.append((start, end, track, (item, media)))
    if not entries:
        REPORT.summary = f"'{timeline.GetName()}' has no clips to name."
        return

    shots = group_stacks(entries)
    existing = []
    for shot in shots:
        numbers = [shot_number_in(entry[3][0].GetName(), prefix, digits) for entry in shot]
        numbers = [n for n in numbers if n is not None]
        existing.append(numbers[0] if numbers else None)
    numbers = plan_shot_numbers(existing, start_number, increment, keep_names)

    first_shot = 0
    if from_playhead:
        playhead = None
        try:
            fps = float(timeline.GetSetting("timelineFrameRate") or 24)
            parts = parse_timecode(timeline.GetCurrentTimecode() or "")
            if parts:
                h, m, sec, f, drop = parts
                playhead = timecode_to_frames(h, m, sec, f, int(round(fps)), drop)
        except Exception:
            playhead = None
        if playhead is not None:
            first_shot = next((i for i, shot in enumerate(shots)
                               if max(e[1] for e in shot) > playhead), len(shots))
            if not keep_names:
                # Numbering starts at the playhead shot, as in Shot Namer v1.
                numbers[first_shot:] = plan_shot_numbers(
                    [None] * (len(shots) - first_shot), start_number, increment, False)

    REPORT.columns = NAMER_LOG_COLUMNS
    named = kept = comments = codes = failed = 0
    code_done: set = set()
    total = len(shots) - first_shot
    for index in range(first_shot, len(shots)):
        shot, number = shots[index], numbers[index]
        _p(f"Naming {format_shot_name(prefix, digits, number)}",
           index - first_shot + 1, total)
        for start, end, track, (item, media) in shot:
            old_name = item.GetName() or ""
            try:
                file_name = media.GetClipProperty("File Name") or ""
            except Exception:
                file_name = ""
            new_name = format_shot_name(prefix, digits, number,
                                        file_stem(file_name) if append_source else "")
            keep = keep_names and shot_number_in(old_name, prefix, digits) == number
            if keep:
                new_name = old_name
            try:
                current_code = media.GetMetadata(SHOT_CODE_FIELD) or ""
            except Exception:
                current_code = ""
            shot_field = current_code
            if shot_code and current_code != shot_code:
                shot_field = (f"{shot_code} (was {current_code})" if current_code
                              else shot_code)
                if dry_run:
                    shot_field = "would be " + shot_field
            key = id(media)
            if dry_run:
                if shot_code and current_code != shot_code and key not in code_done:
                    code_done.add(key)
                    codes += 1
                what = "Keeps its name" if keep else f"Would be named (was {old_name})"
            else:
                what = "Kept its name"
                if not keep:
                    try:
                        ok = bool(item.SetName(new_name))
                    except Exception:
                        ok = False
                    what = f"Named (was {old_name})" if ok else "Rename failed"
                    failed += 0 if ok else 1
                    # Stills keep their Purple, so they still stand out.
                    if ok and not is_still_item(media):
                        if clip_color == CLEAR_COLOR:
                            item.ClearClipColor()
                        elif clip_color != KEEP_COLOR:
                            item.SetClipColor(clip_color)
                if key not in code_done:
                    # Media pool metadata: once per source file.
                    code_done.add(key)
                    comment = add_source_line(media.GetMetadata("Comments") or "", file_name)
                    if comment is not None and media.SetMetadata({"Comments": comment}):
                        comments += 1
                    if shot_code and current_code != shot_code:
                        if media.SetMetadata({SHOT_CODE_FIELD: shot_code}):
                            codes += 1
                        else:
                            shot_field = f"could not set {shot_code}"
            if keep:
                kept += 1
            else:
                named += 1
            REPORT.add(new_name, what, f"{end - start}", file_name,
                       f"{TRACK_NAME_PREFIX}{track}", shot_field)

    tracks = 0 if dry_run else name_video_tracks(timeline)
    if dry_run:
        code_text = ""
        if shot_code:
            code_text = (f" The {SHOT_CODE_FIELD} field would be set to '{shot_code}' "
                         f"on {codes} source clip(s)" + ("." if codes else
                         " (all have it already)."))
        REPORT.summary = (f"Dry run - nothing was changed. {named} clip(s) would be "
                          f"named and {kept} keep their names, in {total} shot(s) on "
                          f"'{timeline.GetName()}'.{code_text}")
        REPORT.can_apply = named > 0 or codes > 0
        return
    parts = [f"{named} clip(s) named", f"{kept} kept their names",
             f"{total} shot(s)"]
    if comments:
        parts.append(f"source name added to {comments} clip(s)' Comments")
    if shot_code:
        parts.append(f"{SHOT_CODE_FIELD} field set to '{shot_code}' on {codes} source "
                     f"clip(s)" + ("" if codes else " (all had it already)"))
    if tracks:
        parts.append(f"{tracks} track(s) renamed {TRACK_NAME_PREFIX}1, "
                     f"{TRACK_NAME_PREFIX}2 ...")
    if failed:
        parts.append(f"{failed} rename(s) failed - see the console")
    REPORT.summary = f"'{timeline.GetName()}': " + ", ".join(parts) + "."
    print(f"{SCRIPT_TITLE}: Shot Namer - " + ", ".join(parts) + ".")


# ---------------------------------------------------------------------------
# Progress UI
# ---------------------------------------------------------------------------

class ProgressUI:
    """Modeless progress window built with Resolve's UIManager.

    Fusion's UI doesn't tick during blocking Python — we call Fusion:Wait(0)
    after each update to flush pending events so the window stays responsive.
    If Wait isn't available, the label/slider values still update; refresh
    happens on the next natural event-loop tick.
    """

    def __init__(self) -> None:
        try:
            # The log's dispatcher, not one of its own: an event from a window
            # a dispatcher does not know makes that dispatcher's RunLoop raise
            # KeyError 'On', and the log's loop was flooded with this one's.
            self.ui = UI_HANDLES.get("ui") or fu.UIManager  # noqa: F821
            self.disp = UI_HANDLES.get("disp") or bmd.UIDispatcher(self.ui)  # noqa: F821
            WINDOW_COUNTER[0] += 1
            window_id = f"GenAllClipsProgress{WINDOW_COUNTER[0]}"
            self.win = self.disp.AddWindow({
                "ID": window_id,
                "WindowTitle": window_title("Progress"),
                "Geometry": centered_geometry(520, 130),
                "StyleSheet": WINDOW_STYLE,
            }, [
                self.ui.VGroup({"ID": "root", "Spacing": 8}, [
                    self.ui.Label({"ID": "StageLabel", "Text": "Starting...",
                                   "StyleSheet": HEADING_STYLE}),
                    self.ui.Slider({
                        "ID": "ProgressBar",
                        "Integer": True,
                        "Minimum": 0,
                        "Maximum": 100,
                        "Value": 0,
                    }),
                    self.ui.Label({"ID": "CounterLabel", "Text": "",
                                   "StyleSheet": HINT_STYLE}),
                ]),
            ])
            self.itm = self.win.GetItems()
            # Every window needs a handler table: without one, an event from
            # this window (it is hidden as the log opens) made the next
            # RunLoop raise KeyError 'On' and ended the script with the log.
            getattr(self.win.On, window_id).Close = lambda ev: None
            self.win.Show()
            self._tick()
            self._ok = True
        except Exception as e:
            print(f"Progress UI unavailable: {e}")
            self._ok = False

    def set(self, stage: str, current: int = 0, total: int = 0) -> None:
        if not self._ok:
            return
        try:
            self.itm["StageLabel"].Text = stage
            if total > 0:
                pct = int(100 * current / total) if total else 0
                if pct < 0:
                    pct = 0
                elif pct > 100:
                    pct = 100
                self.itm["ProgressBar"].Value = pct
                self.itm["CounterLabel"].Text = f"{current} / {total}  ({pct}%)"
            else:
                self.itm["ProgressBar"].Value = 0
                self.itm["CounterLabel"].Text = ""
        except Exception:
            pass
        self._tick()

    def _tick(self) -> None:
        try:
            fusion = bmd.scriptapp("Fusion")  # noqa: F821
            if fusion is not None:
                fusion.Wait(0)
        except Exception:
            pass

    def close(self) -> None:
        if not self._ok:
            return
        try:
            self.win.Hide()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# UI Dialog
# ---------------------------------------------------------------------------

def build_and_show_ui(start_mode: Optional[str] = None) -> Optional[dict]:
    """Build the UI dialog and return user selections, or None if cancelled.

    start_mode opens it on that tab instead of the remembered one (the Shot
    Namer after a Create).
    """
    # fu and bmd are pre-injected globals in Resolve's scripting environment.
    # One dispatcher for every window (see v1.33), so a reopened main window
    # shares it with the logs.
    ui = UI_HANDLES.get("ui") or fu.UIManager  # noqa: F821
    disp = UI_HANDLES.get("disp") or bmd.UIDispatcher(ui)  # noqa: F821
    WINDOW_COUNTER[0] += 1
    window_id = f"MainWin{WINDOW_COUNTER[0]}"
    # Just taller than the tallest page (Update, measured in Resolve 21.1.2):
    # the window must open at its real height, because one that Qt grows to
    # fit after it opens is not redrawn below where it first ended.
    width, height = 600, 529
    geometry = centered_geometry(width, height)
    settings = load_settings()
    if start_mode:
        settings["mode"] = start_mode

    # Look at the current timeline up front so update mode can say what it would
    # be updating, what it was last built from, and offer the settings it was
    # last built with.
    target_label = "Open the Master Sources timeline you want to update first."
    namer_label = "Open the timeline whose shots you want to name first."
    target_uid = ""
    last_built_label = ""
    recorded_settings: dict = {}
    try:
        _project = resolve.GetProjectManager().GetCurrentProject()  # noqa: F821
        _target = _project.GetCurrentTimeline() if _project else None
    except Exception:
        _target = None
    if _target is not None:
        try:
            _manifest, _store = read_manifest(_target)
            _name = _target.GetName()
        except Exception:
            _manifest, _name = None, "?"
        try:
            target_uid = _target.GetUniqueId() or ""
        except Exception:
            target_uid = ""
        namer_label = f"Names the shots on the open timeline '{_name}'."
        if _manifest:
            recorded_settings = _manifest.get("settings") or {}
            runs = _manifest.get("run_counter", 0)
            target_label = (f"Updates the open timeline '{_name}' "
                            + (f"(last updated in run {runs})." if runs
                               else "(built, not updated yet)."))
            last_built_label = "Last built from: " + summarise_names(
                [s.get("name") or "?" for s in _manifest.get("sources") or []])
        else:
            target_label = f"Updates the open timeline '{_name}'."
            last_built_label = ("This timeline has no record of where it came from "
                                "yet; this update builds one from your pick.")

    def row(label, *widgets, label_id=None):
        props = {"Text": label, "MinimumSize": [LABEL_W, 0], "MaximumSize": [LABEL_W, 100]}
        if label_id:
            props["ID"] = label_id
        return ui.HGroup({"Weight": 0}, [ui.Label(props)] + list(widgets))

    def heading(title):
        return ui.Label({"Text": title.upper(), "Weight": 0, "StyleSheet": HEADING_STYLE})

    def section(title, first=False):
        """A section's heading, with the divider line above it (not on the
        first section of a page). The line is the heading's own top border: an
        empty divider label inside a tab page keeps a text line's height with
        the line drawn at its top, so the space under the line came out twice
        the space above it (measured in Resolve 21.1.2, v2.03)."""
        if first:
            return [heading(title)]
        return [ui.Label({"Text": title.upper(), "Weight": 0,
                          "StyleSheet": HEADING_STYLE + SECTION_LINE_STYLE})]

    def check(widget_id, text, checked, tooltip=None):
        props = {"ID": widget_id, "Text": text, "Checked": checked, "Weight": 0}
        if tooltip:
            props["ToolTip"] = wrap_tip(tooltip)
        return ui.CheckBox(props)

    def hint(widget_id, text, lines=1):
        """A small grey note; a wrapped one is given room for its lines, or
        its last line is cut off."""
        props = {"ID": widget_id, "Text": text, "Weight": 0, "WordWrap": lines > 1,
                 "StyleSheet": HINT_STYLE}
        if lines > 1:
            props["MinimumSize"] = [0, 16 * lines]
        return ui.Label(props)

    # Create and Update both read the approved edits, each with its own copy of
    # those options (suffix C or U): a widget can only be on one page.
    def approved_edits_rows(sfx):
        return [
            row("Pick them from", ui.ComboBox({
                "ID": "selectionMethod" + sfx,
                "ToolTip": wrap_tip("Which approved edits to read.\n\n"
                           "Current bin: every timeline directly in the bin that is "
                           "open in the Media Pool (not in bins inside it). Keep "
                           "your approved timelines there and move old versions out.\n\n"
                           "Media Pool selection: only the timelines you have "
                           "selected in the Media Pool.")})),
            hint("pickHint" + sfx, PICK_FROM_HINTS.get(settings["pick_from"], ""), 2),
        ]

    join_tip = ("When the edit uses the same source more than once, the master "
                "normally gets a separate segment for each use. If no more than "
                "this many frames are left out between two uses, they are "
                "joined into one segment that covers both, including the frames "
                "in between.\n\n"
                "Example: frames 100-200 and 210-300 of one clip leave 9 frames "
                "out (201-209), so at 24 they become one segment, 100-300.\n\n"
                "Higher joins more (fewer, longer segments); 0 joins only uses "
                "that touch or overlap.")

    def sources_rows(sfx, threshold):
        return [
            row("Join gaps up to", ui.LineEdit({
                "ID": "ConnectionThreshold" + sfx, "Text": str(threshold),
                "PlaceholderText": str(DEFAULT_CONNECTION_THRESHOLD),
                "MaximumSize": [80, 100], "ToolTip": wrap_tip(join_tip)}),
                ui.Label({"Text": "frames (merges nearby segments into one clip)",
                          "StyleSheet": HINT_STYLE})),
        ]

    def markers_rows(sfx, duplicates, retimed):
        return [
            check("markDuplicates" + sfx, "Mark duplicate sources with colored markers",
                  duplicates, (
                      "A source file on disk that ends up in the master more than "
                      "once, as separate segments, gets the same colored marker on "
                      "each segment: Dup Set #2 (1/3) is segment 1 of 3 from set 2.")),
            check("markRetimedClips" + sfx, "Mark retimed clips with red markers", retimed),
        ]

    dry_run_tip = ("Lists exactly what would be named, lengthened, added or marked "
                   "unused, and writes nothing at all.\n\n"
                   "Resolve's undo stack is not scriptable, so a run "
                   "cannot be undone as a single step. Run this first.")

    # An update offers the settings the timeline was last built with: changing
    # the join gaps between runs reshapes nearly every merged range, which
    # would read as "everything changed".
    update_threshold = recorded_settings.get("connection_threshold",
                                             settings["connection_threshold"])
    update_duplicates = bool(recorded_settings.get("mark_duplicates",
                                                   settings["mark_duplicates"]))
    update_retimed = bool(recorded_settings.get("mark_retimed_clips",
                                                settings["mark_retimed_clips"]))

    create_page = (
        section("1. Approved edits", first=True) + approved_edits_rows("C")
        + section("2. New master sources timeline") + [
            row("Timeline name", ui.LineEdit({
                "ID": "DstTimelineName", "Text": settings["timeline_name"],
                "PlaceholderText": "Master_Sources"})),
            row("Sort clips by", ui.ComboBox({"ID": "sortingMethod", "ToolTip": wrap_tip(
                "Source Name: by clip name.\n\n"
                "Source Timecode: in the order the shots were recorded.\n\n"
                f"{EDIT_ORDER}: in the order the shots first appear in the "
                "edit, for a master built from one timeline (a film). With "
                "several edits the first edit's order comes first.\n\n"
                "Still images always go at the end.")})),
            row("Handles", ui.LineEdit({
                "ID": "Handles", "Text": str(settings["handles"]),
                "PlaceholderText": str(DEFAULT_HANDLES), "MaximumSize": [80, 100],
                "ToolTip": wrap_tip(
                    "Extra source frames added before and after every segment, so "
                    "Deliver's Individual clips export includes them without its "
                    "own handle setting.\n\n"
                    "They are plain source frames (the master plays at normal "
                    "speed), so 10 means 10 even on a retimed shot. Handles stop "
                    "at the start and end of the media, and handles that overlap "
                    "join into one segment.\n\n"
                    "Update keeps the handle length the master was built with.")}),
                ui.Label({"Text": "frames each side", "StyleSheet": HINT_STYLE})),
        ]
        + section("3. Segment merging") + sources_rows("C", settings["connection_threshold"])
        + section("4. Markers") + markers_rows("C", settings["mark_duplicates"],
                                               settings["mark_retimed_clips"])
    )
    namer_page = (
        section("1. Shot names", first=True) + [
            row("Shot pattern", ui.LineEdit({
                "ID": "NamerPattern", "Text": settings["namer_pattern"],
                "PlaceholderText": "sh###", "MaximumSize": [160, 100],
                "ToolTip": wrap_tip("# is a digit: sh### gives sh010, sh020 ...")}),
                ui.Label({"Text": "# = digit, e.g. sh### -> sh010",
                          "StyleSheet": HINT_STYLE})),
            row("Start at", ui.LineEdit({
                "ID": "NamerStart", "Text": str(settings["namer_start"]),
                "MaximumSize": [80, 100]}),
                ui.Label({"Text": "  Increment", "Weight": 0}),
                ui.LineEdit({"ID": "NamerIncrement", "Text": str(settings["namer_increment"]),
                             "MaximumSize": [80, 100]}),
                ui.HGap(0, 1)),
            check("namerKeepNames", "Keep shot names already given (new shots continue "
                  "after the highest number)", settings["namer_keep_names"], (
                      "On (default): a shot whose clips are already named from the "
                      "pattern keeps its name, and shots without one are numbered "
                      "after the highest number on the timeline, so an update's "
                      "new shots follow on.\n\nOff: every shot is numbered again "
                      "from Start at.")),
            check("namerFromPlayhead", "Start from the shot under the playhead",
                  settings["namer_from_playhead"], (
                      "Clips stacked on L1, L2 ... are one shot, with one name.")),
        ]
        + section("2. Clip info") + [
            row("Client code", ui.LineEdit({
                "ID": "NamerCode", "Text": settings["namer_code"],
                "PlaceholderText": "e.g. cfa", "MaximumSize": [120, 100],
                "ToolTip": wrap_tip(
                    "A short code for the client or spot, e.g. cfa for Chick-fil-A.\n\n"
                    f"Written into every clip's {SHOT_CODE_FIELD} metadata field, so "
                    "Deliver's file name can start with it: use the %{Shot} token. "
                    "Leave it empty to leave the field alone.")}),
                ui.Label({"Text": "Shot field, for %{Shot} in Deliver",
                          "StyleSheet": HINT_STYLE})),
            row("Clip color", ui.ComboBox({"ID": "NamerClipColor", "MaximumSize": [180, 100]}),
                ui.HGap(0, 1)),
            check("namerAppendSource", "Append the source file name (sh010_A001C003)",
                  settings["namer_append_source"]),
        ]
        + section("3. Check first") + [
            # Not remembered: a run should be a real one unless asked each time.
            check("dryRunN", "Dry run (report the plan, change nothing)", False,
                  dry_run_tip),
        ]
    )
    update_page = (
        [hint("updateNote", UPDATE_NOTE, 1), ui.VGap(2, 0)]
        + section("1. Approved edits", first=True) + approved_edits_rows("U")
        + ([hint("lastBuiltLabel", last_built_label, 2)] if last_built_label else [])
        + section("2. Segment merging") + sources_rows("U", update_threshold)
        + section("3. Markers") + markers_rows("U", update_duplicates, update_retimed)
        + section("4. Update safety") + [
            check("protectGradedClips",
                  "Skip clips with Fusion comps or extra color versions",
                  settings["protect_graded_clips"], (
                      "Resolve has no trim or move, so changing a clip's range "
                      "means deleting and re-appending it. Its name, color, "
                      "flags and markers are put back, but its grade and any "
                      "Fusion comps cannot be — there is no API to read a grade "
                      "back out.\n\n"
                      "When ON (default): a clip carrying a Fusion comp or more "
                      "than one color version is left alone and marked for "
                      "manual attention instead.\n\n"
                      "When OFF: it is rebuilt anyway and that work is lost.")),
            check("dryRunU", "Dry run (report the plan, change nothing)", False,
                  dry_run_tip),
        ]
    )

    def page(page_rows):
        return ui.VGroup({"Spacing": 4}, page_rows + [ui.VGap(0, 1)])

    rows = [
        ui.TabBar({"ID": "modeTabs", "Weight": 0, "DrawBase": False}),
        ui.Label({"ID": "targetLabel", "Text": target_label, "Weight": 0,
                  "StyleSheet": HINT_STYLE}),
        ui.VGap(4, 0),
        # One page per tab; the window is as tall as the tallest page.
        ui.Stack({"ID": "pages", "Weight": 1},
                 [page(create_page), page(namer_page), page(update_page)]),
        # RecalcLayout() shrinks the window to its narrowest rows; this line
        # holds it at its full width.
        ui.VGap(SECTION_GAP_ABOVE, 0),
        ui.Label({"Weight": 0, "Text": "", "StyleSheet": DIVIDER_STYLE,
                  "MinimumSize": [geometry[2] - 24, 1], "MaximumSize": [4000, 1]}),
        ui.VGap(SECTION_GAP_BELOW, 0),
        ui.HGroup({"Weight": 0}, [             # buttons: Cancel + main right
            ui.HGap(0, 1),
            ui.Button({"ID": "Cancel", "Text": "Cancel", "Weight": 0}),
            # Wide enough for Create / Name Shots / Dry Run: the label changes with
            # the tab after the window is laid out.
            ui.Button({"ID": "Run", "Text": "Create", "Weight": 0, "Default": True,
                       "StyleSheet": "QPushButton { min-width: 96px; }"}),
        ]),
    ]

    UI_HANDLES["ui"], UI_HANDLES["disp"] = ui, disp
    win = disp.AddWindow(
        {"ID": window_id, "WindowTitle": window_title(),
         "Geometry": geometry, "WindowFlags": ON_TOP_FLAGS, "StyleSheet": WINDOW_STYLE},
        ui.VGroup({"Spacing": 4}, rows),
    )

    run_export = {"value": False}

    def on_close(ev):
        disp.ExitLoop()
        run_export["value"] = False

    def on_go(ev):
        disp.ExitLoop()
        run_export["value"] = True

    getattr(win.On, window_id).Close = on_close
    win.On.Cancel.Clicked = on_close
    win.On.Run.Clicked = on_go

    itm = win.GetItems()

    # Populate combo boxes, then select the remembered choices
    for _mode, tab_label in MODE_TABS:
        itm["modeTabs"].AddTab(tab_label)
    for sfx in ("C", "U"):
        for label, _value in PICK_FROM:
            itm["selectionMethod" + sfx].AddItem(label)
        itm["selectionMethod" + sfx].CurrentText = settings["pick_from"]
    for method in SORT_METHODS:
        itm["sortingMethod"].AddItem(method)
    itm["sortingMethod"].CurrentText = settings["sorting_method"]
    for color in [KEEP_COLOR] + CLIP_COLORS + [CLEAR_COLOR]:
        itm["NamerClipColor"].AddItem(color)
    itm["NamerClipColor"].CurrentText = settings["namer_clip_color"]

    def _set(widget_id: str, attr: str, value) -> None:
        """UIManager silently ignores some properties on some builds."""
        try:
            setattr(itm[widget_id], attr, value)
        except Exception:
            pass

    def current_mode():
        index = itm["modeTabs"].CurrentIndex
        return MODE_TABS[index][0] if 0 <= index < len(MODE_TABS) else MODE_CREATE

    def dry_run_box():
        return {MODE_NAMER: "dryRunN", MODE_UPDATE: "dryRunU"}.get(current_mode())

    def run_label():
        mode = current_mode()
        if mode == MODE_CREATE:
            return "Create"
        if itm[dry_run_box()].Checked:
            return "Dry Run"
        return "Name Shots" if mode == MODE_NAMER else "Update"

    def on_mode(ev):
        mode = current_mode()
        _set("pages", "CurrentIndex", itm["modeTabs"].CurrentIndex)
        # What the tab works on: a new timeline, or the open one.
        _set("targetLabel", "Text", {MODE_CREATE: CREATE_LABEL,
                                     MODE_NAMER: namer_label}.get(mode, target_label))
        _set("Run", "Text", run_label())

    def on_dry_run(ev):
        _set("Run", "Text", run_label())

    def on_pick_from(ev):
        for sfx in ("C", "U"):
            _set("pickHint" + sfx, "Text",
                 PICK_FROM_HINTS.get(itm["selectionMethod" + sfx].CurrentText, ""))

    win.On.modeTabs.CurrentChanged = on_mode
    win.On.dryRunN.Clicked = on_dry_run
    win.On.dryRunU.Clicked = on_dry_run
    win.On.selectionMethodC.CurrentIndexChanged = on_pick_from
    win.On.selectionMethodU.CurrentIndexChanged = on_pick_from
    itm["modeTabs"].CurrentIndex = [m for m, _l in MODE_TABS].index(settings["mode"])
    on_mode(None)
    win.Show()
    disp.RunLoop()
    win.Hide()
    # The log window shares this dispatcher. Keep this window alive and cut its
    # handlers loose: when Python later freed it, its Close event reached
    # on_close, whose ExitLoop shut the log a few seconds after it opened.
    UI_HANDLES.setdefault("main_wins", []).append(win)
    for widget_id, event in ((window_id, "Close"), ("Cancel", "Clicked"), ("Run", "Clicked"),
                             ("modeTabs", "CurrentChanged"), ("dryRunN", "Clicked"),
                             ("dryRunU", "Clicked"),
                             ("selectionMethodC", "CurrentIndexChanged"),
                             ("selectionMethodU", "CurrentIndexChanged")):
        try:
            setattr(getattr(win.On, widget_id), event, None)
        except Exception:
            pass

    if not run_export["value"]:
        return None

    mode = current_mode()
    sfx = "U" if mode == MODE_UPDATE else "C"

    timeline_name = itm["DstTimelineName"].Text.strip() or "Master_Sources"

    threshold_text = itm["ConnectionThreshold" + sfx].Text
    try:
        threshold = int(threshold_text)
    except (ValueError, TypeError):
        threshold = DEFAULT_CONNECTION_THRESHOLD

    try:
        handles = max(0, int(itm["Handles"].Text))
    except (ValueError, TypeError):
        handles = DEFAULT_HANDLES

    def _int(widget_id, default):
        try:
            return max(0, int(itm[widget_id].Text))
        except (ValueError, TypeError):
            return default

    pick_label = itm["selectionMethod" + sfx].CurrentText
    params = {
        "mode": mode,
        # Update always reads the timelines picked here, exactly as Create does;
        # the record in the timeline is used only to report what changed.
        "source_selection_mode": "Selection",
        "dst_timeline_name": timeline_name,
        "selection_method": dict(PICK_FROM).get(pick_label, "Current Bin"),
        "sorting_method": itm["sortingMethod"].CurrentText,
        "connection_threshold": threshold,
        "video_only": True,          # always: the master is for picture
        "mark_duplicates": itm["markDuplicates" + sfx].Checked,
        "mark_retimed_clips": itm["markRetimedClips" + sfx].Checked,
        "use_xml_retime": True,      # always: it widens ramped shots to every frame used
        "import_clip_names": True,   # always: shot names given on the edit timeline
        "merge_by_source_file": True,  # always: a file imported twice is one source
        "protect_graded_clips": itm["protectGradedClips"].Checked,
        "dry_run": bool(dry_run_box()) and itm[dry_run_box()].Checked,
        "handles": handles,
        "target_uid": target_uid,
        "namer_pattern": itm["NamerPattern"].Text.strip() or "sh###",
        "namer_start": _int("NamerStart", 10),
        "namer_increment": max(1, _int("NamerIncrement", 10)),
        "namer_from_playhead": itm["namerFromPlayhead"].Checked,
        "namer_keep_names": itm["namerKeepNames"].Checked,
        "namer_append_source": itm["namerAppendSource"].Checked,
        "namer_clip_color": itm["NamerClipColor"].CurrentText or KEEP_COLOR,
        "namer_code": itm["NamerCode"].Text.strip(),
    }
    remembered = {key: params[key] for key in default_settings() if key in params}
    remembered.update(mode=params["mode"], pick_from=pick_label,
                      timeline_name=timeline_name)
    save_settings(remembered)
    return params


def clipboard_text() -> Optional[str]:
    """What is on the macOS clipboard now, or None if it can't be read."""
    try:
        done = subprocess.run(["/usr/bin/pbpaste"], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=5)
        return done.stdout.decode("utf-8", "replace")
    except (OSError, subprocess.SubprocessError):
        return None


def copy_to_clipboard(text: str) -> bool:
    """Put text on the clipboard; True once it is really there.

    pbcopy first, checked by reading the clipboard back; then Fusion's own
    SetClipboard, which works from inside Resolve's script process. Each step
    is printed, so a failure says why in the console.
    """
    try:
        subprocess.run(["/usr/bin/pbcopy"], input=text.encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       check=True, timeout=5)
        if clipboard_text() == text:
            print(f"Copied the log to the clipboard ({len(text)} characters).")
            return True
        print("  pbcopy ran, but the clipboard does not hold the log; "
              "trying Fusion's clipboard.")
    except (OSError, subprocess.SubprocessError) as e:
        print(f"  pbcopy failed ({e}); trying Fusion's clipboard.")
    try:
        fu.SetClipboard(text)  # noqa: F821
    except Exception as e:
        print(f"Copy to clipboard failed: {e}")
        return False
    landed = clipboard_text()
    if landed is None or landed.strip() == text.strip():
        print(f"Copied the log to the clipboard with Fusion ({len(text)} characters).")
        return True
    print("Copy to clipboard failed: the clipboard does not hold the log.")
    return False


def default_csv_name(report: RunReport) -> str:
    """'Generate Master Sources log 2026-10-24_1310.csv'."""
    return f"{SCRIPT_TITLE} log {datetime.now().strftime('%Y-%m-%d_%H%M')}.csv"


def ask_csv_path(default_name: str) -> Optional[str]:
    """Where to save the CSV, from a macOS save dialog; None if cancelled.

    If the dialog can't be shown, the file goes on the Desktop.
    """
    script = ('tell application "System Events" to activate\n'
              'tell application "System Events" to return POSIX path of '
              f'(choose file name with prompt "Export the log as a CSV file" '
              f'default name "{default_name}" '
              'default location (path to desktop folder))')
    try:
        done = subprocess.run(["osascript", "-e", script], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=600)
    except (OSError, subprocess.SubprocessError) as e:
        print(f"Export CSV: no save dialog ({e}); saving on the Desktop.")
        return os.path.join(os.path.expanduser("~/Desktop"), default_name)
    if done.returncode != 0:
        error = done.stderr.decode("utf-8", "replace")
        if "-128" in error:  # Cancel
            return None
        print(f"Export CSV: no save dialog ({error.strip()}); saving on the Desktop.")
        return os.path.join(os.path.expanduser("~/Desktop"), default_name)
    path = done.stdout.decode("utf-8", "replace").strip()
    if path and not path.lower().endswith(".csv"):
        path += ".csv"
    return path or None


def show_report(report: RunReport, can_apply: bool = False,
                apply_label: str = "Apply update") -> bool:
    """Log window: summary, one row per clip, Copy to clipboard and Close.

    With can_apply (a dry run's plan) it also has a teal Apply update button.
    Returns True when Apply update was pressed.
    """
    ui = UI_HANDLES.get("ui") or fu.UIManager  # noqa: F821
    disp = UI_HANDLES.get("disp") or bmd.UIDispatcher(ui)  # noqa: F821
    WINDOW_COUNTER[0] += 1
    window_id = f"Log{WINDOW_COUNTER[0]}"
    win = disp.AddWindow(
        {"ID": window_id, "WindowTitle": window_title("Log"),
         "Geometry": centered_geometry(1180, 560), "WindowFlags": ON_TOP_FLAGS,
         "StyleSheet": WINDOW_STYLE},
        ui.VGroup({"Spacing": 6}, [
            ui.Label({"Text": report.summary or "Nothing to report.", "WordWrap": True,
                      "Weight": 0, "StyleSheet": HEADING_STYLE}),
            ui.Tree({"ID": "Tree", "AlternatingRowColors": True, "RootIsDecorated": False,
                     "SelectionMode": "NoSelection"}),
            ui.Label({"Text": "The same details are in the console (Workspace > Console). "
                              "Copy to clipboard gives a plain-text version to paste "
                              "into a chat or email; Export CSV saves the table for a "
                              "spreadsheet.",
                      "Weight": 0, "WordWrap": True, "StyleSheet": HINT_STYLE}),
            ui.Label({"Text": "", "Weight": 0, "StyleSheet": DIVIDER_STYLE}),
            ui.HGroup({"Weight": 0}, [
                ui.Button({"ID": "Copy", "Text": "Copy to clipboard", "Weight": 0}),
                ui.Button({"ID": "ExportCsv", "Text": "Export CSV...", "Weight": 0}),
                ui.HGap(0, 1),
                ui.Button({"ID": "Close", "Text": "Close", "Weight": 0,
                           "Default": not can_apply}),
            ] + ([ui.Button({"ID": "Apply", "Text": apply_label, "Weight": 0,
                             "Default": True})] if can_apply else [])),
        ]),
    )
    tree = win.Find("Tree")
    columns = report.columns or LOG_COLUMNS
    tree.ColumnCount = len(columns)
    header = tree.NewItem()
    for column, (title, width) in enumerate(columns):
        header.Text[column] = title
        tree.ColumnWidth[column] = width
    tree.SetHeaderItem(header)
    for values in report.rows or [("", "Nothing changed")]:
        row = tree.NewItem()
        for column, value in enumerate(values):
            row.Text[column] = value
            row.ToolTip[column] = value
        tree.AddTopLevelItem(row)

    def on_copy(ev):
        print("Copy to clipboard clicked.")
        try:
            ok = copy_to_clipboard(report.as_text())
        except Exception as e:  # a handler must never fail silently
            print(f"Copy to clipboard failed: {e}")
            ok = False
        win.Find("Copy").Text = "Copied" if ok else "Copy failed - see console"

    def on_export(ev):
        print("Export CSV clicked.")
        # The log stays on top of everything, so it steps aside for the dialog.
        try:
            win.Hide()
            path = ask_csv_path(default_csv_name(report))
        finally:
            win.Show()
            win.Raise()
        if not path:
            return
        try:
            report.write_csv(path)
        except OSError as e:
            print(f"Export CSV failed: {e}")
            win.Find("ExportCsv").Text = "Export failed - see console"
            return
        print(f"Log exported to {path}")
        win.Find("ExportCsv").Text = "Exported"

    closed = {"by_user": False, "apply": False}

    def on_close(ev):
        closed["by_user"] = True
        try:
            win.Hide()  # gone at the click, whatever the event loop does next
        except Exception:
            pass
        disp.ExitLoop()

    def on_apply(ev):
        closed["apply"] = True
        on_close(ev)

    getattr(win.On, window_id).Close = on_close
    win.On.Close.Clicked = on_close
    win.On.Copy.Clicked = on_copy
    win.On.ExportCsv.Clicked = on_export
    if can_apply:
        win.On.Apply.Clicked = on_apply
    # Only Close (or the window's close button) ends it: if anything else stops
    # the loop, show the log again rather than let it vanish unread. A burst of
    # Resolve events (a timeline redraw) can stop it many times in a row, so it
    # only gives up after a full minute of nothing but interruptions.
    give_up_at = time.time() + 60
    win.Show()
    win.Raise()
    while not closed["by_user"] and time.time() < give_up_at:
        win.Show()
        started = time.time()
        try:
            disp.RunLoop()
        except Exception as e:  # an event for another window must not end the log
            print(f"  Log window: event loop interrupted ({e!r}); showing it again.")
        if time.time() - started > 2:
            give_up_at = time.time() + 60  # it was working; start the minute again
        if not closed["by_user"]:
            let_resolve_settle(0.2)  # keeps handling clicks while it waits
    win.Hide()
    return closed["apply"]


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main():
    """Script entry point: show UI, collect parameters, run the chosen workflow.

    After a Create the window opens again on the Shot Namer tab, because
    naming the new master's shots is the next step.
    """
    start_mode = None
    while True:
        params = build_and_show_ui(start_mode)
        if params is None:
            return
        report = run_tab(params)
        # Only a Create that made a timeline (it sets the log's title) moves on.
        if params.get("mode") != MODE_CREATE or not report.title:
            return
        start_mode = MODE_NAMER


def run_tab(params: dict) -> RunReport:
    """Run the tab the window's Run button was pressed on, and show its log."""

    mode = params.get("mode", MODE_CREATE)
    shared = (
        "selection_method", "connection_threshold",
        "video_only", "mark_duplicates", "mark_retimed_clips", "use_xml_retime",
        "import_clip_names", "merge_by_source_file", "handles",
    )

    def run_once(dry_run: bool) -> RunReport:
        global REPORT
        REPORT = RunReport()
        progress = ProgressUI()
        try:
            if mode == MODE_NAMER:
                run_shot_namer(
                    params["namer_pattern"], params["namer_start"],
                    params["namer_increment"], params["namer_from_playhead"],
                    params["namer_keep_names"], params["namer_append_source"],
                    params["namer_clip_color"], params["namer_code"], dry_run,
                    expected_target_uid=params.get("target_uid", ""),
                    progress=progress)
            elif mode == MODE_UPDATE:
                call = {key: params[key] for key in shared}
                call["source_selection_mode"] = params["source_selection_mode"]
                call["protect_graded_clips"] = params["protect_graded_clips"]
                call["dry_run"] = dry_run
                call["expected_target_uid"] = params.get("target_uid", "")
                run_update_workflow(progress=progress, **call)
            else:
                call = {key: params[key] for key in shared}
                call["dst_timeline_name"] = params["dst_timeline_name"]
                call["sorting_method"] = params["sorting_method"]
                run_workflow(progress=progress, **call)
        except Exception as e:  # the log must still open and say what happened
            import traceback
            traceback.print_exc()
            REPORT.summary = (f"Stopped with an error: {e!r}. Anything done before "
                              f"it is listed below; the console (Workspace > Console) "
                              f"has the details.")
        finally:
            progress.close()
        return REPORT

    dry_run = mode in (MODE_UPDATE, MODE_NAMER) and params["dry_run"]
    report = run_once(dry_run)
    # A dry run's plan can be applied straight from its log. The run re-reads
    # the timeline, so the new log shows what was really done.
    apply_label = "Name shots" if mode == MODE_NAMER else "Apply update"
    if show_report(report, can_apply=dry_run and report.can_apply,
                   apply_label=apply_label):
        print(f"{apply_label} pressed - running it for real.")
        report = run_once(False)
        show_report(report)
    return report


main()
