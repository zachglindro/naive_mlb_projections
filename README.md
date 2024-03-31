# Naive MLB projections
Projects next-season wRC+, BB%, and K% using only previous season's stats. Linear regression models are trained on 2015-2023 data (minimum 300 PA in each season), excluding 2020. They work well on players with >300 PA, and conversely do not work well on players with <300 PA. Each set of projections are independent from each other (i.e., projected wRC+ doesn't use projected BB%/K%).

wRC+ projections currently use previous season wRC+, age, maxEV, LA, HardHit%, O-Swing%, O-Contact%, and CStr%. <br />
BB% projections use previous season BB%, O-Swing%, Barrel%, and ISO. <br />
K% projections use previous season K%, Z-Swing%, O-Contact%, and Z-Contact%. <br />

All X variables exhibit p-values less than 0.01.