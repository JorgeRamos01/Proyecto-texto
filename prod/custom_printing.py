#-----------------------------------------------------------------------------#
# Class to create a customized printing in the log files
#
# Author: Kenny Mendez
#-----------------------------------------------------------------------------#

class CustomWrite:

	def __init__(self, name):
		self.name = name
		self.len_lines = 68
		self.counter = 0
		self.tot_elems = None
		self.storedata = False

	# Dotted line
	def single_line(self):
		print("#" + "-" * self.len_lines + "#")

	# Make another type of line
	def single_bar(self, schr = "#", len_bar = None):
		
		if len_bar is None:
			len_bar = self.len_lines  # set default val

		print(schr * len_bar)  # make a line of characters 'schr'

	# Header function
	def header(self):
		self.single_line()
		print("# " + self.name)  # print name of context
		print("\n")

	# Footer function
	def footer(self, message = None):

		if message is not None:
			print(message + "\n")  # some message

		print("\n"  + "*" * 3 + " Finishing task ... ")
		print("\n" * 2)

	# Set total of elements and counter start at 1
	def init_counter(self, tot_elems):
		self.counter = 1
		self.tot_elems = tot_elems

	# Report status
	def status_insert(self):
		print("Register " + str(self.counter) + " of " + \
			str(self.tot_elems) + " retrieved urls was inserted successfully.")

		self.counter += 1  # increment counter

	# Debug message
	def debug(self, message):
		print("** DEBUGGING: " + message)

	# Custom message
	def cmessage(self, message = ""):
		print(message)

	# Highlight message
	def hmessage(self, message):
		self.single_bar()
		self.cmessage("\n" + message + "\n")
		self.single_bar()
		print("\n")

	# When storedata parameter is False
	def storedata_is_false(self):
		mssg = "The retrieved data WON'T BE stored! -> 'storedata" + " = " + str(self.storedata) + "'"
		self.hmessage(mssg)

	# When storedata parameter is True
	def storedata_is_true(self):
		mssg = "-> 'storedata = True'"
		self.hmessage(mssg)

	# Print notifications about the parameters of
	# the CW object (like the storedata status)
	def notifications(self):

		if self.storedata is False:
			self.storedata_is_false()
		else:
			self.storedata_is_true()

