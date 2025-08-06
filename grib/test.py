import intake
import matplotlib.pyplot as plt

def preprocess(ds):
    if 'step' in ds.coords and 'step' not in ds.dims:
        ds = ds.expand_dims('step')
    return ds

cat = intake.open_esm_datastore('rrfs_ak_ensemble.json')
# Optionally filter catalog
subset = cat.search(domain='ak', variable='avrg')


dsets = subset.to_dataset_dict(
    xarray_open_kwargs={
        "engine": "cfgrib",
        "backend_kwargs": {
            "indexpath": ""},
    },
    preprocess=preprocess,
    aggregate=True
)

#print(list(dsets.key()))
#ds = list(dsets.values())[0]
#print(ds)

for key, ds in dsets.items():
    print(f"Dataset key: {key} and dims {ds.dims['step']}")
    #print(ds)


# Assuming you have `dsets` from intake-esm open_dataset_dict call
# Pick the first dataset (forecast hour 1, for example)
ds = list(dsets.values())[0]

print(ds)

print("Dimensions:", ds.dims)
print("Coordinates:", ds.coords)
# List variables available
print("Variables:", list(ds.data_vars))

# Pick a variable to plot, e.g., first variable
var = list(ds.data_vars)[0]
print(f"Plotting variable: {var}")

# 1. Plot a time series (mean over spatial dims) along forecast_hour
# (assuming forecast_hour is coordinate and spatial dims are lat/lon)
# Compute spatial mean over lat/lon dims (adjust to your actual dims)
spatial_dims = [dim for dim in ['x', 'y', 'lat', 'latitude', 'lon', 'longitude'] if dim in ds.dims]
#ts = ds[var].mean(dim=spatial_dims)
#ts.plot()
#plt.title(f"Spatial mean of {var} over forecast lead time")
#plt.xlabel("step")
#plt.ylabel(var)
#plt.grid(True)
#plt.show()

# 2. Plot a spatial map at a specific forecast_hour (e.g., first one)
ds[var].isel(step=0).plot()
plt.title(f"{var} at forecast lead time = {ds.step.values[0]}")
plt.show()


