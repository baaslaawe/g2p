import sys

# 1-1850 and 1901-2200 for training
# 1851-1900 and 2201-end all testing

# read the annotation file
annot_file = sys.argv[1]

with open(sys.argv[1], 'r') as f:
	lines = f.readlines()

train = []
test = []

for i in xrange(len(lines)):
	if i < 1850:
		train.append(lines[i])
	elif i > 1900 and i < 2200:
		train.append(lines[i])
	else:
		test.append(lines[i])

with open('train_annotation.txt', 'w') as f:
	f.write(''.join(train))
with open('test_annotation.txt', 'w') as f:
	f.write(''.join(test))
