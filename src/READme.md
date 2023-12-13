### Scraping Code Modifications
The codes can be modified to an extent to scrape data for other municipals and states in the United States. Because the scraping code was written specifically to scrape for the state of Georgia and its municipals, 
only Municode municipal pages with the same UI and format as the Georgia municipals will be able to be scraped. The majority of municipals in many different states follow the scraping-safe format;
however, there exists codes uploaded in pdf format and municipal codes that redirect users to a different site hosting current building codes that cannot be scraped with the current script.
<li>
  Model Format:
</li>
<img width="300" alt="image" src="https://github.com/macarah/Municode/assets/115976408/26fefaf8-8c9a-45c6-b222-f2f0e88e8823">
<br></br>
<li>
  Non-Scrapable Format:
</li>
<img width="450" alt="image" src="https://github.com/macarah/Municode/assets/115976408/e7d1e976-34bd-44e0-adbc-778c8fce4ce2">
<img width="450" alt="image" src="https://github.com/macarah/Municode/assets/115976408/086bb421-63d5-45b7-a3df-4bd72ed0ed8b">

### Source Code Descriptions
| Name           | Description                                                |
|----------------|------------------------------------------------------------|
| Atlanta_Overtime_Scraping.ipynb  | This notebook scrapes the Municode Archive for Atlanta Building Codes from 2012-2023. |
| Los_Angeles_Overtime_Scraping.ipynb  | This notebook scrapes the Municode Archive for Los Angeles County Building Codes from 2012-2023. |
| Present_municipals_by_state.ipynb  | This notebook scrapes Municodes for all present municpals' building codes in the state of Georgia. |
| Conversion.ipynb  | This notebook converts the outputted folder of txt files to a well-formatted csv file. |
