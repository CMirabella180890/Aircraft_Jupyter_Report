# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 18:37:28 2021

@author: claum
"""
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
class csvla: 
    """
    CS - VLA Amdt1 -  05 Mar 2009
    
      CS - VLA 1 Applicability
      This airworthiness code is applicable to aeroplanes with a single
      engine, spark or compression-ignition, having not more than two
      seats, with a Max Certificated Takeoff Weight of not more than 750 kg
      and a stalling speed in the landing configuration of not more than 83
      km/h (45 KCAS) to be approved for day-VFR only. 
      
      CS - VLA 3 Aeroplane categories
      This CS - VLA applies to aeroplanes intended for non - aerobatic
      operation only. Non - aerobatic operation includes 
      (a) Any manoeuvre incident to normal flying;
      (b) Stalls, excepts whip stalls; and 
      (c) Lazy eights, chandelles, and steep turns, in which the angle of
          bank is not more than 60 degrees. 
      CS - VLA 301 Loads 
      (a) Strength requrements are specified in terms of limit loads,
          the maximum loads to be expected in service, and ultimate
          loads, limit loads multiplied by prescribed factors of
          safety. Unless otherwise provided, prescribed loads are
          limit loads. 
      (b) Unless otherwise provided, the air, groun, and water loads
          must be placed in equilibrium with inertia forces,
          considering each item of mass in the aeroplane. These loads
          must be distributed to conservatively approximate or closely
          represent actual conditions. 
      (c) If deflections under load would significantly change the
          distribution of external or internal loads, this
          redistribution must be taken into account.
      (d) Simplified structural design criteria given in this Subpart
          C and its appendices may be used only for aeroplanes with
          conventional configurations. If Appendix A is used, the
          entire appendix must be substituted for the corresponding
          paragraphs of this subpart, i.e. CS - VLA 321 to 459, see
          also CS - VLA 301 (d).  
    """
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # LOAD FACTOR CALCULATOR
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def calcn(nmax):
        """
            n = calcn(cls, nmax)
             Function that calculates load factors values along the
             stall curve for flight envelope calculation.
            
             CS - VLA 337 Limit manoeuvring load factors
               (a) The positive limit manoeuvring load factor n may not be
                   less than 3.8. 
               (b) The negative limit manoeuvring load factor may not be
                   less than -1.5.
              
              INPUT
              nmax = Appliable limit load factor
              OUTPUT 
              n    = Vector of load factor values
        """
        if nmax > 0.0:
            n = np.linspace(1.0, nmax, 250) 
        elif nmax < 0.0: 
            n = np.linspace(-1.0, nmax, 250)
        return n
    # calcn = staticmethod(calcn)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # STALL SPEED CALCULATOR
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def calcvs(rho, WS, CLmax, n):
        """
            VS = calcvs(rho, WS, CLmax, n)
            Stall speed values correspondent to limit load factors from 1g 
            to limit g's. 

            CS - VLA 335 Design Airspeeds (1)(i)
            VS is a computed stalling speed with flaps retracted at the de-
            sign weight, normally based on the maximum aeroplane normal 
            force coefficients, CNA. 
            CS - VLA 335 Design Airspeeds (1)(ii)
            n is the limit manoeuvring load factor used in design. 

            INPUT 
            rho   = Density at the selected altitude [kg/m**3]
            WS    = Wing loading in [Pa]
            CLmax = Applicable maximum lift coefficient [Non dim.]
            n     = Vector of limit load factor values [g's].
            OUTPUT 
            VS    = Vector of stall speed values. 
        """
        VS = np.sqrt(WS*(2/rho)*(1/CLmax)*n)
        return VS
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # STALL SPEED CALCULATOR
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def calcvd(vcmin, vc):
        """
            VD = calcvd(vcmin, vc)
            Design dive speed CS - VLA (b)(1)(2) VD 
            Vd must not be less than (1.25)*Vc; and, with Vc min, the 
            required minimum design cruising speed, Vd may not be less
            than (1.40)*Vc_min. 

            INPUT 
            vcimn = The required minimum design cruising speed, VD may 
                    not be less than (1.40)*Vc_min 
            vc    = Design cruise speed, which may not be less than 
                    (4.7)*sqrt(W/S)
                    where 
                    W/S = Wing loading in [Pa]
                    Vc  = Cruise speed in [m/s]
            OUTPUT 
            VD    = Design dive speed
        """
        vd1 = 1.4*vcmin 
        vd2 = 1.25*vc

        if vd1 > vd2: 
            VD = vd1
        elif vd2 > vd1: 
            VD = vd2

        return VD
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # STALL SPEED CALCULATOR
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def calcvc(WS, VH):
        """
            VC = calcvc(WS, VH)
            Design cruise speed CS - VLA (b)(1)(2) VC 
            Vc (in [m/s]) may not be less than (2.4)*sqrt(W/S), where 
            W/S = Wing loading in [Pa] 
            Vc  = Cruise speed in [m/s]

            Vc need not to be more than (0.9)*Vh at sea level, where 
            Vh  = Max continous power max horizontal speed in [m/s]

            INPUT 
            WS = Wing loading in [Pa] 
            vh = Max continous power max horizontal speed in [m/s]

            OUTPUT
            VD = Design dive speed 
        """
        VD = (2.4)*np.sqrt(WS)
        x  = (0.9)*VH 

        if VD > x:
            VD = x
        else:
            VD = VD

        return VD
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # V - n DIAGRAM 
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def V_n_diagram(npos, nneg, nmax, nmin, VSpos, VSneg, VD, VG, stat, Reg, Aircraft_name):
        """
            V_n_diagram(npos, nneg, nmax, nmin, VSpos, VSneg, VD, VG, Reg, Aircraft_name)

            This function plot the V - n diagram, based on the applied regulation. 
            The applied regulation is stored inside the local variabel 'Reg' for 
            convenience and it is used to automatically change the output figure 
            title name. Also, the selected aircraft name is stored inside the var-
            iable 'Aircraft_name' and is inserted in the diagram as plain text. 
            This might be an useful feature. 

            INPUT 
            npos          = An array of positive load factor values 
            nneg          = An array of negative load factor values 
            nmax          = Positive maximum load factor 
            nmin          = Negative minimum load factor 
            VSpos         = An array of positive stall speeds
            VSneg         = An array of negative stall speeds 
            VD            = Aircraft dive speed (positive side) 
            VG            = Aircraft dive speed (negative side) 
            stat          = A variable to save and store figure in .pdf
            Reg           = Applied regulation from Aircraft object 
            Aircraft_name = Aircraft name from Aircraft object

            OUTPUT
            fig1          = V - n diagram per regulation applied 

            The V - n diagram is based on CS - VLA 333 Flight Envelope, pag. 39/190

            Further information could be found at: EASA Airworthiness rules 
            url: https://www.easa.europa.eu/sites/default/files/dfu/Easy Access Rules CS-VLA (Amendment 1).pdf
        """
        # ===================================================================
        # ===================================================================
        rc('font',**{'family':'serif','serif':['Palatino']})
        rc('text', usetex=True)
        # ===================================================================
        fig  = plt.figure()
        plt.plot(VSpos, npos, color="red", linewidth=0.5, linestyle = "dashed")
        plt.plot(VSneg, nneg, color="red", linewidth=0.5, linestyle = "dashed")
        tol = 1E-2
        for i in range(len(npos)): 
            if abs(nmax - npos(i)) < tol:
                temp1 = i; 
                
        for i in range(len(npos)):
            if abs(1 - npos(i)) < tol:
                temp2 = i
        
        plt.plot(VSpos[temp2:temp1], npos[temp2:temp1], color="red", linewidth=1.0, linestyle = "solid")
        
        for i in range(len(nneg)):
            if abs(nmin - nneg(i)) < tol:
                temp3 = i
                
        for i in range(len(nneg)):
            if abs(-1.0 - nneg(i)) < tol:
                temp4 = i
                
        plt.plot(VSpos[temp4:temp3], npos[temp4:temp3], color="red", linewidth=1.0, linestyle = "solid")
        plt.plot(np.array([VSpos[temp1], VD]), np.array([nmax, nmax]), color="blue", linewidth=1.0, linestyle = "solid")
        plt.plot(np.array([VSneg[temp3], VG]), np.array([nmin, nmin]), color="blue", linewidth=1.0, linestyle = "solid")
        plt.plot(np.array([VD, VG]), np.array([nmax, nmin]), color="blue", linewidth=1.0, linestyle = "solid")
        plt.plot(np.array([VSpos[temp2], VSpos[temp2]]), np.array([npos[temp2], 0.0]), color="blue", linewidth=1.0, linestyle = "solid")
        plt.plot(np.array([VSneg[temp4], VSneg[temp4]]), np.array([0.0, nneg[temp4]]), color="blue", linewidth=1.0, linestyle = "solid")
        
        plt.xlabel(r'\textsc{Airspeed} ~ $V$ ~ $[m/s]$')   # x-label to the axes.
        plt.ylabel(r'\textsc{Load Factor} ~ $n$ ~ $[g]$')       # y-label to the axes.
        plt.ylim(nmin - 0.5, nmax + 0.5)
        plt.ylim(0.0, VD + 10.0)
        plt.legend(loc="best")
        plt.title(r'V - n diagram per ' + Reg + ' - ' + Aircraft_name) 
        plt.grid(True, linestyle='-.', which="both")
        plt.minorticks_on()
        plt.show()
        stat.savefig(fig)
        stat.close()
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # V - n DIAGRAM 
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def calcmug(WS, MAC, a, rho, g):
        """
        Aeroplane mass ratio = mug = calcmug(WS, MAC, a, rho, g)
        Function that calculates the aeroplane mass ratio mug. See page 41 
        of EASA CS - VLA Easy Access. In particular, 
        
        CS - VLA 341 Gust load factors
        In the abscence of a more rational analysis, the gust load factors
        may be computed as follows: 
            
                      0.5*rho0*V*a*Kg*Ude
            n = 1.0 + -------------------
                             (W/S)
            where 
            Kg = ()/()        

        Parameters
        ----------
        WS : TYPE
            DESCRIPTION.
        MAC : TYPE
            DESCRIPTION.
        a : TYPE
            DESCRIPTION.
        rho : TYPE
            DESCRIPTION.
        g : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """