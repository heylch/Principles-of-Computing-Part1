"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    result = []
    for item in range(0,len(line)):
        if line[item] !=0:
            result.append(line[item])
    print result
    jerry =0
    while jerry<len(result)-1:
        if result[jerry] == result[jerry+1]:
            result[jerry] = 2*result[jerry]
            result[jerry+1] = 0
            jerry +=2
        else:
            jerry+=1
    final_result = []
    for item in range(0,len(result)):
        if result[item] != 0:
            final_result.append(result[item])
    for item in range(0,len(line)-len(final_result)):
        final_result.append(0)
    return final_result

# if __name__ == '__main__':
#     line = list(map(int,raw_input().split()))
#     result = merge(line)
#     print result

