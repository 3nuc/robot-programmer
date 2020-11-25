class NXCBuilder():
    
    def __init__(self, turtle=None):
        
        self.FIRST_CODE_LINE = "task main() {"
        self.LAST_CODE_LINE = "}"
        self.OUTPUTS = "OUT_AC"
        
        self.__commands_stack = []
    
        self.turtle = turtle
    
    def add_forward_command(self, power, time):
        command = ('fwd', power, time)
        self.__commands_stack.append(command)
        self.__visualize_next_command(command)
    
    def add_rotate_command(self, degrees, power=100):
        command = ('rot', power, degrees)
        self.__commands_stack.append(command)
        self.__visualize_next_command(command)

    def add_wait_command(self, time):
        command = ('wait', time)
        self.__commands_stack.append(command)
        self.__visualize_next_command(command)
    
    def undo_last_command(self):
        if len(self.__commands_stack) >= 1:
            self.__commands_stack.pop()
            if self.turtle:
                self.turtle.undo()

    def generate_code(self, filename):
        nxc_code_lines = []

        nxc_code_lines.append(self.FIRST_CODE_LINE)
        
        for command in self.__commands_stack:
            cmd_type = command[0]
            
            if cmd_type == 'fwd':
                nxc_code_lines.append(f"\tOnFwd({self.OUTPUTS}, {command[1]});")
                nxc_code_lines.append(f"\tWait({command[2]});")
            elif cmd_type == 'rot':
                nxc_code_lines.append(f"\tRotateMotor({self.OUTPUTS}, {command[1]}, {command[2]});")
            elif cmd_type == 'wait':
                nxc_code_lines.append(f"\tWait({command[1]});")
            else:
                raise ValueError(f"Unsupported command \"{cmd_type}\". Please use one of these: \"fwd\", \"rot\", \"wait\".")
                
        nxc_code_lines.append(self.LAST_CODE_LINE)
        
        nxc_code = "\n".join(nxc_code_lines)
        
        self.__save_to_file(filename, nxc_code)
    
    def __visualize_next_command(self, command):
        if self.turtle:
            cmd_type = command[0]
            if cmd_type == 'fwd':
                self.turtle.forward(command[1] * (command[2]/1000))
            elif cmd_type == 'rot':
                self.turtle.right(command[2] * (command[1]/100))
            elif cmd_type == 'wait':
                pass # Do nothing
            else:
                raise ValueError(f"Unsupported command \"{cmd_type}\". Please use one of these: \"fwd\", \"rot\", \"wait\".")
        
    def __save_to_file(self, filename, code):
        with open(filename, 'w') as f:
            f.write(code)
        print("Done saving to file!")