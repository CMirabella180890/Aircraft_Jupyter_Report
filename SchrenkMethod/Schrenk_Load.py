import numpy as np
import math

def Schrenk_Load(b, S, c_root, c_tip, n):
    # FUNCTION DESCRIPTION: 
    # [y(m) eta(...) chord_distr.(m)  elliptical_load cCl(m) Schrenk_load cCl(m) unit_load cCl(m)] = Schrenk_Load(b, S, c_root, c_tip, n)
    # ---------------------------------------------------------------------------------------------------------------
    # Wing loading distribution along wingspan can be calculated with the Schrenk method.
    # The Schrenk method relies on the fact that the distribution across the span of an 
    # unswept wing does not differ much from elliptic load distribution, even for a highly 
    # non-elliptic planform. 
    # OUTPUT 
    # y               = Station across the semi-span of the wing;
    # eta             = Non-dimensional station across the semi-span of the wing; 
    # chord           = Chord distribution across the semi-span of the wing; 
    # elliptical_load = Chord-times-lift coefficient [c(y)*Cl(y)] elliptical load 
    #                   distribution 
    # Schrenk_load    = Schrenk load across the semi-span, defined as:
    #                           (chord + elliptical load)*0.5
    # Unit_load       = Unit load distribution across the semi-span: 
    #                           (Schrenk_load)/(chord)
    #
    # TEST CASE: 
    # S      = 66.5 ft**2
    # b      = 19.0 ft 
    # c_tip  = 2.0 ft
    # c_root = 5.0 ft
    
   y   = np.linspace(0, b/2, n).reshape(-1,1)
   y   = np.flip(y)
   # Ellipse 
   eta = y/(b/2)
   # Chord distr. for tapered wing 
   taper_ratio  = c_tip/c_root
   c_y          = ((2*S)/((1 + taper_ratio)*b))*(1 - (1 - taper_ratio)*abs(eta))
   ell_height   = ((4*S)/(math.pi*b))
   x              = np.sqrt(1 - (eta**2))
   Ellipse     = ell_height*x
   Schrenk_cCl = (c_y + Ellipse)*0.5
   Unit_cCl    = (Schrenk_cCl)/(c_y)

   out1 = [y, eta, c_y, Ellipse, Schrenk_cCl, Unit_cCl]

   return out1