#Solitaire: Seahaven

import cards, random
random.seed(100) #random number generator will always generate 
                 #the same random number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tableau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from end of Cell s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''

def initialize():
    ''' Creates and initializes the tableau, foundation and cells, and then returns them as a tuple''' 
    foundation = [ [] , [] , [] , [] ] 
    tableau = [ [] , [] , [] , [] , [] , [] , [] , [] , [] , [] ] 
    cells = [ None , None , None , None ]  
    
    stock = cards.Deck()
    stock.shuffle() 
 
    for card in range(5): #takes it from 5 per
        for each_list in tableau: 
            each_list.append(stock.deal()) #apppends 5 cards

    cells[1] = stock.deal() #puts in last two to cells
    cells[2] = stock.deal() 
            
    
    return tableau, foundation, cells

def display(tableau, foundation, cells):
    '''Display the cell and foundation at the top.
       Display the tableau below.'''
       
    print("\n{:<11s}{:^16s}{:>10s}".format( "foundation","cell", "foundation"))
    print("{:>14s}{:>4s}{:>4s}{:>4s}".format( "1","2","3","4"))
    for i,f in enumerate(foundation):
        if f and (i == 0 or i == 1):
            print(f[-1],end=' ')  # print first card in stack(list) on foundation
        elif i == 0 or i == 1:
            print("{:4s}".format( " "),end='') # fill space where card would be so foundation gets printed in the right place
    print("{:3s}".format(' '),end='')
    for c in cells:
        if c:
            print(c,end=' ')  # print first card in stack(list) on foundation
        else:
            print("[  ]",end='') # fill space where card would be so foundation gets printed in the right place
    print("{:3s}".format(' '),end='')
    for i,f in enumerate(foundation):
        if f and (i == 2 or i == 3):
            print(f[-1],end=' ')  # print first card in stack(list) on foundation
        elif i == 2 or i == 3:
            print("{}{}".format( " ", " "),end='') # fill space where card would be so foundation gets printed in the right place
        
    print()
    print("\ntableau")
    print("   ",end=' ')
    for i in range(1,11):
        print("{:>2d} ".format(i),end=' ')
    print()
    # determine the number of rows in the longest column        
    max_col = max([len(i) for i in tableau])
    for row in range(max_col):
        print("{:>2d}".format(row+1),end=' ')
        for col in range(10):
            # check that a card exists before trying to print it
            if row < len(tableau[col]):
                print(tableau[col][row],end=' ')
            else:
                print("   ",end=' ')
        print()  # carriage return at the end of each row
    print()  # carriage return after printing the whole tableau
    
        
def validate_move_within_tableau(tableau,src_col,dst_col):
 
    ''' checks if a requested move within tableau is valid '''
   
    if tableau[src_col] == []:  #Make sure the source col is not empty
        return False
    
    else:  #We can get a source card
        source_card = tableau[src_col][-1]  
        
        if tableau[dst_col] == []: #checks if destination is empty
            
            if source_card.rank() == 13: #then only king can move
                return True 
            else:
                return False
        else:
            destination_card = tableau[dst_col][-1] 
            if source_card.suit() == destination_card.suit() and destination_card.rank() - source_card.rank() == 1:
                 return True 
            else:
                return False
        
    


def validate_move_cell_to_tableau(tableau,cells,cell_no,dst_col):
    
    ''' checks if a requested move from cell to tableau is valid '''
    
    if cell_no > 3: #cell number cannot be greater than 3
        return False
    else:
        if cells[cell_no] == None: #checks for empty cell 
            return False  #cannot move any card from an empty cell
        else: 
            cells_source_card = cells[cell_no]  #get card if not empty 
            if tableau[dst_col] == []:  #checks if destination is empty
                
                if cells_source_card.rank() == 13: #only king can move if empty
                    return True 
                else:
                    return False
            else:
                destination_card = tableau[dst_col][-1] #else get the source card and check rank and suit
                
                if cells_source_card.suit() == destination_card.suit() and destination_card.rank() - cells_source_card.rank() == 1:
                     return True 
                else:
                    return False
            
            
            
    

def validate_move_tableau_to_cell(tableau,cells,src_col,cell_no):
    
    ''' checks if a requested move from tableau to cell is valid '''   
    
    if tableau[src_col] == []: 
        return False 
    else:
        
        if cells[cell_no] == None:
            return True 
        else:
            return False

def validate_move_tableau_to_foundation(tableau,foundation,src_col,found_no):

    ''' checks if a requested move from tableau to foundation is valid '''       

    if tableau[src_col] == []: 
        return False 
    else:
        source_card = tableau[src_col][-1]   
        
        if foundation[found_no] == [] :
            if source_card.rank() == 1: #only ace moves if foundation is empty 
                return True 
            else:
                return False 
        else:
            destination_card = foundation[found_no][-1] 
            
            if source_card.suit() == destination_card.suit() and source_card.rank() - destination_card.rank() == 1:
                return True 
            else:
                return False
            
                
    

def validate_move_cell_to_foundation(cells,foundation,cell_no,found_no):
    
    ''' checks if a requested move from cell to foundation is valid '''       
    
    
    if cell_no > 3: #cell number cannot be greater than 3
        return False
    else:
    
        
        if cells[cell_no] == None: 
            return False 
        else:
            source_card = cells[cell_no]
            
            if foundation[found_no] == []:
                
                if source_card.rank() == 1:
                    return True 
                else:
                    return False 
            else:
                foundation_card = foundation[found_no][-1] 
                
                if source_card.suit() == foundation_card.suit() and source_card.rank() - foundation_card.rank() == 1:
                    return True 
                else:
                    return False
            
    
    
