+++
title = "Alex Tardif: Area Lights"
draft = false
+++

link
: <http://www.alextardif.com/arealights.html>

tags
: [graphics programming]({{< relref "20201215183931-graphics_programming" >}}), [area lights]({{< relref "20201215224331-area_lights" >}}), [lighting]({{< relref "20201215224339-lighting" >}})

All lighting computations are done in view-space (not world-space!)
This implementation is based on a deferred renderer,it renders geometry in the shape of the lights and uses a stencil pass to compute lighting only on pixels affected by lights.


## Sphere Area Lights {#sphere-area-lights}

```glsl
float3 r = reflect(-viewDir, normal);
float3 L = input.lightPositionView.xyz - positionView;
float3 centerToRay = (dot(L, r) * r) - L;
float3 closestPoint = L + centerToRay * saturate(sphereRadius / length(centerToRay));
L = normalize(closestPoint);
float distLight = length(closestPoint);
...
float alphaPrime = saturate(sphereRadius/(distL*2.0)+alpha);
...
float falloff = pow(saturate(1.0 - pow(distLight/(lightRadius), 4)), 2) / ((distLight * distLight) + 1.0);
float3 light = (specularFactor + diffuseFactor) * falloff * lightColor * luminosity;
```


## Tube Area Lights {#tube-area-lights}

```glsl
float3 L0 = input.lightPositionView.xyz - positionView;
float3 L1 = input.lightPositionView2.xyz - positionView;

float distL0 = length( L0 );
float distL1 = length( L1 );
float NoL0 = dot( L0, normal ) / ( 2.0 * distL0 );
float NoL1 = dot( L1, normal ) / ( 2.0 * distL1 );
float NoL = ( 2.0 * saturate( NoL0 + NoL1 )) / ( distL0 * distL1 + dot( L0, L1 ) + 2.0 );
float3 Ldist = L1 - L0;
float RoLd = dot( r, Ldist);
float distLd = length(Ldist);
float t = ( dot( r, L0 ) * RoLd - dot( L0, Ldist) ) / ( distLd * distLd - RoLd * RoLd );

float3 closestPoint = L0 + Ldist * saturate(t);
float3 centerToRay = dot(closestPoint, r) * r - closestPoint;
closestPoint = closestPoint + centerToRay * saturate(tubeRadius / length(centerToRay));
float3 L = normalize(closestPoint);
float distLight = length(closestPoint);
```


## Rectangular Area Lights {#rectangular-area-lights}

```glsl
float3 v0 = input.lightPositionView.xyz - positionView;
float3 v1 = input.lightPositionView2.xyz - positionView;
float3 v2 = input.lightPositionView3.xyz - positionView;
float3 v3 = input.lightPositionView4.xyz - positionView;

float facingCheck = dot( v0, cross( ( input.lightPositionView3.xyz - input.lightPositionView.xyz ).xyz, ( input.lightPositionView2.xyz - input.lightPositionView.xyz ).xyz ) );

if (facingCheck > 0.0)
{
    return float4(0.0, 0.0, 0.0, 1.0);
}
...
float3 n0 = normalize ( cross (v0 , v1 ));
float3 n1 = normalize ( cross (v1 , v2 ));
float3 n2 = normalize ( cross (v2 , v3 ));
float3 n3 = normalize ( cross (v3 , v0 ));
float g0 = acos ( dot (-n0 , n1 ));
float g1 = acos ( dot (-n1 , n2 ));
float g2 = acos ( dot (-n2 , n3 ));
float g3 = acos ( dot (-n3 , n0 ));

float solidAngle = g0 + g1 + g2 + g3 - 2.0 * 3.14159265359;

float NoL = solidAngle * 0.2 * (
    saturate ( dot( normalize ( v0 ), normal ) ) +
    saturate ( dot( normalize ( v1 ) , normal ) )+
    saturate ( dot( normalize ( v2 ) , normal ) )+
    saturate ( dot( normalize ( v3 ) , normal ) )+
    saturate ( dot( normalize ( input.lightPositionViewCenter.xyz - positionView ) , normal )));
...
float3 intersectPoint = CalculatePlaneIntersection(positionView, r, lightDir, input.lightPositionViewCenter.xyz);
...
float3 CalculatePlaneIntersection(float3 viewPosition, float3 reflectionVector, float3 lightDirection, float3 rectangleLightCenter)
{
    return viewPosition + reflectionVector * (dot(lightDirection,rectangleLightCenter-viewPosition)/dot(lightDirection,reflectionVector));
}
...
float3 intersectionVector = intersectPoint - input.lightPositionViewCenter.xyz;
float2 intersectPlanePoint = float2(dot(intersectionVector,right), dot(intersectionVector,up));
float2 nearest2DPoint = float2(clamp(intersectPlanePoint.x, -lightSizeX, lightSizeX), clamp(intersectPlanePoint.y, -lightSizeY, lightSizeY));
...
float3 specularFactor = float3(0,0,0);
float specularAmount = dot(r,lightDir);
if (specularAmount > 0.0)
{
    float specFactor = 1.0 - clamp(length(nearest2DPoint - intersectPlanePoint) * pow((1.0 - roughness), 2) * 32.0, 0.0, 1.0);
    specularFactor += surfaceSpec * specFactor * specularAmount * NoL;
}
...
float3 nearestPoint = input.lightPositionViewCenter.xyz + (right * nearest2DPoint.x + up * nearest2DPoint.y);
float dist = distance(positionView, nearestPoint);
float falloff = 1.0 - saturate(dist/lightRadius);
...
float3 light = (specularFactor + diffuseFactor) * falloff * lightColor * luminosity;
```
