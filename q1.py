# Question 1 - Solving file administration via shell scripting
# Import libraries
import os, pwd, grp
from pwd import getpwnam
from grp import getgrnam

# Initialize variables
# By default we have that permissions are set by:
#   0 = none, 1 = x, 2 = w, 3 = wx, 4 = r, 5 = rx, 6 = rw and 7 = rwx
dir_data = [
    {'filename': 'config.txt', 'owner': 'admin', 'group': 'ops', 'modeID': '640'},
    {'filename': 'server.log', 'owner': 'admin', 'group': 'ops', 'modeID': '644'},
    {'filename': 'backup.tar', 'owner': 'admin', 'group': 'ops', 'modeID': '600'},
    {'filename': 'run.sh', 'owner': 'floris', 'group': 'devs', 'modeID': '750'},
    {'filename': 'notes.md', 'owner': 'floris', 'group': 'devs', 'modeID': '664'},
]


# Main Function
def main():
    # Obtains the verified input path
    dir_path = getPath()
    
    # Create file if not present
    for file in dir_data:
        file_path = os.path.join(dir_path, file['filename'])
        
        try:
            f = open(file_path, 'a+')
            f.close()
        except OSError:
            print('\nError: file could not be created.')
            return 10
         
        # Obtain uID and gID
        uID, gID = getID(file)
        
        # Get file information
        file_data = os.stat(file_path)
        
        # Verify owner, else adjust
        if file_data.st_uid != uID:   
            try:
                os.chown(file_path, uID, -1)
            except OSError:
                print('\nError: no permission, or else.')
                return 20
        
        # Verify group, else adjust
        if file_data.st_gid != gID:   
            try:
                os.chown(file_path, -1, gID)
            except OSError:
                print('\nError: no permission, or else.')
                return 20
        
        # Get mode octal string
        modeID = int(file['modeID'], 8)
        
        # Verify permissions, else adjust
        if (file_data.st_mode & 0o777) != modeID:   
            try:
                os.chmod(file_path, modeID)
            except OSError:
                print('\nError: no permission, or else')
                return 30
    
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
