# FreeCADEquidistant
A macro for calculating an equidistant out of an existing wire e.g. a svg-image.
BSplines are readable.
The result is build out of 1D-lines and a bsplie.
Various constructionlines are displayed.
You could delete them if you want to.

Change 1:

    Create a Point by hand in the Center of the Spline.( The Spline should be near the Center too)

    Select the Point first, then the base-spline.

    Start the Script

    The Script calculates the wire-equidistant, and then samples points on it around the selected point. At least it creates a b-spline based on the sampled points.
    
![Bildschirmfoto vom 2024-03-05 15-01-04](https://github.com/CalzitPLA/FreeCADEquidistant/assets/118506426/aa43f875-97f3-4633-a647-ffea73e29aa2)
