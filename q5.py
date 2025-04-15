# Question 5 - Solving user iteration and file scanning
# Import libraries
import os, pwd, stat


# Initialize variables
sens_files = ['.bash_history', '.ssh', '.ssh/authorized_keys', '.ssh/id_rsa', '.ssh/id_rsa.pub']

# Main function
def main():
    try: 
        # Obtain user database
        user_database = pwd.getpwall()
        
        # Loop through user database
        for user in user_database:
            if user.pw_uid >= 1000:
                if '/home' in user.pw_dir:                
                    # Obtain home directory info
                    home_info = os.stat(user.pw_dir)
                    
                    # Validate owner
                    if home_info.st_uid == user.pw_uid:  
                        err_home_own = False
                    else:
                        err_home_own = True
                    
                    # Valid modes for home directory
                    val_mode1 = int('700', 8)
                    val_mode2 = int('750', 8)
                    home_mode = home_info.st_mode & 0o777
                    
                    # Validate permissions
                    if home_mode == val_mode1 or home_mode == val_mode2:
                        err_home_per = False
                    else:
                        err_home_per = True
                    
                    # Create empty list for printing
                    err_file_own = []
                    err_file_per = []
                        
                    # Searches for sensitive files
                    for file in sens_files:                    
                        # Define path
                        file_path = os.path.join(user.pw_dir, file)
                        
                        if os.path.isfile(file_path):
                            # Obtain file info
                            file_info = os.stat(file_path)
                                                    
                            # Validate owner
                            if file_info.st_uid != user.pw_uid:
                                err_file_own.append(file)
                            
                            # Obtain file mode
                            file_mode = file_info.st_mode
                            
                            # Validate permissions
                            if file_mode & stat.S_IRGRP or file_mode & stat.S_IWGRP:
                                err_file_per.append(file)
                    
                    printOutput(user.pw_name, user.pw_dir, err_home_own, err_home_per, err_file_own, err_file_per)
                    
        print('Execution successful')
        return 0
    except PermissionError:
        print('\nError: no permission to access the user database.')
        return 10
    except OSError as e:
        print(f'\nError: OS error while accessing: {e}')
        return 30
    except Exception as e:
        print(f'\nError: unexpected error: {e}')
        return 30


# Print output summarized per user
def printOutput(name, home, ehome_own, ehome_per, efile_own, efile_per):
    print('Summary for', name)
    print('_'*25)
    if not ehome_own and not ehome_per and not efile_own and not efile_per:
        print('No issues found.')
    else:
        print('Home directory:', home)
        if ehome_own:
            print('Home directory is not owned by', name)
        
        if ehome_per:
            print('Home directory has insecure permissions.')
            
        if efile_own != []:
            print('The following files are not owned by' + name + ':')
            for file in efile_own:
                print('   -', file)
                
        if efile_per != []:
            print('The following files have insecure permissions:')
            for file in efile_per:
                print('   -', file)
                
    print('')
                    
            
# Starts script
output_code = main()
print(output_code)