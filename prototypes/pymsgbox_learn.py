import pymsgbox

text_input = pymsgbox.prompt('Enter some text:', 'Text Input')

print(text_input)
pymsgbox.alert(f'You entered: {text_input}', 'Result')  # Pop-up message box