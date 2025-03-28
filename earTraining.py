import os
import random
import threading
import time
import pygame
import streamlit as st
import json

path = 'Notes/'                    # Enter your path

files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ] # Return list with filenames of notes
files = sorted(files)

pygame.mixer.init()

start_event = threading.Event()
stop_event = threading.Event()

def noteThread(file):
    start_event.wait()
    note = pygame.mixer.Sound(file)
    note.play()
    stop_event.wait()

    fade_duration = 0.1  # 2 seconds
    fade_steps = 50      # Number of steps to fade out (higher means smoother fade)

    # Calculate the volume decrement per step
    volume_decrement = 1.0 / fade_steps

    # Gradually decrease the volume over time
    for step in range(fade_steps):
        volume = 1.0 - (step * volume_decrement)
        note.set_volume(volume)  # Set the volume for the current step
        time.sleep(fade_duration / fade_steps)  # Wait before reducing volume further
    note.stop()

def playNotes(duration = 1):
    threads = []
    delay = 60/settings.tempo if not settings.simultaneous else 0
    time.sleep(0.1)
    start_event.clear()
    stop_event.clear()

    if not settings.simultaneous:
        start_event.set()
    for note in st.session_state.notes:
        threads.append(threading.Thread(target=noteThread, args=(path + files[note],)))      # Create own thread for every note

    for thread in threads:
        thread.start()                                                                        # Play note
        delay = delay / random.choice([0.5,1,2]) if settings.rhythm else delay                         # Use random rhythm for playback (quarter, eigth, sixteenth)
        time.sleep(delay)

    if settings.simultaneous:
        start_event.set()
    time.sleep(settings.duration)
    stop_event.set()

def returnNoteNames(notes):
    names = []
    for note in notes:
        name = files[note].split('.')[2]
        names.append(name)
    return (' ').join(names)

def check_solution(answer_key = None, check_key = False, showAnswer = True):
    answerOutput = ''
    if answer_key or check_key:
        if settings.answerMode:
            if st.session_state.answer == (' ').join(st.session_state.playedIntervals):
                answerOutput += "Correct!"
            else:
                answerOutput += "False! Interval(s): " + (' ').join(st.session_state.playedIntervals)
            changeWeights(st.session_state.answer.split(' '), st.session_state.playedIntervals)
        else:
            answerOutput += 'Intervals: ' + (' ').join(st.session_state.playedIntervals)  # Print solution
        if settings.showNotes:
            answerOutput += '  \nNotes: ' + st.session_state.noteNames
    if showAnswer and settings.saveProgress:
        st.write(answerOutput)

def changeWeights(answer, solution):
    with open('config.json') as f: config = json.loads(f.read())

    for x in range(len(solution)):
        specifier = st.session_state.directions[x]
        interval = [halfsteps for halfsteps, name in data.intervals.items() if name == solution[x]][0]

        if solution[x] == answer[x]:                        # if correct answer -> decrease weight, else increase
            modificator = -settings.weightModificator
        else:
            modificator = settings.weightModificator

        config['weights'][settings.mode][str(interval)][specifier] += modificator

    updateConfig(config)

def updateConfig(config):
    config = json.dumps(config, indent = 4)
    with open('config.json', 'w') as f: f.write(config)

