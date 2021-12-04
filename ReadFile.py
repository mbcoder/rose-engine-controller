import csv

offsets = []

with open('Pattern1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        offsets.append(int(row[1]))

print len(offsets)

currentOffset = offsets[0]

for offset in offsets:
    steps = offset - currentOffset  # type: int

    currentOffset = offset

    print('steps {0} offset {1}'.format(steps, offset))