def move_within_tableau(tableau,src_col,dst_col):
    
    '''moves card within tableau '''
    
    if validate_move_within_tableau(tableau,src_col,dst_col) == True: 
        source_card = tableau[src_col].pop() #takes the last card as source card
        tableau[dst_col].append(source_card) #appends last card to destination
        return True 
    else:
        return False
   
def move_tableau_to_cell(tableau,cells,src_col,cell_no):

    '''moves card from tableau to cell'''    

    if validate_move_tableau_to_cell (tableau,cells,src_col,cell_no) == True:
        
        source_card = tableau[src_col].pop() 
        cells[cell_no] = source_card
        return True
    else:
        return False
        
def move_cell_to_tableau(tableau,cells,cell_no,dst_col):

    '''moves card from cell to tableau '''    

    if validate_move_cell_to_tableau(tableau,cells,cell_no,dst_col) == True: 
        
    
        source_card = cells[cell_no] #gets card and replace it with None
        cells[cell_no] = None
        
        tableau[dst_col].append(source_card) #appends card
        
        return True
    
    else:
        return False
        

def move_cell_to_foundation(cells,foundation,cell_no,found_no):
    
    '''moves card from tableau to cell'''    
   
    if validate_move_cell_to_foundation(cells,foundation,cell_no,found_no) == True: 
        source_card = cells[cell_no]  
        cells[cell_no] = None
        
        foundation[found_no].append(source_card) 
        return True 
    else:
        return False
        
        
            
def move_tableau_to_foundation(tableau,foundation,src_col,found_no):
    
    '''moves card from tableau to cell'''    
   
    if validate_move_tableau_to_foundation(tableau,foundation,src_col,found_no) == True:    
        source_card = tableau[src_col].pop() 
        foundation[found_no].append(source_card) 
        return True
    else:
        return False
        

def check_for_win(foundation):

    '''checks if game is won'''    

    for each_pile in foundation: #loops through every foundation pile
        if len(each_pile) == 13 : 
            continue #if all 13 cards, continue to next pile
        else:
            return False #false if any of pile != 13
    return True #true if all are 13

def get_option():
    '''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tableau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from Cells s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''
    option = input( "\nInput an option (MTT,MTC,MCT,MTF,MCF,R,H,Q): " )
    option_list = option.strip().split()
    
    opt_char = option_list[0][0].upper()
    
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'M' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0]
        if opt_str in ['MTT','MTC','MCT','MTF','MCF']:
            return [opt_str,int(option_list[1]),int(option_list[2])]

    print("Error in option:", option)
    return None   # none of the above
 
def main():
    print("\nWelcome to Seahaven Solitaire.\n")
    tableau, foundation, cells = initialize()
    display(tableau, foundation, cells)
    print(MENU)
    
    ##########  your code goes here #############
    
    while True:
        options = get_option()
      
    
        
        if options[0] == "MTT":
            src_col =  options[1] - 1 
            dst_col = options[2] - 1
           
            
            if move_within_tableau(tableau, src_col, dst_col) == True:
                display(tableau, foundation, cells)
              
                
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    continue
                else:
                    continue
            
            elif move_within_tableau(tableau, src_col, dst_col) == False:
                print("Error in move: ", options[0], options[1], options[2])
                print(MENU)
                continue
            
        elif options[0] == "MTC":
            src_col =  options[1] - 1
            cell_no = options[2] - 1
            
            
            if move_tableau_to_cell(tableau, cells, src_col, cell_no) == True:
                display(tableau, foundation, cells)

                
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    continue
                else:
                    continue
            
            elif move_tableau_to_cell(tableau, cells, src_col, cell_no) == False:
                print("Error in move: ", options[0], options[1], options[2])
                print(MENU)
                continue
            
        elif options[0] == "MCT":
            cell_no =  options[1] - 1
            dst_col= options[2] - 1
            
            
            if move_cell_to_tableau(tableau, cells, cell_no, dst_col) == True:
                display(tableau, foundation, cells)
            
                
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    continue
                else:
                    continue
            
            elif move_cell_to_tableau(tableau, cells, cell_no, dst_col) == False:
                print("Error in move: ", options[0], options[1], options[2])
                #print(MENU)
                continue
            
        elif options[0] == "MCF":
            cell_no =  options[1] - 1
            found_no = options[2] - 1
            
            if move_cell_to_foundation(cells, foundation, cell_no, found_no) == True:
                display(tableau, foundation, cells)
                
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    continue
                else:
                    continue
            
            elif move_cell_to_foundation(cells, foundation, cell_no, found_no) == False:
                print("Error in move: ", options[0], options[1], options[2])
                print(MENU)
                continue
            
        elif options[0] == "MTF":
            src_col =  options[1] - 1
            found_no = options[2] - 1
            
            
            if move_tableau_to_foundation(tableau, foundation, src_col, found_no) == True:
                display(tableau, foundation, cells)
                
                
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    continue
                else:
                    continue
            
            elif move_tableau_to_foundation(tableau, foundation, src_col, found_no) == False:
                print("Error in move: ", options[0], options[1], options[2])
                print(MENU)
                continue
            
        elif options[0] == "Q":
            break

        elif options[0] == "H":
            print(MENU)
            continue
        
        else: 
            options[0] == "R"
            tableau, foundation, cells = initialize()
            tableau.shuffle()
            display(tableau, foundation, cells)
            continue
            
                    
            
            
    print("Thank you for playing.")

