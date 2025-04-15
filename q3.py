# Question 3 - Solving recursive file scanning
# Import libraries
import os, pwd, grp, pathlib, stat, datetime
from pwd import getpwnam
from grp import getgrnam


# Main function
def main():
    # Obtains and verifies input path
    dir_path = getPath()
    if dir_path == 10:
        print('\nError: path is invalid.')
        return 10
    else:
        dir_path = pathlib.Path(dir_path)
    
    # Obtain current time
    cur_time = datetime.datetime.now()
    
    # Obtain all paths of this directory
    for path in dir_path.rglob('*'):
        if path.is_file():
            # Prints relative path
            print('File:', path.relative_to(dir_path))
            
            try:
                # Obtain file information
                file_info = os.stat(path)
                file_per = stat.filemode(file_info.st_mode)
            
                # Print owner, group and permissions
                print('Owner:', pwd.getpwuid(file_info.st_uid)[0])
                print('Group:', grp.getgrgid(file_info.st_gid)[0])
                print('Permission:', file_per)
                
                # Check the age of the file
                file_lastmod = datetime.datetime.fromtimestamp(file_info.st_mtime)
                if (cur_time - file_lastmod).days > 30:
                    if file_info.st_mode & stat.S_IWOTH:
                        print('Warning: Old and world-writable file found:', path)
                        inp_delete = input('Do you want to delete this file? [y/N]')
                        
                        # Delete file only if user wants to
                        if inp_delete == 'y' or inp_delete == 'Y':
                            if fileDelete(path):
                                print('File was deleted successfully')
                            else:
                                print('\nError: file deletion failed')
                                return 20
                print('')
            except OSError:
                print('\nError: no permission, or else')
                return 30   
                
    print('Execution successful')
    return 0


# Asks for the input path
def getPath():
    inp_path = input('Enter the path: ')
    
    # Verifies validity
    if os.path.isdir(inp_path):
        return inp_path
    else:
        return 10
        
        
# Delete file
def fileDelete(file):
    try:
        os.remove(file)
        return True
    except OSError:
        return False
        

# Starts script
output_code = main()
print(output_code)
