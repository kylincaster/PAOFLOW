def _getHighSymPoints(ibrav,alat,cellOld):
    '''
    Searching for the ibrav number in the input file for the calculation
    to determine the path for the band structure calculation
    Returns:
          special_points (list): list of the HSP names
          band_path (str): path in string form
    '''
    a,b,c,alpha,beta,gamma =  free2abc(cellOld,cosine=False,bohr=False,string=False)
###############################################################################
###############################################################################
    if   ibrav==1:  ibrav_var =  'CUB'
    elif ibrav==2:  ibrav_var =  'FCC'
    elif ibrav==3:  ibrav_var =  'BCC'
    elif ibrav==4:  ibrav_var =  'HEX'
    elif ibrav==6:  ibrav_var =  'TET'
    elif ibrav==8:  ibrav_var =  'ORC'
    elif ibrav==9:  ibrav_var =  'ORCC'
    elif ibrav==11: ibrav_var =  'ORCI'
    elif ibrav==5:
        if alpha < numpy.pi/2.0:   ibrav_var =  'RHL1'
        elif alpha > numpy.pi/2.0: ibrav_var =  'RHL2'
    elif ibrav==7:
        if(c < a):   ibrav_var =  'BCT1'
        elif(c > a): ibrav_var =  'BCT2'
        else:        ibrav_var =  'BCC'
    elif ibrav==10:
        if (1.0/a**2 >1.0/b**2+1.0/c**2):  ibrav_var =  'ORCF1'
        elif (1.0/a**2<1.0/b**2+1.0/c**2): ibrav_var =  'ORCF2'
        else:                              ibrav_var =  'ORCF2'
    elif(int(ibrav)==14):
        minAngle = numpy.amin([alpha,beta,gamma])
        maxAngle = numpy.amax([alpha,beta,gamma])
        if alpha==90.0 or beta==90.0 or gamma==90.0:
            if alpha>=90.0 or beta>=90.0 or gamma>=90.0: ibrav_var =  'TRI2A'
            if alpha<=90.0 or beta<=90.0 or gamma<=90.0: ibrav_var =  'TRI2B'
        elif minAngle>90.0:                              ibrav_var =  'TRI1A'
        elif maxAngle<90:                                ibrav_var =  'TRI1B'
