import math
from os import path
import wave_helper as helper

MAX_VOLUME = 32767
SAMPLE_RATE = 2000
MIN_VOLUME = -32768


def show_main_menu():
    """
    Prints the main menu and gets an input from the user
    :return: returns the input from the user
    """
    print(
        '1. Edit .wav file\n2. Compose melody in the .wav format\n3. '
        'Exit the program')
    return input("Please enter your choice: ")


def show_edit_menu():
    """
    Prints the edit menu and gets an input from the user
    :return: returns the input from the user
    """
    print(
        '1. Reverse\n2. Fast forward\n3. Slow motion\n4. Volume '
        'enhancing\n5. Volume reducing\n6. Low pass filter\n7. End '
        'menu')
    return input("Please enter your choice: ")


def reverse_audio(audio_data):
    """
    :param audio_data: List of lists with the current wav data
    :return reversed_list: list from end to beginning
    """
    reversed_list = [audio_data[i] for i in range(len(audio_data) - 1, -1, -1)]
    return reversed_list


def fast_forward(audio_data):
    """
    :param audio_data: List of lists with the current wav data
    :return fast_audio: every even sample in audio_data
    """
    fast_audio = [audio_data[location] for location in
                  range(0, len(audio_data), 2)]
    return fast_audio


def slow_motion(audio_data):
    """
    :param audio_data: List of lists with the current wav data
    :return slow audio: audio_data, with extra sample between every tow.
    """
    slow_audio = []
    # Running util the place before the last one so that i could do the average
    for location in range(len(audio_data) - 1):
        slow_audio.append(audio_data[location])
        slow_audio.append([int((audio_data[location][0] +
                                audio_data[location + 1][0]) / 2),
                           int((audio_data[location][1] +
                                audio_data[location + 1][1]) / 2)])
    # Adding the last audio data
    slow_audio.append(audio_data[-1])
    return slow_audio


def enhancing_volume(audio_data):
    """
    :param audio_data: List of lists with the current wav data
    :return enhanced_audio: every sample is 1.2 times bigger
    """
    enhanced_audio = []
    for data in audio_data:
        current_data = []
        if data[0] * 1.2 > MAX_VOLUME:
            current_data.append(MAX_VOLUME)
        elif data[0] * 1.2 < MIN_VOLUME:
            current_data.append(MIN_VOLUME)
        else:
            current_data.append(int(data[0] * 1.2))
        if data[1] * 1.2 > MAX_VOLUME:
            current_data.append(MAX_VOLUME)
        elif data[1] * 1.2 < MIN_VOLUME:
            current_data.append(-MIN_VOLUME)
        else:
            current_data.append(int(data[1] * 1.2))
        enhanced_audio.append(current_data)
    return enhanced_audio


def reducing_volume(audio_data):
    """
    :param audio_data: List of lists with the current wav data
    :return enhanced_audio: every sample is 1.2 times bigger
    """
    reduced_audio = [[int(data[0] / 1.2), int(data[1] / 1.2)] for data in
                     audio_data]
    return reduced_audio


def average_low_bass(first, second, third):
    """
    :param first: the first tuple with the audio data
    :param second: the second tuple with the audio data
    :param third: the third tuple with the audio data
    :return: list with two items - the average of the first item in the data,
    adn the average of the second item in the data.
    """
    return [int((first[0] + second[0] + third[0]) / 3),
            int((first[1] + second[1] + third[1]) / 3)]


def low_pass_filter(audio_data):
    """
    :param audio_data: List of lists with the current wav data
    :return low_pass_data: updated data by formula.
    """
    # First value:
    low_pass_data = [[int((audio_data[0][0] + audio_data[1][0]) / 2),
                      int((audio_data[0][1] + audio_data[1][1]) / 2)]]
    # Running from the second list to the list before the last:
    for index in range(1, len(audio_data) - 1):
        low_pass_data.append(average_low_bass(audio_data[index - 1],
                                              audio_data[index],
                                              audio_data[index + 1]))
    # Adding the last value:
    low_pass_data.append([int((audio_data[-2][0] + audio_data[-1][0]) / 2),
                          int((audio_data[-2][1] + audio_data[-1][1]) / 2)])
    return low_pass_data


