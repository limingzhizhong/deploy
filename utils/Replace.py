import fileinput


def ModifyFile(file_name, time):
    for line in fileinput.input(file_name, backup='.bak', inplace=True):
        print(line.rstrip().replace('$time', time))
