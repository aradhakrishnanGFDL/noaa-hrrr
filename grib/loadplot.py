import intake
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Load the catalog
cat = intake.open_esm_datastore("catalog.json")

# Search (can include more filters if needed)
query = cat.search(variable="avrg")

# Load as a dictionary of datasets
dset_dict = query.to_dataset_dict(xarray_open_kwargs={"engine": "cfgrib","backend_kwargs": 
            {"indexpath": ""}})

# Merge into one dataset along forecast_hour (or step)
# Assume keys differ only in forecast_hour
ds_agg = xr.concat(list(dset_dict.values()), dim="forecast_hour")

# Assign 'step' coordinate from forecast_hour (in hours)
ds_agg = ds_agg.assign_coords(step=[np.timedelta64(fh, 'h') for fh in ds_agg.forecast_hour.values])

# Plot: spatial average of total precipitation over forecast_hour
ts = ds_agg.tp.mean(dim=["y", "x"])
ts.plot(x='step')
plt.title("Mean Total Precipitation")
plt.xlabel("Forecast Hour (step)")
plt.ylabel("mm")
plt.grid()
plt.show()

