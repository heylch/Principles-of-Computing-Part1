"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0,None,0.0,0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        states_string = ''
        states_string += "Time: " + str(self._current_time) + " "
        states_string += "Current Cookies: " + str(self._current_cookies) + " "
        states_string += "CPS: " + str(self._current_cps) + " "
        states_string += "Total Cookies: " + str(self._total_cookies) + " "
        states_string += "History: (length: " + str(len(self._history)) + "): " + str(self._history)
        return states_string

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        copy_history = self._history
        return copy_history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time = 0.0
        if self._current_cookies < cookies:
            time = math.ceil((cookies-self._current_cookies)/self._current_cps)
        return time

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time >0:
            self._current_time += time
            self._current_cookies += time*self._current_cps
            self._total_cookies += time*self._current_cps


    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cps += additional_cps
            self._current_cookies -= cost
            self._history.append((self._current_time, item_name, cost, self._total_cookies))



def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    copy_build = build_info.clone()
    states = ClickerState()
    while states.get_time() <= duration:
        item = strategy(states.get_cookies(),states.get_cps(),states.get_history(),duration- states.get_time(),copy_build)
        if item == None:
            states.wait(duration-states.get_time())
            break
        elif item == 'Cursor':
            if states.get_cps() * (duration - states.get_time()) + states.get_cookies() < copy_build.get_cost(item):
                states.wait(duration-states.get_time())
                break

        wait_time = states.time_until(copy_build.get_cost(item))
        states.wait(wait_time)
        states.buy_item(item,copy_build.get_cost(item),copy_build.get_cps(item))
        copy_build.update_item(item)

    return states


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    all_item = build_info.build_items()
    cost_list = []
    for item in all_item:
        cost_list.append(build_info.get_cost(item))
    cheapest_cost = min(cost_list)
    idx = cost_list.index(cheapest_cost)
    if cheapest_cost <= cookies+time_left*cps:
        return all_item[idx]
    else:
        return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    all_item = build_info.build_items()
    cost_list = []
    for item in all_item:
        cost_list.append(build_info.get_cost(item))
    afford_list = [dummy_i for dummy_i in cost_list if dummy_i <= cookies+time_left*cps]
    if len(afford_list) >0:
        max_cost = max(afford_list)
        idx = afford_list.index(max_cost)
        return all_item[idx]
    else:
        return None


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    all_item = build_info.build_items()
    afford_cost = []
    afford_item = []
    cps_list = []
    for item in all_item:
        if build_info.get_cost(item) <=cookies+time_left*cps:
            afford_cost.append(build_info.get_cost(item))
            afford_item.append(item)
            cps_list.append(build_info.get_cps(item))
    if len(afford_item) >0:
        cost_cps = [afford_cost[dummy_i]/(float(cps_list[dummy_i])) for dummy_i in range(len(afford_cost))]
        min_ratio = min(cost_cps)
        idx = cost_cps.index(min_ratio)
        return afford_item[idx]
    else:
        return None

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

run()


