import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Import both data tables into python using pandas. Set the index column to "MESS_DATUM" and parse the column values as dates. [1P]
data_ex4 = Path('C:/Users/Admin/Documents/GitHub/exercise-4-SoBoeckler')
data_dir = data_ex4 / 'data'
output_dir = data_ex4 / 'results'
output_dir.mkdir(parents=True,exist_ok=True)

garmisch = pd.read_csv(data_dir / "produkt_klima_tag_20171010_20190412_01550.txt", sep = ";", 
                       index_col="MESS_DATUM", parse_dates=["MESS_DATUM"], na_values=-999.0)

zugspitze = pd.read_csv(data_dir / "produkt_klima_tag_20171010_20190412_05792.txt", sep = ";", 
index_col="MESS_DATUM", parse_dates=["MESS_DATUM"], na_values=-999.0)



# Clip the tables to the year 2018: [1P]
garmisch  = garmisch["2018"] 
zugspitze = zugspitze["2018"] 

# Resample the temperature data to monthly averages (" TMK") and store them in simple lists: [1P]
garmisch_agg  =  list(garmisch.loc[:," TMK"].resample("1M").agg(["mean"])["mean"])
zugspitze_agg =  list(zugspitze.loc[:," TMK"].resample("1M").agg(["mean"])["mean"])

# Define a plotting function that draws a simple climate diagram
# Add the arguments as mentioned in the docstring below [1P]
# Set the default temperature range from -15°C to 20°C and the precipitation range from 0mm to 370mm [1P]
def create_climate_diagram(df,
                           temp_col,
                           prec_col,
                           title,
                           filename,
                           temp_min=-15,
                           temp_max=20,
                           prec_min=0,
                           prec_max=370):
   
    """
    Draw a climate diagram.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with values to plot from
    temp_col : str
        Name of temperature column
    prec_col : str
        Name of precipitation column
    title : String
        The title for the figure
    filename : String
        The name of the output figure
    temp_min : Number
        The minimum temperature value to display
    temp_max : Number
        The maximum temperature value to display
    prec_min : Number
        The minimum precipitation value to display
    prec_max : Number
        The maximum precipitation value to display

    Returns
    -------
    The figure
    
    """
    
    fig = plt.figure(figsize=(10,8))
    plt.rcParams['font.size'] = 16

    ax2 = fig.add_subplot(111)
    ax1 = ax2.twinx()

    dfagg = df.resample(rule = "1MS", ).agg({temp_col:"mean", prec_col:"sum"})
    print(dfagg.index)
    # Draw temperature values as a red line and precipitation values as blue bars: [1P]
    # Hint: Check out the matplotlib documentation how to plot barcharts. Try to directly set the correct
    #       x-axis labels (month shortnames).
   
    ax2.bar(dfagg.index, dfagg[prec_col], color = "blue", width = 20, align = 'center')
    ax1.plot(dfagg[temp_col], color= "red")
    
    ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    
    ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    # Set appropiate limits to each y-axis using the function arguments: [1P]
    ax2.set_ylim(prec_min,prec_max)
    ax1.set_ylim(temp_min,temp_max)
    
    
    # Set appropiate labels to each y-axis: [1P]
    ax2.set_ylabel("Precipitation in mm")
    ax1.set_ylabel("Temperature in °C")

    # Give your diagram the title from the passed arguments: [1P]
    plt.title(title)

    # Save the figure as png image in the "output" folder with the given filename. [1P]
    #plt.savefig(output_dir + ".png")
    plt.savefig(filename)
    return fig

# Use this function to draw a climate diagram for 2018 for both stations and save the result: [1P]
create_climate_diagram(garmisch, temp_col=" TMK", prec_col=" RSK",
                       title="Temp & Percipitation Garmisch 2018",
filename = output_dir / "Garmisch.png")
create_climate_diagram(zugspitze,temp_col=" TMK", prec_col=" RSK",
                       title="Temp & Percipitation Zugspitze 2018",
filename = output_dir / "Zugspitze.png" )
