# Question 4 - Solving file naming and permissions
# Import libraries
import os, stat


# Initialize variables
allowed_ext = ['.py', '.sh', '.conf', '.md', '.txt']


# Main function
def main():
    # Obtains and verifies input path
    dir_path = getPath()
    if dir_path == 10:
        print('\nError: path is invalid.')
        return 10
            
    # Obtain all files of this directory
    for file_fname in os.listdir(dir_path):
        # Absolute path
        file_path = os.path.join(dir_path, file_fname)
        
        if os.path.isfile(file_path):
            # Split filename and extension
            file_name, file_ext = os.path.splitext(file_fname)

            # Validate name
            if not valName(file_name):
                print('Warning: invalid filename:', file_fname)  
                
            # Validate extension
            if not valExt(file_ext):
                print('Warning: invalid extension:', file_fname) 
            
            try:
                # Obtain file mode for permission
                file_mode = os.stat(file_path).st_mode
                
                # Validate permission and correct
                val_result = valPer(file_path, file_mode, file_name)
                
                if val_result != 0:
                    print('\nError: no permission to modify file permissions.')
                    return val_result
                
            except OSError:
                print('\nError: file stat failed. No permission, or else')
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


# Validate name
def valName(name):
    for char in name:
        # Name only contains numbers, letters, underscore or dash
        if not char.isalnum() and char != '_' and char != '-':
            return False
    return True
    
    
# Validate extension
def valExt(ext):
    return ext in allowed_ext
        
        
# Remove permissions
def valPer(path, mode, name):
    # Validate only group reading permission
    if mode & stat.S_IWGRP or mode & stat.S_IXGRP:
        print('Warning: group has writing and/or executing permission:', name)
        
        try:
            # Correct permissions
            cor_mode = mode & ~stat.S_IWGRP & ~stat.S_IXGRP
            os.chmod(path, cor_mode)
            print('Note: group writing and/or executing permission has been removed for:', name)
            return 0
        except OSError:
            return 20
    
    return 0


# Starts script
output_code = main()
print(output_code)