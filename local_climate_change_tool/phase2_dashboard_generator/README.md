# Climate Dashboard

In this directory, there is a jupyter notebook called climate_dashboard.ipynb that creates a web application that launches in a new tab in your browser. There are two ways to do this as outlined below:

## How to run dashboard on your computer (i.e. not on ocean.pangeo.io):

**OPTION 1**: Open climate_dashboard.ipynb and run entire notebook. Uncomment the climate_dashboard.show(), and it will open in a new tab of your browser. 

**OPTION 2**: In your terminal run: 
```
panel serve --show climate_dashboard.ipynb
```

## How to run dashboard on ocean.pangeo.io server

**STEP 1**: in your terminal window on ocean.pangeo.io: 
``` 
panel serve --show climate_dashboard.ipynb --allow-websocket-origin=ocean.pangeo.io
```

**STEP 2**: in your local browser go to:
> https://ocean.pangeo.io/user/XXXX-XXXX-XXXX-XXXX/proxy/5006/climate_dashboard

* but replace XXXX-XXXX-XXXX-XXXX with your unique user ID (e.g. mine is 0000-0001-9992-3785)
