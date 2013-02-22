#!/usr/bin/python
import subprocess
import os, sys
from sys import argv

#zeroes out the first 512 bytes of the given disk. this is used to prevent partition table conflicts.
def zero_mbr(disk):
	output = subprocess.call(['dd', 'if=/dev/zero', 'of=/dev/%s' % disk, 'bs=512', 'count=1'], shell=False, stdout=subprocess.PIPE)

#converts iso to dmg file using hdiutil, returns a string of the newly created dmg file for imaging
def iso_to_dmg(iso):
        tmp_image = iso + ".dmg"
	output = subprocess.call(['hdiutil', 'convert', '-format', 'UDRW','-o', tmp_image, iso], shell=False, stdout=subprocess.PIPE)
	return tmp_image	

#writes dmg to usb stick using dd
def dmg_to_usb(dmg, disk):
	if_str = "if=%s" % dmg
	of_str = "of=/dev/%s" % disk
	output = subprocess.call(['dd', if_str, of_str], shell=False, stdout=subprocess.PIPE)

def main():
	disk = argv[1]
	iso = argv[2]

	print "Baking %s onto %s" % (iso, disk)

	if os.getuid() != 0:
		print "isobake needs sudo access!"
		sys.exit()
	try:
   		with open(iso) as f: pass
	except IOError as e:
   		print 'Cannot open supplied iso file. Please check file path and try again.'
		sys.exit()

	if len(argv) < 2:
		print "Usage: isobake rdisk2 test.iso"
	elif len(argv) < 3:
		print "Usage: isobake rdisk2 test.iso"
	else:	
		confirm = raw_input("CONFIRM:: we will write %s to %s: [y/n]" % (iso, disk))
		if confirm == "y":
			print "Zeroing out partiiton table and MBR on %s" % disk
			zero_mbr(disk)
			print "converting image"
			tmp_image = iso_to_dmg(iso)
			print "imaging file to usb drive"
			process = dmg_to_usb(tmp_image, disk)
		elif confirm == "n":
			print "exiting.."
			sys.exit(1)
		else: 
			print "try that again."
	
			

	

if __name__=='__main__':
	main()
