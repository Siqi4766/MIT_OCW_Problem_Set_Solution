# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    permutation_list = []
    if len(sequence) == 1:
        permutation_list.append(sequence)
        return permutation_list
    else: 
        hold_character = sequence[0]
        permutation_sublist = get_permutations(sequence[1:])
        for i in permutation_sublist:
            for index in range(len(i)+1):
                permutation_list.append(i[:index]+hold_character+i[index:])
        return permutation_list
           
            
    

if __name__ == '__main__':
    #print(get_permutations('a'))
    #print(get_permutations('ab'))
    print(get_permutations('abc'))
    #print(get_permutations('abcd'))
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)


