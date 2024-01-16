# Naive MLB projections
Projects next-season wRC+ using linear regression based on previous season wRC+, Barrel%, K%, BB%, and age. Model is trained on 2015-2023 data (minimum 300 PA in each season), excluding 2020. The model works well on players with >300 PA, and conversely does not work well on players with <300 PA.

Notable 2024 projections:
- Highest wRC+: Aaron Judge (161)
- Lowest wRC+: Joey Wendle (73)
- Highest wRC+ jump, minimum 100 wRC+: Luis Garcia (84->106)
- Highest wRC+ jump, minimum 110 wRC+: Trent Grisham (91->110)
- Highest wRC+ fall: Freddie Freeman, Yandy Diaz (163->128)
- Highest wRC+ fall, maximum 100 wRC+: Donovan Solano (116->98)
