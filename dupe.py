import os, re, sys, math, getopt
from collections import Counter

totalBytesDeleted = 0
totalFilesDeleted = 0

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def query(question, default = "yes"):
	valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("Invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = input().lower()
		if default is not None and choice == "":
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def checkDelete(match, autoaccept, trial):
	global totalBytesDeleted
	global totalFilesDeleted

	if (os.path.getsize(str(match[0])) > os.path.getsize(str(match[1]))):
		if trial:
			print("Remove " + str(match[1]))
			totalFilesDeleted += 1
			totalBytesDeleted += os.path.getsize(str(match[1]))
		elif autoaccept:
			totalFilesDeleted += 1
			totalBytesDeleted += os.path.getsize(str(match[1]))
			os.remove(str(match[1]))
			print("Removed " + str(match[1]))
		else:
			if query("Confirm deletion of " + str(match[1])):
				totalFilesDeleted += 1
				totalBytesDeleted += os.path.getsize(str(match[1]))
				os.remove(str(match[1]))
				print("Removed " + str(match[1]))
			else:
				print("Skipped " + str(match[1]))
	elif (os.path.getsize(str(match[0])) < os.path.getsize(str(match[1]))):
		if trial:
			print("Remove " + str(match[0]))
			totalFilesDeleted += 1
			totalBytesDeleted += os.path.getsize(str(match[0]))
		elif autoaccept:
			totalFilesDeleted += 1
			totalBytesDeleted += os.path.getsize(str(match[0]))
			os.remove(str(match[0]))
			print("Removed " + str(match[0]))
		else:
			if query("Confirm deletion of " + str(match[0])):
				totalFilesDeleted += 1
				totalBytesDeleted += os.path.getsize(str(match[0]))
				os.remove(str(match[0]))
			else:
				print("Skipped " + str(match[0]))
	elif (os.path.getsize(str(match[0])) == os.path.getsize(str(match[1]))):
		if trial:
			print("Remove " + str(match[1]))
			totalFilesDeleted += 1
			totalBytesDeleted += os.path.getsize(str(match[1]))
		elif autoaccept:
			totalFilesDeleted += 1
			totalBytesDeleted += os.path.getsize(str(match[1]))
			os.remove(str(match[1]))
			print("Removed " + str(match[1]))
		else:
			if query("Confirm deletion of " + str(match[1])):
				totalFilesDeleted += 1
				totalBytesDeleted += os.path.getsize(str(match[1]))
				os.remove(str(match[1]))
				print("Removed " + str(match[1]))
			else:
				print("Skipped " + str(match[1]))

def process(dir, output, autoaccept, trial):
	idList = list()
	pathList = list()
	matchList = list()

	for file in os.listdir(dir):
		x = os.path.join(dir, file)
		if(x[-4:] == '.mkv'):
			idList.append(str(x[-15:-4]))
			pathList.append(x)

	for ID, count in Counter(idList).items():
		if((count > 1) and (str(dir + " - " + ID) not in output)):
			output.append(dir + " - " + ID)
			matchList.append(list(filter(lambda x: ID in x, pathList)))

	for match in matchList:
		checkDelete(match, autoaccept, trial)

def navigate(dir, output, autoaccept, trial):
	for obj in os.listdir(dir):
		x = os.path.join(dir, obj)
		if os.path.isdir(x):
			navigate(x, output, autoaccept, trial)
		else:
			process(dir, output, autoaccept, trial)

def main(argv):
	root = ''
	autoaccept = False
	trial = False
	excluded = ''

	global totalBytesDeleted
	global totalFilesDeleted

	try:
		opts, args = getopt.getopt(argv, "hatd:x:",["help", "autoaccept", "trial", "directory=", "exclude="])
	except getopt.Getopterror:
		print("Usage python dupe.py [OPTIONS] -d <DIRECTORY>")
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print("Usage python dupe.py [OPTIONS] -d <DIRECTORY>\n")
			print("Options:")
			print("\t-h, --help\t\t\t\t\t\t\t\t\tPrint this help text and exit")
			print("\t-a, --autoaccept\t\t\t\t\t\t\t\tAccept deletions without prompting")
			print("\t-t, --trial\t\t\t\t\t\t\t\t\tPrint proposed deletions instead of deleting")
			print("\t-d, --directory PATH\t\t\t\t\t\t\t\tThe desired starting point of the recursive search")
			#print("\t-x, --exclude PATH\t\t\t\t\t\t\t\tExclude specified directory from search")
			sys.exit()
		elif opt in ("-a", "--autoaccept"):
			autoaccept = True
		elif opt in ("-t", "--trial"):
			trial = True
		elif opt in ("-d", "--directory"):
			root = arg
		# elif opt in ("-x", "--exclude"):
		# 	excluded = arg

	outputList = list()

	navigate(root, outputList, autoaccept, trial)

	if totalBytesDeleted > 0:
		if trial:
			print("Total files to be deleted:\t" + str(totalFilesDeleted))
			print("Total space to be saved:\t" + convert_size(totalBytesDeleted))
		else:
			print("Total files deleted:\t" + str(totalFilesDeleted))
			print("Total space saved:\t" + convert_size(totalBytesDeleted))
	else:
		print("No duplicates found!")


if __name__ == '__main__':
	main(sys.argv[1:])