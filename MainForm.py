# coding: utf-8

from time import time, sleep
import string
import sys

import System.Drawing
import System.Windows.Forms

from System import Enum, Byte, Array
from System.Text import Encoding
from System.Windows.Forms import *

from textbuf import Text
from comm import zmq


# fixme: move
keys = {
    Keys.Left: 'Left',
    Keys.Right: 'Right',
    Keys.Up: 'Up',
    Keys.Down: 'Down',
    Keys.End: 'End',
    Keys.Home: 'Home',
    Keys.Delete: 'Delete',
    Keys.Back: 'BackSpace',
    Keys.Tab: 'Tab',
    Keys.PageDown: 'Page_Down',
    Keys.PageUp: 'Page_Up',
    Keys.Space: 'space',
    Keys.OemMinus: 'minus',
    Keys.OemPeriod: '.',
    Keys.OemQuestion: '/',
    Keys.Oemcomma: ',',
    Keys.Oemplus: '=',
    Keys.OemOpenBrackets: '[',
    Keys.Oemtilde: '~',
    Keys.D0: '0',
    Keys.D1: '1',
    Keys.D2: '2',
    Keys.D3: '3',
    Keys.D4: '4',
    Keys.D5: '5',
    Keys.D6: '6',
    Keys.D7: '7',
    Keys.D8: '8',
    Keys.D9: '9',
    Keys.D0: '0',
    Keys.F1: 'F1',
    Keys.F2: 'F2',
    Keys.F3: 'F3',
    Keys.F4: 'F4',
    Keys.F5: 'F5',
    Keys.F6: 'F6',
    Keys.F7: 'F7',
    Keys.F8: 'F8',
    Keys.F9: 'F9',
    Keys.F10: 'F10',
    Keys.F11: 'F11',
    Keys.F12: 'F12',
    Keys.Oem1: ';',
    Keys.Oem5: '|',
    Keys.Oem6: ']',
    Keys.Oem7: '\'',
}


import logging as log


