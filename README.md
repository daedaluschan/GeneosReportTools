# GeneosReportTools

When using ITRS Geneos to monitor your company's infrastructure. A question that often raised is that how many alerts were produced from individual application ? and for how long it has been staying for ?

There are different approach to do that. In my own opinions, none of those can archive the task in all scenarios.

### Audit Log / Database logging ###
> **Pros:**
> * In most cases, unlimited space for storing the data
> * Easy for config
> 
> **Cons:**
> * By default, you can only log down manual (audit) action performed by users (e.g. snoozing, accepting errors, re-sampling ... etc)
> * To log more other that the default audit data, additional config is required and it is usually complicated.
> 
> **Conclusion:**
> * Generally a good way to record manual actions. Not ideal (designed) for tracking historical alerts.

### EventTicker ###
> **Pros:**
> * It can records every single alerts. You won't miss anything
> * Minimal setup is needed
> 
> **Cons:**
> * It rely the ActiveConsole to be launched for the whole time. And you need to manually export the data into files.
> * When dealing with huge amount of alerts, memory consumption on your PC can be a problem. i..e you better export the result to disk and re-launch ActiveConsole in order ot release memory.
> * The output format depends on your EventTicker panel customization. One can get different set of columns from others and even next time it is exported.
> You don't really have an idea for how long an alerts hasn't be handled cleared.
> 
> **Conclusion:**
> * I know many people would go for this option to make some analysis / reports about alerts. But it is difficult to automate it. Depending on the frequency you relaunch ActiveConsole, huge amount of data can loss if A/C crashed.

### Scheduled Reporting###
> **Pros:**
> * Space (local disk) to store the data is generally not a problem
> * Data is captured in a snapshot manner. I.e. the same alert will reported across extractions. This is good to reflect how alerts are pending for long.
> * no manual export is needed. csv will be generated upon schedule.
> * Since Csv files are exported automatically from time to time, so the performance on handling environment with large amount of data is more stable.
> 
> **Cons:**
> * It still rely the ActiveConsole to be launched for the whole time.
> * You cannot include self-defined attribute (usually used to construct the tree structure on your A/C statetree) into the report.
> * There is a bug (being followed by PEBL) on ActiveConsole that when A/C is re-launched, you need to re-enable the scheduling in order to make it effective.
> * You can miss alerts if it only popped between snapshot schedules and got cleared before the next schedule
> * the most frequent schedule you can do is hourly.
> 
> **Conclusion:**
> * An options with most potential, in my opinions.
> * Not good if you want to capture all alerts. But it can give you a brief idea how much alerts and of which type is the support team facing day-to-day.

In the rest of this article I am going to illustrate more on how we can make use of the "Scheduled Reporting" feature to produce you summary of Geneos alerts for a given time frame. I also developed some Python scripting (on [GitHub](https://github.com/daedaluschan/GeneosReportTools) as open source) to aid.

I am not going to go thru the detail on how to use the Reporting feature. You may find more information in ITRS's documentation (Gateway2 Reference Guide.pdf).

Okay, so once you received your regularly generated csv file, there are a few things you might want to do. Few things that make you a better format report. 

> 1. Remove the first 2 rows which are appended by ActiveConsole and doesn't give you much advantage on producing a good looking report.
> 2. Associate the date and time of when the alerts are seen (captured). This is not a necessary step, although I found it quite usage for my situation.
> 3. Extract the useful fields from the "User Readable Path", as ITRS did not organize if in separate column in the CSV.
> 4. Associate the key attribute (which is usually use for distinguishing which application the alert belongs to) on to each captured alert.
> 

Step #1, #2 and #3 are pretty straight forward. I'm sure you have no problem to automate it with basic file / data (I used Python panadas for it's comprehensive feature on handling data) manipulation programming module.

I would like to explain the tricks here to do Step #4. Basically, the managed entities' name doesn't always provide you good clues which application it belongs to (in most cases, it is the name of the server, named by your server team and doesn't make any sense to you). So it is extremely useful to work out a mapping between managed entity and the logical identity within your applications estate. A very common practice is assigning self-defined attribute as the application name on all managed entities. Managed entities will then be grouped in a structured manner according to your preferred "viewpath" on the "state tree" panel.

How to we extract this mapping ? One might suggest to dig it out from the gateway config xml. But it is not always straight forward, because attributes can be assigned at the folder level of manged entities.

One trick we can do is to make use of the ITRS's gateway-managedEntitiesData sampler (Yes, you need to enable the sampler first. Together with other gateway sampling function, those are good samplers when managing your Geneos infrastructure). Once you start this sampler, a dataview with all the managed entities will be shown with it's associated attributes as a column.

Now, we are almost there and the next questions is - how do we extract the information by programs, in order to automate the process ? Thanks to ITRS, there is a service exposed from the gateways as a debug interface, namely Orb. You can access Orb via a browser with the url - http://(gatewayhost):(gatewayport)/ORB

My [code](https://github.com/daedaluschan/GeneosReportTools/blob/master/geneosAlertsCsvMassage.py) shared on GitHub shows how we can "hack" into ORB and get the information required for the mapping purpose described earlier. The code also demonstrates the logic of extracting csv content and join (merge) those together.
