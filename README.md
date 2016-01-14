# GeneosReportTools

When using ITRS Geneos to monitor your company's infrastructure. A question that often raised is that how many alerts were produced from individual application ? and for how long it has been staying for ?

There are different approach to do that. In my own opinions, none of those can archive the task in all scenarios.

### Audit Log / Database logging ###
> **Pros:**
> * In most cases, unlimited space for storing the data
> * Easy for config
> **Cons:**
> * By default, you can only log down manual (audit) action performed by users (e.g. snoozing, accepting errors, re-sampling ... etc)
> * To log more other that the default audit data, additional config is required and it is usually complicated.
> **Conclusion**
> Generally a good way to record manual actions. Not ideal (designed) for tracking historical alerts.

### EventTicker ###
> **Pros:**
> * It can records every single alerts. You won't miss anything
> * Minimal setup is needed
> **Cons:**
> * It rely the ActiveConsole to be launched for the whole time. And you need to manually export the data into files.
> * When dealing with huge amount of alerts, memory consumption on your PC can be a problem. i..e you better export the result to disk and re-launch ActiveConsole in order ot release memory.
> * The output format depends on your EventTicker panel customization. One can get different set of columns from others and even next time it is exported.
> You don't really have an idea for how long an alerts hasn't be handled cleared.
> **Conclusion**
> * I know many people would go for this option to make some analysis / reports about alerts. But it is difficult to automate it. Depending on the frequency you relaunch ActiveConsole, huge amount of data can loss if A/C crashed.
