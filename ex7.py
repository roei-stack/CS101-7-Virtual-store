import sys


def menu_and_choice():

    """
    # function Name: menu_and_choice
    # Input: none, it asks the user for input
    # Output: the choice of the user/error
    # Function Operation: prints a menu to the user and asks for corresponding input
    # If the user entered 0-4 -> return its input
    # Otherwise -> return 'error'
    """

    # All 4 possible valid choices
    leave = '0'
    by_category = '1'
    by_item = '2'
    buy = '3'
    admin_panel = '4'

    # The menu
    print('Please select an operation:')
    print('\t0. Exit.')
    print('\t1. Query by category.')
    print('\t2. Query by item.')
    print('\t3. Purchase an item.')
    print('\t4. Admin panel.')

    # Reading the input, and removing leading spaces
    choice = input().lstrip()
    # If the choice matches any of the possible options above, return it ('0'-'4'), otherwise, return 'error'
    if choice is leave or choice is by_category or choice is by_item or choice is buy or choice is admin_panel:
        return choice
    return 'error'


def check_input_and_return_arguments_for1(s, categories, cache_1, cache_1_ans):

    """
    # function Name: check_input_and_return_arguments_for1
    # Input: the user's input for task 1, the dict() database and the cache
    # Output: the arguments (category1, category2, operator)
    # 'error', 'error', 'error' -> error
    # 'Cached', 'Cached', 'Cached' -> if we got a cache hit
    # Function Operation: making sure the input has 2 ',' (format is "cat1, cat2, operator")
    # then checking if we got a cache hit and if we did print the cache answer and return 'cached'
    # make sure both categories exist and the operator is valid and one of the following ('&', '|', '|')
    """

    # I cant believe how short this one is
    op_and = '&'
    op_or = '|'
    op_xor = '^'
    delimiter = ','
    denim_appliance = 2

    # The format is ("category1, category2, operation") -> therefore the delimiter ',' should appear twice (2!!)
    if s.count(delimiter) < denim_appliance:
        # i changed the condition from 'is not' to '<' in order to match my output to the correct output
        print('Error: not enough data.')
        return 'error', 'error', 'error'

    # Getting the categories and the operator, we only unpack twice because there should be 2 ','
    cat1, cat2, operation = s.split(delimiter, denim_appliance)
    # Removing leading white spaces
    cat1 = cat1.lstrip()
    cat2 = cat2.lstrip()
    operation = operation.lstrip()

    # If we got a cache hit -> print the cache answer and return 'cached'
    if cache_1 == [cat1, cat2, operation] or cache_1 == [cat2, cat1, operation]:
        if len(cache_1_ans) == 0:
            cache_1_ans = []
        print('Cached:', cache_1_ans)
        return 'Cached', 'Cached', 'Cached'

    # Making sure the categories exist in the store
    if cat1 not in categories or cat2 not in categories:
        print('Error: one of the categories does not exist.')
        return 'error', 'error', 'error'

    # validating the operator -> the ope
    if operation is not op_and and operation is not op_or and operation is not op_xor:
        print('Error: unsupported query operation.')
        return 'error', 'error', 'error'
    # Returning the arguments
    return cat1, cat2, operation


def query_by_category(categories, cache_1, cache_1_ans):

    """
    # function Name: query_by_category
    # Input: the categories database (dict) and the caches for task 1
    # Output: does a query of 2 categories with an operation, and return the state of the cache
    # Function Operation: if the cache contains the same query->return the cache answer
    otherwise -> do the operation
    RETURNS THE NEW STATE OF THE CACHE
    """

    s = input()
    op_and = '&'
    op_or = '|'
    op_xor = '^'
    # calling that function that checks input (if the input is caches, it'll return 'cached' and print the answer)
    category1, category2, operator = check_input_and_return_arguments_for1(s, categories, cache_1, cache_1_ans)
    generated_list = []

    # if the input is invalid/cached ->return the same cache (the actual output done in the check_input_1 function)
    if operator is 'error' or operator is 'Cached':
        return cache_1, cache_1_ans

    # checking which operator was entered
    if operator is op_and:
        generated_list = categories[category1].keys() & categories[category2].keys()
    elif operator is op_or:
        generated_list = categories[category1].keys() | categories[category2].keys()
    elif operator is op_xor:
        generated_list = categories[category1].keys() ^ categories[category2].keys()

    # if the set is empty the terminal prints "set()" so i changes it
    if len(generated_list) is 0:
        print([])
    else:
        # Sorting the list, then printing it
        generated_list = sorted(generated_list)
        print(generated_list)
    # Returning the new cache
    return [category1, category2, operator], generated_list


