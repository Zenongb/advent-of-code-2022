import verified_solution
import solution


good_one = verified_solution.main()

mine = solution.main()

# los que estan bien
well_done = [i for i in mine if i in good_one]
print('indices that are correctly selected by my sol', well_done)

# los que estan mal
bad_one = [i for i in mine if i not in good_one]
print('the indices that are extra in my sol', bad_one)

# los que no selecciono mi program
not_selected = [i for i in good_one if i not in mine]
print('the indices that are not selected by my sol', not_selected)

