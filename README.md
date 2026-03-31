<h2>About Dzimba</h2>
<p>
	Dzimba is a bot to search select websites and/or platforms in the Netherlands for the latest apartment listings, apply user-defined filters, and send email alerts, all in near-real time. Currently, the following platforms are scraped:
	<ol>
	    <li><a href="https://www.verra.nl/" target="_blank">Verra Makelaars</a></li>
	    <li><a href="https://househunting.nl/" target="_blank">HouseHunting</a></li>
	    <li><a href="https://www.rentanapartment.nl/" target="_blank">Rent An Apartment NL</a></li>
	    <li><a href="https://www.pararius.com/english" target="_blank">Pararius</a></li>
	    <li><a href="https://www.rentalrotterdam.nl/" target="_blank">Rental Rotterdam</a></li>
	    <li><a href="https://livresidential.nl/" target="_blank">LIV Residential</a></li>
	    <li><a href="https://woonzeker.com/" target="_blank">Woonzeker</a></li>
    </ol> 
</p>


<h2>Requirements</h2>
<ul>
	<li>Ubuntu 22.04</li>
	<li>Docker</li>
	<li>Email address eg. gmail, yahoo etc</li>
	<li>App password associated with email address</li>
</ul>


<h2>Installation and Usage</h2>

1. Clone the repository. 

```bash
git clone https://github.com/tendaiwbm/dzimba.git <directory>
```

2. Step into the directory containing the cloned repository.
```bash
cd <directory>
```

3. Create an env file in the following path:
```bash
<directory>/mufambi/
```
   In this file, add the following environment variables (and values):
   ```bash
   sender_email_address=<ndiani@uyu.com>
   sender_email_password=<password>
   recipient_email_address=<ndiani@uyo.com>
   smtp_server=<smtp_server_address>
   smtp_port=<smtp_port_number>
   ```

4. Create an env file in the following path:
```bash
<directory>/infra/
```
   
   In this file, add the following environment variables (and values):
```bash
DZIMBA_IMAGE_NAME=<image_name>
DZIMBA_CONTAINER_NAME=<container_name>
DZIMBA_CRON_TMP=<temporary_crontab_filename>
DZIMBA_APP_LOGFILE=<logs_filename>
DZIMBA_VARIABLES_INSTALLED=1
```

5. Run the following command to set up a job that will run periodically (every 5 mins) to search, filter, and send alerts.
```bash
source dzimba.sh
```

<h2>Uninstalling Dzimba</h2>
Uninstalling the project means removing the cron job that runs the app on the specified schedule, the associated environment variables, and Docker infrastructure. To do so, navigate to the root of the project and run the following command:

```bash
source uninstall.sh
```