def query_by_item(categories, cache_2, cache_2_ans):

    """
    # function Name: query_by_item
    # Input: the categories dictionary database, and the state of all caches
    # Output: asks for a product and prints every product that shares a category with it
    # Function Operation: read the name, iterate through the categories in the database, if the product is in that
    # category -> add the list of products to the _commons_ list, and remove the product inputted
    # If you didn't find an item with item -> error massage
    # RETURNS THE INPUT AND THE CORRESPONDING OUTPUT AS CACHE
    """

    # Will indicate if the product exists
    found = False
    # removing leading spaces
    product_name = input().lstrip()

    # if the cache contains the save input, print the cache's output
    if cache_2 == product_name:
        print('Cached:', cache_2_ans)
        return cache_2, cache_2_ans

    common_categories_list = []

    # iterate through the categories, if you find that product->add the products from that list (W.O.the input product)
    for category in categories.keys():

        if product_name in categories[category].keys():
            # We found the product which means it exists
            found = True
            common_categories_list += categories[category].keys()
            common_categories_list.remove(product_name)

    # did not found a product with that name -> error massage
    if found is False:
        print('Error: no such item exists.')
        return cache_2, cache_2_ans
    # Sorting the list, then printing it
    common_categories_list.sort()
    print(common_categories_list)
    # returning a changed cache
    return product_name, common_categories_list


def buy_item(categories, cache_1, cache_1_ans, cache_2, cache_2_ans):

    """
    # function Name: buy_item
    # Input: the categories database and the cache state
    # Output: lets the user buy a product, then deletes it
    # if the input was valid, the user bought an item and it was deleted -> we made changes -> return an empty cache
    # bad input -> no changes made -> return the same cache
    # Function Operation: get the name from the user, iterate through the categories, and whenever you find a product
    # with that name -> remove it
    # At the end the user will get a massage he bought the product
    """

    price = None
    found = False
    # Removing leading spaces from the user's input
    name = input().lstrip()

    # For each category -> if the product is in that category, save it's price and remove it from there
    for category in categories.keys():
        if name in categories[category].keys():
            # Changing the found state to true -> we made changes
            found = True
            # saving the price
            price = categories[category][name]
            # deleting the product
            categories[category].pop(name, None)

    # If we didn't find a product with that name -> error massage
    if found is False:
        print('Error: no such item exists.')
        # error -> return the save cache
        return cache_1, cache_1_ans, cache_2, cache_2_ans

    print('You bought a brand new "', name, '" for ', price, '$.', sep='')
    # Emptying the cache because we made a change to the database
    return list(), list(), str, list()


