# How to run dashboard on ocean.pangeo.io server

**STEP 1**: in your terminal window on ocean.pangeo.io: 
> panel serve --show NOTEBOOK_NAME.ipynb --allow-websocket-origin=ocean.pangeo.io
* but replace NOTEBOOK_NAME with the name of the notebook (e.g. here, better_panel)

**STEP 2**: in your local browser go to:
> https://ocean.pangeo.io/user/XXXX-XXXX-XXXX-XXXX/proxy/5006/NOTEBOOK_NAME

* but replace XXXX-XXXX-XXXX-XXXX with your unique user ID (e.g. mine is 0000-0001-9992-3785)
* but replace NOTEBOOK_NAME with the name of the notebook (e.g. here, better_panel)