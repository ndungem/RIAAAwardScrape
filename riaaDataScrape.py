import sys
import argparse
import os

explanation = 'This program runs the necessary files for datascraping the RIAA Awards in the Gold&Platinum program. To run for just gold, use -a gold and for other awards, run -a others.'
parser = argparse.ArgumentParser(description=explanation)
parser.add_argument("-a", "--award", help="action chooses to run gold or run other awards.")
parser.add_argument("-f", "--firefox", help="action chooses firefox driver", action='store_true')
parser.add_argument("-o", "--outputfile", help="output file for csv")
parser.add_argument("-s", "--servicefile", help="file for chromeDriver", required=True)

# parser.add_argument("-o", "--outputfile", help="outputfile")

args = parser.parse_args()
filepath = args.outputfile
servicefile = args.servicefile
command = 'python3 '
if args.award == "gold":
    command += 'getGold.py '
elif args.award == "plat":
    command += 'getPlat.py '
elif args.award == "mplat":
    command += 'getMPlat.py '
elif args.award == "diamond":
    command += 'getDiamond.py '
else:
    command += 'getOtherAwards.py '

if args.firefox:
    command += '--firefox '

servicecommand = '-s ' + servicefile + ' '
command += servicecommand
if args.outputfile:
    filecommand = '-o ' + filepath
    command += filecommand

print("Running command:" + command)
os.system(command)
