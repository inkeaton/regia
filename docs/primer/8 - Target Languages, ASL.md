Regia on its own cannot run: it must be translated into another executable language. We do not plan for a single language: the usefulness of Regia is how it allows to reason cleanly on the problem od agents. Its actual implementation as such, must not be limited to a single language, since it may be used in multiple contexts. Our first target language will be AgentSpeak (ASL), but in designing how the emission portion of the transpiler works, we must consider that multiple ones will be available in the future.

Now, the ASL translation is as follows:
+ Each Playbook becomes an agent file, a collection of plans
+ Each Role is an agent file, which includes all playbook files which could be assigned to it in its lifetime, and some infrastructural plans
+ Each Plot is implemented as an agent file, which represents the director, and contains infrastructural plans, information on the agents and the transitions between phases
This ASL code is meant to work inside of the Jason interpreter, together with VEsNA to run inside of the Godot game engine. As such, these files must then be instanced through a .jcm file, and each custom action must be implemented as a Java internal action #changes We must add the ability to generate the .jcm files, through instructions contained inside of compilation comments. We may specify also which is is the starting plot of the files we give, and as such, we may transpiler less role files, since some of those will just be assigned later in subplots. We may also generate different types of configuration files, based on the interpreter (besides Jason, we are working on a custom Python based one, and a C++ one)

#discuss we must reason on how playbooks are added and removed. Currently, we just compute which playbooks may be added to a role throughout its lifetime, also considering subplots, and as such, include the playbook file in there. Then, based on a belief, we activate and deactivate them. We may reason on dynamic addition, how it would actually work, and if it would be better

#changes currently infrastructural plans are copied inside of each file. we should change that to be static files to be imported by each type of file

Logging is important, and this is true of each target translation. we should always log the actions of the agents, in order to track down their behaviour, for debugging, and future runtime verification

Some details are not said for brevity, but surely we must reason more on this translation, in particular also how infrastructural information is stored in the agents (Which playbooks do i have, from which plots, etc.) For more information on the ASL translation itself, we have an example translation of 1.0 in the examples folder