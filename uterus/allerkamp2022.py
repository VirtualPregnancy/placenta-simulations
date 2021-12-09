import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from SALib.sample import saltelli
from scipy.optimize import curve_fit, minimize,least_squares
import os
import placentagen as pg
import csv

D0_list = [150,150,172.8,172.8,170.8,135.8,43,230,255.6,301.6,304.1,108.1,85.7,60.7,235.6,156.5,255.4,164.8,100.8,64.9]
Cpass_list = [1.168,1.168,1.416,1.416,1.386,1.067,0.316,1.697,1.417,1.672,1.857,0.843,0.655,0.371,1.802,1.043,1.719,1.141,0.687,0.459]
Cpassdash_list = [7.24,7.24,7.901,7.901,10.568,10.516,11.247,5.298,5.628,5.324,5.226,24.279,36.785,21.035,6.782,8.293,14.354,13.828,12.606,13.431]
Cact_list = [1.108, 1.103, 1.499, 1.858, 1.514, 1.202, 0.392, 3.995, 2.649, 1.395, 3.748, 1.665, 1.024, 0.654,
             0.908, 3.491, 1.564, 1.36, 1.131, 0.405]
D0_list_act = [150,172.8,170.8,135.8,43,156.5,255.4,164.8,100.8,64.9]
Cmyo_list = [7.479,8.871,8.462,7.973,24.934,9.018,4.674,7.508,15.977,22.252]

expt_pressure = np.array([10.,30.,50.,70.,90.]) # defined in mmHg
passive_diameter_preg = np.array([76.258, 122.33566667, 145.152, 137.5625, 144.64166667])
passive_se_preg = np.array([10.8693589, 10.23274183, 13.36969036, 11.7338111, 12.88427201])
passive_diameter = np.array([54.11314286, 74.08128571, 88.831, 89.99828571, 86.769])
passive_se = np.array([3.71311161,5.78277879,9.940847,9.98130157,12.93325597])
active_diameter_preg = np.array([92.70733333,113.74933333,121.8715,107.93166667,101.19983333])
active_se_preg = np.array([8.36576993,6.12886374,15.68328409,15.01816237,19.29603708])
active_diameter = np.array([65.587,74.17528571,79.87185714,83.58714286,80.92285714])
active_se = np.array([5.52633482,5.86497481,7.06835057,7.71278033,9.02834107])

