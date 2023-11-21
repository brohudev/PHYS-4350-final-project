# 7.6 cluster growth models
- growth of clusters such as soot or snowflakes (I should make a snowflake growth model o.O)
- the Eden model of building clusters:
    - also known as the cancer model (lmao wut) because the model grows from the "inside out" like a culture multiplying.
    1. create a lattice of points that will serve as the set of legal locations for points in our cluster
    2. place aseed at the origin (middle of the lattice basically)
    3. clusters grow by adding particles to the perimiter of the existing cluster. 
    4. the initial cluster will have four nearest neighbor points on the lattice ~ the perimeter sites of the cluster.
    5. you randomly choose a perimeter location and "add" a particle at that location. now the cluster is bigger, the perimiter size has updated.
    6. rinse and repeat until the cluster size is big enough. (adding at the perimeter means you WILL get blanks in the middle sometimes)
- DLA (Diffusion Limited Aggression) model of building cluster models. 
    - models how snowflakes and soot particle clusters grow, wherein particles originate from outsidethe cluster. 
    1. start with a seed at the origin. 
    2. randomly release another particle some distance away from the seed and let it perform a random walk. it "sticks" with the seed where it does, thereby increasing the cluster size.
    3. rinse and repeat, until your desired cluster size is reached. 
- a quantitative difference between the two types of growth models can be found by analyzing fractals. 
    - you can say that if m(r) is the mass of a circle in 2 dimensions, then we find that m(r) ~ r^d_f i.e the power of its radius is the fractal dimensionality. 2 gives a circle, 1 gives a line. what does a non integer value give?
    - to calculate the mass of the cluster to find its d_f:
        1. define the seed particle as the center and give all particles some mass m
        simply count the amount of particles within a radius r and your mass is simply calculated as r*m.
        2. instead of directly plotting the mass vs radius to find d_f, plot the log of both sides because then youd be plotting logm ~ d_flogr, which is easy to calulate from linear regression.
        practically, a particular cluster can only be used to estimate m(r) for distances up to about r_max/2
        