# Question 2 - Solving directory administration via shell scripting
# Import libraries
import os, pwd, grp
from pwd import getpwnam
from grp import getgrnam

# Initialize variables
# By default we have that permissions are set by:
#   0 = none, 1 = x, 2 = w, 3 = wx, 4 = r, 5 = rx, 6 = rw and 7 = rwx
dir_data = [
    {'subdir': 'config', 'owner': 'admin', 'group': 'ops', 'modeID': '700'},
    {'subdir': 'data', 'owner': 'admin', 'group': 'ops', 'modeID': '770'},
    {'subdir': 'logs', 'owner': 'floris', 'group': 'devs', 'modeID': '750'},
    {'subdir': 'scripts', 'owner': 'admin', 'group': 'ops', 'modeID': '755'}
]


# Main Function
def main():
    # Obtains the verified input path
    dir_path = getPath()
    
    for directory in dir_data:
        # Set subdir path
        subdir_path = os.path.join(dir_path, directory['subdir'])
    
        # Get mode octal string
        modeID = int(directory['modeID'], 8)
        
        # Obtain uID and gID
        uID, gID = getID(directory)
    
        # Verifies if subdir exists
        if os.path.isdir(subdir_path):
            # Get subdir information
            subdir_data = os.stat(subdir_path)
            
            # Verify owner, else adjust
            if subdir_data.st_uid != uID:   
                try:
                    os.chown(subdir_path, uID, -1)
                except OSError:
                    print('\nError: no permission, or else.')
                    return 20
        
            # Verify group, else adjust
            if subdir_data.st_gid != gID:   
                try:
                    os.chown(subdir_path, -1, gID)
                except OSError:
                    print('\nError: no permission, or else.')
                    return 20
            
            # Verify permissions, else adjust
            if (subdir_data.st_mode & 0o777) != modeID:   
                try:
                    os.chmod(subdir_path, modeID)
                except OSError:
                    print('\nError: no permission, or else')
                    return 30
                       
        else:
            # Subdir not present, so create
            try:
                os.makedirs(subdir_path)
                os.chmod(subdir_path, modeID)
                os.chown(subdir_path, uID, gID)
            except OSError:
                print('\nError: no permission, or else')
                return 10
    
    print('\nExecution successful')
    return 0
        

# Returns required input
def getPath():
    while True:
        inp_path = input('Enter the path: ')
        
        # Verifies validity
        if os.path.isdir(inp_path):
            return inp_path
        print('Error: path is invalid. Please retry.')


# Obtains user ID and group ID
def getID(file):
    uID = getpwnam(file['owner']).pw_uid
    gID = getgrnam(file['group']).gr_gid
    
    return uID, gID


# Starts script
output_code = main()
print(output_code)