num_plot= 101
def main():
    ## Create a directory to output figures
    export_directory = 'output'
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
    passive_file = 'data/PassiveFits.csv'
    active_file = 'data/ActiveFits.csv'
    shear_file = 'data/FlowFits.csv'
    file = open(passive_file)
    passive_data = csv.reader(file)
    header = next(passive_data)
    rows = []
    for row in passive_data:
        rows.append(row)
    file.close()
    D0 = float(rows[0][0])
    Cpass = float(rows[1][0])
    Cpassdash = float(rows[2][0])

    Cpass_preg = float(rows[4][0])
    Cpassdash_preg = float(rows[5][0])
    D0_preg = float(rows[3][0])

    file = open(active_file)
    active_data = csv.reader(file)
    header = next(active_data)
    rows = []
    for row in active_data:
        rows.append(row)
    print(rows)
    file.close()

    Cact = float(rows[0][0])
    Cactdash = float(rows[1][0])
    Cactdashdash = float(rows[2][0])
    Cmyo = float(rows[3][0])
    Cdashdashtone = float(rows[4][0])
    Cact_preg = float(rows[5][0])
    Cactdash_preg = float(rows[6][0])
    Cactdashdash_preg = float(rows[7][0])
    Cmyo_preg = float(rows[8][0])
    Cdashdashtone_preg = float(rows[9][0])

    file = open(shear_file)
    shear_data = csv.reader(file)
    header = next(shear_data)
    rows = []
    for row in shear_data:
        rows.append(row)
    print(rows)
    file.close()

    Cshear = float(rows[0][0])
    Cshear1 = float(rows[1][0])
    shear_offset1 = float(rows[2][0])
    shear_offset2 = float(rows[3][0])
    Cshear_preg = float(rows[4][0])
    Cshear1_preg = float(rows[5][0])
    shear_offset1_preg = float(rows[6][0])
    shear_offset2_preg = float(rows[7][0])

    print("Non-pregnant D0 (um) ", D0)
    print("Non-pregnant Cpass (N.m)", Cpass/1000.)
    print("Non-pregnant Cpassdash (no units)",Cpassdash)
    print("Non-pregnant Cact (N.m) ", Cact / 1000.)
    print("Non-pregnant Cactdash (no units) ", Cactdash)
    print("non-pregnant Cactdashdash (no units)", Cactdashdash)
    print("non-pregnant Cmyo (m/N)", Cmyo * 1000.)
    print("non-pregnant C'tone (no units)", Cdashdashtone)
    print("non-pregnant Cshear (no units)", Cshear)
    print("non-pregnant Cshear1 (no units)", Cshear1)
    print("non-pregnant tau1 (no units)", shear_offset1)
    print("non-pregnant tau2 (no units)", shear_offset2)
    print("-------------------------------------")
    print("pregnant D0 (um) ", D0_preg)
    print("pregnant Cpass (N.m)", Cpass_preg/1000.)
    print("pregnant Cpassdash (no units)",Cpassdash_preg)
    print("pregnant Cact (N.m) ", Cact_preg / 1000.)
    print("pregnant Cactdash (no units) ", Cactdash_preg)
    print("pregnant Cactdashdash (no units)", Cactdashdash_preg)
    print("pregnant Cmyo (m/N)", Cmyo_preg * 1000.)
    print("pregnant C'tone (no units)", Cdashdashtone_preg)
    print("pregnant Cshear (no units)", Cshear_preg)
    print("pregnant Cshear1 (no units)", Cshear1_preg)
    print("pregnant tau1 (no units)", shear_offset1_preg)
    print("pregnant tau2 (no units)", shear_offset2_preg)

    new_passive_d = np.zeros((num_plot, 1))
    new_passive_d_preg = np.zeros((num_plot, 1))
    new_active_d = np.zeros((num_plot, 1))
    new_active_d_preg = np.zeros((num_plot, 1))
    fit_passive_params = [D0, Cpass, Cpassdash]
    fit_passive_params_preg = [D0_preg, Cpass_preg, Cpassdash_preg]
    dummy_myo_params = [0., 0., 0., 0., 0.]
    fit_myo_params = [Cact, Cactdash,Cactdashdash,Cmyo,Cdashdashtone]
    fit_myo_params_preg = [Cact_preg, Cactdash_preg, Cactdashdash_preg, Cmyo_preg, Cdashdashtone_preg]
    dummy_flow_params = [0., 0., 0., 0.]
    dummy_fixed_flow_params = [0., 0., 0.]
    new_pressure = np.linspace(10, 90, num_plot) * 133. / 1000.

    for i in range(0, num_plot):
        new_passive_d[i] = pg.diameter_from_pressure(fit_passive_params,
                                                 dummy_myo_params, dummy_flow_params, dummy_fixed_flow_params, new_pressure[i],
                                                 True)
        new_passive_d_preg[i] = pg.diameter_from_pressure(fit_passive_params_preg,
                                                 dummy_myo_params, dummy_flow_params, dummy_fixed_flow_params, new_pressure[i],
                                                 True)
        new_active_d[i] = pg.diameter_from_pressure(fit_passive_params,
                                                 fit_myo_params, dummy_flow_params, dummy_fixed_flow_params,
                                                 new_pressure[i],
                                                 True)
        new_active_d_preg[i] = pg.diameter_from_pressure(fit_passive_params_preg,
                                                      fit_myo_params_preg, dummy_flow_params, dummy_fixed_flow_params,
                                                      new_pressure[i],
                                                      True)

    ###############################################
    #Plot passive results against experimental data
    ###############################################

    plt.errorbar(expt_pressure, passive_diameter_preg, passive_se_preg, marker='s', ls='--', color='#F01D7F',
                 label="Experimental data (pregnant)", capsize=5.)
    plt.errorbar(expt_pressure, passive_diameter, passive_se, marker='o', ls='--', color='.5',
                 label="Experimental data (non-pregnant)", capsize=5.)
    plt.ylim((0, 250.))
    plt.xlim((0., 100.))
    plt.plot(np.linspace(10, 90, num_plot), new_passive_d_preg, '#F01D7F', label="Model fit (pregnant)")
    plt.plot(np.linspace(10, 90, num_plot), new_passive_d, '0.5', label="Model fit (non-pregnant)")
    plt.xlabel('Pressure (mmHg)')
    plt.ylabel('Inner diameter ($\mu$m)')
    plt.legend()
    plt.savefig(export_directory + '/PassiveFitsNonNormalised.png')
    plt.close()

    plt.errorbar(expt_pressure, passive_diameter_preg / passive_diameter_preg[0], passive_se_preg / passive_diameter_preg[0],
                 marker='s', ls='--', color='#F01D7F', label="Experimental data (pregnant)", capsize=5.)
    plt.errorbar(expt_pressure, passive_diameter / passive_diameter[0],
                 passive_se / passive_diameter[0], marker='o', ls='--', color='.5',
                 label="Experimental data (non-pregnant)", capsize=5.)
    plt.ylim((0, 2.5))
    plt.xlim((0., 100.))
    plt.plot(np.linspace(10, 90, num_plot), new_passive_d_preg / passive_diameter_preg[0], '#F01D7F', label="Model fit (pregnant)")
    plt.plot(np.linspace(10, 90, num_plot), new_passive_d / passive_diameter[0], '0.5', label="Model fit (non-pregnant)")
    plt.xlabel('Pressure (mmHg)')
    plt.ylabel('Inner diameter / Diameter at 10mmHg')
    plt.legend()
    plt.savefig(export_directory + '/PassiveFitsNormalisedTo10mmHg.png')
    plt.close()

    ##################################################################
    #Plot active model results against experimental data
    #################################################################
    plt.errorbar(expt_pressure, passive_diameter_preg, passive_se_preg, marker='s',
                 markerfacecolor='none', ls='--', color='#F01D7F', label="Passive data (pregnant)", capsize=5.)
    plt.errorbar(expt_pressure, passive_diameter, passive_se, marker='o',
                 markerfacecolor='none', ls='--', color='.5', label="Passive data (non-pregnant)", capsize=5.)
    plt.errorbar(expt_pressure, active_diameter_preg, active_se_preg, marker='s', color='#F01D7F',
                 label="Active data (pregnant)", capsize=5.)
    plt.errorbar(expt_pressure, active_diameter, active_se, marker='o', color='.5',
                 label="Active data (non-pregnant)", capsize=5.)
    plt.ylim((0, 250.))
    plt.xlim((0., 100.))
    plt.xlabel('Pressure (mmHg)')
    plt.ylabel('Inner diameter ($\mu$m)')
    plt.legend()
    plt.savefig(export_directory + '/ExperimentalDataActiveNoFlow.png')
    plt.close()

    plt.ylim((0, 250.))
    plt.xlim((0., 100.))
    plt.xlabel('Pressure (mmHg)')
    plt.ylabel('Inner diameter ($\mu$m)')
    plt.plot(np.linspace(10, 90, num_plot), new_passive_d_preg, color='#F01D7F', linestyle='--',
             label="Passive model fit (pregnant)")
    plt.plot(np.linspace(10, 90, num_plot), new_passive_d, color='0.5', linestyle='--',
             label="Passive model fit (non-pregnant)")
    plt.plot(np.linspace(10, 90, num_plot), new_active_d_preg, color='#F01D7F', label="Active model fit (pregnant)")
    plt.plot(np.linspace(10, 90, num_plot), new_active_d, color='0.5', label="Active model fit (non-pregnant)")
    plt.errorbar(expt_pressure, active_diameter_preg, active_se_preg, marker='s', ls=':', color='#F01D7F',
                 label="Experimental data (pregnant)", capsize=5.)
    plt.errorbar(expt_pressure, active_diameter, active_se, marker='o', ls=':', color='0.5',
                 label="Experimental data (non-pregnant)", capsize=5.)

    plt.savefig(export_directory + '/ActiveNoFlowFits.png')
    plt.close()


    ##########################################################
    #Plot Cpass Comparisons
    ############################################################
    x = np.linspace(30, 320, 3)
    y = 0.0059 * x + 0.1892
    plt.plot(D0_list, Cpass_list, color='k', marker='x', linestyle='None', label="Carlson and Secombe (2005)")
    plt.plot(x, y, color='k', ls=':', label='Fit to Carlson and Secombe data')
    plt.plot(D0, Cpass/1000., marker='o', color='#F01D7F', linestyle='None', label='Rat radial (non-pregnant)')
    plt.plot(D0_preg, Cpass_preg/1000., marker='s', color='#F01D7F', linestyle='None', label='Rat radial  (pregnant)')
    plt.annotate("", xy=(0.975*D0_preg,0.975*Cpass_preg/1000.), xytext=(D0, Cpass/1000.), arrowprops=dict(headwidth=5, headlength=5, width=0.1,color='#F01D7F'))
    matplotlib.pyplot.text(48., 0.75, "R=0.94", fontsize=12)
    plt.xlabel('D$_0$ ($\mu$m)', fontsize=16)
    plt.ylabel('C$_{pass}$ (N/m)', fontsize=16)
    plt.legend()
    plt.savefig(export_directory + '/CpassComparison.png')
    plt.close()
    ##########################################################
    #Plot Cpass Comparisons
    ############################################################
    x = np.linspace(30, 320, 3)
    y = -0.0574 * x + 21.239
    plt.plot(D0_list, Cpassdash_list, color='k', marker='x', linestyle='None', label="Carlson and Secombe (2005)")
    plt.plot(x, y, color='k', ls=':', label='Fit to Carlson and Secombe data')
    plt.plot(D0, Cpassdash, marker='o', color='#F01D7F', linestyle='None',
             label='Rat radial (non-pregnant)')
    plt.plot(D0_preg, Cpassdash_preg, marker='s', color='#F01D7F', linestyle='None', label='Rat radial  (pregnant)')
    plt.annotate("", xy=(0.975*D0_preg,0.975*Cpassdash_preg), xytext=(D0, Cpassdash), arrowprops=dict(headwidth=5, headlength=5, width=0.1,color='#F01D7F'))
    matplotlib.pyplot.text(100., 18., "R=-0.57", fontsize=12)
    plt.xlabel('D$_0$ ($\mu$m)', fontsize=16)
    plt.ylabel('C$^{,}_{pass}$', fontsize=16)
    plt.legend()
    plt.savefig(export_directory + '/CpassdashComparison.png')
    plt.close()

    ###########################################################
    #Plot Cmyo comparisons
    ############################################################
    x = np.linspace(30,320,3)
    y  = -0.104*x + 26.426
    plt.ylim((0.,27.))
    plt.plot(D0_list_act,Cmyo_list,color = 'k',marker='x',linestyle ='None',label = "Carlson and Secombe (2005)")
    plt.plot(x,y,color='k',ls=':', label = 'Fit to Carlson and Secombe data')
    plt.plot(D0,Cmyo*1000.,marker='o',color = '#F01D7F', linestyle ='None',label ='Rat radial (non-pregnant)')
    plt.plot(D0_preg,Cmyo_preg*1000.,marker='s',color='#F01D7F',linestyle ='None',label = 'Rat radial  (pregnant)')
    plt.annotate("", xy=(0.975*D0_preg,0.975*Cmyo_preg*1000.), xytext=(D0, Cmyo*1000.), arrowprops=dict(headwidth=5, headlength=5, width=0.1,color='#F01D7F'))
    matplotlib.pyplot.text(100., 18., "R=-0.91", fontsize=12)
    plt.xlabel('D$_0$ ($\mu$m)',fontsize=16)
    plt.ylabel('C$_{myo}$',fontsize=16)
    plt.legend()
    plt.savefig(export_directory + '/CmyoComparison.png')
    plt.close()

    ##################################################################
    #Plot Cact Comparisons
    ##################################################################
    x = np.linspace(30, 320, 3)
    y = 0.008 * x + 0.3037
    plt.plot(D0_list, Cact_list, color='k', marker='x', linestyle='None', label="Carlson and Secombe (2005)")
    plt.plot(x, y, color='k', ls=':', label='Fit to Carlson and Secombe data')
    plt.plot(D0,Cact/1000., marker='o', color='#F01D7F', linestyle='None', label='Rat radial (non-pregnant)')
    plt.plot(D0_preg, Cact_preg/1000., marker='s', color='#F01D7F', linestyle='None', label='Rat radial  (pregnant)')
    plt.xlabel('D$_0$ ($\mu$m)', fontsize=16)
    plt.ylabel('C$_{act}$', fontsize=16)
    plt.annotate("", xy=(0.985*D0_preg,1.025*Cact_preg/1000.), xytext=(D0, Cact/1000.), arrowprops=dict(headwidth=5, headlength=5, width=0.1,color='#F01D7F'))
    matplotlib.pyplot.text(50., 1.2, "R=0.60", fontsize=12)
    plt.savefig(export_directory + '/CactComparison.png')
    plt.close()


