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
> * An options with most potential in my opinions.
