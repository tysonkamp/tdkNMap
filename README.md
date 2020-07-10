# tdkNMap
<br/>
<br/>
<strong>Summary</strong>
<p>Layer 3 and higher port scanner initially of limited functionality (TCP scans only).  This is a UNIX/LINUX style tool, configurability coming from the command line and all output going to stdout/stderr.  Currently this is under dev with Python 3.8.1.
</p>

<br><strong>History</strong></br>

<p>The actual functionality of this will be evolving, but at the start it was just a port scanning exercise.  One of the questions that comes up is: What are you scanning, TCP, UDP, Services (banners)?  The first step is TCP ports, one host or a network, and aim to be able to pipeline this script.  As functionality is completed, more will be attempted, so this is a "baby steps" approach. Ideally it'll evolve into something useful. Also, I know we already have nmap.  This will prompt a more thorough investigation into nmap and a deeper understanding of the attack surfaces of layer 3 (of the osi model) and higher (4 and up).
</p>
<p>In order to be useful, it needs to be able to be plugged into a larger system.  Initial requirements are</p>
<br/>
1) Report all output in a standardized way to stdout.<br/>
2) Needs to be fully configurable from the command line<br/>
3) Next step:  Take configuration info in .json format (so this could be invoked remotely).<br/>

  