class data:
    def __init__(self):
        self.intervals = {
            0: '1', 1: 'b2', 2: '2', 3: 'b3', 4: '3', 5: '4', 6: 'b5', 7: '5', 8: 'b6', 9: '6',
            10: 'b7', 11: 'M7', 12: '8', 13: 'b2+8', 14: '2+8', 15: 'b3+8', 16: '3+8', 17: '4+8',
            18: 'b5+8', 19: '5+8', 20: 'b6+8', 21: '6+8', 22: 'b7+8', 23: 'M7+8', 24: '2*8',
            25: 'b2+2*8', 26: '2+2*8', 27: 'b3+2*8', 28: '3+2*8', 29: '4+2*8', 30: 'b5+2*8',
            31: '5+2*8', 32: 'b6+2*8', 33: '6+2*8', 34: 'b7+2*8', 35: 'M7+2*8', 36: '3*8',
            37: 'b2+3*8', 38: '2+3*8', 39: 'b3+3*8', 40: '3+3*8', 41: '4+3*8', 42: 'b5+3*8',
            43: '5+3*8', 44: 'b6+3*8', 45: '6+3*8', 46: 'b7+3*8', 47: 'M7+3*8', 48: '4*8',
            49: 'b2+4*8', 50: '2+4*8', 51: 'b3+4*8', 52: '3+4*8', 53: '4+4*8', 54: 'b5+4*8',
            55: '5+4*8', 56: 'b6+4*8', 57: '6+4*8', 58: 'b7+4*8', 59: 'M7+4*8', 60: '5*8',
            61: 'b2+5*8', 62: '2+5*8', 63: 'b3+5*8', 64: '3+5*8', 65: '4+5*8', 66: 'b5+5*8',
            67: '5+5*8', 68: 'b6+5*8', 69: '6+5*8', 70: 'b7+5*8', 71: 'M7+5*8', 72: '6*8',
            73: 'b2+6*8', 74: '2+6*8', 75: 'b3+6*8', 76: '3+6*8', 77: '4+6*8', 78: 'b5+6*8',
            79: '5+6*8', 80: 'b6+6*8', 81: '6+6*8', 82: 'b7+6*8', 83: 'M7+6*8', 84: '7*8',
            85: 'b2+7*8', 86: '2+7*8', 87: 'b3+7*8'
        }

class generateIntervals:
    # Dictionary to convert half steps to interval:
    def __init__(self):


        with open('config.json') as f: config = json.loads(f.read())

        intervalWeights = config['weights']['Intervals']

        if settings.direction == 'All':
            direction = random.choice(['Ascending', 'Descending'])
        else:
            direction = settings.direction
        self.directions = []                    # Initialise Directions list for weight adjusting

        if direction == 'Ascending':
            self.notes = [random.randint(settings.pitchRange[0], settings.pitchRange[1]-settings.intervalRange[0])]             # First Note
        elif direction == 'Descending':
                self.notes = [random.randint(settings.pitchRange[0]+settings.intervalRange[0], settings.pitchRange[1])]

        for i in range(0, settings.n):
            if direction == 'Ascending':
                intervalLimitHigh = min(settings.intervalRange[1]+1, settings.pitchRange[1]-self.notes[i]+1)                      # Max interval can be the distance from the last note to the highest in range
                sign = 1        # Positive
            elif direction == 'Descending':
                intervalLimitHigh = min(settings.intervalRange[1]+1, self.notes[i]-settings.pitchRange[0]+1)                  # Max interval can be the distance from the last note to the lowest in range
                sign = -1       # Negative -> invert interval

            intervalLimitLow = settings.intervalRange[0]

            mode = 'Simultaneous' if settings.simultaneous else direction

            intervalSelectMap = {x: intervalWeights[str(x)][mode] for x in range(intervalLimitLow, intervalLimitHigh)}
            possibleIntervals = list(intervalSelectMap.keys())
            weights = list(intervalSelectMap.values())

            interval = random.choices(possibleIntervals, weights, k = 1)[0]
            self.notes.append(self.notes[i]+sign*interval)
            self.directions.append(direction)

            if settings.direction == 'All':                                                         # Determine direction for next interval
                direction = random.choice(['Ascending', 'Descending'])
            else:
                direction = settings.direction

        self.noteNames = returnNoteNames(self.notes)
        self.playedIntervals = []
        for j in range(len(self.notes)-1):
            self.playedIntervals.append(data.intervals[abs(self.notes[j+1]-self.notes[j])])

        st.session_state.noteNames = self.noteNames
        st.session_state.playedIntervals = self.playedIntervals
        st.session_state.notes = self.notes
        st.session_state.directions = self.directions

