# ---------------------------------------------------------------------------- #
# Title: Assignment 07
# Description: Program that gathers guest names and group sizes from the user,
#              shows the totals, and pickles the output to a binary file called RSVP.dat.
#              Will create a new binary file if it does not yet exist in the directory,
#              or open and add to the existing file if present.
#              Demonstrates pickling and error handling.
# ChangeLog (Who,When,What):
# KLMartinez,12/7/21,Created script
# ---------------------------------------------------------------------------- #

import pickle  # Imports the pickle module

# Data ---------------------------------------------------------------------- #
# Declare variables and constants
rsvp_file = 'RSVP.dat'
rsvp_lst = []  # A list that acts as a 'table' of dictionary rows

# Processing  --------------------------------------------------------------- #

def unpickle_data_from_file(file_name):
    """ Unpickes data from a binary file and loads it to a list.
        :param file_name: (string?) represents the file object
        :return: (list) of dictionary rows
    """
    objFile = open(file_name, 'rb')  # Reads the file, will give an error if there is no file
    list_of_rows = pickle.load(objFile)
    objFile.close()
    return list_of_rows

def pickle_data_to_file(file_name, list_of_rows):
    """ Saves data to a binary file by pickling it.
        :param file_name: (string?) represents the file object
        :param list_of_rows: (list) of dictionary rows to save
        :return: nothing
    """
    objFile = open(file_name, 'wb')  # Write mode, to overwrite previous contents with updated list
    pickle.dump(list_of_rows, objFile)
    objFile.close()

def add_guest_to_list(guest_name, group_size, list_of_rows):
    """ Adds data to the list

    :param guest_name: (string) guest name, to be entered by the user
    :param group_size: (string) number of guests in the group, to be entered by the user
    :param list_of_rows: (list) you want filled with file data
    :return: (list) of dictionary rows, with the new task added to it
    """
    row = {'Name': guest_name.strip(), 'Number': group_size}
    list_of_rows.append(row)
    return list_of_rows

def sum_guests(list_of_rows):
    """ Calculates the sum of the total number of guests attending.
        :param list_of_rows: (list) of dictionary rows to sum
        :return: (int) sum
    """
    guest_total = sum(item['Number'] for item in list_of_rows)  # Sum all Number values - must be stored as an integer
    return guest_total


# Presentation (Input/Output)  -------------------------------------------- #

def output_welcome():
    """  Display the description of the program to the user

    :return: nothing
    """
    print('\nWelcome to the RSVP program! \n'
          'This program helps you track the number of guests who are coming to your party.')
    #print()  # Extra line

def output_existing_list_confirmation():
    """ Tells the user that they will add to their existing file

    :return: nothing
    """
    print('Guests will be added to your existing list.')

def output_new_list_confirmation():
    """ Tells the user that a new file will be created

    :return: nothing
    """
    print('You are starting a new list.')

def output_menu():
    """  Display the program menu to the user

    :return: nothing
    """
    print('''
    Menu of Options
    1) Add a guest
    2) View full RSVP list
    3) Save and exit program
    ''')

def input_menu_choice():
    """ Gets the menu choice from a user

    :return: string
    """
    choice = str(input('Which option would you like to perform (1, 2, or 3)?: ')).strip()
    print()  # Add an extra line for looks
    return choice

def input_new_guest():
    """ Gets a guest name and number in party from the user

    :return: (tuple) new name and number in group
    """
    print('Enter the name of the invited guest, and the number in their group')
    guest_name = input('Name: ')  # User enters a name
    group_size = int(input('Number in group: '))  # User enters an integer
    print()  # Extra line
    return guest_name, group_size

def output_total_guests(total_guests):
    """ Prints the guest total, to be used with the output of sum_guests(list_of_rows)

    :param total_guests: (int) number of guests
    :return: (tuple) new name and number in group
    """
    print('The total number of guests is', total_guests)

def output_view_list(list_of_rows):
    """ Prints the guest total, to be used with the output of sum_guests(list_of_rows)

    :param list_of_rows: (list) of dictionary rows
    :return: nothing
    """
    print('Guest name and number in group:')
    for row in list_of_rows:
        print(row['Name'], row['Number'], sep='| ')

def output_pickle_exit_confirmation():
    """ Confirms that the list was saved

    :return: nothing
    """
    print('Your list has been pickled. Have a great party! Goodbye.')

def output_nodata_exit_confirmation():
    """ Says goodbye to the user

    :return: nothing
    """
    print('There was no list to save. To enter guests, please start the program again. Goodbye.')
    print()  # Add an extra line for looks

def output_exception_ValueError():
    """ Display an error message for ValueError

    :return: nothing
    """
    print('Group size must be an integer. Please try again.')
    print()  # Add an extra line for looks

class CustomException_UserChoice(Exception):
    """ Custom error message to raise if the user choice is not 1, 2, or 3

    :return: nothing
    """
    def __str__(self):
        return 'Oops! Please enter either 1, 2, or 3.'

# Main Body of Script  ------------------------------------------------------ #

output_welcome()  # Display program description

# Try/Except block to check if the file already exists in the same directory
try:  # If the file exists, unpickle it and load the list to the object rsvp_lst
    rsvp_lst = unpickle_data_from_file(rsvp_file)  # Unpickle the list do that it can be added to
    output_existing_list_confirmation()  # Confirm to the user that the existing list will be added to
    output_total_guests(sum_guests(rsvp_lst))  # Print a reminder of how many guests are on the list
except FileNotFoundError:  # If the file does not yet exist, print a message and move on
    output_new_list_confirmation()  # Confirm to the user that this will be a new list

while (True):
    output_menu()  # Display menu of options
    userChoice = input_menu_choice()  # Capture user menu selection
    try:  # Try/Except block to catch cases where the user enters a off-menu text
        if userChoice.strip() not in ['1','2','3']:  # Custom exception to remind the user to use 1, 2, or 3
            raise CustomException_UserChoice()
    except Exception as e:  # To handle other unexpected error cases
        print(e)


    if userChoice.strip() == '1':  # User selection 1: Add a guest
        try:  #Try/Except block to be sure group_size is an integer
            guest_name, group_size = input_new_guest()  # Prompt for new guest & number, upnack tuple
            add_guest_to_list(guest_name, group_size, rsvp_lst)  # Use input values as arguments
            output_total_guests(sum_guests(rsvp_lst))  # Display guest total
        except ValueError:  # Display error if the user entry is not an integer
            output_exception_ValueError()
        except Exception as e:  # To handle unexpected error cases
            print(e)

    elif userChoice == '2':  # User selection 2: View full RSVP list
        try:
            output_view_list(rsvp_lst)  # Display full contents of the list of dictionary rows
            output_total_guests(sum_guests(rsvp_lst))  # Display guest total
        except Exception as e:  # To handle unexpected error cases
            print(e)

    elif userChoice == '3':  # User selection 3: Save and exit
        if not rsvp_lst:  # Check if there is data in the list object, to avoid saving an empty list
            output_nodata_exit_confirmation()  # If list is empty, print an exit confirmation
        else:  # If list contains data, pickle and then exit
            pickle_data_to_file(rsvp_file, rsvp_lst)  # Pickles the list to the file. Overwrites any existing list.
            output_pickle_exit_confirmation()   # Print pickle and exit confirmation
        break  # Exit program