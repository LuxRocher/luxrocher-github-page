# Create dummy files with age > 30 days
import os, datetime
dir_path = '/home/floris/Documents/OS3/Q3/data'
file_names = ['dummy1.csv', 'dummy2.csv']

# Main function
def main():
    for file in file_names:
        file_path = os.path.join(dir_path, file)
        
        try:
            f = open(file_path, 'a+')
            f.close()
        except OSError:
            print('\nError: file could not be created.')
            return 10
            
        # Get mode octal string
        # Here everyone gets full permission
        modeID = int('777', 8)
        
        try:
            os.chmod(file_path, modeID)
        except OSError:
            print('\nError: no permission, or else')
            return 20
            
        # Change last modification date
        new_mod_time = datetime.datetime(2024, 5, 1, 12, 0, 0)
        timestamp = new_mod_time.timestamp()
        os.utime(file_path, (timestamp, timestamp))
    
    print('Successful')
    return 0


# Starts script
output_code = main()
print(output_code)