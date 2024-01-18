# Naive MLB projections
Projects next-season wRC+ using linear regression based on previous season wRC+, Barrel%, HardHit%, maxEV, O-Swing%, O-Contact%, CStr% and age. Model is trained on 2015-2023 data (minimum 300 PA in each season), excluding 2020. The model works well on players with >300 PA, and conversely does not work well on players with <300 PA.

Notable 2024 projections (minimum 300 PA last season):
- Highest wRC+: Ronald Acuna Jr. (162)
- Lowest wRC+: Paul DeJong (72)
- Highest wRC+ jump: Nick Fortes (53->97)
- Highest wRC+ jump, minimum 100 wRC+: Maikel Garcia (84->115)
- Highest wRC+ fall: Jose Altuve (154->111)
- Highest wRC+ fall, maximum 100 wRC+: Harold Ramirez (128->97)
