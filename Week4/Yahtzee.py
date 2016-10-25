# coding=utf-8
"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    This function takes as input a tuple hand that
    represents the die values in the given Yahtzee hand.
    Since ordering of the die values in Yahtzee hands is unimportant,
    tuples corresponding to Yahtzee hands will always be stored in sorted order
    to guarantee that each tuple corresponds to a unique Yahtzee hand.
    The function score(hand) computes a score for hand as the maximum of the possible values
    for each choice of box in the upper section of the Yahtzee scorecard.

    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    score_list = []
    num = []
    for dummy_i in hand:
        if dummy_i not in score_list:
            score_list.append(dummy_i)
            num.append(1)
        else:
            idx = score_list.index(dummy_i)
            num[idx] += 1
    multi_score = [score_list[dummy_i]*num[dummy_i] for dummy_i in range(len(score_list))]
    max_score = max(multi_score)
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    This function computes the expected value of the scores for the possible Yahtzee hands
    that result from holding some dice and rolling the remaining free dice.
    The dice being held are specified by the sorted tuple held_dice.
    The number of sides and the number of dice that are free to be rolled are specified by
    num_die_sides and num_free_dice, respectively.
    You should use gen_all_sequence to compute all possible rolls for the dice being rolled.
    As an example, in a standard Yahtzee game using five dice,
    the length of held_dice plus num_free_dice should always be five.

    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcome = [dummy_i +1 for dummy_i in range(num_die_sides)]
    all_set = gen_all_sequences(outcome, num_free_dice)
    sum_list = []
    for item in all_set:
        sum_list.append(score(item+held_dice))
    expect_value = float(sum(sum_list))/len(sum_list)

    return expect_value


def gen_all_holds(hand):

    """
    This function takes a sorted tuple hand and returns the set of all possible sorted tuples
    formed by discarding a subset of the entries in hand.
    The entries in each of these tuples correspond to the dice that will be held.
    If the tuple hand has the entries (h0,h1,...,hm−1), the returned tuples should have the form (hi0,hi1,...,hik−1)
    where 0≤k≤m and the integer indices satisfy 0≤i0<i1<...<ik−1<m.
    In the case where values in the tuple hand happen to be distinct,
    the set of tuples returned by gen_all_holds will correspond to all possible subsets of hand.

    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    from_hand = [()]
    for item in hand:
        for subset in from_hand:
            from_hand = from_hand + [tuple(subset) + (item, )]

    return set(from_hand)



def strategy(hand, num_die_sides):
    """
    This function takes a sorted tuple hand and computes
    which dice to hold to maximize the expected value of the score of the possible hands
    that result from rolling the remaining free dice (with the specified number of sides).
    The function should return a tuple consisting of this maximal expected value
    and the choice of dice (specified as a sorted tuple) that should be held to achieve this value.
    If there are several holds that generate the maximal expected value, you may return any of these holds.

    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_expect_value = 0
    best_holds = tuple()
    for item in all_holds:
        expect_value = expected_value(item, num_die_sides, len(hand)-len(item))
        if expect_value >= max_expect_value:
            max_expect_value = expect_value
            best_holds = item
    return (max_expect_value, best_holds)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)







