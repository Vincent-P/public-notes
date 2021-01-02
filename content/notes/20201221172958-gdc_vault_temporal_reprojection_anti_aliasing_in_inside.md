+++
title = "GDC Vault - Temporal Reprojection Anti-Aliasing in INSIDE"
draft = false
+++

link
: <https://www.gdcvault.com/play/1022970/Temporal-Reprojection-Anti-Aliasing-in>

tags
: [graphics programming]({{< relref "20201215183931-graphics_programming" >}}),[ temporal integration]({{< relref "20201221173148-temporal_integration" >}})

Playdead's INSIDE makes strong use of Temporal Reprojection Anti-Aliasing to deliver satisfactorily clean and stable images.

Temporal Reprojection Anti-Aliasing is a spatio-temporal post-process technique, where fragments from the most recent frame are correlated with fragments from a history buffer through reprojection. By carefully jittering the view frustum, and by making sensible choices for when to accept or reject a history sample, this technique can produce images that are superior to the input in terms of information density, because the information in every fragment accumulates over time.

This talk will focus on Temporal Reprojection Anti-Aliasing in the context of INSIDE. It will touch on the process, the initial research, and the pleasant side-effects. Most importantly, it will discuss in-depth the individual stages of the implementation written for INSIDE, and how it deals with common problems such as disocclusion and trailing artefacts.
