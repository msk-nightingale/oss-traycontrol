#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#
#	Регулятор громкости для OSS в трей (ossvolume, ov)
#		Version 0.23
#
#	© Copyright 2014, Соловьев Алексей <al.moscwich@gmail.com>
#	Это произведение доступно на условиях лицензии Creative Commons Attribution 3.0 Unported.
#

import re, gtk
import os, commands
import ConfigParser

dev = "1 "
mxr = "vmix0-outvol "
cfg = os.getenv ('HOME') + '/.config/ov.prefs'

def getline ():
	i = re.match ('Value of mixer control (.*) is currently set to (.*)\:(.*)', commands.getoutput ('ossmix -d ' + dev + "line"))
	return int (i.group (2))

def setline (vol):
	os.system ("ossmix -d " + dev + "line " + str (vol))

def getmxr ():
	global dev, mxr
	if os.access (cfg, os.F_OK):
		config = ConfigParser.ConfigParser ()
		config.read (cfg)
		dev = config.get ('main', 'device') + " "
		mxr = config.get ('main', 'channel') + " "
	i = re.match ('Value of mixer control (.*) is currently set to (.*).. \(dB\)', commands.getoutput ('ossmix -d ' + dev + mxr))
	if i != None: vol = int (i.group (2))
	else: vol = 0
	volume.set_value (25 - vol)
	getline ()

def setmxr (scale):
	volume = str (25 - scale.get_value ())
	os.system ("ossmix -d " + dev + mxr + volume)

def newcfg ():
	config = ConfigParser.RawConfigParser ()
	config.add_section ('main')
	config.set ('main', 'device', dev)
	config.set ('main', 'channel', mxr)
	with open (cfg, 'w') as configfile:
		config.write (configfile)

def pref (item):

	d = gtk.Entry (2)
	d.set_text (dev.strip ())
	d.connect ('changed', chd)

	db = gtk.VBox ()
	db.set_border_width (4); db.set_spacing (4)
	db.add (gtk.Label (commands.getoutput ('ossinfo -x').strip ()))
	db.add (d)

	df = gtk.Frame ("Устройство")
	df.add (db)

	m = gtk.combo_box_entry_new_text ()
	i = mxr.strip (); m.append_text (i)
	if i != 'vmix0-outvol': m.append_text ('vmix0-outvol')
	m.set_border_width (4); m.set_active (0)
	m.connect ('changed', chm)

	mb = gtk.VBox ()
	mb.set_border_width (4)
	mb.add (m)

	mf = gtk.Frame ("Канал")
	mf.add (mb)

	b = gtk.VBox ()
	b.set_spacing (4)
	b.add (df)
	b.add (mf)

	w = gtk.Window ()
	w.set_title ('Настройки')
	w.set_border_width (10)
	w.move (50, 50)
	w.add (b); w.show_all ()

def menu (icon, button, time):

	dpref = gtk.MenuItem ('Настройки')
	dpref.connect ('activate', pref)
	dpref.show ()

	dtail = gtk.MenuItem ('Выход')
	dtail.connect ('activate', tail)
	dtail.show ()

	dxmix = gtk.MenuItem ('Запустить OSSXMix')
	dxmix.connect ('activate', xmix)
	dxmix.show ()

	if getline () == 0:
		line = gtk.MenuItem ('Включить микшер')
		line.connect ('activate', lineon)
		line.show ()
	else:
		line = gtk.MenuItem ('Отключить микшер')
		line.connect ('activate', lineoff)
		line.show ()

	menu = gtk.Menu ()
	menu.append (line); menu.append (dxmix); menu.append (dpref); menu.append (dtail)
	menu.popup (None, None, gtk.status_icon_position_menu, button, time, icon)

def chd (d):
	global dev
	dev = d.get_text ()
	newcfg (); getmxr ()

def chm (m):
	global mxr
	mxr = m.get_active_text ()
	newcfg (); getmxr ()

def hide (icon):
	if not window.get_visible (): window.show ()
	else: window.hide ()

def move (w, icon):
	r = gtk.status_icon_position_menu (gtk.Menu (), icon)
	w.move (r[0], r[1])

def xmix (item): os.system ('ossxmix &')
def tail (item): exit ()

def lineon (item):
	setline (100)
	item.set_label ("Отключить микшер")
	item.connect ('activate', lineoff)

def lineoff (item):
	setline (0)
	item.set_label ("Включить микшер")
	item.connect ('activate', lineon)

volume = gtk.VScale ()
volume.set_draw_value (False)
volume.connect ("value-changed", setmxr)
volume.set_range (0, 25); volume.set_size_request (15, 150)
volume.show ()

icon = gtk.status_icon_new_from_file (os.path.dirname (__file__) + "/icon.svg")
icon.connect ('popup-menu', menu)
icon.connect ('activate', hide)

window = gtk.Window (gtk.WINDOW_POPUP)
window.set_default_size (25, 160)
window.connect ('show', move, icon)
window.add (volume)

getmxr ()
gtk.main ()