def edit_main_func(audio_data):
    """
    The main function the is responsible to edit the audio data according to
    the user input
    :param audio_data: the audio data of the file
    :return: the edited audio data
    """
    # A dict that I use to check if the input is valid and to call the relevant
    # change functions
    edit_menu_dict = {'1': reverse_audio,
                      '2': fast_forward,
                      '3': slow_motion,
                      '4': enhancing_volume,
                      '5': reducing_volume,
                      '6': low_pass_filter,
                      '7': show_main_menu}
    changed_data = audio_data[:]
    while True:
        user_input = show_edit_menu()
        # Invalid input:
        if user_input not in edit_menu_dict.keys():
            continue
        # Valid input:
        else:
            # Exit input:
            if user_input == '7':
                return changed_data
            else:
                changed_data = edit_menu_dict[user_input](changed_data)
                print("The file has been edited\n")


def get_guidelines_file():
    """
    Waiting for the an input file with the composition data
    :return: the path of the file with the composition data
    """
    # Runs until valid input from the user
    while True:
        file = input("Enter file name. The file should include guidelines "
                     "for composition:\n")
        # Checks if the file exists
        if path.isfile(file):
            return file
        else:
            print("File not found")


def get_guidelines(guidelines_file):
    """
    extracts the instructions from the guidelines file
    :param guidelines_file: the file with the guidelines
    :return: the guide lines list with the
    """
    with open(guidelines_file, 'r') as file:
        list_file = file.read()
    list_file = list_file.split()
    instructions = [(list_file[i], list_file[i + 1]) for i in
                    range(0, len(list_file), 2)]
    return instructions


def calc_sample(note, index):
    """
    calculates the value of the audio according to the note and index
    :param note: the note the user wants to compose
    :param index: the location in the composition list
    :return:
    """
    note_frequency = {'A': 440,
                      'B': 494,
                      'C': 523,
                      'D': 587,
                      'E': 659,
                      'F': 698,
                      'G': 784,
                      'Q': 0
                      }
    sample_per_cycle = SAMPLE_RATE / note_frequency[note]
    return int(MAX_VOLUME * math.sin(math.pi * 2 * (index / sample_per_cycle)))


def compose(instructions):
    """
    creates the composition according to the instructions
    :param instructions: list with the composing instructions
    :return: a list with the audio of the composition
    """
    composition = []
    for item in instructions:
        note = item[0]
        time = int(item[1])
        # The first item should be [0,0]
        composition.append([0, 0])
        for i in range(time * 125):
            composition.append([calc_sample(note, i), calc_sample(note, i)])
    return composition


def finish_process(frame_rate, audio_data):
    """
    saves the audio file to the location given by the user
    :param frame_rate: the frame rate of the sample
    :param audio_data: list with the data of the audio
    """
    file_name = input("Enter a name for the audio file:\n")
    helper.save_wave(frame_rate, audio_data, file_name)


def get_file_to_edit():
    """
    gets the file to edit. runs until the user enters a valid input, and prints
    error messages if he enters invalid ones.
    :return: the loaded audio file
    """
    # Runs until the user enters a valid file
    while True:
        file = input("Enter file name. The file should include audio to "
                     "edit\n")
        if path.isfile(file):
            # Succeeded loading the wav file
            if helper.load_wave(file) != -1:
                return helper.load_wave(file)
            # Failed loading the wav file
            else:
                print("File could not be loaded properly")
        else:
            print("File not found")


def main_menu_func():
    """
    the core of the program. Shows the main menu and lets the user decide what
    he wants to do with the wav file. In the end, saves the new file to the
    location given by the user, and by pressing 3 exits the program.
    """
    # Runs until the user presses 3 and exists the program
    while True:
        user_input = show_main_menu()
        # Runs until the user enters a valid input to the main menu
        while True:
            # Checks for invalid input
            if user_input not in ['1', '2', '3']:
                print("Invalid input!")
            else:
                break
            user_input = show_main_menu()
        if user_input == '1':
            # Gets the frame rate and the audio data using get_file_to_edit
            frame_rate, data_list = get_file_to_edit()
            # Runs the edit menu
            new_data_list = edit_main_func(data_list)
            # Saves the edited file
            finish_process(frame_rate, new_data_list)
        if user_input == '2':
            guideline_file = get_guidelines_file()
            instructions = get_guidelines(guideline_file)
            # Creates the composition according to the instructions
            composition = compose(instructions)
            # Enters the composition audio data to the variable
            new_data_list = edit_main_func(composition)
            # Saves the edited composition file
            finish_process(SAMPLE_RATE, new_data_list)
        if user_input == '3':
            break


if __name__ == '__main__':
    main_menu_func()
