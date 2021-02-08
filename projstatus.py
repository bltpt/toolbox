#!/usr/bin/python3

'''projstatus: [Path] -> StdOut
   Purpose: if Path is a Project File, print its status to StdOut.
            If Path is a Project Directory, print the status of its
            Project File to StdOut. If Path is a directory with
            immediate children that are Project Directories, print
            the status of each child's Project File. If no Path is
            given, assume the current working directory is the Path
            to be considered.'''

import os
import sys

def printStatuses(statuses):
    '''printStatuses(): ListOfTuples -> StdOut
    Purpose: to pretty-print the contents of each tuple in LIstOfTuples
             to StdOut.'''

    # Pretty print the output with a header
(printf "PROJECT${delim}STATUS${delim}LAST MODIFIED${delim}NEXT STEP\n"; printf "${results[*]}") | column -s "${delim}" -t


        


def getStatus(project):
    '''getStatus(): Tuple1 -> Tuple2
    Purpose: to unpack the Project Name and Project File path from 
             Tuple1, determine the project's status, and return Tuple2
             containing the Project Name, the project's status, the
             last modified date of the Project File, and the Next Step
             in the project.'''
    
# For each file, determine the status
for file in $projFiles
do

    # Determine project name. If the name of the org file does not
    # have a case-insensitive match with its parent directory,
    # skip this loop since it's not the project file for its project.
    dirFile=`echo $file | sed "s/^\.\///"`
    dir=`echo $dirFile | cut -f 1 -d "/"`
    fileNameBase=`echo $dirFile | cut -f 2 -d "/" | sed "s/\.org$//g"`
    dirLower=`echo "$dir" | tr [:upper:] [:lower:]`
    if [ "$dirLower" == "$fileNameBase" ]
    then
	project="$dir"
    else
	continue
    fi

    # Determine the supported states in the given org file, if any.
    headerLine=`head -n 1 $file`
    states=`projstates "${headerLine}"`

    # Determine the status of the project. If there are no TODO states
    # defined in the file, set status to "No Header"
    if [ -z $states ]
    then
	status="No Header"
    else
	# Grep for the state of the Next Steps line and determine
	# the status of the project
	status=$(grep -E "^\* .+Next Steps" $file | tail -n 1 | grep -Eo "$states")
	if [ -z $status ]
	then
	    status="Undefined"
	else
	    status=$status
	fi
    fi
    
    # Initiate nextStep for this run of the loop.
    nextStep=""
    
    if [[ "$status" == "WAITING" || "$status" == "SCHEDULED" || "$status" == "HANDED-OFF" || "$status" == "POSTPONED" || "$status" == "CANCELLED" || "$status" == "DONE" ]]
    then
	# Determine the line on which Next Steps resides
	nextStepsLine=$(grep -En "^\* .+Next Steps" $file | tail -n 1 | cut -f 1 -d ":")
	nextStepLine=$(expr $nextStepsLine + 3)
	nextStep=$(sed -n ${nextStepLine}p $file | sed "s/^ *//")
    fi

    if [[ "$status" == "TODO" || "$status" == "Undefined" ]]
    then
	nextStep="Start the project."
    fi

    if [ "$status" == "IN-PROGRESS" ]
    then
	# The Next Step is the first incomplete checklist item after the
	# Next Steps header
	nextStep=`sed -e "1,/^.*Next Steps.*/d" $file | grep -m 1 -E "^\- \[ \] |^\- \[\-\] " \\
		      | sed "s/- \[ \] //" | sed "s/- \[-\] //"`
    fi

    if [ `uname` == "Linux" ]
    then
	# Grab the last modification time of the org file.
	lastMod=$(ls -l --time-style=long-iso $file | cut -f 6,7 -d " ")
    else
	if [ `uname` == "Darwin" ]
	then
	    # Grab the last modification time of the org file.
	    # This is the macOS-specific invocation.
	    rawLastMod=`stat -x $file | grep Modify | sed 's/^Modify: //' | cut -f 2-5 -d " "`
	    lastMod=`date -jf "%b %e %H:%M:%S %Y" "$rawLastMod"  +"%Y-%m-%d %H:%M"`
	else
	    lastMod='Unsupported platform'
	fi
    fi
    
    # Results Delimeter
    # Could replace this with '\x00'
    delim=$(printf '\xe2\x98\x95')
    
    # Add to the results array
    results+=$project$delim$status$delim$lastMod$delim$nextStep"\n"
    
done


def validateInput(path):
    '''validateInput(): Str -> ListOfTules
    Purpose: to determine whether Str represents a Project File, a
             Project Directory, or a directory with immediate
             children that are Project Directories, and return a
             ListOfTuples containing the Project Name and path to each
             Project File to be processed.'''

        if [ "$1" != "" ]
    then
        root="./`echo $1 | sed -E 's/\.|\///g'`"
        input=1
    else
        root="."
        input=0
    fi

    # Find the project files
if [ $input == 0 ]
   then
   projFiles=$(find -L $root -maxdepth 2 -type f -name \*.org)
   else
       if [ $input == 1 ]
	  then
	  projFiles=$(find -L $root -maxdepth 1 -type f -name \*.org)
	  else
	      echo "Error: can't determine where to start looking for .org files"
       fi
fi
    

def main(path):
    '''main(): Str -> StdOut
    Purpose: if Str is a Project File, print its status to StdOut.
             If Str is a Project Directory, print the status of its
             Project File to StdOut. If Str is a directory with
             immediate children that are Project Directories, print
             the status of each child's Project File.'''
    
    # Determine the Projects to be processed
    projects = validateInput(path)

    # Print status of each project
    try:
        statuses = list()
        for project in projects:
            status.append(getStatus(project))
        printStatuses(statuses)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        if not sys.argv[1]:
            # the program is invoked with no argument. Assume the
            # current working directory contains immediate child
            # Project Directories
            main(os.getcwd())
        else:
            if os.path.exists(sys.argv[1]):
                main(sys.argv[1])
    except Exception as e:
        print(e)
