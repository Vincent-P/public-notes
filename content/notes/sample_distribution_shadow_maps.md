+++
title = "Sample Distribution Shadow Maps"
draft = false
+++

link
: <http://advances.realtimerendering.com/s2010/Lauritzen-SDSM(SIGGRAPH%202010%20Advanced%20RealTime%20Rendering%20Course).pdf>

tags
: [graphics programming]({{< relref "20201215183931-graphics_programming" >}}), [shadow mapping]({{< relref "20201215183947-shadow_mapping" >}})


## Algorithm {#algorithm}

Basically PSSM but instead of partitioning the entire frustum, tight bounds are used.

Two partitioning variants:

-   K-means clustering: place partitions where there are a lot of samples, good results for average error
-   Adaptive logarithmic: avoids gaps in Z

But these two approaches require a depth histogram and are very situational.
A simpler min/max reduction with a basic logarithmic scheme is recommended.


## Advantages {#advantages}

-   Sometimes faster than traditional PSSM because less geometry gets rendered.
-   Sub-pixel shadow resolution with sufficient partition resolution (~ screen res.)


## Possible improvements {#possible-improvements}

-   better partitioning scheme
-   smarter/more expensive algorithms to address projective aliasing