###############################################################################
###############################################################################
    if ibrav_var=='CUB':
        band_path = 'gG-X-M-gG-R-X|M-R'
        special_points = {'gG'   : (0.0, 0.0, 0.0),
                           'M'   : (0.5, 0.5, 0.0),
                           'R'   : (0.5, 0.5, 0.5),
                           'X'   : (0.0, 0.5, 0.0)}
                           
    if ibrav_var=='FCC':
        band_path = 'gG-X-W-K-gG-L-U-W-L-K|U-X'
        special_points = {'gG'   : (0.0, 0.0, 0.0),
                          'K'    : (0.375, 0.375, 0.750),
                          'L'    : (0.5, 0.5, 0.5),
                          'U'    : (0.625, 0.250, 0.625),
                          'W'    : (0.5, 0.25, 0.75),
                          'X'    : (0.5, 0.0, 0.5)}
                          
    if ibrav_var=='BCC':
        band_path = 'gG-H-N-gG-P-H|P-N'
        special_points = {'gG'   : (0, 0, 0),
                          'H'    : (0.5, -0.5, 0.5),
                          'P'    : (0.25, 0.25, 0.25,), 
                          'N'    : (0.0, 0.0, 0.5)}
            
    if ibrav_var=='HEX':
        band_path = 'gG-M-K-gG-A-L-H-A|L-M|K-H'
        special_points = {'gG'   : (0, 0, 0),
                          'A'    : (0.0, 0.0, 0.5),
                          'H'    : (1.0/3.0, 1.0/3.0, 0.5),
                          'K'    : (1.0/3.0, 1.0/3.0, 0.0),
                          'L'    : (0.5, 0.0, 0.5),
                          'M'    : (0.5, 0.0, 0.0)}
        
    if ibrav_var=='RHL1':
        eta1 = 1.0 + 4.0*numpy.cos(alpha)
        eta2 = eta1+1.0
        eta=eta1/eta2
        nu =0.75-eta/2.0
        band_path = 'gG-L-B1|B-Z-gG-X|Q-F-P1-Z|L-P'
        special_points = {'gG'   : (0.0, 0.0, 0.0),
                          'B'    : (eta, 0.5, 1.0-eta),
                          'B1'   : (0.5, 1.0-eta, eta-1.0),
                          'F'    : (0.5, 0.5, 0.0),
                          'L'    : (0.5, 0.0, 0.0),
                          'L1'   : (0.0, 0.0, -0.5),
                          'P'    : (eta, nu, nu),
                          'P1'   : (1.0-nu, 1.0-nu, 1.0-eta),
                          'P2'   : (nu, nu, eta-1.0),
                          'Q'    : (1.0-nu, nu, 0.0),
                          'X'    : (nu, 0.0, -nu),
                          'Z'    : (0.5, 0.5, 0.5)}
         
    if ibrav_var=='RHL2':
        eta=1.0/(2*numpy.tan(alpha/2.0)**2)
        nu =0.75-eta/2.0
        band_path = 'gG-P-Z-Q-gG-F-P1-Q1-L-Z'
        special_points = {'gG'   : (0.0, 0.0, 0.0),
                          'F'    : (0.5, -0.5, 0.0),
                          'L'    : (0.5, 0.0, 0.0),
                          'P'    : (1.0-nu, -nu, 1.0-nu),
                          'P1'   : (nu, nu-1.0, nu-1.0),
                          'Q'    : (eta, eta, eta),
                          'Q1'   : (1.0-eta, -eta, -eta),
                          'Z'    : (0.5, -0.5, 0.5)} 

    if ibrav_var=='TET':
        band_path = 'gG-X-M-gG-Z-R-A-Z|X-R|M-A'
        special_points = {'gG'   : (0.0, 0.0, 0.0),
                          'A'    : (0.5, 0.5, 0.5),
                          'M'    : (0.5, 0.5, 0.0),
                          'R'    : (0.0, 0.5, 0.5),
                          'X'    : (0.0, 0.5, 0.0),
                          'Z'    : (0.0, 0.0, 0.5)}

    if ibrav_var=='BCT1':
       eta = (1+c**2/a**2)/4
       band_path = 'gG-X-M-gG-Z-P-N-Z1-M|X-P'
       special_points = {'gG'    : (0.0, 0.0, 0.0),
                         'M'     : (-0.5, 0.5, 0.5),
                         'N'     : (0.0, 0.5, 0.0),
                         'P'     : (0.25, 0.25, 0.25),
                         'X'     : (0.0, 0.0, 0.5),
                         'Z'     : (eta, eta, -eta),
                         'Z1'    : (-eta, 1.0-eta, eta)}
         
    if ibrav_var=='BCT2':
       band_path = 'gG-X-Y-gS-gG-Z-gS1-N-P-Y1-Z|X-P'
       eta = (1 + a**2/c**2)/4.0
       zeta = a**2/(2.0*c**2)
       special_points = {'gG'    : (0.0, 0.0, 0.0),
                         'N'     : (0.0, 0.5, 0.0),
                         'P'     : (0.25, 0.25, 0.25),
                         'gS'    : (-eta, eta, eta),
                         'gS1'   : (eta, 1-eta, -eta),
                         'X'     : (0.0, 0.0, 0.5),
                         'Y'     : (-zeta, zeta, 0.5),
                         'Y1'    : (0.5, 0.5, -zeta),
                         'Z'     : (0.5, 0.5, -0.5)}
         
    if ibrav_var=='ORC':
         band_path = 'gG-X-S-Y-gG-Z-U-R-T-Z|Y-T|U-X|S-R'
         special_points = {'gG'  : (0.0, 0.0, 0.0),
                           'R'   : (0.5, 0.5, 0.5),
                           'S'   : (0.5, 0.5, 0.0),
                           'T'   : (0.0, 0.5, 0.5),
                           'U'   : (0.5, 0.0, 0.5),
                           'X'   : (0.5, 0.0, 0.0),
                           'Y'   : (0.0, 0.5, 0.0),
                           'Z'   : (0.0, 0.0, 0.5)}

    if ibrav_var=='ORCF1':
       band_path = 'gG-Y-T-Z-gG-X-A1-Y|T-X1|X-A-Z|L-gG'
       eta = (1+a**2/b**2+a**2/c**2)/4
       zeta =(1+a**2/b**2-a**2/c**2)/4
       special_points = {'gG'    : (0.0, 0.0, 0.0),
                         'A'     : (0.5, 0.5 + zeta, zeta),
                         'A1'    : (0.5, 0.5-zeta, 1.0-zeta),
                         'L'     : (0.5, 0.5, 0.5),
                         'T'     : (1.0, 0.5, 0.5),
                         'X'     : (0.0, eta, eta),
                         'X1'    : (1.0, 1.0-eta, 1.0-eta),
                         'Y'     : (0.5, 0.0, 0.5),
                         'Z'     : (0.5, 0.5, 0.0)}

    if ibrav_var=='ORCF2':
       band_path = 'gG-Y-C-D-X-gG-Z-D1-H-C|C1-Z|X-H1|H-Y|L-gG'
       eta = (1+a**2/b**2-a**2/c**2)/4
       phi = (1+c**2/b**2-c**2/a**2)/4
       delta=(1+b**2/a**2-b**2/c**2)/4
       special_points = {'gG'    : (0.0, 0.0, 0.0),
                         'C'     : (0.5, 0.5-eta, 1.0-eta),
                         'C1'    : (0.5, 0.5+eta, eta),
                         'D'     : (0.5-delta, 0.5, 1.0-delta),
                         'D1'    : (0.5+delta, 0.5, delta),
                         'L'     : (0.5, 0.5, 0.5),
                         'H'     : (1.0-phi, 0.5-phi, 0.5),
                         'H1'    : (phi, 0.5+phi, 0.5),
                         'X'     : (0.0, 0.5, 0.5),
                         'Y'     : (0.5, 0.0, 0.5),
                         'Z'     : (0.5, 0.5, 0.0),}

    if ibrav_var=='ORCF3':
       band_path = 'gG-Y-T-Z-gG-X-A1-Y|X-A-Z|L-R'
       eta =(1+a**2/b**2+a**2/c**2)/4
       zeta=(1+a**2/b**2-a**2/c**2)/4
       special_points = {'gG'    : (0.0, 0.0, 0.0),
                         'A'     : (0.5, 0.5 + zeta, zeta),
                         'A1'    : (0.5, 0.5-zeta, 1.0-zeta),
                         'L'     : (0.5, 0.5, 0.5),
                         'T'     : (1.0, 0.5, 0.5),
                         'X'     : (0.0, eta, eta),
                         'X1'    : (1.0, 1.0-eta, 1.0-eta),
                         'Y'     : (0.5, 0.0, 0.5),
                         'Z'     : (0.5, 0.5, 0.0)}

    if ibrav_var=='ORCC':
       band_path = 'gG-X-S-R-A-Z-gG-Y-X1-A1-T-Y|Z-T'
       zeta=(1+a**2/b**2)/4.0
       special_points = {'gG'    : (0.0, 0.0, 0.0),
                         'A'     : (zeta, zeta, 0.5),
                         'A1'    : (-zeta, 1.0-zeta, 0.5),
                         'R'     : (0.0, 0.5, 0.5),
                         'S'     : (0.0, 0.5, 0.0),
                         'T'     : (-0.5, 0.5, 0.5),
                         'X'     : (zeta, zeta, 0.0),
                         'X1'    : (-zeta, 1.0-zeta, 0.0),
                         'Y'     : (-0.5, 0.5, 0.0),
                         'Z'     : (0.0, 0.0, 0.5)}
         
    if ibrav_var=='ORCI':
         band_path = 'gG-X-L-T-W-R-X1-Z-gG-Y-S-W|L1-Y|Y1-Z'
         chi = (1.0 + (a/c)**2)/4.0
         eta = (1.0 + (b/c)**2)/4.0
         delta = (b*b - a*a)/(4*c*c)
         mu = (b*b + a*a)/(4*c*c)
         special_points = {'gG'   : (0, 0, 0),
                           'L'    : (-mu, mu, 0.5-delta),
                           'L1'   : (mu, -mu, 0.5+delta),
                           'L2'   : (0.5-delta, 0.5+delta, -mu),
                           'R'    : (0.0, 0.5, 0.0),
                           'S'    : (0.5, 0.0, 0.0),
                           'T'    : (0.0, 0.0, 0.5),
                           'W'    : (0.25,0.25,0.25),
                           'X'    : (-chi, chi, chi),
                           'X1'   : (chi, 1.0-chi, -chi),
                           'Y'    : (eta, -eta, eta),
                           'Y1'   : (1.0-eta, eta, -eta),
                           'Z'    : (0.5, 0.5, -0.5)}
   
    if ibrav_var=='TRI1A':        
        band_path = 'X-gG-Y|L-gG-Z|N-gG-M|R-gG' 
        special_points = {'gG'    : (0.0,0.0,0.0),
                          'L'     : (0.5,0.5,0.0),
                          'M'     : (0.0,0.5,0.5),
                          'N'     : (0.5,0.0,0.5),
                          'R'     : (0.5,0.5,0.5),
                          'X'     : (0.5,0.0,0.0),
                          'Y'     : (0.0,0.5,0.0),
                          'Z'     : (0.0,0.0,0.5),}
        
    if ibrav_var=='TRI2A':        
        band_path = 'X-gG-Y|L-gG-Z|N-gG-M|R-gG'
        special_points = {'gG'    : (0.0,0.0,0.0),
                          'L'     : (0.5,0.5,0.0),
                          'M'     : (0.0,0.5,0.5),
                          'N'     : (0.5,0.0,0.5),
                          'R'     : (0.5,0.5,0.5),
                          'X'     : (0.5,0.0,0.0),
                          'Y'     : (0.0,0.5,0.0),
                          'Z'     : (0.0,0.0,0.5),}
 
    if ibrav_var=='TRI1B':        
        band_path = "X-gG-Y|L-gG-Z|N-gG-M|R-gG"
        special_points = {'gG'    : ( 0.0, 0.0,0.0),
                          'L'     : ( 0.5,-0.5,0.0),
                          'M'     : ( 0.0, 0.0,0.5),
                          'N'     : (-0.5,-0.5,0.5),
                          'R'     : ( 0.0,-0.5,0.5),
                          'X'     : ( 0.0,-0.5,0.0),
                          'Y'     : ( 0.5, 0.0,0.0),
                          'Z'     : (-0.5, 0.0,0.5),}

    if ibrav_var=='TRI2B':        
        band_path = 'X-gG-Y|L-gG-Z|N-gG-M|R-gG'
        special_points = {'gG'    : ( 0.0, 0.0,0.0),
                          'L'     : ( 0.5,-0.5,0.0),
                          'M'     : ( 0.0, 0.0,0.5),
                          'N'     : (-0.5,-0.5,0.5),
                          'R'     : ( 0.0,-0.5,0.5),
                          'X'     : ( 0.0,-0.5,0.0),
                          'Y'     : ( 0.5, 0.0,0.0),
                          'Z'     : (-0.5, 0.0,0.5),}
            
    # if ibrav_var=='MCLC':
    #    sin_gamma = numpy.sin(numpy.arccos(cos_gamma)) 
    #    mu        = (1+(b/a)**2.0)/4.0
    #    delta     = b*c*cos_gamma/(2.0*a**2.0)
    #    xi        = mu -0.25*+(1.0 - b*cos_gamma/c)*(4.0*(sin_gamma**2.0))
    #    eta       = 0.5 + 2.0*xi*c*cos_gamma/b
    #    phi       = 1.0 + xi - 2.0*mu
    #    psi       = eta - 2.0*delta

    # if ibrav_var=='MCLC2':        
    #     pass

    # if ibrav_var=='MCLC5':        
    #     pass

    
    # def MCL(cellOld):
    #    a1 = cellOld[0][0]
    #    b1 = (cellOld[1][0]**2 + cellOld[1][1]**2)**(0.5)
    #    c1 = cellOld[2][2]
    #    gamma = numpy.arctan(cellOld[1][1]/cellOld[1][0])
    #    myList = [a1, b1, c1]
    #    c = max(myList)
    #    a = min(myList)
    #    myList.remove(c)
    #    myList.remove(a)
    #    b = myList[0]
    #    alpha = gamma

    #    eta = (1 - b*numpy.cos(alpha)/c)/(2*numpy.sin(alpha)**2)
    #    nu = 0.5 - eta*c*numpy.cos(alpha)/b
    #    band_path = 'gG-Y-H-C-E-M1-A-X-H1|M-D-Z|Y-D'
    #    special_points = {
    #        'gG'    : (0.0, 0.0, 0.0),
    #        'A'    : (0.5, 0.5, 0.0),
    #        'C'    : (0.0, 0.5, 0.5),
    #        'D'    : (0.5, 0.0, 0.5),
    #        'D1'    : (0.5, 0.0, -0.5),
    #        'E'    : (0.5, 0.5, 0.5),
    #        'H'    : (0.0, eta, 1.0-nu),
    #        'H1'    : (0.0, 1.0-eta, nu),
    #        'H2'    : (0.0, eta, -nu),
    #        'M'    : (0.5, eta, 1.0-nu),
    #        'M1'    : (0.5, 1.0-eta, nu),
    #        'M2'    : (0.5, eta, -nu),
    #        'X'    : (0.0, 0.5, 0.0),
    #        'Y'    : (0.0, 0.0, 0.5),
    #        'Y1'    : (0.0, 0.0, -0.5),
    #        'Z'    : (0.5, 0.0, 0.0)
    #      }

       
    #    band_path = default_band_path
    #    return special_points, band_path
    
