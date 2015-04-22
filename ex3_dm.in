MAXIMIZE
profit_1 + profit_2 + profit_3 + profit_4

SUBJECT TO

// Number of actives with the ex-trainees
actives_1 + trainees_1 - actives_2 = 0
actives_2 + trainees_2 - actives_3 = 0
actives_3 + trainees_3 - actives_4 = 0
// The builders and teachers are actives.
builders_1 + teachers_1 - actives_1 <= 0
builders_2 + teachers_2 - actives_2 <= 0
builders_3 + teachers_3 - actives_3 <= 0
builders_4 + teachers_4 - actives_4 <= 0
// At most three trainees per teacher.
3 teachers_1 - trainees_1 >= 0
3 teachers_2 - trainees_2 >= 0
3 teachers_3 - trainees_3 >= 0
3 teachers_4 - trainees_4 >= 0
// Salaries of the actives and traineers.
200 actives_1 + 100trainees_1 - salaries_1 = 0
200 actives_2 + 100trainees_2 - salaries_2 = 0
200 actives_3 + 100trainees_3 - salaries_3 = 0
200 actives_4 + 100trainees_4 - salaries_4 = 0
// We must produce all the phones within the four weeks.
50 builders_1 + 50 builders_2 + 50 builders_3 + 50 builders_4 = 20000
// The profit is the sell price minus the salaries and the production costs.
750 builders_1 - salaries_1 - profit_1 = 0
650 builders_2 - salaries_2 - profit_2 = 0
550 builders_3 - salaries_3 - profit_3 = 0
450 builders_4 - salaries_4 - profit_4 = 0

BOUNDS

actives_1 = 40
actives_2 >= 0
actives_3 >= 0
actives_4 >= 0
trainees_1 >= 0
trainees_2 >= 0
trainees_3 >= 0
trainees_4 >= 0
builders_1 >= 0
builders_2 >= 0
builders_3 >= 0
builders_4 >= 0
teachers_1 >= 0
teachers_2 >= 0
teachers_3 >= 0
teachers_4 >= 0
salaries_1 >= 0
salaries_2 >= 0
salaries_3 >= 0
salaries_4 >= 0


VARIABLES
actives_1
actives_2
actives_3
actives_4
trainees_1
trainees_2
trainees_3
trainees_4
builders_1
builders_2
builders_3
builders_4
teachers_1
teachers_2
teachers_3
teachers_4
salaries_1
salaries_2
salaries_3
salaries_4
profit_1
profit_2
profit_3
profit_4