def set_product(categories):

    """
    # function Name: set_product
    # Input: the store's database
    # Output: adds/updates a product with a price on an existing categories
    # RETURN TRUE -> IF WE MADE CHANGES TO THE DATA AND CACHE SHOULD BE DELETED
    # RETURN FALSE -> IF NO CHANGES WERE MADE
    # PLEASE NOTE -> A PRICE UPDATE TO AN EXISTING PRODUCT WILL NOT BE CONSIDERED A CHANGE
    # BECAUSE IT WONT CHANGE THE ANSWERS OF THE CACHE THAT FOCUS ON THE PRODUCT NAME AND NOT IT'S PRICE
    # Function Operation: Split the categories from the product (':'), for each product name in the list,
    # assign the product to that list
    """

    # Indicates if any changes were made
    changed = False
    delimiter = ','
    categories_product_delimiter = ':'

    # Getting input
    x = input()

    # FORMAT == category_1, category_2,.....,category_N: product_name, product_price -> must have a ':'
    if x.count(categories_product_delimiter) is not 1:
        print('Error: not enough data.')
        # no changes were made
        return False

    categories_list, product = x.split(categories_product_delimiter)
    categories_list = categories_list.lstrip()
    product = product.lstrip()

    if product.count(delimiter) is 0:
        print('Error: not enough data.')
        # no changes were made
        return False

    categories_list = [category.lstrip() for category in categories_list.split(delimiter)]
    if set(categories_list).issubset(set(categories.keys())) is False:
        print('Error: one of the categories does not exist.')
        # no changes were made
        return False

    p_name, p_price = product.split(delimiter)
    p_price = p_price.lstrip()
    if p_price.isdigit() is False:
        print('Error: price is not a positive integer.')
        # no changes were made
        return False

    p_price = int(p_price)

    # For each category -> if the product exists, change its price, otherwise -> create it
    for category in categories.keys():
        if p_name in categories[category].keys():
            categories[category][p_name] = p_price
        categories[category][p_name] = p_price
        # If the user inputs a new product for that category, we make changes to the database
        changed = True
    print('Item "' + p_name + '" added.')
    return changed


def write_list(products_list, out_file):

    """
    # function Name: write_list
    # Input: a products list dictionary and a file to write to
    # Output: writes the list of products to the file by lexicographic value
    # Function Operation: create a sorted list of the product's names, then print them 1 by one
    """

    sorted_products = sorted(products_list.keys())

    for product_name in sorted_products:
        # Saving the name
        p_name = product_name
        # accessing the corresponding price of that product by its name
        p_price = products_list[product_name]
        # Creating the line according to to printing requirements -> " name, price;"
        line = ' ' + p_name + ', ' + str(p_price) + ';'
        # Writing the line containing the product name and the price
        out_file.write(line)

    # After writing the whole line, we need to go down 1 line for the next category
    out_file.write('\n')


def save(categories):

    """
        # function Name: save
        # Input: the categories database
        # Output: overwrites an existing file the database, by lexicographic values
        # Function Operation: sort the category names, then sort the products assigned to that name and write them too
    """

    out_file_index = 3
    # Sorting the category names ans saving it to a list
    sorted_categories = sorted(categories.keys())
    file_name = sys.argv[out_file_index]
    # Gaining access to the out file
    out_file = open(sys.argv[out_file_index], 'w')

    """
    # FOR EACH CATEGORY:
    # 1. Write the category to the file
    # 2. Write the products in that category using the "write_list" function
    """
    for category in sorted_categories:
        c_name = category
        out_file.write(c_name + ':')
        write_list(categories[category], out_file)

    print('Store saved to "' + file_name + '".')


def admin(categories, cache_1, cache_1_ans, cache_2, cache_2_ans):

    """
    # function Name: admin
    # Input: the categories and the cache
    # Output: allows the admin to make changes to the database and to create a file of the database
    # If any changes were made, we return an empty cache, if no changes were made, we return the save cache
    # Function Operation: we ask for the password and compare it with the one provided at "admin.txt"
    # If the password is correct the user will be prompted to a menu that allows him to do one of the following:
    0->go back to main menu
    1->set a product
    2->save the database to a file
    """

    # This will indicate on weather we made any changes to the data and if we did, return an empty cache
    changed_database = False
    # Asking for password
    user_password = input('Password: ')
    # Accessing the correct password, and comparing it to the input password
    admin_pass_file_index = 2
    correct_password = open(sys.argv[admin_pass_file_index], 'r').read()

    if user_password != correct_password:
        print('Error: incorrect password, returning to main menu.')
        return cache_1, cache_1_ans, cache_2, cache_2_ans

    while True:
        # Printing the admin options after each operation
        print('Admin panel:')
        print('\t0. Return to main menu.')
        print('\t1. Insert or update an item.')
        print('\t2. Save.')
        choice = input()
        if choice is '0':
            break
        elif choice is '1':
            # This operation may change the database, and if it does it will return 'True'
            changed_database = set_product(categories)
        elif choice is '2':
            save(categories)
        else:
            print('Error: unrecognized operation.')

    # If we made any changes, return an empty cache, otherwise -> return the save cache
    if changed_database is True:
        return list(), list(), str, list()
    return cache_1, cache_1_ans, cache_2, cache_2_ans


