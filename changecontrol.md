### Change Control Form 
- So This document can be taken along with the change control video and used for your environment or as an additional resource for your existing change control information.

##WHO IS MAKING THE CHANGE
- Who is making the change.  This can be an entire team or it can be a specific person but it should be documented for contact purposes.

##WHO IS AFFECTED CHANGE FOR
- What unit or units will need to test their functionality after the change is made to make sure that everything related to it is working properly.  Also who needs to be contacted the most before, during, and after the change process.

##WHAT IS THE CHANGE BEING MADE:
- Your general information about the change occuring.  This is used mostly for the communication piece as the HOW step will cover the in depth plan.

##WHEN WILL THE CHANGE BE MADE:
- As we dicussed on the video there's a few things to take into account here and we'll break this into 2 seperate bits
    # RISK LEVEL
    - The risk level helps explain to your change control group how broad the effects of this change will be. 
        - No Interruption    - This can usually be done during the regular work day if allowed, and is usually very simple things such as removing old cabling, changing a branging graphic or decomissioning something that has been migrated previously.
        - Small Interruption - This is usually a single service outage and I would say less than an hour of downtime.  
        - Large Interruption - This is a single service or more that is expected to be down multiple hours.
        - Total downtime     - This type of change requires a full maintence window and will take down practically all services.
    # TIME PERIODS
    - These should be pre decided by your organization but you should at least have these types of time frames discussed and figured out.
        - Business hours     - If the change isn't going to cause any sort of interruption then business hours should be fine.  
        - Standard Window    - You should have a standing standard window to do work that will take down services.  This should have communication templates and be explained to everyone in the organiziation before hand to make sure everyone knows that                   a window can and will occur during these windows but may not (but err more on the will occur).
        - Emergency Window   - This is for a serious vulnerability patch or some major change that can wait till low utilization time for your business but can't wait until the standard window comes around.  These should be used very rarely.
##WHERE WILL THE CHANGE BE MADE:
- This is the general description of where the work will be done.  In the datacenter, in a network cloest, in a different building or office floor that people work on.  This helps managers plan other working conditions if needed and pass communication to the users affected so that they don't have to call the service desk to find out things are offline.
##WHY IS THE CHANGE BEING MADE:
- This is your information to explain to everyone in the change control group why this change is required.  This should be a simple clear answer that supports making your IT environment better.
##HOW IS THE CHANGE BEING MADE:
- This is your detailed plan.  You should write out every step and think very carefully on your change and what all is entailed and also make sure to set yourself checkpoints if available to test different parts of the change to verify if things are working earlier as opposed after you've made a massive datacenter wide change and then see nothing is working as expected. 
    Example Change (Migrate DHCP from network equipment to centralized dhcp server)
        "verify all network switches running version of config has been saved and migrated off and documented"
        "pre verify that the new central dhcp server can assign dchp addresses (this should have been doing during a testing phase)"
        "pull the configuration off 1 production level network switch and then access a device and verify it can pull a new dhcp address"
        "continue to follow the same steps for evey network switch that will be affected"
    You can add other steps such as pre configuring steps that will need to be done so certain parts of access aren't broken and things of that nature just remember to document as much as you can and if your change group asks about a step you've left off have a reason it's not there, or tell them you need to add it and that may require rescheduling the work.
##HOW WILL YOU ROLLBACK IF THE CHANGE FAILS:
- You always need to have a backout plan if something goes poorly during the change implementation.  Usually this is as easy as reversing your steps in your main plan but you better make sure that will work before just listing that in your plan as your rollback.