const { firefox } = require('playwright'); //import playwright with firefox

async function scrapeLibraryHours(url) {
  const browser = await firefox.launch({ headless: true });  //headless
  const page = await browser.newPage();  

  try {
    await page.goto(url);  

    
    const hoursSelector = '#todayshours';  
    await page.waitForSelector(hoursSelector); //waits for todays hours to load, dependent on power of device 

    //scrape all <p> sections
    const hours = await page.$$eval(`${hoursSelector} p`, (paragraphs) => {
    //create map of scraped contents
      return paragraphs.map(p => {
        const name = p.querySelector('strong')?.textContent || ''; //finds strong element inside p section. 
                                                                   //if it is found, call .textContent to 
                                                                   //get the inner text of strong element 
                                                                   //(name of facility), else if its empty 
                                                                   //return empty string 

        const time = p.textContent.split("\n").pop().trim() || ''; //call .textContent to get everything,  
                                                                   //call .split with line delimiter 
                                                                   //such that the 1st line is the name and 2nd 
                                                                   //is the time info, call .pop to get time,
                                                                   //then call .trim to get rid of 1st element 
                                                                   //(name of facility), return empty string
                                                                   //if empty
        return { name, time };
      });
    });

    console.log(hours);  

  } catch (error) {
    console.log('Error during scraping:', error);
  } finally {
    await browser.close(); 
  }
}

const libraryUrl = 'https://www.brandeis.edu/library/';
scrapeLibraryHours(libraryUrl);
