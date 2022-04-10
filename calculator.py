from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
import math

# Set window default size
Window.size = (550,750)

# Set window background-color
Window.clearcolor = (255, 255, 255, 1)

# Load .kv file
Builder.load_file('calcUI.kv')

# Main window of app
class MyLayout(Widget):
    def clear(self):
        # Set default text when opened
        self.ids.calc_input.text = "0"
    
    # Function to display the buttons pressed
    def button_press(self, button):
        # Get current text from screen
        temp = self.ids.calc_input.text
        
        # If the display is '0' or Error, clear the screen before the next button press
        if temp == '0' or temp == 'Error':
            # But if there are certain fuctions pressed, then apply them to the 0
            if (temp == '0' or temp == 'Error') and (button == '^' or button == '!'):
                self.ids.calc_input.text = f'0{button}'
            else:
                self.ids.calc_input.text = f'{button}'
        
        # Not allow two signs to be next to one another and replace the previous with the one pressed
        else:
            if button == '+' and (temp[-1] == '+' or temp[-1] == '-' or temp[-1] == 'x' or temp[-1] == '/' or temp[-1] == '.' or temp[-1] == '^' or temp[-1] == '√'):
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
            if button == '-' and (temp[-1] == '+' or temp[-1] == '-' or temp[-1] == 'x' or temp[-1] == '/' or temp[-1] == '.' or temp[-1] == '^' or temp[-1] == '√'):
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
            if button == 'x' and (temp[-1] == '+' or temp[-1] == '-' or temp[-1] == 'x' or temp[-1] == '/' or temp[-1] == '.' or temp[-1] == '^' or temp[-1] == '√'):
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
            if button == '/' and (temp[-1] == '+' or temp[-1] == '-' or temp[-1] == 'x' or temp[-1] == '/' or temp[-1] == '.' or temp[-1] == '^' or temp[-1] == '√'):
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
            if button == '^' and (temp[-1] == '+' or temp[-1] == '-' or temp[-1] == 'x' or temp[-1] == '/' or temp[-1] == '.' or temp[-1] == '^' or temp[-1] == '√'):
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
                
            # For the 'π' and 'e' characters we can allow signs but not 'π' and 'e' next to one another
            if button == 'π' and temp[-1] == 'e':
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
            if button == 'e' and temp[-1] == 'π':
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
            if button == '!' and (temp[-1] == '+' or temp[-1] == '-' or temp[-1] == 'x' or temp[-1] == '/' or temp[-1] == '.' or temp[-1] == '^' or temp[-1] == '√'):
                temp = temp[:-1]
                self.ids.calc_input.text = f'{temp}{button}'
            else:
                self.ids.calc_input.text = f'{temp}{button}'
    
    # Function that does not allow more than 1 dot in a number or right after a sign
    def dot(self):
        # Assign the current text in a variable 'temp'
        temp = self.ids.calc_input.text
        # Remove the signs from the text and then split them into a list
        num_list = temp.replace('+', ' ').replace('-', ' ').replace('x', ' ').replace('/', ' ').split()
        
        # Not allow two dots next to one another, right after signs or after characters 'π' and 'e'
        if '.' in num_list[-1] or (temp[-1] == '+' or temp[-1] == '-' or temp[-1] == 'x' or temp[-1] == '/' or temp[-1] == '.' or temp[-1] == 'π' or temp[-1] == 'e' or temp[-1] == '√'):
            pass
        else:
            self.ids.calc_input.text = temp+'.'
            
    # Function after pressing '=' that calculates the answer
    def equals(self):
        # Assign the current text in a variable 'temp'
        temp = self.ids.calc_input.text
        
        # A string with all the numbers right after the sqrt sign
        nums = ''
        
        # We use a boolean variable as a switch in order to get the numbers right after the sqrt sign and stop
        # when we find a sign
        stat = False
        
        # Put it in a try function in order to display 'Error', if any error occurs
        try:
            # Replace certain signs that the 'eval()' function does not recognize
            if 'x' in temp:
                temp = temp.replace('x', '*')
            if '^' in temp:
                temp = temp.replace('^', '**')
            if 'π' in temp:
                temp = temp.replace('π', '3.141')
            if 'e' in temp:
                temp = temp.replace('e', '2.718')
            
            # The only way to calculate the '√' signs is with 'sqrt()' function from the math module
            # and then replace them with the answer
            if '√' in temp:
                for i in temp:
                    if stat == True:
                        if i == '+' or i == '-' or i == 'x' or i == '*' or i == '/' or i == '^' or i == '**':
                            break  
                        else:
                            nums += i
                    if i == '√':
                        stat = True
        
                sqrt_ans = math.sqrt(float(nums))
                nums = f'√{nums}'
                temp = temp.replace(str(nums), str(sqrt_ans))
                            
            answer = str(eval(temp))
            dotlen = answer.split('.')
            
            # If the answer has more than 7 decimal numbers, remove 6 of them in order to fit the screen
            if '.' in answer and len(dotlen[1]) > 7:
                 answer = answer[:-6]
            
            # Dispaly the answer on screen
            self.ids.calc_input.text = str(answer)
            
            # Display the previous calculaton above the current calculation
            self.ids.prev_calc.text = f'{temp} = {answer}'
        except:
            # Error handling
            self.ids.calc_input.text = 'Error'            
    
    # Function that deletes the last typed number, for the button '<<'
    def DeleteLast(self):
        temp = self.ids.calc_input.text
        temp = temp[:-1]
        self.ids.calc_input.text = temp
        
        
        

# App Class
class CalculatorApp(App):
    def build(self):
        return MyLayout()

# Start the app
if __name__ == '__main__':
    CalculatorApp().run()