def direct(categories, cache_1, cache_1_ans, cache_2, cache_2_ans):

    """
    # function Name: direct
    # Input: the database dictionary, and all of the cache for tasks 1 and 2
    # Output: gets us to the wanted operation, by calling the right function and saving the cache returned by it
    # Function Operation: gets the user input, if the input is 0-4 -> call an operation assigned to that number
    # Otherwise, print an error massage
    """

    # This function prints the interactive menu, gets the user's choice and returns it, bad choice -> error
    choice = menu_and_choice()
    if choice is 'error':
        print('Error: unrecognized operation.')
    elif choice is '0':
        # Exit
        return
    elif choice is '1':
        # Query by category
        cache_1, cache_1_ans = query_by_category(categories, cache_1, cache_1_ans)
    elif choice is '2':
        # Query by item
        cache_2, cache_2_ans = query_by_item(categories, cache_2, cache_2_ans)
    elif choice is '3':
        # Buy an item, if we made any changes to the database the cache will be deleted
        cache_1, cache_1_ans, cache_2, cache_2_ans = buy_item(categories, cache_1, cache_1_ans, cache_2, cache_2_ans)
    else:
        # Choice 4 -> Go to admin panel, if we made any changes to the database the cache will be deleted
        cache_1, cache_1_ans, cache_2, cache_2_ans = admin(categories, cache_1, cache_1_ans, cache_2, cache_2_ans)

    # Recalling the function with the cache returned by the last operation
    direct(categories, cache_1, cache_1_ans, cache_2, cache_2_ans)


def main():

    """
    # function Name: main
    # Input: none, besides the files that were added (sys.argv[])
    # Output: none, it calls the "direct" function
    # Function Operation: the program takes the input from the txt file and stores the data in
    # a dictionary data type where each key is the category name and each value is a dictionary that
    # stores the products name's as keys and their prices as values
    # Then -> close the files, initialize an empty cache and sent the database with the empty cache to "direct"
    """

    # Sys.argv[0] -> name of program, sys.argv[1] -> the input txt file
    input_file_index = 1
    # Initializing the database
    categories = dict()
    products = dict()
    # Defining delimiters
    name_products_delimiter = ':'
    products_pairs_delimiter = ';'
    product_price_delimiter = ','
    # Gaining access to the input file
    file = open(sys.argv[input_file_index], 'r')

    """
    # FOR EACH LINE IN THE INPUT FILE:
    # 1. REMOVE LEADING SPACES
    # 2. Split the category name from the product's list by the ':' delimiter
    # 3. Create a list of products (PRODUCT,PRICE) and remove the '\n' at the end
    # 4. FOR EVERY ITEM IN THAT LIST:
    #   4.1. Split the name from the price
    #   4.2. Assign the product key to its price
    #5. Assign the category name to it's products list
    #6. Closing file, creating cache, and sending the database with the cache to the "direct" function
    """
    for line in file:
        # Removing leading spaces
        line = line.lstrip()

        # If the current line is empty, move on to the next line
        if len(line) is 0:
            continue

        cat_name, list_of_products = line.split(name_products_delimiter)
        list_of_products = list_of_products.split(products_pairs_delimiter)
        list_of_products.pop()

        for product in list_of_products:
            p_name, price = product.split(product_price_delimiter)
            p_name = p_name.lstrip()
            price = int(price)
            products[p_name] = price
            # We need to clear the product's list every line but without losing data, so we store a copy of the data

        categories[cat_name] = products.copy()
        # And we delete the original
        products.clear()

    # Closing the file
    file.close()
    # Creating cache
    cache_1 = list()
    cache_1_ans = list()
    cache_2 = str
    cache_2_ans = list()
    direct(categories, cache_1, cache_1_ans, cache_2, cache_2_ans)


if __name__ == '__main__':
    main()
