import matplotlib.pyplot as plt
import metpy.calc as mcalc
import metpy.plots as mplots

def plot_vertical(sonde_df, ax=None, *args, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    for t in sonde_df.columns:
        ax.plot(sonde_df[t].values, sonde_df.index, label=t)
        ax.legend()
    return ax

def plot_skewT(sonde,
               fig, 
               title=None,
               subplot=None,
               rotation=45,
               rect=None,
               aspect=80.5,
               barb_count=20
               ):
    
    """Plot SkewT diagram. 

    Adopted from metpy.
    """
    skew = mplots.SkewT(fig, rotation=rotation, rect=rect, aspect=aspect)
    
    p = sonde.pressure
    T = sonde.temperature
    Td = sonde.dewpoint
    u = sonde.wind_east
    v= sonde.wind_north
    barb_step = len(p) // barb_count
    # handle the case where automatic bar_step is zero
    if barb_step == 0:
        barb_step = 1

    # provide default title
    if title is None:
        time_str = sonde.launch_time.strftime("%F %H:%M")
        title = f"Sonde launched @ ({sonde.launch_lat:5.3f}N, {sonde.launch_lon:5.3f}E)"+\
                f"\nLaunch Time: {time_str}"
    skew.ax.set(title=title)

    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot.
    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')
    skew.plot_barbs(p[::barb_step], u[::barb_step], v[::barb_step])
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-40, 60)

    # Calculate LCL height and plot as black dot. Because `p`'s first value is
    # ~1000 mb and its last value is ~250 mb, the `0` index is selected for
    # `p`, `T`, and `Td` to lift the parcel from the surface. If `p` was inverted,
    # i.e. start from low value, 250 mb, to a high value, 1000 mb, the `-1` index
    # should be selected.
    lcl_pressure, lcl_temperature = mcalc.lcl(p[0], T[0], Td[0])
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

    # Calculate full parcel profile and add to plot as black line
    prof = mcalc.parcel_profile(p, T[0], Td[0]).to('degC')
    skew.plot(p, prof, 'k', linewidth=2)

    # Shade areas of CAPE and CIN
    skew.shade_cin(p, T, prof)
    skew.shade_cape(p, T, prof)

    # An example of a slanted line at constant T -- in this case the 0
    # isotherm
    skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

    # Add the relevant special lines
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    
    return skew
