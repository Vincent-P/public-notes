+++
title = "Advances in Real-Time Rendering- SIGGRAPH 2016"
draft = false
+++

link
: <http://advances.realtimerendering.com/s2016/index.html>

tags
: [graphics programming]({{< relref "20201215183931-graphics_programming" >}}), [temporal integration]({{< relref "20201221173148-temporal_integration" >}})


## Temporal Antialiasing in Uncharted 4 {#temporal-antialiasing-in-uncharted-4}

<span class="underline">Abstract:</span> As GPUs become more powerful, many aspects of video game graphics are approaching pre-rendered CG quality. However there are still some areas that instantly give away its real time nature. Image cleanness is one of them. Anti-aliasing techniques have been used for more than a decade to create cleaner images in games, and have become fairly effective at solving certain types of aliasing such as stepping edges. Unfortunately, the recent adoption of physically based rendering among game developers made one type of unsolved aliasing even worse, namely shader aliasing. Several methods have been developed recently to solve this problem and among them, temporal anti-aliasing has shown nearly perfect results in tech demos and even been shipped in a few games, albeit with different degrees of success. Uncharted 4 is one of the first games to fully embrace temporal AA, and in this talk we will present its basic algorithms, implementation details, the problems encountered when used in a full scale AAA game with vastly different varieties of environment and their solutions, as well as some of its additional benefits to other graphical features.

Materials: <http://advances.realtimerendering.com/s2016/s16%5FKe.pptx>