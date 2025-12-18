
# currentWorkingDirectory = "D:\\BHT_Class\\Advance_Software\\Project\\berlingeoheatmap\\"
# currentWorkingDirectory = "/mount/src/berlingeoheatmap1/"

# -----------------------------------------------------------------------------
import os
currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentWorkingDirectory)
print("Current working directory\n" + os.getcwd())

import pandas                        as pd
from core import methods             as m1
from core import HelperTools         as ht

from config                          import pdict

# -----------------------------------------------------------------------------
@ht.timer
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""

    # Load raw geodata (postal code polygons)
    df_geodat_plz   = pd.read_csv(os.path.join("datasets", pdict["file_geodat_plz"]), sep=';', encoding='latin-1')
    
    # Load and preprocess electric charging station dataset
    df_lstat        = pd.read_csv(os.path.join("datasets", pdict["file_lstations"]), sep=';', encoding='latin-1', skiprows=10, header=0)
    df_lstat2       = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
    gdf_lstat3      = m1.count_plz_occurrences(df_lstat2)

    # for KW specific counts
    gdf_lstat3_kw   = m1.count_plz_by_kw(df_lstat2)    
    
    # Load and preprocess residents dataset
    df_residents    = pd.read_csv(os.path.join("datasets", pdict["file_residents"]), encoding='latin-1')
    gdf_residents2  = m1.preprop_resid(df_residents, df_geodat_plz, pdict)
    
# -----------------------------------------------------------------------------------------------------------------------
    # Start Streamlit map visualization
    m1.make_streamlit_electric_Charging_resid(
        gdf_lstat3,
        gdf_residents2,
        gdf_lstat3_kw
    )


if __name__ == "__main__": 
    main()

