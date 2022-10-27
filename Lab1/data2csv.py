from optparse import OptionParser
import csv

def datatocsv(_fn):
    data = open('{}.data'.format(_fn),'r')
    with open('{}.csv'.format(_fn),'w') as file:
        writer = csv.writer(file)
        for line in data:
            writer.writerow(str(line).replace('\n','').split(' ')[3:])
    data.close()

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing data", default='A.data'
    )

    (options, args) = optparser.parse_args()
    _filename = str(options.input)[0:str(options.input).find('.')]
    datatocsv(_filename)
