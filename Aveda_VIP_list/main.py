from database import DatabaseManager

db = DatabaseManager('aveda_vip.db')
db.setup_db()

# Display menu, checks if the user input is an integer.


def main_menu(client):
    menu_string = (
        '\n\t** MAIN MENU **\n'
        '\nClient: {} {}\n'
        '\t1) Register for an appointment\n'
        '\t2) Drop an appointment\n'
        '\t3) Display appointments\n'
        '\t4) Quit\n'
        '\nEnter Selection'
    ).format(client.first_name, client.last_name)
    while True:
        menu_choice = get_user_int(menu_string, range(1, 5))

        if menu_choice == 1:
            add_appointment(client)
        elif menu_choice == 2:
            delete_appointment(client)
        elif menu_choice == 3:
            display_appointment(client)
        elif menu_choice == 4:
            break


# Menu for register an appointment
def add_appointment(client):
    menu_string = (
        '\nREGISTER AN APPOINTMENT\n'
        '\t1) By Appointment ID\n'
        '\t2) Search for an appointment by Name\n'
        '\t3) Back\n'
        '\n-> Enter Selection'
    )
    # Loop to check the options entered by the user
    while True:
        menu_choice = get_user_int(menu_string, range(1, 4))

        if menu_choice == 1:
            appointment_id = get_user_int('-> Enter Appointment ID')
            appointment = db.get_appointment(appointment_id)
            if appointment:
                db.register_appointment(client, appointment)
                print('\n --> Appointment for '+appointment.name+' was successfully entered for ' + client.first_name+'<--')
                print('------------------------------------------------------------------------------')
            else:
                print('** No appointment found with id:', appointment_id)
        elif menu_choice == 2:
            appointment = search_appointment(client)
            if appointment:
                db.register_appointment(client, appointment)
                print('\n --> Appointment for '+appointment.name+' was successfully entered for ' + client.first_name+'<--')
                print('------------------------------------------------------------------------------')
        elif menu_choice == 3:
            return


# Drop a appointment based on the appointment id entered by the user
# and print message with current appointment list for current client
def delete_appointment(client):
    client_appointment_list = db.get_appointment_by_client_id(client.id)
    if len(client_appointment_list) == 0:
        print(client.full_name + " does not have any appointment in the list yet")
        return
    else:
        print('The current appointment list for ' + client.full_name)
        for appointment in client_appointment_list:
            print("\t{}.{} ".format(appointment.id, appointment.name))
    while True:
        drop_question = '-> Enter appointment id to drop from the given appointment list'
        drop_appointment_id = get_user_int(drop_question)
        Confirmation_Message = input('Do You want to drop ' + db.get_appointment(drop_appointment_id).name + ' from your appointment list(Y/N)?')
        if str(Confirmation_Message).upper() == 'Y':
            client_appointment_idlist = [appointment.id for appointment in client_appointment_list]
            if drop_appointment_id in client_appointment_idlist:
                db.drop_appointment(client.id, drop_appointment_id)
                print('\n -->'+ str(db.get_appointment(drop_appointment_id).name) + 'has been dropped from your current appointment list')
                print('-------------------------------------------------------------------------------------------------------')
                break
            else:
                print('No appointment found with this ID in this list. Please try again')
        elif str(Confirmation_Message).upper() == 'N':
            return
        else:
            print("XX~~ Invalid entry ~~XX")
            continue
    return


# Display the schedule for the current client.
def display_appointment(client):
    appointment_info = db.get_appointment_by_client_id(client.id)
    if len(appointment_info) == 0:
        print(client.full_name + ' does not have any appointment in the list yet')
    else:

        print('\n -->Appointment list for client name: ' + client.full_name)
        print('------------------------------------------------------------------------------')
        for appointment in appointment_info:
            print("\t{} ({})".format(appointment.name, appointment.professional.full_name))


# Search for appointment by name
def search_appointment(client):
    appointment_name = get_user_string('Enter appointment Name')
    appointments = db.get_appointment_by_name(appointment_name)
    if not appointments:
        print('No appointment with that name found.')
        return
    while True:
        appointment_count = len(appointments)
        menu_string = '\nSelect an appointment\n'
        for n, appointment in enumerate(appointments):
            menu_string += '\t{}) {}\n'.format(n + 1, appointment.name)
        menu_string += '\t{}) Back\n'.format(appointment_count + 1)
        menu_string += '\nSelect a appointment'
        menu_choice = get_user_int(menu_string, range(1, appointment_count + 2))
        if menu_choice <= appointment_count:
            return appointments[menu_choice - 1]
        else:
            return None


# type and range validation
def get_user_int(message, valid_range=None):
    while True:
        user_input = input('{}: '.format(message))
        try:
            number = int(user_input)
        except ValueError:
            print('You must enter a whole number.')
            continue
        if valid_range and number not in valid_range:
            _min = min(valid_range)
            _max = max(valid_range)
            print('You must enter a number from {} to {}.'.format(_min, _max))
            continue
        return number


# If user's input is empty, it will ask user to enter something
def get_user_string(message):
    while True:
        user_input = input('{}: '.format(message))
        if user_input:
            return user_input
        else:
            print('You must enter something.')

# Get client name and displays for the first time
def main():
    client = None
    while True:
        client_id = get_user_int('Enter client ID')
        client = db.get_client(client_id)
        # If id does not exist
        if not client:
            print('No client found with id:', client_id)
            continue
        break
        # Calls menu if id is invalid
    if client:
        main_menu(client)
    # If user selects option 4 to quit
    print('\n ** Program is closed! **')

main()
