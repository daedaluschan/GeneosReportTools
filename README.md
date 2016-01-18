# GeneosReportTools

When using ITRS Geneos to monitor your company's infrastructure. A question that often raised is that how many alerts were produced from individual application ? and for how long it has been staying for ?

There are different approaches to do that. In my own opinions, none of those can fulfill all scenarios.

### Database logging / Audit Log ###
> **Pros:**
> * In most cases, storage for the data is not a concern
> * Easy to setup / config
> 
> **Cons:**
> * By default, you can only log down manual (audit) action performed by users (e.g. snoozing, accepting errors, re-sampling ... etc).
> * Complicated configuration will be involved if you want to fine tune it for alerts capturing.
> * No good tools so far to extract the captured data from database.
> 
> **Conclusion:**
> * it is designed for recording manual actions. Not a good choice for tracking historical alerts.

### EventTicker ###
> **Pros:**
> * It can records every single alerts. You won't miss anything
> * Minimal setup is needed
> 
> **Cons:**
> * It rely the ActiveConsole to be launched for the whole time. And you need to manually export the data into files.
> * When dealing with huge amount of alerts, memory consumption on your PC can be a problem. You are recommended to export the result to disk and re-launch ActiveConsole from time to time (otherwise, ActiveConsole will crash at some point).
> * The output format depends on your EventTicker panel customization. i.e. it is not really a standardized report.
> * Information about how long an alert has not been handled cannot be studied.
> 
> **Conclusion:**
> * Many people would go for this option to make some analysis / reports about alerts. But it is difficult to automate it. And there are chances you might crash your A/C and lose all your data if you have too much alerts .

### Scheduled Reporting###
> **Pros:**
> * Storage for the data is usually not a concern
> * Data is captured in a snapshot manner. I.e. the same alert will reported across extractions. This is good to reflect how alerts are pending for long.
> * no manual export is needed. csv will be generated upon schedule.
> * Since Csv files are exported automatically from time to time, so the performance impact to ActiveConsole are minimal.
> 
> **Cons:**
> * It still rely the ActiveConsole to be launched for the whole time.
> * You cannot include self-defined attribute (commonly used to construct the tree structure on your A/C statetree) into the report.
> * There is a bug (being followed by PEBL) on ActiveConsole that when A/C is re-launched, you need to re-enable the scheduling in order to make it effective.
> * You can miss alerts if it only popped between snapshot schedules and got cleared before the next schedule
> * the most frequent schedule you can do is hourly.
> 
> **Conclusion:**
> * An options with most potential, in my opinions.
> * Not good if you want to capture every single alerts. But it can give you a brief idea how much alerts and of which type is the support team facing day-to-day.

In the rest of this article I am going to illustrate more on how we can make use of the "Scheduled Reporting" feature to produce a summary of Geneos alerts for a given time frame. I also developed some Python scripting (on [GitHub](https://github.com/daedaluschan/GeneosReportTools) as open source) to automate.

I am not going to go thru the detail on how to use the Reporting feature. You may find more information in ITRS's documentation (Gateway2 Reference Guide.pdf).

Okay, so once you received your regularly generated csv file, there are a few things you might want to do. Few things that make a report with good formatting and details. 

> 1. Remove the first 2 rows. 2 rows that are appended by ActiveConsole and not really useful.
> 2. Associate the date and time of when the alerts were captured. This is not a necessary step, although I found it quite usage on the sub-sequence steps.
> 3. Extract the useful fields from the "User Readable Path". ITRS did not organize it in separate columns in the CSV.
> 4. Associate the key attribute (which is usually use for distinguishing which application the alert belongs to) on to each captured alert.
> 

Step #1, #2 and #3 are pretty straight forward. I'm sure you have no problem to automate it (I used Python panadas for it's comprehensive feature on handling data).

I would like to explain more on the tricks here to do Step #4. Basically, the managed entities' name doesn't always provide you good clues which application it belongs to (in most cases, it is the name of the server, named by your server team). So it is extremely useful to work out a mapping between managed entity and the logical identity within your applications estate. A very common practice is assigning self-defined attribute as the application name on all managed entities. Managed entities will then be grouped in a structured look according to your preferred "viewpath" on the "state tree" panel.

How do we extract this mapping ? One might suggest to dig it out from the gateway config xml. But it is not always straight forward, because attributes can be assigned at the folder level of manged entities.

One way we can do is to make use of the ITRS's gateway-managedEntitiesData sampler (Yes, you need to enable the sampler first. It is one of the built-in administrative sampler). Once you start this sampler, a dataview with all the managed entities will be shown with it's associated attributes as a column.

Now, we are almost there and the next questions is - how do we extract the information by programs to automate the process ? Thanks to ITRS, there is a debug interface exposed from the gateways, namely Orb. You can access Orb via a browser with the url - http://(gatewayhost):(gatewayport)/ORB

My [code](https://github.com/daedaluschan/GeneosReportTools/blob/master/geneosAlertsCsvMassage.py) shared on GitHub shows how we can "hack" into ORB and get the mapping information described earlier. The code also demonstrates the logic of extracting csv content and join (merge) those together. You will need to modify the variable defining section to provide the following settings.

- gateway host
- gateway port
- the self-defined attribute used to distinguish application name
- sampler (view) name of the "gateway-managedEntitiesData" sampler



