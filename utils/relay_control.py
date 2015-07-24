#!/usr/bin/env python
#
# Configure, and toggle SainSmart relays on the RaspberryPi
#
#

from common import relay
import cmd2
import re

#########################################
# Define your relay -> mcp i2c GPIO expender chip pin mapping
relay_pin_map = {'r00': 0,
                 'r01': 1,
                 'r02': 2,
                 'r03': 3,
                 'r04': 4,
                 'r05': 5,
                 'r06': 6,
                 'r07': 7,
                 'r08': 8,
                 'r09': 9,
                 'r10': 10,
                 'r11': 11,
                 'r12': 12,
                 'r13': 13,
                 'r14': 14,
                 'r15': 15}

i2c_address = 0x27

relays = {}

########################################
# Don't change anything below this point
ON = False
OFF = True
relay_re = re.compile('r\d+')


class RelayControl(cmd2.Cmd):

    def __init__(self):
        cmd2.Cmd.__init__(self)
        for relay_name in sorted(relay_pin_map.iterkeys()):
            relays[relay_name] = relay.Relay(mcp_pin=relay_pin_map[relay_name])
        self.prompt = "RC>> "
        self.intro = "RaspberryPi Relay Control Shell"
        self._hist = None
        self._locals = None
        self._globals = None

    # Command definitions #
    def do_hist(self):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_quit(self, args):
        """Exits from the console"""
        return -1

    # Command definitions to support Cmd object functionality #
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        # The only reason to define this method is for the help text in the doc string
        cmd2.Cmd.do_help(self, args)

    # Override methods in Cmd object #
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd2.Cmd.preloop(self)  # sets up command completion
        self._hist = []        # No history yet
        self._locals = {}      # Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd2.Cmd.postloop(self)   # Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [line.strip()]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def do_setall(self, args):
        """Set all relays to a state (on|off, True|False, 0|1)"""
        l = args.split()
        if len(l) != 1:
            print("Incorrect number of arguments. Command expects a state (on|off, True|False, 0|1)")
            return
        state = l[0]
        if re.match("^(true|on)$", state, re.IGNORECASE) or state == '1':
            for r in relays:
                my_relay = relays[r]
                my_relay.set_state(my_relay.ON)
        elif re.match("^(off|false)$", state, re.IGNORECASE) or state == '0':
            for r in relays:
                my_relay = relays[r]
                my_relay.set_state(my_relay.OFF)

    def do_setstate(self, args):
        """Set the state of a relay. Takes a relay and a state (on|off, True|False, 0|1)."""
        l = args.split()
        if len(l) != 2:
            print("Incorrect number of arguments. Command expects a relay (r1, r2, etc.) and a state (on|off, True|False, 0|1)")
            return
        my_relay_name = l[0]
        if not re.match(relay_re, my_relay_name):
            print("Command expects a relays (r1, r2, etc.)")
            return
        my_relay = relays[my_relay_name]
        state = l[1]
        if re.match("^(true|on)$", state, re.IGNORECASE) or state == '1':
            try:
                my_relay.set_state(my_relay.ON)
            except KeyError:
                print("Relay: %s does not exist" % my_relay_name)
        elif re.match("^off|false$", state, re.IGNORECASE) or state == '0':
            try:
                my_relay.set_state(my_relay.OFF)
            except KeyError:
                print("Relay: %s does not exist" % my_relay_name)

    def do_getstate(self, args):
        """Get the state of a relay."""
        l = args.split()
        if len(l) != 1:
            print("Wrong number of arguments. Command expects a relays (r1, r2, etc.)")
            return
        my_relay_name = l[0]
        if my_relay_name not in relays.iterkeys():
            print("Command expects a relay (r1, r2, etc.)")
            return
        else:
            my_relay = relays[my_relay_name]
            try:
                state = my_relay.get_state()
                if state == my_relay.ON:
                    print("ON")
                else:
                    print("OFF")
            except KeyError:
                print("Relay: %s does not exist" % my_relay_name)

    def do_toggle(self, args):
        """Toggle a relay. Takes a relay. Sets relay to opposite of it's current state"""
        l = args.split()
        if len(l) != 1:
            print("Incorrect number of arguments. Command expects a relay (r1, r2, etc.)")
            return
        my_relay_name = l[0]
        if not re.match(relay_re, my_relay_name):
            print("Command expects a relays (r1, r2, etc.)")
            return
        if not re.match(relay_re, my_relay_name):
            print("Command expects a relays (r1, r2, etc.)")
            return
        else:
            my_relay = relays[my_relay_name]
            my_relay.toggle()

    def do_list(self, args):
        """List all relays."""
        for key in sorted(relays.iterkeys()):
            print(key)

    def do_showall(self, args):
        """Show the states of all relays"""
        for relay_name in sorted(relays.iterkeys()):
            s = ""
            s += relay_name
            my_relay = relays[relay_name]
            state = my_relay.get_state()
            if state == my_relay.ON:
                s += " ON"
            else:
                s += " OFF"
            print s


if __name__ == '__main__':
    rc = RelayControl()
    rc.cmdloop()
