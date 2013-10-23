﻿import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

from comm import zmq


class MainForm(Form):
	def __init__(self):
		self.previous_position = 0
		self.InitializeComponent()
		
	
	def InitializeComponent(self):
		self._menuStrip1 = System.Windows.Forms.MenuStrip()
		self._statusStrip1 = System.Windows.Forms.StatusStrip()
		self._fileToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._exitToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._textbox = System.Windows.Forms.RichTextBox()
		self._menuStrip1.SuspendLayout()
		self.SuspendLayout()
		# 
		# menuStrip1
		# 
		self._menuStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._fileToolStripMenuItem]))
		self._menuStrip1.Location = System.Drawing.Point(0, 0)
		self._menuStrip1.Name = "menuStrip1"
		self._menuStrip1.Size = System.Drawing.Size(284, 24)
		self._menuStrip1.TabIndex = 0
		self._menuStrip1.Text = "menuStrip1"
		# 
		# statusStrip1
		# 
		self._statusStrip1.Location = System.Drawing.Point(0, 240)
		self._statusStrip1.Name = "statusStrip1"
		self._statusStrip1.Size = System.Drawing.Size(284, 22)
		self._statusStrip1.TabIndex = 1
		self._statusStrip1.Text = "statusStrip1"
		# 
		# fileToolStripMenuItem
		# 
		self._fileToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._exitToolStripMenuItem]))
		self._fileToolStripMenuItem.Name = "fileToolStripMenuItem"
		self._fileToolStripMenuItem.Size = System.Drawing.Size(37, 20)
		self._fileToolStripMenuItem.Text = "File"
		# 
		# exitToolStripMenuItem
		# 
		self._exitToolStripMenuItem.Name = "exitToolStripMenuItem"
		self._exitToolStripMenuItem.Size = System.Drawing.Size(92, 22)
		self._exitToolStripMenuItem.Text = "Exit"
		# 
		# textbox
		# 
		self._textbox.BorderStyle = System.Windows.Forms.BorderStyle.None
		self._textbox.Dock = System.Windows.Forms.DockStyle.Fill
		self._textbox.ImeMode = System.Windows.Forms.ImeMode.Off
		self._textbox.Location = System.Drawing.Point(0, 24)
		self._textbox.Name = "textbox"
		self._textbox.Size = System.Drawing.Size(284, 216)
		self._textbox.TabIndex = 3
		self._textbox.Text = ""
		self._textbox.TextChanged += self.TextboxTextChanged
		self._textbox.KeyPress += self.TextboxKeyPress
		self._textbox.KeyUp += self.TextboxKeyUp
		self._textbox.PreviewKeyDown += self.TextboxPreviewKeyDown
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(284, 262)
		self.Controls.Add(self._textbox)
		self.Controls.Add(self._statusStrip1)
		self.Controls.Add(self._menuStrip1)
		self.MainMenuStrip = self._menuStrip1
		self.Name = "MainForm"
		self.Text = "IPYZMQ"
		self._menuStrip1.ResumeLayout(False)
		self._menuStrip1.PerformLayout()
		self.ResumeLayout(False)
		self.PerformLayout()


	def TextboxTextChanged(self, sender, e):
#		zmq.send_text(e.Text)
#		print sender, e
		zmq.send_key('text changed')
		
		start_position = self.previous_position
		index = sender.SelectionStart + sender.SelectionLength
		text = sender.Text
		
		print self.previous_position, index
		
#		print sender.Text[index]
#		print self.prevous_position#, index
		print text[start_position:index]
#		print type(sender.Text)
		zmq.send_key(text[start_position:index])
		self.previous_position = index

	def TextboxKeyPress(self, sender, e):
#		print sender.SelectionStart, sender.SelectionLength
#		print e.KeyChar
#		index = sender.SelectionStart + sender.SelectionLength
#		
#		print sender.Text[index]
		
#		zmq.send_key(e.KeyChar)
		pass

	def TextboxKeyUp(self, sender, e):
		index = sender.SelectionStart + sender.SelectionLength - 1
#		
#		print sender.Text[index]
#		zmq.send_key(sender.Text[index])

	def TextboxPreviewKeyDown(self, sender, e):
		pass