def triads():
    simultaneous = settings.simultaneous
    direction = settings.direction
    limits = [settings.lowerLimit, settings.upperLimit]
    answerMode = settings.answerMode
    tempo = settings.tempo
    rhythm = settings.rhythm

    triadOptions = {'Major': [[0,4,7],[0,3,8],[0,5,9]], 'Augmented': [[0,4,8],[0,4,8],[0,4,8]], 'Major b5': [[0,4,6],[0,2,8],[0,6,10]], 'Minor': [[0,3,7],[0,4,9],[0,5,8]], 'Diminished': [[0,3,6],[0,3,9],[0,6,9]], 'Sus': [[0,5,7],[0,2,7],[0,5,10]]}

    while True:
        triad, intervals = random.choice(list(triadOptions.items()))
        inversion = random.randint(0,2)
        lowest = random.randint(limits[0], limits[1])
        if lowest + intervals[inversion][2] > 87:
            lowest = 87 - intervals[inversion][2]

        if direction == 'All':
            direction = random.choice(['Ascending', 'Descending'])
        direction = 'Ascending' if simultaneous else direction

        match direction:
            case 'Ascending':
                notes = [lowest, lowest+intervals[inversion][1], lowest+intervals[inversion][2]]
            case 'Descending':
                notes = [lowest+intervals[inversion][2], lowest+intervals[inversion][1], lowest]
            case _:
                print('Not a valid play direction')
                quit()

        repeat = True
        while repeat:
            playNotes(notes, simultaneous, tempo, rhythm)
            if answerMode:
                solution = input('Enter Solution: ')           # Repeat until solution is entered
                if solution != '':
                    repeat = False
            else:
                repeat = input('Repeat? (y/n), (n = Show solution): ').lower().strip() == 'y'           # Repeat as long as y is entered, else go on

        noteNames = returnNoteNames(notes)

        if triad == 'Augmented':
            inversion = ''
        inversion = str(inversion)
        if answerMode:
            if solution == (triad + inversion):
                print("Correct!")
            else:
                print("False! It was ",  triad, inversion)
        else:
            print(f'Triad: {triad}, Inversion: {inversion}')
        print('Notes: ', noteNames)
        input("Next Triad")  # Wait for enter to play next interval

class getSettings:
    def __init__(self):
        with open('config.json') as f: config = json.loads(f.read())

        settings = config['settings']

        if st.session_state.get('show_settings', False):                    # Only if show settings is true

            st.header('Training mode Settings')
            st.write('')

            if st.button('Reset Settings', key = 'reset_settings'):
                with open('config_backup.json') as f: config_backup = json.loads(f.read())
                settings = config_backup['settings']

            self.mode = st.selectbox('Ear Training Area', ['Intervals', 'Triads'])
            match self.mode:
                case 'Intervals':
                    self.n = st.slider('How many?', 1, 10, settings['n'])
                    self.intervalRange = st.slider('Interval Range', 0, 88, settings['intervalRange'])
                    self.simultaneous = st.toggle('Play simultaneous?', settings['simultaneous'])
                    if not self.simultaneous:
                        self.direction = st.selectbox('Direction', ['Ascending', 'Descending', 'All'])

                        st.header('General Play Settings')
                        st.write('')

                        self.tempo = st.slider('Tempo', 1, 300, value = settings['tempo'], step = 5)
                        self.rhythm = settings['rhythm'] #self.rhythm = input('Randomize Rythm? (y/n) ').lower().strip() == 'y'
                    else:
                        self.direction = 'Ascending'
                        self.tempo = 0
                        self.rhythm = False
                case 'Triads':
                    self.simultaneous = st.checkbox('Play simultaneous?', settings['simultaneous'])
                    if not self.simultaneous:
                        self.direction = st.selectbox('Direction', ['Ascending', 'Descending', 'All'])

                        st.header('General Play Settings')
                        st.write('')

                        self.tempo = st.slider('Tempo', 1, 300, value = settings['tempo'], step = 5)
                        self.rhythm = settings['rhythm'] #self.rhythm = input('Randomize Rythm? (y/n) ').lower().strip() == 'y'
                    else:
                        self.direction = 'Ascending'
                        self.tempo = 0
                        self.rhythm = False
            self.duration = st.slider('Playback duration', min_value=0.0, max_value=5.0, value=settings['duration'], step=0.1)
            self.pitchRange = st.slider('Pitch Range', 0, 87, value = settings['pitchRange'])
            if self.intervalRange[0] > self.pitchRange[1]- self.pitchRange[0]:
                st.error('Decrease lower interval or pitch limit!')
                self.disableStart = True
            else:
                self.disableStart = False

            st.header('Answer and Progress Settings')
            st.write('')

            self.answerMode = st.toggle('Type answer mode?', settings['answerMode'], key = 'answerModeToggle')
            if self.answerMode:
                self.saveProgress = st.toggle('Save Progress', settings['saveProgress'], key = 'saveProgressToggle')
                if self.saveProgress:
                    self.weightModificator = st.slider('Learning Speed', 0.0, 0.2, value = settings['weightModificator'], step = 0.01)
                st.button('Reset Progress in current mode?', key = 'resetModeProgress')
                st.button('Reset all Progress?', key = 'resetProgress')
            possibleAdvanceModes = ['Click Button', 'Press enter'] if self.answerMode else ['Click Button', 'Auto']
            presetAdvanceMode = possibleAdvanceModes.index('Click Button' if settings['advanceMode'] not in possibleAdvanceModes else settings['advanceMode'])
            self.advanceMode = st.selectbox(label = 'Next question mode', options = possibleAdvanceModes, index = presetAdvanceMode)
            if self.advanceMode == 'Auto':
                self.answerMode = False
                self.questionPeriod = st.slider('Time between questions', 0.5, 10.0, value = settings['questionPeriod'], step = 0.5)
            self.showNotes = st.toggle('Show notes in answer?', settings['showNotes'])

            for key in self.__dict__:
                if key == 'tempo' and self.__dict__[key] == 0:      # Don't write tempo 0 (only if simultaneous playback is turned on)
                    continue
                config['settings'][key] = self.__dict__[key]
            updateConfig(config)
        else:                                                               # Get settings from file
            for key in settings:
                exec(f'self.{key} = settings[key]')         # Generate variables

        st.write('')
        st.write('')

