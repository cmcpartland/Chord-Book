import sys

from PyQt4.QtCore import * 
from PyQt4.QtGui import *

from GUI_Sub_Folder.ChordBookUI import Ui_MainWindow
	
class MyForm(QMainWindow):
	def __init__(self, parent = None):
		
		# standard GUI code
		QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.connect(self.ui.identify_chord, SIGNAL("clicked()"), self.identify_chord)
		self.connect(self.ui.clear_fret_selections, SIGNAL("clicked()"), self.clear_fret_selections)
		self.connect(self.ui.tuning, SIGNAL("currentIndexChanged(int)"), self.set_tuning)
		
		global string_choices
		string_choices = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#']
		# Populate string tunings with selections
		self.ui.S1.addItems(string_choices)
		self.ui.S2.addItems(string_choices)
		self.ui.S3.addItems(string_choices)
		self.ui.S4.addItems(string_choices)
		self.ui.S5.addItems(string_choices)
		self.ui.S6.addItems(string_choices)
		
		global tuning_choices
		tuning_choices = ['Standard E', 'Standard Eb', 'Drop D', 'Drop C']
		self.ui.tuning.addItems(tuning_choices)	
		# Populate tuning choices
		
		# Set tuning to Standard E
		self.ui.tuning.setCurrentIndex(tuning_choices.index('Standard E'))
		
	def identify_chord(self):
		note_collections = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#']
		notes = []
		for string in range(1,7):
			string_fretted = False
			open_string_name = 'self.ui.S%s' % str(string)
			current_text = getattr(eval(open_string_name), 'currentText')
			open_string = current_text()
			#print 'open string', open_string
			open_string_index = note_collections.index(open_string)
			for fret in range(23):
				button_name = 'self.ui.S%sF%s' % (str(string), str(fret))
				is_checked = getattr(eval(button_name), 'isChecked')
				if is_checked():
					
					# find the appropriate index for the fretted note from the note_collections list
					if open_string_index + fret >= 12 and open_string_index + fret < 24:
						note_index = fret + open_string_index - 12
					elif open_string_index + fret >= 24:
						note_index = fret + open_string_index - 24
					else:
						note_index = fret + open_string_index
					#print 'string', string
					#print 'note index', note_index
					#print 'open string index', open_string_index
					notes.append(note_collections[note_index])
					string_fretted = True
					break
		# notes will become the unique set of all notes played
		notes = set(notes)
		
		# search all chord possibilities for a match
		distinctions = ['maj', 'min', 'maj7', 'min7', '7', 'maj9', 'min9']
		chord_found = False
		for note in note_collections:
			if not chord_found:
				for distinction in distinctions:
					chord_notes = self.get_chord(note, distinction)
					#print 'chord name: ', note + distinction
					#print 'chord notes', chord_notes
					if set(notes) == set(chord_notes):
						self.ui.results.setText('The chord is ' + note + distinction)
						chord_found = True
						break
			else: break
		if not chord_found:
			self.ui.results.setText('The chord could not be identified!')
	
	def clear_fret_selections(self):
		for string in range(1,7):
			button_name = 'self.ui.S%sF0' % str(string)
			set_checked = getattr(eval(button_name), 'setChecked')
			set_checked(True)
	
	def set_tuning(self):
		tuning = tuning_choices[self.ui.tuning.currentIndex()]
		if tuning == 'Standard E':
			self.ui.S6.setCurrentIndex(string_choices.index('E'))
			self.ui.S5.setCurrentIndex(string_choices.index('A'))
			self.ui.S4.setCurrentIndex(string_choices.index('D'))
			self.ui.S3.setCurrentIndex(string_choices.index('G'))
			self.ui.S2.setCurrentIndex(string_choices.index('B'))
			self.ui.S1.setCurrentIndex(string_choices.index('E'))
		elif tuning == 'Standard Eb':
			self.ui.S6.setCurrentIndex(string_choices.index('Eb'))
			self.ui.S5.setCurrentIndex(string_choices.index('G#'))
			self.ui.S4.setCurrentIndex(string_choices.index('C#'))
			self.ui.S3.setCurrentIndex(string_choices.index('F#'))
			self.ui.S2.setCurrentIndex(string_choices.index('Bb'))
			self.ui.S1.setCurrentIndex(string_choices.index('Eb'))
		elif tuning == 'Drop D':
			self.ui.S6.setCurrentIndex(string_choices.index('D'))
			self.ui.S5.setCurrentIndex(string_choices.index('A'))
			self.ui.S4.setCurrentIndex(string_choices.index('D'))
			self.ui.S3.setCurrentIndex(string_choices.index('G'))
			self.ui.S2.setCurrentIndex(string_choices.index('B'))
			self.ui.S1.setCurrentIndex(string_choices.index('E'))
		elif tuning == 'Drop C':
			self.ui.S6.setCurrentIndex(string_choices.index('C'))
			self.ui.S5.setCurrentIndex(string_choices.index('G'))
			self.ui.S4.setCurrentIndex(string_choices.index('C'))
			self.ui.S3.setCurrentIndex(string_choices.index('F'))
			self.ui.S2.setCurrentIndex(string_choices.index('A'))
			self.ui.S1.setCurrentIndex(string_choices.index('D'))
		self.ui.tuning.setCurrentIndex(tuning_choices.index(tuning))
	
	def get_chord(self, name, distinction):
		note_collections = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#']
		notes = []
		current_index = note_collections.index(name)
		#print 'chord', name + distinction
		#print 'current index', current_index
		notes.append(name)
		if distinction == 'maj':
			# add the Major Third
			if current_index + 4 < len(note_collections):
				notes.append(note_collections[current_index + 4])
			else:
				notes.append(note_collections[current_index + 4 - len(note_collections)])
			# add the Perfect Fifth
			if current_index + 7 < len(note_collections):
				notes.append(note_collections[current_index + 7])
			else:
				notes.append(note_collections[current_index + 7 - len(note_collections)])
		elif distinction == 'min':
			# add the Minor Third
			if current_index + 3 < len(note_collections):
				notes.append(note_collections[current_index + 3])
			else:
				notes.append(note_collections[current_index + 3 - len(note_collections)])
			# add the Perfect Fifth
			if current_index + 7 < len(note_collections):
				notes.append(note_collections[current_index + 7])
			else:
				notes.append(note_collections[current_index + 7 - len(note_collections)])
		elif distinction == 'maj7':
			# add the Major Third
			if current_index + 4 < len(note_collections):
				notes.append(note_collections[current_index + 4])
			else:
				notes.append(note_collections[current_index + 4 - len(note_collections)])
			# add the Perfect Fifth
			if current_index + 7 < len(note_collections):
				notes.append(note_collections[current_index + 7])
			else:
				notes.append(note_collections[current_index + 7 - len(note_collections)])
			# add the Major Seventh
			if current_index + 11 < len(note_collections):
				notes.append(note_collections[current_index + 11])
			else:
				notes.append(note_collections[current_index + 11 - len(note_collections)])
		elif distinction == 'min7':
			# add the Minor Third
			if current_index + 3 < len(note_collections):
				notes.append(note_collections[current_index + 3])
			else:
				notes.append(note_collections[current_index + 3 - len(note_collections)])
			# add the Perfect Fifth
			if current_index + 7 < len(note_collections):
				notes.append(note_collections[current_index + 7])
			else:
				notes.append(note_collections[current_index + 7 - len(note_collections)])
			# add the Minor Seventh
			if current_index + 11 < len(note_collections):
				notes.append(note_collections[current_index + 10])
			else:
				notes.append(note_collections[current_index + 10 - len(note_collections)])	
		elif distinction == 'maj9':
			# add the Major Third
			if current_index + 4 < len(note_collections):
				notes.append(note_collections[current_index + 4])
			else:
				notes.append(note_collections[current_index + 4 - len(note_collections)])
			# add the Perfect Fifth
			if current_index + 7 < len(note_collections):
				notes.append(note_collections[current_index + 7])
			else:
				notes.append(note_collections[current_index + 7 - len(note_collections)])
			# add the Major Seventh
			if current_index + 11 < len(note_collections):
				notes.append(note_collections[current_index + 11])
			else:
				notes.append(note_collections[current_index + 11 - len(note_collections)])
			# add the Major Ninth
			if current_index + 2 < len(note_collections):
				notes.append(note_collections[current_index + 2])
			else:
				notes.append(note_collections[current_index + 2 - len(note_collections)])
		elif distinction == 'min9':
			# add the Minor Third
			if current_index + 3 < len(note_collections):
				notes.append(note_collections[current_index + 3])
			else:
				notes.append(note_collections[current_index + 3 - len(note_collections)])
			# add the Perfect Fifth
			if current_index + 7 < len(note_collections):
				notes.append(note_collections[current_index + 7])
			else:
				notes.append(note_collections[current_index + 7 - len(note_collections)])
			# add the Minor Seventh
			if current_index + 10 < len(note_collections):
				notes.append(note_collections[current_index + 10])
			else:
				notes.append(note_collections[current_index + 10 - len(note_collections)])
			# add the Major Ninth
			if current_index + 2 < len(note_collections):
				notes.append(note_collections[current_index + 2])
			else:
				notes.append(note_collections[current_index + 2 - len(note_collections)])	
		elif distinction == '7':
			# add the Major Third
			if current_index + 4 < len(note_collections):
				notes.append(note_collections[current_index + 4])
			else:
				notes.append(note_collections[current_index + 4 - len(note_collections)])
			# add the Perfect Fifth
			if current_index + 7 < len(note_collections):
				notes.append(note_collections[current_index + 7])
			else:
				notes.append(note_collections[current_index + 7 - len(note_collections)])
			# add the Seventh
			if current_index + 10 < len(note_collections):
				notes.append(note_collections[current_index + 10])
			else:
				notes.append(note_collections[current_index + 10 - len(note_collections)])
		return notes
			
		
	
# The if statement below checks to see if this module is the main module and not being imported by another module
# If it is the main module if runs the following which starts the GUI
# This is here in case it is being imported, then it will not immediately start the GUI upon being imported
if __name__ == "__main__":
    # Opens the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()
    
    # Shows the GUI
    myapp.show()
    
    # Exits the GUI when the x button is clicked
    sys.exit(app.exec_())