if __name__ == '__main__':
    main()

'''


#plot pregnant results independently
plt.ylim((0,250.))
plt.xlim((0.,100.))
plt.xlabel('Pressure (mmHg)')
plt.ylabel('Inner diameter ($\mu$m)')
plt.title("Rat non-pregnant radial artery (D$_0$ =  94 $\mu$m)")
plt.errorbar(expt_pressure,expt_diameter_non_preg,expt_se_non_preg,marker='o',ls=':',color='0.5',label="Experimental data",capsize=5.)
plt.plot(np.linspace(10,90,num_plot),active_diam, color = '0.5', label = "Active model fit")
plt.plot(np.linspace(10,90,num_plot),passive_diam,color = '0.5',linestyle = '--',label = "Passive model fit")
plt.legend()
plt.show()

Dmax = D0*(Cpassdash + 1)
Dmax_preg = D0_preg*(Cpassdash_preg + 1)
print(Dmax,Dmax_preg)
stone =  Cmyo * np.linspace(10,90,num_plot) * active_diam / 2. + Cdashdashtone
A = 1./(1.+np.exp(-stone))
Tmaxact = Cact * np.exp(-((active_diam / D0 - Cactdash) / Cactdashdash) ** 2.)
Tpass = Cpass * np.exp(Cpassdash * (active_diam / D0 - 1.))
Tpass_preg = Cpass_preg * np.exp(Cpassdash_preg * (active_diam_preg / D0_preg - 1.))
stone_preg =  Cmyo_preg * np.linspace(10,90,num_plot) * active_diam_preg / 2. + Cdashdashtone_preg
A_preg = 1./(1.+np.exp(-stone_preg))
Tmaxact_preg = Cact_preg * np.exp(-((active_diam_preg / D0_preg - Cactdash_preg) / Cactdashdash_preg) ** 2.)
plot_np = (A*Tmaxact)/Tpass#/np.max(A*Tmaxact) #normalised active tension
plot_p = (A_preg*Tmaxact_preg)/Tpass_preg#/np.max(A_preg*Tmaxact_preg)
#fig, ax = plt.subplots(constrained_layout=True)
#ax2=ax.twinx()
#plt.xlim(10.,90.)
#ax.set_ylim(-4.,30)
#ax2.set_ylim(0.,1.1)
plt.plot(np.linspace(10,90,num_plot),plot_np, color = '0.5', label = "Non-pregnant model active tension")
plt.plot(np.linspace(10,90,num_plot),plot_p, color = '0.5', label = "Non-pregnant model passive tension")
#plt.plot(np.linspace(10,90,num_plot),(passive_diam-active_diam)/passive_diam, color = '0.5', label = "Non-pregnant")
#plt.plot(np.linspace(10,90,num_plot),plot_p, color = '#F01D7F', label = "Non-pregnant")
#plt.plot(np.linspace(10,90,num_plot),(passive_diam_preg-active_diam_preg)/passive_diam_preg, color = '#F01D7F', label = "Non-pregnant")
plt.show()
'''
'''
xpos = [30.,50.,70.]
ypos = [-1.645220431,7.837462658,2.07281238]
error = [2.467874887,1.643298051,4.167023468]
ax.errorbar(xpos,ypos,error,marker='o',ls=':',color='0.5',label="Non-pregnant myogenic tone",capsize=5.)
#ax.bar(xpos,ypos,yerr=error,
#       align='center',
#      alpha=0.5,color = '0.5')
plt.show()

fig, ax = plt.subplots(constrained_layout=True)
ax2=ax.twinx()
plt.xlim(20.,80.)
ax.set_ylim(-4.,30)
ax2.set_ylim(0.,1.1)
ax2.plot(np.linspace(10,90,num_plot),plot_p, color = '#F01D7F', label = "Non-pregnant model active tension")
#ax2.plot(np.linspace(10,90,num_plot),Tpass_preg/np.max(Tpass_preg), color = '#F01D7F', label = "Non-pregnant model active tension")
#plt.plot(np.linspace(10,90,num_plot),(passive_diam-active_diam)/passive_diam, color = '0.5', label = "Non-pregnant")
#plt.plot(np.linspace(10,90,num_plot),plot_p, color = '#F01D7F', label = "Non-pregnant")
#plt.plot(np.linspace(10,90,num_plot),(passive_diam_preg-active_diam_preg)/passive_diam_preg, color = '#F01D7F', label = "Non-pregnant")
xpos = [30.,50.,70.]
ypos = [4.363417522,14.38276927,20.09353259]
error = [3.226036136,4.70926462,5.167192609]
ax.errorbar(xpos,ypos,error,marker='o',ls=':',color='#F01D7F',label="Non-pregnant myogenic tone",capsize=5.)
#ax.bar(xpos,ypos,yerr=error,
#       align='center',
#      alpha=0.5,color = '0.5')
plt.show()

quit()
#plot non-pregnant results independently
plt.ylim((0,250.))
plt.xlim((0.,100.))
plt.xlabel('Pressure (mmHg)')
plt.ylabel('Inner diameter ($\mu$m)')
plt.title("Rat pregnant radial artery (D$_0$ =  156 $\mu$m)")
plt.errorbar(expt_pressure,expt_diameter_preg,expt_se_preg,marker='s',ls=':',color='#F01D7F',label="Experimental data",capsize=5.)
plt.plot(np.linspace(10,90,num_plot),active_diam_preg,color = '#F01D7F', label = "Active model fit")
plt.plot(np.linspace(10,90,num_plot),passive_diam_preg,color = '#F01D7F',linestyle = '--',label = "Passive model fit")
plt.legend()
plt.show()

total_tension = np.linspace(0.,2.5,100)
Cpass = Cpass/1000.
Cact = Cact/1000.
Cmyo = Cmyo*1000.
Cpass_preg = Cpass_preg/1000.
Cact_preg = Cact_preg/1000.
Cmyo_preg = Cmyo_preg*1000.

print(Cpass,Cpassdash)
diameter_pass = np.linspace(0,2*D0,100)
diameter = np.linspace(0,2*D0,100)
Tpass = Cpass * np.exp(Cpassdash * (diameter_pass / D0 - 1.))
Tmaxact = Cact * np.exp(-((diameter / D0 - Cactdash) / Cactdashdash) ** 2.)
Anonpreg = 1./(1+np.exp(-Cmyo*total_tension-Cdashdashtone))

plt.ylim((0,4.))
plt.xlim((0.,2.))
plt.plot(diameter_pass/D0,Tpass,color='k',linestyle = '--',label="Passive tension")
plt.plot(diameter/D0,Tmaxact,color = 'k', linestyle = 'dotted',label = "Maximally active tension")
plt.plot(diameter/D0,Tpass+Tmaxact,color='k', label = "Total tension with maximum activation")
plt.legend()
plt.xlabel("Diameter/D$_0$")
plt.ylabel("Tension (N.m)")
plt.title("Rat non-pregnant radial artery (D$_0$ = 94 $\mu$m)")
plt.show()

plt.xlim((0.,2.5))
plt.plot(total_tension, Anonpreg,color = '0.5')
plt.xlabel("Total tension (N.m)")
plt.ylabel("Smooth muscle activation (no units)")
plt.title("Rat non-pregnant radial artery (D$_0$ =  94 $\mu$m)")
plt.show()

diameter_pass = np.linspace(0,2*D0_preg,100)
diameter = np.linspace(0,2*D0_preg,100)
Tpass = Cpass_preg * np.exp(Cpassdash_preg * (diameter_pass / D0_preg - 1.))
Tmaxact = Cact_preg * np.exp(-((diameter / D0_preg - Cactdash_preg) / Cactdashdash_preg) ** 2.)
Apreg = 1./(1+np.exp(-Cmyo_preg*total_tension-Cdashdashtone_preg))


plt.ylim((0,4.))
plt.xlim((0.,2.))
plt.plot(diameter_pass/D0_preg,Tpass,color='k',linestyle = '--',label="Passive tension")
plt.plot(diameter/D0_preg,Tmaxact,color = 'k', linestyle = 'dotted',label = "Maximally active tension")
plt.plot(diameter/D0_preg,Tpass+Tmaxact,color='k', label = "Total tension with maximum activation")
plt.legend()
plt.xlabel("Diameter/D$_0$")
plt.ylabel("Tension (N.m)")
plt.title("Rat pregnant radial artery (D$_0$ = 156 $\mu$m)")
plt.show()

plt.xlim((0.,2.5))
plt.plot(total_tension, Anonpreg,color = '0.5')
plt.xlabel("Total tension (N.m)")
plt.ylabel("Smooth muscle activation (no units)")
plt.title("Rat pregnant radial artery (D$_0$ =  156 $\mu$m)")
plt.show()

#msenteric vessel
D0 = 150
Cpass = 1.168
Cpassdash = 7.24
Cact = 1.108
Cactdash = .843 #84#
Cactdashdash = .406
Cmyo = 7.479
Cdashtone = 4.614 

print("Mesenteric Cact (N.m) ", Cact)
print("Mesenteric Cactdash (no units) ", Cactdash)
print("Mesenteric Cactdashdash (no units)", Cactdashdash)
print("Mesenteric Cmyo (m/N)", Cmyo)
print("Mesenteric C'tone (no units)", Cdashdashtone)

diameter_pass = np.linspace(0,2*D0,100)
diameter = np.linspace(0,2*D0,100)
Tpass = Cpass * np.exp(Cpassdash * (diameter_pass / D0 - 1.))
print(Tpass)
Tmaxact = Cact * np.exp(-((diameter / D0 - Cactdash) / Cactdashdash) ** 2.)
Ames = 1./(1+np.exp(-Cmyo*total_tension+Cdashtone))

plt.ylim((0,4.))
plt.xlim((0.,2.))
plt.plot(diameter_pass/D0,Tpass,color='k',linestyle = '--',label="Passive tension")
plt.plot(diameter/D0,Tmaxact,color = 'k', linestyle = 'dotted',label = "Maximally active tension")
plt.plot(diameter/D0,Tpass+Tmaxact,color='k', label = "Total tension with maximum activation")
plt.legend()
plt.xlabel("Diameter/D$_0$")
plt.ylabel("Tension (N.m)")
plt.title("Rat Mesenteric Artery (D$_0$ = 150 $\mu$m)")
plt.show()


#porcine coronary
D0 = 100.8
Cpass = 0.685
Cpassdash = 12.61
Cact = 1.131
Cactdash = .910
Cactdashdash = .343
Cmyo =15.977
Cdashtone = 4.180
diameter_pass = np.linspace(0,2*D0,100)
diameter = np.linspace(0,2*D0,100)
Tpass = Cpass * np.exp(Cpassdash * (diameter_pass / D0 - 1.))
Tmaxact = Cact * np.exp(-((diameter / D0 - Cactdash) / Cactdashdash) ** 2.)
Aporc = 1./(1+np.exp(-Cmyo*total_tension+Cdashtone))

plt.ylim((0,4.))
plt.xlim((0.,2.))
plt.plot(diameter_pass/D0,Tpass,color='k',linestyle = '--',label="Passive tension")
plt.plot(diameter/D0,Tmaxact,color = 'k', linestyle = 'dotted',label = "Maximally active tension")
plt.plot(diameter/D0,Tpass+Tmaxact,color='k', label = "Total tension with maximum activation")
plt.legend()
plt.xlabel("Diameter/D$_0$")
plt.ylabel("Tension (N.m)")
plt.title("Porcine coronary artery (D$_0$ =  num_plot $\mu$m)")
plt.show()

plt.xlim((0.,2.5))
plt.plot(total_tension, Ames,color = 'k')
plt.xlabel("Total tension (N.m)")
plt.ylabel("Smooth muscle activation (no units)")
plt.title("Rat Mesenteric Artery (D$_0$ = 150 $\mu$m)")
plt.show()
plt.xlim((0.,2.5))

plt.plot(total_tension, Aporc, color = 'k')
plt.xlabel("Total tension (N.m)")
plt.ylabel("Smooth muscle activation (no units)")
plt.title("Porcine coronary artery (D$_0$ =  num_plot $\mu$m)")
plt.show()


quit()


########################################

D0 = 150
Cpass = 1.168*1000.
Cpassdash = 7.24
Cact = 1.108*1000.
Cactdash = .843
Cactdashdash = .406
Cmyo = 7.479/1000.
Cdashtone = -4.614
fit_passive_params = [D0,Cpass,Cpassdash]
fit_myo_params = [Cact, Cactdash, Cactdashdash, Cmyo, Cdashdashtone]
fit_flow_params = [0.,0.,0.,0.]
fixed_flow_params = [0.,0.,0.]
active_diam_mes = np.zeros(num_plot)
passive_diam_mes = np.zeros(num_plot)
pressure = np.linspace(10,90,num_plot)*133./1000.
for i in range(0,num_plot):
    fit_myo_params = [Cact, Cactdash, Cactdashdash, Cmyo, Cdashdashtone]
    active_diam_mes[i] = pg.diameter_from_pressure(fit_passive_params,fit_myo_params,fit_flow_params,fixed_flow_params,pressure[i],True)
    fit_myo_params = [0.,0., 0.,0., 0.]
    passive_diam_mes[i]=pg.diameter_from_pressure(fit_passive_params,fit_myo_params,fit_flow_params,fixed_flow_params,pressure[i],True)


plt.ylim((0,250.))
plt.xlim((0.,100.))
plt.xlabel('Pressure (mmHg)')
plt.ylabel('Inner diameter ($\mu$m)')
plt.title("Rat Mesenteric Artery (D$_0$ = 150 $\mu$m)")
plt.plot(np.linspace(10,90,num_plot),active_diam_mes,color = 'k', label = "Active model")
plt.plot(np.linspace(10,90,num_plot),passive_diam_mes,color = 'k',linestyle = '--',label = "Passive model")
plt.plot(np.linspace(10,90,num_plot),active_diam_preg,color = '#F01D7F', label = "Active model fit")
plt.plot(np.linspace(10,90,num_plot),passive_diam_preg,color = '#F01D7F',linestyle = '--',label = "Passive model fit")
plt.legend()
plt.show()

D0 = 100.8
Cpass = 0.685*1000.
Cpassdash = 12.61
Cact = 1.131*1000.
Cactdash = .910
Cactdashdash = .343
Cmyo =15.977/1000.
Cdashtone = -4.180
fit_passive_params = [D0,Cpass,Cpassdash]
fit_myo_params = [Cact, Cactdash, Cactdashdash, Cmyo, Cdashdashtone]
fit_flow_params = [0.,0.,0.,0.]
fixed_flow_params = [0.,0.,0.]
active_diam_mes = np.zeros(num_plot)
passive_diam_mes = np.zeros(num_plot)
pressure = np.linspace(10,90,num_plot)*133./1000.
for i in range(0,num_plot):
    fit_myo_params = [Cact, Cactdash, Cactdashdash, Cmyo, Cdashdashtone]
    active_diam_mes[i] = pg.diameter_from_pressure(fit_passive_params,fit_myo_params,fit_flow_params,fixed_flow_params,pressure[i],True)
    fit_myo_params = [0.,0., 0.,0., 0.]
    passive_diam_mes[i]=pg.diameter_from_pressure(fit_passive_params,fit_myo_params,fit_flow_params,fixed_flow_params,pressure[i],True)


plt.ylim((0,250.))
plt.xlim((0.,100.))
plt.xlabel('Pressure (mmHg)')
plt.ylabel('Inner diameter ($\mu$m)')
plt.title("Porcine coronary artery (D$_0$ =  num_plot $\mu$m)")
plt.plot(np.linspace(10,90,num_plot),active_diam_mes,color = 'k', label = "Active model")
plt.plot(np.linspace(10,90,num_plot),passive_diam_mes,color = 'k',linestyle = '--',label = "Passive model")
plt.legend()
plt.show()
'''