class MainForm(Form):
    def __init__(self):
        self.text = Text()
        self.handling_keypress = False
        self.processing_dictation = False
        self.InitializeComponent()
        self.start_worker()

    def start_worker(self):
        self.backgroundWorker1.WorkerReportsProgress = True;
        self.backgroundWorker1.WorkerSupportsCancellation = True;
        self.backgroundWorker1.RunWorkerAsync();

    def InitializeComponent(self):
        self.components = System.ComponentModel.Container();
        self.backgroundWorker1 = System.ComponentModel.BackgroundWorker();
        self._statusStrip1 = System.Windows.Forms.StatusStrip()
        self._textbox = System.Windows.Forms.RichTextBox()
        self._status = System.Windows.Forms.ToolStripStatusLabel()
        self._statusStrip1.SuspendLayout()
        self.SuspendLayout()
        #
        # backgroundWorker1
        #
        self.backgroundWorker1.DoWork += System.ComponentModel.DoWorkEventHandler(self.backgroundWorker1_DoWork);
        self.backgroundWorker1.ProgressChanged += System.ComponentModel.ProgressChangedEventHandler(self.backgroundWorker1_ProgressChanged);
        #
        # statusStrip1
        #
        self._statusStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
            [self._status]))
        self._statusStrip1.Location = System.Drawing.Point(0, 240)
        self._statusStrip1.Name = "statusStrip1"
        self._statusStrip1.Size = System.Drawing.Size(284, 22)
        self._statusStrip1.TabIndex = 1
        #
        # textbox
        #
        self._textbox.AcceptsTab = True
        self._textbox.BorderStyle = System.Windows.Forms.BorderStyle.None
        self._textbox.Dock = System.Windows.Forms.DockStyle.Fill
        self._textbox.HideSelection = False
        self._textbox.ImeMode = System.Windows.Forms.ImeMode.Off
        self._textbox.Location = System.Drawing.Point(0, 24)
        self._textbox.Name = "textbox"
        self._textbox.ShortcutsEnabled = False
        self._textbox.Size = System.Drawing.Size(284, 216)
        self._textbox.TabIndex = 0
        self._textbox.Text = ""
        self._textbox.KeyUp += self.TextboxKeyUp
        self._textbox.PreviewKeyDown += self.TextboxPreviewKeyDown
        self._textbox.SelectionChanged += self.TextboxSelectionChanged

        #
        # status
        #
        self._status.Name = "status"
        self._status.Size = System.Drawing.Size(0, 17)
        #
        # MainForm
        #
        self.ClientSize = System.Drawing.Size(284, 262)
        self.Controls.Add(self._textbox)
        self.Controls.Add(self._statusStrip1)
        self.Name = "MainForm"
        self.Text = "Dragon Relay"
        self._statusStrip1.ResumeLayout(False)
        self._statusStrip1.PerformLayout()
        self.ResumeLayout(False)
        self.PerformLayout()

    def backgroundWorker1_ProgressChanged(self, sender, e):
        self.set_text(e.UserState)

    def backgroundWorker1_DoWork(self, sender, e):
        COMMAND_CLEAR = '\x1a'
        COMMAND_TEXT = '\x02'
        log.info('control_thread started')

        message = sys.stdin.readline()

        while message:
            if message[0] == '\x12':
                log.info('control message: "%s"', message)
                command = message[1]

                if command == COMMAND_TEXT:
                    message = message[2:-1]
                    log.info('set text buffer: %s', message)
                else:
                    log.info('clear text buffer')
                    message = ''

                self.backgroundWorker1.ReportProgress(0, message)

            message = sys.stdin.readline()

    def TextboxSelectionChanged(self, sender, e):
        if self.handling_keypress:
            return True

        start, length = sender.SelectionStart, sender.SelectionLength
        text = sender.Text

        log.info('selection changed, text="%s" [%d:%d]',
                 repr(text), start, length)

        if self.text.text != text:
            self.text, text_delta = self.text.set_text(text)
        else:
            text_delta = []

        self.text, selection_delta = self.text.set_selection(start, length)

        delta = text_delta + selection_delta
        for op in delta:
            if isinstance(op, basestring):
                zmq.send_key(op)
            else:
                command, key, count = op

                for _ in range(count):
                    zmq.send_command(key)

        return True

    def TextboxKeyUp(self, sender, e):
        log.info('key up')
        self.text = Text(sender.Text, sender.SelectionStart,
                         sender.SelectionLength)
        self.handling_keypress = False
        return True

    def TextboxPreviewKeyDown(self, sender, e):
        log.info('preview key down')

        ctrl, alt, shift = [(Control.ModifierKeys & modifier) == modifier
                            for modifier in (Keys.Control, Keys.Alt, Keys.Shift)]
        modifiers = filter(bool, [ctrl and 'Ctrl', alt and 'Alt', shift and 'Shift'])
        self._status.Text = '+'.join(modifiers + [str(e.KeyCode)])

        modifiers = [e.Control and 'c', e.Alt and 'a', e.Shift and 's']#,
                     #e.Win and 'w']
        modifiers = ''.join(filter(bool, modifiers))

        prefix = modifiers and modifiers + '-' or ''

        if e.KeyCode in keys:
            key = keys[e.KeyCode]
        elif e.KeyCode in (Keys.ControlKey, Keys.ShiftKey):
            key = None
        else:
            key = str(e.KeyCode)

            if key in set(string.uppercase):
                key = key.lower()

        if key:
            self.handling_keypress = True
            zmq.send_command(prefix + key)

        return True

    def intercepted_key(self, e):
        log.info('intercepted key event')
        # FIXME: Split key intercept handling out of this program
        # FIXME: abstract key processing to a helper module; replace key
        # processing here and in preview key down

        # should always be a modifier
        modifier, keyname = e.Key.split('-', 1)

        # http://www.codeproject.com/Articles/6768/Tips-about-NET-Enums
        key = Enum.Parse(Keys, keyname)

        if key in keys:
            key = keys[key]

        key = str(key)

        if key in set(string.uppercase):
            key = key.lower()

        key = '-'.join((modifier, key))

        log.info('intercepted key: ' + key)
        zmq.send_command(key)

    def set_text(self, text='', cursor_position=None):
        self.handling_keypress = True

        selection_start = len(text)
        self._textbox.Text = text
        self._textbox.SelectionStart = selection_start
        self._textbox.SelectionLength = 0

        self.text = Text(text, selection_start)

        self.handling_keypress = False