###############################################################################
###############################################################################           
    aflow_conv = numpy.identity(3)
    qe_conv    = numpy.identity(3)

    if ibrav==2:
        aflow_conv = numpy.asarray([[ 0.0, 1.0, 1.0],[ 1.0, 0.0, 1.0],[ 1.0, 1.0, 0.0]])/2.0     
        qe_conv    = numpy.asarray([[-1.0, 0.0, 1.0],[ 0.0, 1.0, 1.0],[-1.0, 1.0, 0.0]])/2.0
    if ibrav==3:
        aflow_conv = numpy.asarray([[-1.0, 1.0, 1.0],[ 1.0,-1.0, 1.0],[ 1.0, 1.0,-1.0]])/2.0     
        qe_conv    = numpy.asarray([[ 1.0, 1.0, 1.0],[-1.0, 1.0, 1.0],[-1.0,-1.0, 1.0]])/2.0     
    if ibrav==7:
        aflow_conv = numpy.asarray([[-1.0, 1.0, 1.0],[ 1.0,-1.0, 1.0],[ 1.0, 1.0,-1.0]])/2.0
        qe_conv    = numpy.asarray([[ 1.0,-1.0, 1.0],[ 1.0, 1.0, 1.0],[-1.0,-1.0, 1.0]])/2.0
    if ibrav==9:
        aflow_conv = numpy.asarray([[ 1.0,-1.0, 0.0],[ 1.0, 1.0, 0.0],[ 0.0, 0.0, 2.0]])/2.0
        qe_conv    = numpy.asarray([[ 1.0, 1.0, 0.0],[-1.0, 1.0, 0.0],[ 0.0, 0.0, 2.0]])/2.0
    if ibrav==10:
        aflow_conv = numpy.asarray([[ 0.0, 1.0, 1.0],[ 1.0, 0.0, 1.0],[ 1.0, 1.0, 0.0]])/2.0
        qe_conv    = numpy.asarray([[ 1.0, 0.0, 1.0],[ 1.0, 1.0, 0.0],[ 0.0, 1.0, 1.0]])/2.0  
    if ibrav==11:
        aflow_conv = numpy.asarray([[-1.0, 1.0, 1.0],[ 1.0,-1.0, 1.0],[ 1.0, 1.0,-1.0]])/2.0
        qe_conv    = numpy.asarray([[ 1.0, 1.0, 1.0],[-1.0, 1.0, 1.0],[-1.0,-1.0, 1.0]])/2.0

                                   

    for k,v in special_points.iteritems():
        first  = numpy.array(v).dot(numpy.linalg.inv(aflow_conv))
        second = qe_conv.dot(first)
        special_points[k]=tuple(second.tolist())