class appState:
    def __init__(self):
        if st.session_state.get('resetModeProgress', False) or st.session_state.get('resetProgress', False):
            with open('config.json') as f: config = json.loads(f.read())
            with open('config_backup.json') as f: backup_config = json.loads(f.read())
            if st.session_state.get('resetProgress', False):
                config['weights'] = backup_config['weights']
            else:
                config['weights'][settings.mode] = backup_config['weights'][settings.mode]
            updateConfig(config)
            st.error("Progress Reset!")

        st.toggle('Show Settings', False, key = 'show_settings')
        if st.session_state.get('stopped', False) or not st.session_state.get('started', False):
            st.button('Start', 'started', disabled = settings.disableStart)
        else:
            st.session_state.started = True
            st.button('Stop', 'stopped')
            if not settings.advanceMode == 'Auto':
                st.button('Repeat', 'repeat')
        if (st.session_state.get('check', False) or st.session_state.get('answer', '') != '') and settings.advanceMode == 'Click Button' and not st.session_state.get('next', False) and not st.session_state.get('stopped', False):
            st.button('Next', 'next')


class getSolution:
    def __init__(self, answer_key = None, check_key = False):
        if settings.answerMode and (answer_key == None or settings.advanceMode != 'Click Button'):
            answerInput = st.text_input('Answer', key = 'answer')
        elif not settings.answerMode and check_key == False and not st.session_state.get('stopped', False):
            st.button('Check', 'check')

def train():
    start_key = st.session_state.get('started', False)
    stop_key = st.session_state.get('stopped', False)
    repeat_key = st.session_state.get('repeat', False)
    answer_key = st.session_state.get('answer', None)
    check_key = st.session_state.get('check', False)
    next_key = st.session_state.get('next', False)
    showAnswer = True

    if next_key or answer_key == '' and settings.advanceMode == 'Click Button':
        showAnswer = False
        answer_key = None
        check_key = False

    #print(start_key, repeat_key, answer_key, check_key, next_key)

    if start_key:
        if not settings.advanceMode == 'Auto':
            getSolution(answer_key, check_key)         # Create text input if not existing / check button if not pressed

        check_solution(answer_key, check_key, showAnswer)

        if answer_key and settings.advanceMode == 'Click Button':
            st.text_input('Answer', key = 'answer', value = st.session_state.answer, disabled=True)         # Disable Input
        if (not repeat_key and not answer_key) or ((answer_key or check_key) and settings.advanceMode != 'Click Button' and not repeat_key):
            match settings.mode:
                case 'Intervals':
                    generateIntervals()
                case 'Triads':
                    triads(settings)
        if (start_key and not stop_key) and (not (answer_key or check_key) or next_key or repeat_key or ((answer_key or check_key) and settings.advanceMode != 'Click Button')):    # Start or next or repeat --> play note
            playNotes()

        if settings.advanceMode == 'Auto' and (start_key and not stop_key):
            time.sleep(settings.questionPeriod)
            st.session_state.check = True
            st.rerun()




st.title('Ear Training (Under Development)')
st.write('')


data = data()
settings = getSettings()

#st.write(settings)

app = appState()

#st.write(app)



train()



