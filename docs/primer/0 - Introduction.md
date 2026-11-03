Regia is a Domain Specific Language, meant to allow game designers and programmers alike to describe game agents (NPCs) through a modular and extensible model based on BDI. Such agents are then meant to live inside of a game environment. The language must accomodate some features which are already familiar to this audience, while stille being true to its MAS focused origins. The language syntax is meant to be highly verbose and readable, to ensure accessibility to an audience who has little experience with coding 

The language needs to be transpiled into other languages to work. Currently only one is considered, AgentSpeak (ASL), but multiple targets may be considered in the future, and the design of the tools must consider this.

The language is implemented through two tools. First a CLI transpiler, whose role is to translate the DSL into a target language. Moreover, a Visual Editor should be provided, whose role is to allow the users to edit the regia files, while simultaneously having a visual flowchart representation of its components, in a split view. Both views should be editable, modifying the other representation

---

The language has already been realised in a first version, which we will be calling 1.0, as part of Master's Thesis. Such version implemented the transpiler through Python, and the Visual Editor as a Web application, which relied on the transpiler as a back-end. Such version was mostly a prototype, most notably the editor, but is a first reference of the implementation

In these files we will be describing a new version of the language, called 2.0. Our description will start from what 1.0 already implements, and will cite the new desired features, and discuss which may need further reflection. These points will be tagged as #discuss. We may also point out specific changes from 1.0. These will be tagged as #changes. We will also describe the language's transpilation into AgentSpeak, which while, as mentioned, not the only one possible, is the only which has already been realised. As such, we will describe the language syntax, domain, constructs, semantics, transpiler, AgentSpeak mapping, visual editor, instancing. 

Since 2.0 does not yet exist, the code snippets in these files will usually be taken from 1.0 files, with maybe some small changes for whatever we may be talking about in that moment