#    for k,v in special_points.iteritems():
#        second = (aflow_conv*numpy.linalg.inv(qe_conv))*numpy.matrix(v).T
#        special_points[k]=tuple(second.flatten().tolist()[0])


    return special_points, band_path 

def free2abc(cellparamatrix,cosine=True,degrees=True,string=True,bohr=False):
    '''
    Convert lattice vectors to a,b,c,alpha,beta,gamma of the primitive lattice
    Arguments:
          cellparamatrix (numpy.matrix): matrix of cell vectors
    Keyword Arguments:
          cosine (bool): If True alpha,beta,gamma are cos(alpha),cos(beta),cos(gamma),
          degrees (bool): If True return alpha,beta,gamma in degrees; radians if False
          string (bool): If True return a,b,c,alpha,beta,gamma as a string; if False return as a list
          bohr (bool): If True return a,b,c in bohr radii; if False return in angstrom
    Returns:
         paramArray (list): a list of the parameters a,b,c,alpha,beta,gamma generated from the input matrix
    '''        

    ibrav = getIbravFromVectors(cellparamatrix)
    try:
        cellparamatrix=cellparamatrix.getA()
    except Exception,e:
        pass
#        print e
    try:
        a = numpy.sqrt(cellparamatrix[0].dot(cellparamatrix[0].T))
        b = numpy.sqrt(cellparamatrix[1].dot(cellparamatrix[1].T))
        c = numpy.sqrt(cellparamatrix[2].dot(cellparamatrix[2].T))
    except:
        cellparamatrix = numpy.array(cellparamatrix)
        a = numpy.sqrt(cellparamatrix[0].dot(cellparamatrix[0]))
        b = numpy.sqrt(cellparamatrix[1].dot(cellparamatrix[1]))
        c = numpy.sqrt(cellparamatrix[2].dot(cellparamatrix[2]))

    degree2radian = numpy.pi/180
    alpha,beta,gamma=(0.0,0.0,0.0)


    alpha = numpy.arccos(cellparamatrix[1].dot(cellparamatrix[2].T)/(b*c))
    beta  = numpy.arccos(cellparamatrix[0].dot(cellparamatrix[2].T)/(a*c))
    gamma = numpy.arccos(cellparamatrix[0].dot(cellparamatrix[1].T)/(a*b))

    if numpy.abs(alpha)<0.000001:
        alpha=0.0
    if numpy.abs(beta)<0.000001:
        beta=0.0
    if numpy.abs(gamma)<0.000001:
        gamma=0.0


    AngstromToBohr = 1.88971616463207
    BohrToAngstrom = 1/AngstromToBohr
    if bohr==False:
        a*=BohrToAngstrom
        b*=BohrToAngstrom
        c*=BohrToAngstrom

        a=float('%10.5e'%numpy.around(a,decimals=5))
        b=float('%10.5e'%numpy.around(b,decimals=5))
        c=float('%10.5e'%numpy.around(c,decimals=5))

    if cosine==True:
        cosBC=numpy.cos(alpha)
        cosAC=numpy.cos(beta)
        cosAB=numpy.cos(gamma)
        paramArray = [a,b,c,cosBC,cosAC,cosAB]

        param_list=[]
        for v in range(len(paramArray)):
            param_list.append(float('%10.5e'%numpy.around(paramArray[v],decimals=5)))
        paramArray=tuple(param_list)

        returnString = 'a=%s,b=%s,c=%s,cos(alpha)=%s,cos(beta)=%s,cos(gamma)=%s' % tuple(paramArray)

    if degrees==True:
        alpha/=degree2radian
        beta/= degree2radian
        gamma/=degree2radian

    if cosine!=True:
        paramArray = (a,b,c,alpha,beta,gamma)

        param_list=[]
        for v in range(len(paramArray)):
            param_list.append(float('%10.5e'%numpy.around(paramArray[v],decimals=5)))
        paramArray=tuple(param_list)
            
        returnString = 'A=%s,B=%s,C=%s,alpha=%s,beta=%s,gamma=%s' % tuple(paramArray)

    if string==True:
        return returnString
    else:

        return paramArray